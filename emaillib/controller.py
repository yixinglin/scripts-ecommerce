from flask import render_template, request, abort
import glo
from web_init import app
from pylib.ioutils import *
from service import NewLetterService
import logging 
import traceback
import sqlite3 
from flask import g  
from common import nofity_syserr

OS_TYPE = glo.OS_TYPE

@app.route('/newsletter/unsub', methods=['GET'])
def ad_unsubscribed():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    service = NewLetterService()
    service.save_as_unsubscribed(email_addr)
    logging.info(f":unsubscribed: {email_addr}") 
    return render_template("newsletter_unsub.html", email=email_addr)

@app.route('/newsletter/sub', methods=['GET'])
def ad_subscribed():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    service = NewLetterService()
    service.save_as_subscribed(email_addr)
    logging.info(f":subscribed: {email_addr}") 
    return render_template("newsletter_sub.html", email=email_addr)

@app.route('/newsletter/sent', methods=['POST'])
def ad_sent():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    service = NewLetterService()
    service.save_as_sent(email_addr)
    logging.info(f":sent: {email_addr}") 
    return "sent"


@app.route('/newsletter/registered', methods=['POST'])
def get_list_registered_email():
    logging.info(f":list_unsubscribed") 
    data = request.json
    username = data.get("username").strip()
    password = data.get("password").strip()
    print(username, password)
    if username == "admin-newsletter" and password == "uFwdsi9":
        service = NewLetterService()
        reg = service.get_list_registered_email()
        res = dict(data=reg, total=len(reg))
        return res
    else: 
        logging.error(f":AuthErr: username or password is incorrect. {username} {password}")
        raise abort(404)

@app.route('/newsletter/registered', methods=['GET'])
def get_register_email():
    em = request.args.get("em")  # Email addr was encoded in base64
    email_addr = base64decode_urlsafe(em)
    service = NewLetterService()
    reg = service.get_registered_email(email_addr)
    res = dict(data=reg, total=len(reg))
    return res

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
    logging.error(traceback.format_exc())
    # Send notification email to developers
    eapp = glo.emailNofity
    nofity_syserr(eapp, eapp.notify_err_emails, "Error: Web Server (Newsletter)", traceback.format_exc())
    return render_template("500_generic.html", error="Internal Server Error ", status_code=500), 500

def connect_db():
    f_db = glo.getValue('f_db')
    return sqlite3.connect(f_db)

