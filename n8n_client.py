import requests
import json
import time
from typing import Optional
from utils import get_env_var, logger

class N8NClient:
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize n8n client
        
        Args:
            webhook_url: n8n webhook URL (optional, will use env var if not provided)
        """
        self.webhook_url = webhook_url or get_env_var('N8N_WEBHOOK_URL', required=True)
        self.timeout = int(get_env_var('N8N_TIMEOUT', default='30', required=False))
        self.max_retries = int(get_env_var('N8N_MAX_RETRIES', default='3', required=False))
        self.retry_delay = int(get_env_var('N8N_RETRY_DELAY', default='2', required=False))
        logger.info(f"N8N Client initialized with URL: {self.webhook_url[:50]}...")
    
    def _send_request(self, data: dict) -> bool:
        """
        Send request to n8n webhook (internal method)
        
        Args:
            data: Data dictionary to send
        
        Returns:
            True if successful
        
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        response = requests.post(
            self.webhook_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=self.timeout
        )
        response.raise_for_status()
        return True
    
    def push_data(self, json_data: str) -> bool:
        """
        Push data to n8n webhook with retry logic
        
        Args:
            json_data: JSON data to send (string or dict)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse JSON if string
            if isinstance(json_data, str):
                try:
                    data = json.loads(json_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON data: {e}")
                    return False
            else:
                data = json_data
            
            # Validate data structure
            if not isinstance(data, dict):
                logger.error(f"Data must be a dictionary, got {type(data)}")
                return False
            
            if 'type' not in data or 'data' not in data:
                logger.warning("Data missing 'type' or 'data' field, sending anyway")
            
            # Send request with retry logic
            logger.info(f"Sending data to n8n: type={data.get('type', 'unknown')}, "
                       f"items={len(data.get('data', []))}")
            
            last_exception = None
            for attempt in range(self.max_retries):
                try:
                    self._send_request(data)
                    logger.info(f"✅ Successfully sent to n8n (attempt {attempt + 1})")
                    return True
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (attempt + 1)
                        logger.warning(
                            f"Attempt {attempt + 1}/{self.max_retries} failed: {e}. "
                            f"Retrying in {wait_time} seconds..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {self.max_retries} attempts failed")
            
            # Handle specific exception types
            if isinstance(last_exception, requests.exceptions.Timeout):
                logger.error(f"❌ Timeout sending to n8n after {self.timeout} seconds")
            elif isinstance(last_exception, requests.exceptions.ConnectionError):
                logger.error(f"❌ Connection error to n8n: {last_exception}")
            elif isinstance(last_exception, requests.exceptions.HTTPError):
                logger.error(f"❌ HTTP error from n8n: {last_exception}")
                if hasattr(last_exception, 'response') and last_exception.response is not None:
                    logger.error(f"Response: {last_exception.response.text}")
            else:
                logger.error(f"❌ Unexpected error pushing to n8n: {last_exception}")
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in push_data: {e}", exc_info=True)
            return False
