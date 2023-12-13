from flask import render_template, request, abort
from werkzeug.exceptions import HTTPException
import glo 
from glo import app
from pylib.ioutils import *
from service import NewLetterService
import logging 
import traceback
import sqlite3 
from flask import g  

OS_TYPE = glo.OS_TYPE

@app.route('/newsletter', methods=['GET'])
def ad_unsubscribed():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    service = NewLetterService()
    service.unsubscribe(email_addr)
    logging.info(f":unsubscribed: {email_addr}") 
    return render_template("unsubs_newsletter.html", email=email_addr)

@app.route('/newsletter/list-unsubscribed', methods=['POST'])
def list_unsubscribed():
    logging.info(f":list_unsubscribed") 
    data = request.json
    username = data.get("username")
    password = data.get("password")
    encode = data.get("encode")
    print(username, password)
    if username == "admin-newsletter" and password == "uFwdsi9":
        service = NewLetterService()
        unsubs = service.get_list_unsubscribed(encode)
        s = "\n".join(unsubs)
        return s
    else: 
        logging.error(f":AuthErr: username or password is incorrect. {username} {password}")
        raise abort(404)

@app.before_request
def before_request():
    g.conn = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'conn'):
        g.conn.close()

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

def connect_db():
    conf = glo.getValue('conf')
    return sqlite3.connect(conf[OS_TYPE]['db'])

