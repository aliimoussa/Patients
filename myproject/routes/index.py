from flask import Blueprint, render_template, request

index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/', methods=['GET'])
def index():
    base_url = request.base_url
    # return render_template('index.html', base_url=base_url)
    return render_template('index.html')
