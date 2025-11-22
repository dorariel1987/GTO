import uuid
import os
from typing import Optional
from xml_converter import XMLConverter
from n8n_client import N8NClient
from utils import get_env_var, logger

class QBWCHandler:
    def __init__(self):
        """Initialize QBWC Handler"""
        self.sessions = {}
        self.xml_converter = XMLConverter()
        self.n8n_client = N8NClient()
        self.qbwc_user = get_env_var('QBWC_USER', default='admin', required=False)
        self.qbwc_pass = get_env_var('QBWC_PASS', required=True)
        logger.info("QBWC Handler initialized")
    
    def server_version(self) -> str:
        """Return server version"""
        version = "1.0.0"
        logger.debug(f"Server version requested: {version}")
        return version
    
    def client_version(self, client_version: str) -> str:
        """
        Validate client version
        
        Args:
            client_version: Client version string
        
        Returns:
            "OK" if valid, warning message otherwise
        """
        if client_version:
            logger.debug(f"Client version: {client_version}")
            return "OK"
        logger.warning("Client version not provided")
        return "W:Server version mismatch"
    
    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticate QBWC user
        
        Args:
            username: Username
            password: Password
        
        Returns:
            Ticket string if authenticated, error message otherwise
        """
        logger.info(f"Authentication attempt for user: {username}")
        
        if username == self.qbwc_user and password == self.qbwc_pass:
            ticket = str(uuid.uuid4())
            self.sessions[ticket] = {
                'authenticated': True,
                'jobs': [],
                'username': username,
                'created_at': os.urandom(8).hex()  # Simple timestamp placeholder
            }
            logger.info(f"✅ Authentication successful, ticket: {ticket[:8]}...")
            return f"{ticket}\nnone\n0"
        
        logger.warning(f"❌ Authentication failed for user: {username}")
        return "nvu\nInvalid credentials"
    
    def send_request_xml(self, ticket: str, hcp_response: str, company_file: str) -> str:
        """
        Generate QBXML request for invoices
        
        Args:
            ticket: Session ticket
            hcp_response: HCP response (unused)
            company_file: Company file name
        
        Returns:
            QBXML string or empty string if invalid ticket
        """
        if ticket not in self.sessions:
            logger.warning(f"Invalid ticket: {ticket[:8]}...")
            return ""
        
        logger.info(f"Generating invoice query for company: {company_file}")
        
        # Build QBXML query for invoices
        qbxml = """<?xml version="1.0" encoding="utf-8"?>
<?qbxml version="13.0"?>
<QBXML>
  <QBXMLMsgsRq onError="stopOnError">
    <InvoiceQueryRq requestID="1">
      <ModifiedDateRangeFilter>
        <FromModifiedDate>2000-01-01</FromModifiedDate>
        <ToModifiedDate>2099-12-31</ToModifiedDate>
      </ModifiedDateRangeFilter>
    </InvoiceQueryRq>
  </QBXMLMsgsRq>
</QBXML>"""
        
        return qbxml
    
    def receive_response_xml(self, ticket: str, response_xml: str, hresult: str, message: str) -> str:
        """
        Process QBXML response from QuickBooks
        
        Args:
            ticket: Session ticket
            response_xml: QBXML response string
            hresult: HRESULT error code
            message: Error message
        
        Returns:
            "0" for success, "100" for more data
        """
        if ticket not in self.sessions:
            logger.warning(f"Invalid ticket in receive_response_xml: {ticket[:8]}...")
            return "0"
        
        # Check for errors from QuickBooks
        if hresult and hresult != "0":
            logger.error(f"Error from QuickBooks: {hresult} - {message}")
            return "0"
        
        if not response_xml:
            logger.warning("Empty response XML received")
            return "0"
        
        try:
            logger.info(f"Processing response XML (length: {len(response_xml)} bytes)")
            
            # Convert QBXML to JSON
            json_data = self.xml_converter.qbxml_to_json(response_xml)
            
            # Send to n8n
            if json_data:
                success = self.n8n_client.push_data(json_data)
                if success:
                    logger.info("✅ Successfully processed and sent data to n8n")
                else:
                    logger.error("❌ Failed to send data to n8n")
            else:
                logger.warning("No data to send to n8n (empty or invalid response)")
                
        except Exception as e:
            logger.error(f"Error processing response XML: {e}", exc_info=True)
        
        return "0"  # 0 = success, 100 = more data
    
    def connection_error(self, ticket: str, hresult: str, message: str) -> str:
        """
        Handle connection error
        
        Args:
            ticket: Session ticket
            hresult: HRESULT error code
            message: Error message
        
        Returns:
            "done" to close connection
        """
        logger.error(f"Connection error for ticket {ticket[:8] if ticket else 'N/A'}...: "
                    f"{hresult} - {message}")
        return "done"
    
    def get_last_error(self, ticket: str) -> str:
        """
        Get last error message
        
        Args:
            ticket: Session ticket
        
        Returns:
            Error message or "No error"
        """
        # In a production system, you might want to track errors per ticket
        logger.debug(f"Last error requested for ticket: {ticket[:8] if ticket else 'N/A'}...")
        return "No error"
    
    def close_connection(self, ticket: str) -> str:
        """
        Close connection and clean up session
        
        Args:
            ticket: Session ticket
        
        Returns:
            "OK"
        """
        if ticket in self.sessions:
            username = self.sessions[ticket].get('username', 'unknown')
            del self.sessions[ticket]
            logger.info(f"Connection closed for ticket: {ticket[:8]}... (user: {username})")
        else:
            logger.warning(f"Attempted to close non-existent ticket: {ticket[:8] if ticket else 'N/A'}...")
        return "OK"
