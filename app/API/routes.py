from . import api
from flask import render_template

@api.route('/docs', methods=['GET'])
def show_docs():
    return render_template('api_doc.html')