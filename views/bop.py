from flask import Blueprint, render_template

blueprint = Blueprint('bop', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('bop.html')
