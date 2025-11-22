"""
Utility functions for the QBWC Adapter
"""
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def get_env_var(name: str, default: Optional[str] = None, required: bool = True) -> str:
    """
    Get environment variable with validation
    
    Args:
        name: Environment variable name
        default: Default value if not set
        required: Whether the variable is required
    
    Returns:
        Environment variable value
    
    Raises:
        ValueError: If required variable is not set
    """
    value = os.getenv(name, default)
    
    if required and not value:
        raise ValueError(f"Required environment variable {name} is not set")
    
    if value:
        logger.debug(f"Environment variable {name} is set")
    else:
        logger.warning(f"Environment variable {name} is not set, using default: {default}")
    
    return value


def safe_float(value, default=0.0):
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Float value or default
    """
    try:
        if value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"Could not convert {value} to float, using default {default}")
        return default


def validate_invoice_data(invoice_data: dict) -> bool:
    """
    Validate invoice data before sending
    
    Args:
        invoice_data: Invoice data dictionary
    
    Returns:
        True if valid
    
    Raises:
        ValueError: If validation fails
    """
    required_fields = ['ref_number', 'txn_id', 'date', 'total_amount']
    
    for field in required_fields:
        if field not in invoice_data:
            raise ValueError(f"Missing required field: {field}")
    
    if invoice_data['total_amount'] < 0:
        raise ValueError("Total amount cannot be negative")
    
    if not invoice_data['txn_id']:
        raise ValueError("TxnID cannot be empty")
    
    logger.debug(f"Invoice data validated: {invoice_data.get('ref_number', 'N/A')}")
    return True

