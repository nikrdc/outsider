from flask import Blueprint, render_template

import models

blueprint = Blueprint('index', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
