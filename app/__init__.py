from flask import Flask, Blueprint
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
import os

from app.main.restaurante.restaurante_controller import api as dataset_ns

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)


api = Api(
    app,
    title='Restaurante APP API',
    version='0.1',
    description='A simple API to access Restaurante DB',
    endpoint='api'
)

api.add_namespace(dataset_ns, path='/restaurante')