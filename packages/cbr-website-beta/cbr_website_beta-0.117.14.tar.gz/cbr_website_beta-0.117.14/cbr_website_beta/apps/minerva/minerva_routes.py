from flask import render_template
from cbr_website_beta.apps.minerva import blueprint

EXPECTED_ROUTES__MINERVA = [ '/minerva']

@blueprint.route('')
def minerva_root():
    return render_template('minerva/index.html')

