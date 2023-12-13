from flask import render_template, request, abort
from werkzeug.exceptions import HTTPException
import glo 
from glo import app
from pylib.ioutils import *
from service import NewLetterService
import logging 
import traceback

@app.route('/newsletter', methods=['GET'])
def ad_unsubscribed():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    logging.info(f":ad_unsubscribed: {email_addr}")
    # conf = glo.getValue("conf")
    service = NewLetterService()
    service.unsubscribe(email_addr)
    return render_template("unsubs_newsletter.html", email=email_addr)

@app.route('/newsletter/list-unsubscribed', methods=['POST'])
def list_unsubscribed():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    if username == "admin-newsletter" and password == "uFwdsi9":
        service = NewLetterService()
        unsubs = service.get_list_unsubscribe()
        s = "\n".join(unsubs)
        return s
    else: 
        logging.error(f":AuthErr: username or password is incorrect. {username} {password}")
        raise abort(404)

@app.route('/newsletter/index_test', methods=['GET'])
def newsletter_index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def custom500(error):
    app.logger.error(traceback.format_exc())
    return render_template("500_generic.html", error="Internal Server Error ", status_code=500), 500