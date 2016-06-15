from datetime import datetime
from flask import Blueprint, render_template
from pytz import timezone

import models

blueprint = Blueprint('region', __name__)


def open_now(place, timezone):
    current_utc = timezone('UTC').localize(datetime.utcnow())
    current_local = current_utc.astimezone(timezone(place.timezone))
    index = (current_local.day * 48) + (current_local.hour * 2)
    minute = current_local.minute
    if minute > 20:
        index += 1
    if minute > 50:
        index += 1
    if place.halfhours[index] == 'O' and place.halfhours[index+1] == 'O':
        return True
    else:
        return False


@blueprint.route('/<shortname>', methods=['GET', 'POST'])
def region(shortname):
    print models.prices
    region = models.Region.query.filter_by(shortname=shortname).first_or_404()
    return render_template('region.html', region=region)
