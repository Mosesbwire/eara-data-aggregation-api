from api.v1.blueprints.amazon_bp import amazon_bp
from controllers.amazon_sp_api_controller import verify_order

@amazon_bp.route('/verify_order/<order_id>', methods=['GET'])
def verify_order_route(order_id):
    
    return verify_order(order_id)

