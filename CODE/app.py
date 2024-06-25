from flask import Flask, render_template,request,session,redirect,url_for
import pymysql
import pandas as pd
from random import *

app=Flask(__name__)
app.config['SECRET_KEY']='f9bf78b9a18ce6d46a0cd2b0b86df9da'

db = pymysql.connect(host='localhost',user='root',password='',db='secure_data_dynamics',port=3306)
cursor=db.cursor()
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("Home.html")

@app.route("/dataowner",methods=["POST","GET"])
def dataowner():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        pwd = request.form["pwd"]
        cpwd = request.form["cpwd"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        sql = "insert into dataowner (name,email,age,pwd,cpwd,gender,mobile) values (%s,%s,%s,%s,%s,%s,%s)"
        values = (name, email, age, pwd, cpwd, gender, mobile)
        cursor.execute(sql, values)
        db.commit()
        return render_template("dataowner.html", ms="success")
    return render_template("dataowner.html")

@app.route("/dataownerlogin",methods=['POST','GET'])
def dataownerlogin():
    if request.method=='POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        sql="select * from dataowner where name=%s and pwd=%s and status='accepted'"
        val=(name,pwd)
        X=cursor.execute(sql,val)
        Results=cursor.fetchall()
        if X>0:
            session["dataownerloginid"]=Results[0][0]
            session["dataownername"]=Results[0][1]
            return render_template("dataownerhome.html",msg="sucess")
        else:
            return render_template("dataownerlogin.html",mfg="not found")
    return render_template("dataownerlogin.html")

@app.route("/css",methods=["POST","GET"])
def css():
    if request.method=="POST":
        name=request.form["name"]
        pwd=request.form["pwd"]
        if name=="CSS" and pwd=="CSS":
            return render_template("csshome.html",msg="success")
    return render_template("css.html")

@app.route("/View_data_owners")
def View_data_owners():
    sql = "select * from dataowner"
    data = pd.read_sql_query(sql, db)
    print(data)
    data.drop(["cpwd","status"],inplace=True,axis=1)
    data["Action"]="Action"
    print(data.values.tolist())
    return render_template("View_data_owners.html",row_val=data.values.tolist())

@app.route("/add_delete/<s1>")
def add_delete(s1=0):
    print(s1)
    sql = "update dataowner set status='%s' where sno='%s' " % ("accepted", s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('View_data_owners'))

@app.route("/uplodfiles",methods=["POST","GET"])
def uplodfiles():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Keywords = request.form["Keywords"]
        Files = request.form["Files"]
        # session["dcb"] = "No Request Recieved"
        dd = "D:/rupesh/secure data/uploadFiles/" + Files
        f = open(dd, "r")
        data = f.read()
        sql = "insert into files_upload (oname,ownername,FileName,Keywords,files_data) values (%s,%s,%s,%s,AES_ENCRYPT(%s,'rupesh'))"
        values = (session["dataownername"],session["dataownerloginid"], FileName, Keywords, data)
        cursor.execute(sql, values)
        db.commit()
        return render_template("uplodfiles.html", msg="success", files=Files)
    return render_template("uplodfiles.html")

@app.route("/viewfiles")
def viewfiles():
    sql = "select * from files_upload where status='%s' and ownername='%s'" % ("accepted",session["dataownerloginid"])
    data = pd.read_sql_query(sql, db)
    data.drop(["status"],axis=1,inplace=True)
    print(data)
    return render_template("viewfiles.html",row_val=data.values.tolist())

@app.route("/publicauditing")
def publicauditing():
    sql = "select * from files_upload where status='%s'" % ("pending")
    data = pd.read_sql_query(sql, db)
    return render_template("publicauditing.html",row_val=data.values.tolist())

@app.route("/updaterequest/<s1>")
def updaterequest(s1=0):
    sql = "update files_upload set status='accepted' where sno='%s' " % (s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('publicauditing'))

#searching files
@app.route("/SearchFiles",methods=['POST','GET'])
def SearchFiles():
    if request.method=='POST':
        Name=request.form['Keywords']
        try:
            sql = "select * from files_upload where Keywords='%s' " % (Name)
            # print(X[0][0])#important
            results=pd.read_sql_query(sql,db)
            db.commit()
            print(results)
            results.drop(["status"],axis=1,inplace=True)
            results["action"]=""
            print(results)
            return render_template("SearchFilesDisplay.html", col_name=results.columns.values,row_val=results.values.tolist())
        except:
            return render_template("SearchFiles.html",msg="not found")
    return render_template("SearchFiles.html")

@app.route('/fgh/<s1>/<s2>')
def fgh(s1=0,s2=0):
    print(s1,s2)
    sql="insert into filerequest (Oname,fileid,userid) values('%s','%s','%s')"%(session["dataownername"],s1,s2)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('SearchFiles'))

@app.route("/filestatus")
def filestatus():
    sql="select * from filerequest"
    data=pd.read_sql_query(sql,db)
    data.drop(["gkey"],axis=1,inplace=True)
    print(data)
    return render_template("filestatus.html",row_val=data.values.tolist())

@app.route('/TPA')
def TPA():
    return render_template("TPA.html")

@app.route("/tpalogin",methods=["POST","GET"])
def tpalogin():
    if request.method=="POST":
        name=request.form["name"]
        pwd=request.form["pwd"]
        if name=="tpa" and pwd=="tpa":
            return render_template("tpahome.html",msg="success")
    return render_template("TPA.html")

@app.route('/TPAFiles')
def TPAFiles():
    sql="select * from filerequest where status='pending'"
    data=pd.read_sql_query(sql,db)
    data.drop(["gkey"],axis=1,inplace=True)
    print(data)
    return render_template("TPAFiles.html",row_val=data.values.tolist())

@app.route("/genearatekey/<s1>")
def genearatekey(s1=0):
    otp = randint(123593489, 600876509)
    print(type(s1),otp)
    sql = "update filerequest set status='%s', gkey='%s' where sno='%s' " % ("accepted",otp,s1)
    cursor.execute(sql)
    db.commit()
    return render_template('genearatekey.html')

@app.route("/downloadfile")
def downloadfile():
    sql = "select * from filerequest where status='accepted'"
    data = pd.read_sql_query(sql, db)
    print(data)
    data["Action"]='Action'
    return render_template("downloadfile.html",row_val=data.values.tolist())

@app.route('/filesf/<s1>')
def filesf(s1=0):
    sql = "select AES_DECRYPT(files_data,'rupesh') from files_upload where sno='%s' " % (s1)
    cursor.execute(sql)
    data = pd.read_sql_query(sql, db)
    print(data)
    return render_template("filesf.html", row_val=[[data.values[0][0].decode('utf8')]])
    # return render_template(".html")
if(__name__)==("__main__"):
    app.secret_key="f9bf78b9a18ce6d46a0cd2b0b86df9da"
    app.run(debug=True)