
from email import message
from unicodedata import name
from flask import Flask,render_template,request,redirect,url_for,session,Response,make_response
from dbconnection import DBConnection
import os
from werkzeug.utils import secure_filename
import uuid
import pandas as pd
dbconn = DBConnection("student")

import time
app = Flask(__name__)
app.secret_key='jntu@Gv'
uploads_dir = os.path.join(app.instance_path, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.route('/', methods=["POST","GET"])
def login():
    if request.method == "POST":
        session['myuser']=request.form['myuser']
        user = request.form['myuser']
        password = request.form['passwd']
        if user == "admin" and password == "password":
            return redirect(url_for('index'))
        else:
            return render_template ("login.html",msg = "Invalid cerditenials")
    return render_template('login.html')


@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('myuser',None)
    return redirect(url_for('login'))


# btech function
@app.route("/academic_b.tech")
def btech():
    if request.method == "POST":
            rows=dbconn.select_query(condition="where stream ='b.tech'",column_name='RollNo,Name,stream,semester,guide,title,domain,year,desc')
            df = pd.DataFrame(rows,columns='RollNo,Name,stream,semester,guide,title,domain,year,desc'.split(','))
            print(df)
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            resp.headers["Content-Type"] = "text/csv"
            return resp
    rows = dbconn.select_query(condition="where stream ='b.tech'",column_name="RollNo,Name,guide,title,domain,stream,semester")
        # rows1 = rows[:-2]
    return render_template("academic_b.tech.html",rows=rows)
        # rnumber =   session.get('rnumber', '')
        # rname =   session.get('rname', '')
        # rguide =   session.get('rguide','')
        # rtitle =   session.get('rtitle', '')
        # rdomain =   session.get('rdomain', '')
        # rstream =   session.get('rstream', '')
        # rsemester =   session.get('rsemester', '')
        # return render_template("academic.html", rnumber = rnumber, rname = rname, rguide = rguide, rtitle = rtitle, rdomain= rdomain, rstream = rstream, rsemester = rsemester)

        
#mtech funtion
@app.route("/academic_m.tech")
def mtech():
        rows = dbconn.select_query(condition="where stream ='m.tech'")
        rows1 = []
        return render_template("academic_m.tech.html",rows=rows)


# phd function
@app.route("/academic_phd")
def phd():
        rows = dbconn.select_query(condition="where stream ='phd'")
        rows1 = []
        return render_template("academic_phd.html",rows=rows)



# mca function
@app.route("/academic",methods=['POST','GET'])
def mca():
        if request.method == "POST":
            rows=dbconn.select_query(condition="where stream ='mca'",column_name='RollNo,Name,stream,semester,guide,title,domain,year,desc')
            df = pd.DataFrame(rows,columns='RollNo,Name,stream,semester,guide,title,domain,year,desc'.split(','))
            print(df)
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            resp.headers["Content-Type"] = "text/csv"
            return resp
        rows = dbconn.select_query(condition="where stream ='mca'",column_name="RollNo,Name,guide,title,domain,stream,semester")
        # rows1 = rows[:-2]
        return render_template("academic.html",rows=rows)
        # rnumber =   session.get('rnumber', '')
        # rname =   session.get('rname', '')
        # rguide =   session.get('rguide','')
        # rtitle =   session.get('rtitle', '')
        # rdomain =   session.get('rdomain', '')
        # rstream =   session.get('rstream', '')
        # rsemester =   session.get('rsemester', '')
        # return render_template("academic.html", rnumber = rnumber, rname = rname, rguide = rguide, rtitle = rtitle, rdomain= rdomain, rstream = rstream, rsemester = rsemester)



@app.route("/register", methods=["POST","GET"])
def register():
    stream_data=[{'name':'B.Tech'}, {'name':'M.tech'}, {'name':'MCA'}, {'name':'Phd'}]
    semster_data=[{'name':'I - 1'}, {'name':'I - 2'}, {'name':'II - 1'}, {'name':'II - 2'},{'name':'III - 1'}, {'name':'III - 2'},{'name':'IV - 1'}, {'name':'IV - 2'}]
    if request.method == "POST":
        # session['rnumber']=request.form['rnumber']
        # session['rname']=request.form['rname']
        # session['rstream']=request.form['rstream']
        # session['rsemester']=request.form['rsemester']
        # session['rguide']=request.form['rguide']
        # session['rtitle']=request.form['rtitle']
        # session['rdomain']=request.form['rdomain']
        # session['ryear']=request.form['ryear']
        # session['rfile']=request.form['rfile']
        # session['rdesc']=request.form['rdesc']
        
        rnumber=request.form['rnumber']
        rname=request.form['rname']
        rstream=(request.form['rstream']).lower()
        rsemester=request.form['rsemester']
        rguide=request.form['rguide']
        rtitle=request.form['rtitle']
        rdomain=request.form['rdomain']
        ryear=request.form['ryear']
        rfile=request.files['rfile']
        rdesc=request.form['rdesc']
        rfile_path = rfile.filename.split(".")[-1]
        if rfile_path.lower() != "pdf":
            return render_template("register.html", stream_data=stream_data, semster_data=semster_data, messsage='Format allows only pdf')
        
        print("all values extracted successfully")
        print(rfile)
        myfilename = f"{str(uuid.uuid4())}_{rfile.filename}"
        print(myfilename)
        myfilepath = os.path.join(uploads_dir, secure_filename(myfilename))
        rfile.save(myfilepath)
        resume = dbconn.convertToBinaryData(myfilepath)
        print("binary data read has done successfully")
        values = (rnumber,rname,rstream,rsemester,rguide,rtitle,rdomain,ryear,resume,rdesc,myfilepath)
        dbconn.insert_query(values)
        return render_template("register.html", stream_data=stream_data, semster_data=semster_data, messsage='form submitted sucessfully')
    return render_template("register.html", stream_data=stream_data, semster_data=semster_data)


if __name__ == "__main__":
    app.run(debug=True)


    