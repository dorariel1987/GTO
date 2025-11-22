from flask import Flask, request, Response, jsonify
from qbwc_handler import QBWCHandler
import os
import logging
from datetime import datetime
from utils import get_env_var, logger

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
qbwc_handler = QBWCHandler()

# Request logging
@app.before_request
def log_request():
    """Log incoming requests"""
    logger.debug(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.debug(f"Response: {response.status_code}")
    return response

@app.route('/qbwc', methods=['POST', 'GET'])
def qbwc_endpoint():
    """
    Main QBWC endpoint - handles all QBWC protocol actions
    """
    action = request.args.get('action', '')
    
    if not action:
        logger.warning("QBWC endpoint called without action parameter")
        return Response('Missing action parameter', status=400)
    
    logger.info(f"QBWC action: {action}")
    
    try:
        if action == 'serverVersion':
            return qbwc_handler.server_version()
        
        elif action == 'clientVersion':
            client_version = request.args.get('strVersion', '')
            return qbwc_handler.client_version(client_version)
        
        elif action == 'authenticate':
            username = request.args.get('strUserName', '')
            password = request.args.get('strPassword', '')
            if not username or not password:
                logger.warning("Authentication attempt with missing credentials")
                return Response('Missing credentials', status=400)
            return qbwc_handler.authenticate(username, password)
        
        elif action == 'sendRequestXML':
            ticket = request.args.get('ticket', '')
            hcp_response = request.args.get('strHCPResponse', '')
            company_file = request.args.get('strCompanyFileName', '')
            if not ticket:
                logger.warning("sendRequestXML called without ticket")
                return Response('Missing ticket', status=400)
            return qbwc_handler.send_request_xml(ticket, hcp_response, company_file)
        
        elif action == 'receiveResponseXML':
            ticket = request.args.get('ticket', '')
            response_xml = request.data.decode('utf-8') if request.data else ''
            hresult = request.args.get('hresult', '')
            message = request.args.get('message', '')
            if not ticket:
                logger.warning("receiveResponseXML called without ticket")
                return Response('Missing ticket', status=400)
            return qbwc_handler.receive_response_xml(ticket, response_xml, hresult, message)
        
        elif action == 'connectionError':
            ticket = request.args.get('ticket', '')
            hresult = request.args.get('hresult', '')
            message = request.args.get('message', '')
            return qbwc_handler.connection_error(ticket, hresult, message)
        
        elif action == 'getLastError':
            ticket = request.args.get('ticket', '')
            return qbwc_handler.get_last_error(ticket)
        
        elif action == 'closeConnection':
            ticket = request.args.get('ticket', '')
            return qbwc_handler.close_connection(ticket)
        
        else:
            logger.warning(f"Unknown action: {action}")
            return Response(f'Unknown action: {action}', status=400)
            
    except Exception as e:
        logger.error(f"Error handling QBWC action {action}: {e}", exc_info=True)
        return Response(f'Internal server error: {str(e)}', status=500)

@app.route('/health', methods=['GET'])
def health():
    """
    Enhanced health check endpoint
    """
    health_status = {
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }
    
    status_code = 200
    
    # Check environment variables
    try:
        get_env_var('N8N_WEBHOOK_URL', required=True)
        get_env_var('QBWC_PASS', required=True)
        health_status['checks']['env_vars'] = 'ok'
    except ValueError as e:
        health_status['checks']['env_vars'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
        status_code = 503
    
    # Check n8n connectivity (optional, don't fail if unreachable)
    try:
        from n8n_client import N8NClient
        n8n_client = N8NClient()
        # Try a simple HEAD request to check connectivity
        import requests
        response = requests.head(n8n_client.webhook_url, timeout=5)
        health_status['checks']['n8n'] = 'reachable'
    except Exception as e:
        health_status['checks']['n8n'] = f'unreachable: {str(e)[:50]}'
        # Don't fail health check if n8n is unreachable, just warn
    
    # Check active sessions
    health_status['checks']['sessions'] = len(qbwc_handler.sessions)
    
    return jsonify(health_status), status_code

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'QuickBooks to Monday.com Adapter',
        'version': '1.0.0',
        'endpoints': {
            '/qbwc': 'QBWC protocol endpoint',
            '/health': 'Health check endpoint'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(get_env_var('PORT', default='5000', required=False))
    debug = get_env_var('DEBUG', default='False', required=False).lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
