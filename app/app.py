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
    



# curl -v --location --request POST "https://api.amazon.com/auth/o2/token" \
#   --header "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
#   --data "grant_type=refresh_token" \
#   --data "refresh_token=Atzr|IwEBIOivkUnWfkcioje_cTezXYAz2qMw4KSFA_F_WgWvNnfmmswq7zPqQisjgT3BfRWRNBNHDKojRWR6pmdtiWzLRzQZkMxHx70Nm4lYGJ7A9gcb7hVu0t_YFlAFoQgnx8gH52j4-E9erT5QXeDnnP8n8IcSQ8P9jaBk02NmsCNYr47EE1vVKrVQEBqQQ6ghIPIlvWuBi2_-evs0t5KKCFYDUrQ_-WrSnmDxl0EHcszewSe0x3w59sdwVq6EMVzCaJORyFENXihE5w4eN9Kh-m8bSnazFKkt_v6Rg-KoYM_dhqEPlZuaYB4JmCg0JR76TN9yx-Y" \
#   --data "client_id=amzn1.application-oa2-client.9e3ff1a49f8e481c86b6cb1f8b216876" \
#   --data "client_secret=amzn1.oa2-cs.v1.3f223e9ca0bc0799692c25601085a97f3bd39504fa22ad49af07fd8abdcb1046"
