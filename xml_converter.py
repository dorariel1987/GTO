import xmltodict
import json
from datetime import datetime
from typing import Optional, Dict, List
from utils import logger, safe_float, validate_invoice_data

class XMLConverter:
    def qbxml_to_json(self, qbxml_string: str) -> Optional[str]:
        """
        Convert QBXML to JSON with improved error handling
        
        Args:
            qbxml_string: QBXML string to convert
        
        Returns:
            JSON string or None if conversion fails
        """
        try:
            if not qbxml_string or not qbxml_string.strip():
                logger.warning("Empty QBXML string received")
                return None
            
            qbxml_dict = xmltodict.parse(qbxml_string)
            
            if 'QBXML' not in qbxml_dict:
                logger.warning("QBXML root element not found")
                return None
            
            qbxml = qbxml_dict['QBXML']
            if 'QBXMLMsgsRs' not in qbxml:
                logger.warning("QBXMLMsgsRs not found in response")
                return None
            
            msgs = qbxml['QBXMLMsgsRs']
            if 'InvoiceQueryRs' in msgs:
                return self._process_invoice_query(msgs['InvoiceQueryRs'])
            else:
                logger.warning(f"Unknown message type in QBXML response: {list(msgs.keys())}")
                return None
            
        except xmltodict.expat.ExpatError as e:
            logger.error(f"XML parsing error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error converting QBXML to JSON: {e}", exc_info=True)
            return None
    
    def _process_invoice_query(self, invoice_query_rs: Dict) -> Optional[str]:
        """
        Process InvoiceQueryRs response
        
        Args:
            invoice_query_rs: InvoiceQueryRs dictionary
        
        Returns:
            JSON string or None
        """
        try:
            # Handle status code
            status_code = invoice_query_rs.get('@statusCode', '0')
            if status_code != '0':
                status_message = invoice_query_rs.get('@statusMessage', 'Unknown error')
                logger.warning(f"InvoiceQueryRs returned status {status_code}: {status_message}")
                # Continue anyway, might have partial data
            
            # Extract invoices
            invoices = invoice_query_rs.get('InvoiceRet', [])
            if not invoices:
                logger.info("No invoices found in response")
                return None
            
            # Ensure invoices is a list
            if not isinstance(invoices, list):
                invoices = [invoices]
            
            # Parse invoices
            parsed_invoices = []
            for invoice in invoices:
                if not invoice:
                    continue
                parsed = self._parse_invoice(invoice)
                if parsed:
                    try:
                        validate_invoice_data(parsed)
                        parsed_invoices.append(parsed)
                    except ValueError as e:
                        logger.warning(f"Invoice validation failed: {e}, skipping invoice")
                        continue
            
            if not parsed_invoices:
                logger.warning("No valid invoices after parsing")
                return None
            
            result = {
                "type": "invoices",
                "timestamp": datetime.now().isoformat(),
                "count": len(parsed_invoices),
                "data": parsed_invoices
            }
            
            logger.info(f"Successfully parsed {len(parsed_invoices)} invoices")
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"Error processing invoice query: {e}", exc_info=True)
            return None
    
    def _parse_invoice(self, invoice: Dict) -> Optional[Dict]:
        """
        Parse invoice data from QBXML with improved error handling
        
        Args:
            invoice: Invoice dictionary from QBXML
        
        Returns:
            Parsed invoice dictionary or None if parsing fails
        """
        try:
            # Validate structure
            if not isinstance(invoice, dict):
                logger.warning(f"Invalid invoice format: {type(invoice)}")
                return None
            
            # Extract customer name
            customer_name = self._extract_customer_name(invoice)
            
            # Parse numeric values
            subtotal = safe_float(invoice.get('Subtotal', 0))
            total_amount = safe_float(invoice.get('TotalAmount', 0))
            balance_remaining = safe_float(invoice.get('BalanceRemaining', 0))
            
            # Build parsed invoice
            parsed = {
                "ref_number": invoice.get('RefNumber', ''),
                "txn_id": invoice.get('TxnID', ''),
                "date": invoice.get('TxnDate', ''),
                "due_date": invoice.get('DueDate', ''),
                "subtotal": subtotal,
                "total_amount": total_amount,
                "balance_remaining": balance_remaining,
                "customer": customer_name,
                "memo": invoice.get('Memo', ''),
                "is_paid": balance_remaining == 0
            }
            
            # Validate required fields
            if not parsed['txn_id']:
                logger.warning("Invoice missing TxnID, skipping")
                return None
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing invoice: {e}", exc_info=True)
            return None
    
    def _extract_customer_name(self, invoice: Dict) -> str:
        """
        Extract customer name from invoice
        
        Args:
            invoice: Invoice dictionary
        
        Returns:
            Customer name or empty string
        """
        try:
            customer_ref = invoice.get('CustomerRef', {})
            
            if isinstance(customer_ref, dict):
                return customer_ref.get('FullName', '')
            elif isinstance(customer_ref, list) and len(customer_ref) > 0:
                first_ref = customer_ref[0]
                if isinstance(first_ref, dict):
                    return first_ref.get('FullName', '')
            
            return ''
        except Exception as e:
            logger.warning(f"Error extracting customer name: {e}")
            return ''
