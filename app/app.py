from api.v1.routes import all_blueprints
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
def create_app():

    app = Flask(__name__)
    
    origin_url = os.getenv("ORIGIN_URL")
    if origin_url:
        CORS(app,origins=[origin_url])
    else:
        CORS(app)
    
    for bp in all_blueprints:
        app.register_blueprint(bp, url_prefix="/api/v1")  

    
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True)
    

