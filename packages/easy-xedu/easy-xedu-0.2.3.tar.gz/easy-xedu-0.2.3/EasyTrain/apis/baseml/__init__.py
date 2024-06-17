from flask import Blueprint

baseml_bp = Blueprint('baseml', __name__,url_prefix='/baseml')

from. import baseml


