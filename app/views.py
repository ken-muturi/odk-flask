from __future__ import with_statement
import os
import os.path
from sqlite3 import dbapi2 as sqlite3
from flask import render_template, Response, request, session, g, redirect, url_for, abort, flash, _app_ctx_stack, make_response
from app import app

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return top.sqlite_db

@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = flask._request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Kenneth'}  # fake user
    return render_template('home.html')

# https://flask-odk.herokuapp.com/
@app.route('/formList',methods=['HEAD','POST','GET'])
def formList():
    _forms = ["<?xml version='1.0' encoding='UTF-8' ?>"]
    _forms.append( '<xforms xmlns="http://openrosa.org/xforms/xformsList">' )
    path =  app.static_folder + '/uploads/odk/'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f) ) ]
    for f in files :
        if f.endswith('.xml') :
            basename = os.path.basename(f)
            # url =  'https://flask-odk.herokuapp.com/'+ basename
            _forms.append( "<xform>" )
            _forms.append( "<formID>"+ basename +"</formID>" )
            _forms.append( "<name>"+ basename +"</name>" )
            _forms.append( "<version>1.1</version>" )
            _forms.append( "<downloadUrl>/static/uploads/odk/"+ f +"</downloadUrl>" )
            _forms.append( "</xform>" )

    _forms.append("</xforms>")
    xml = "".join(_forms)
    response = Response(xml, mimetype='text/xml')
    response.headers['X-OpenRosa-Version'] = '1'
    return response

@app.route('/getForm',methods=['HEAD','POST','GET'])
def getForm():
    xml ="""
<h:html xmlns="http://www.w3.org/2002/xforms" xmlns:h="http://www.w3.org/1999/xhtml" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
  <h:head>
    <h:title>Customer Billing</h:title>
    <model>
      <instance>
        <data id="Customer_Billing_Addition_123">
          <meta>
            <instanceID/>
          </meta>
          <customer_mobile/>
          <bill_amount/>
          <billing_period_start_date/>
          <billing_period_end_date/>
        </data>
      </instance>
      <itext>
        <translation lang="eng">
          <text id="/data/customer_mobile:label">
            <value>Customer Mobile</value>
          </text>
          <text id="/data/customer_mobile:hint">
            <value>Existing Customer Mobile Number</value>
          </text>
          <text id="/data/customer_mobile:constraintMsg">
            <value>Customer Mobile</value>
          </text>
          <text id="/data/bill_amount:label">
            <value>Bill Amount</value>
          </text>
          <text id="/data/billing_period_start_date:label">
            <value>Billing Period Start Date</value>
          </text>
          <text id="/data/billing_period_end_date:label">
            <value>Billing Period End Date</value>
          </text>
        </translation>
      </itext>
      <bind nodeset="/data/meta/instanceID" type="string" readonly="true()" calculate="concat('uuid:', uuid())"/>
      <bind nodeset="/data/customer_mobile" type="long" required="true()" />
      <bind nodeset="/data/bill_amount" type="int" required="true()" constraint="(. &gt;= '1' and . &lt;= '5000')" jr:constraintMsg="Value must be between 1 and 5000"/>
      <bind nodeset="/data/billing_period_start_date" type="date" required="true()"/>
      <bind nodeset="/data/billing_period_end_date" type="date" required="true()"/>
    </model>
  </h:head>
  <h:body>
    <input ref="/data/customer_mobile">
      <label ref="jr:itext('/data/customer_mobile:label')"/>
      <hint ref="jr:itext('/data/customer_mobile:hint')"/>
    </input>
    <input ref="/data/bill_amount">
      <label ref="jr:itext('/data/bill_amount:label')"/>
    </input>
    <input ref="/data/billing_period_start_date">
      <label ref="jr:itext('/data/billing_period_start_date:label')"/>
    </input>
    <input ref="/data/billing_period_end_date">
      <label ref="jr:itext('/data/billing_period_end_date:label')"/>
    </input>
  </h:body>
</h:html>
"""
    response = Response(xml, mimetype='text/xml')
    response.headers['X-OpenRosa-Version'] = '1'

    return response

@app.route('/submission',methods=['HEAD','POST','GET'])
def submission():
    print request.headers
    if request.environ['REQUEST_METHOD'] == 'HEAD':
        response = make_response(render_template('head_request.txt'))
        response.headers['X-OpenRosa-Version'] = '1'
        return response, 204
    elif request.environ['REQUEST_METHOD'] == 'POST':
        xml = ""
        upFile = request.files['xml_submission_file']
        print upFile.name
        xml = upFile.read()
        print xml
    
        #return response
        response = make_response(render_template('home.html'))
        response.headers['X-OpenRosa-Version'] = '1'
        return response, 201
    elif request.environ['REQUEST_METHOD'] == 'GET':
        response = make_response(render_template('home.html'))
        return response, 200
