from datetime import datetime
from flask import Blueprint, render_template
from pytz import timezone

from forms import FilterForm
from models import Region

blueprint = Blueprint('region', __name__)


def open(place, current_utc):
    #current_utc = timezone('UTC').localize(datetime.utcnow())
    current_local = current_utc.astimezone(timezone(place.region.timezone))
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
    region = Region.query.filter_by(shortname=shortname).first_or_404()
    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        pass
    return render_template('region.html', region=region, places=region.places.all(), filter_form=filter_form)
