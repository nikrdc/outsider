from datetime import datetime
from flask import Blueprint, render_template
from pytz import timezone

from forms import FilterForm
from models import Region, Place

blueprint = Blueprint('region', __name__)


@blueprint.route('/<shortname>', methods=['GET', 'POST'])
def region(shortname):
    region = Region.query.filter_by(shortname=shortname).first_or_404()
    relevant_places = region.places

    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        utc = timezone('UTC').localize(datetime.utcnow())
        local_time = utc.astimezone(timezone(region.timezone))
        print relevant_places.filter(Place.open_at(local_time)).all()

    return render_template('region.html', region=region, places=relevant_places.all(), filter_form=filter_form)
