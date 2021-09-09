from __init__ import *


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/error_404.html'), 404
