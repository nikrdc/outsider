from flask import Blueprint, render_template

import models

blueprint = Blueprint('region', __name__)


@blueprint.route('/<shortname>', methods=['GET'])
def region(shortname):
    print models.prices
    region = models.Region.query.filter_by(shortname=shortname).first_or_404()
    return render_template('region.html', region=region)
