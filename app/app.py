from api.v1.routes import all_blueprints
from flask import Flask
from flask_cors import CORS
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():

    app = Flask(__name__)
    CORS(app,origins=["https://www.earahearing.com"])
    for bp in all_blueprints:
        print(f"Registering blueprint: {bp.name} at {bp.url_prefix}")
        app.register_blueprint(bp, url_prefix="/api/v1")  


    for rule in app.url_map.iter_rules():
        print("rules")
        print(rule, rule.methods)
    
    # @app.errorhandler(404)
    # def not_found(e):
    #     return {"error": "Not found"}, 404

    # @app.errorhandler(500)
    # def server_error(e):
    #     return {"error": "Internal server error"}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True)
    

