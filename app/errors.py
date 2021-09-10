from __init__ import *


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/error_404.html'), 404


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/error_404.html'), 404
