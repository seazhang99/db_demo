from flask import Flask

from config import Config
from main.views import main_bp
#from extensions import db, migrate
#from custom_encoder import CustomEncoder

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #register_extensions(app)
    register_blueprints(app)
    #register_shellcontext(app)
    return app

def register_blueprints(app):
    app.register_blueprint(main_bp)

app = create_app()
#app.json_encoder = CustomEncoder


port = Config.PORT
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = port)