
from flask import request,Flask,render_template,session,redirect,url_for
import pymysql
import pandas as pd


app=Flask(__name__)
app.config['SECRET_KEY']='f9bf78b9a18ce6d46a0cd2b0b86df9da'

db = pymysql.connect(host='localhost',user='root',password='',db='multisource',port=3306)
cursor=db.cursor()

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/admin",methods=["POST","GET"])
def admin():
    if request.method=="POST":
        name=request.form["name"]
        pwd=request.form["pwd"]
        if name=="admin" and pwd=="admin":
            return render_template("adminhome.html",msg="success")
    return render_template("admin.html")

@app.route("/viewdoctors")
def viewdoctors():
    sql="select * from doctor"
    data=pd.read_sql_query(sql,db)
    data["Action"]="Action"
    data.drop(["email","pwd","cpwd","gender","mobile"],inplace=True,axis=1)

    return render_template("viewdoctors.html",row_val=data.values.tolist())

@app.route("/adddoct/<s1>/<s2>/<s3>")
def adddoct(s1="",s2="",s3=""):
    return render_template("adddoctors.html",s1=s1,s2=s2,s3=s3)

@app.route("/updoctors",methods=["POST","GET"])
def updoctors():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        role=request.form["role"]
        sql = "insert into addoctors (name,age,role) values (%s,%s,%s)"
        values = (name,age,role)
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('viewdoctors'))

@app.route("/viewpatients")
def viewpatients():
    sql = "select * from patient"
    data = pd.read_sql_query(sql, db)
    data.drop(["email","pwd","cpwd","gender","mobile"],inplace=True,axis=1)
    data["Action"]="Action"
    return render_template("viewpatients.html",row_val=data.values.tolist())

@app.route("/addpatients/<s1>/<s2>/<s3>")
def addpatients(s1="",s2="",s3=""):
    return render_template("addpat.html",s1=s1,s2=s2,s3=s3)
@app.route("/uppat",methods=["POST","GET"])
def uppat():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        disease=request.form["disease"]
        sql = "insert into adpatients (name,age,disease) values (%s,%s,%s)"
        values = (name, age, disease)
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('viewpatients'))


@app.route("/viewmedicines")
def viewmedicines():
    sql="select * from filesupload"
    data = pd.read_sql_query(sql, db)
    data.drop(["requeststofiles"],axis=1,inplace=True)
    data["Action"]="Action"
    return render_template("viewmedicines.html",row_val=data.values.tolist())

@app.route(("/addreqtoioh/<s1>"))
def addreqtoioh(s1=0):
    sql="update filesupload set requeststofiles='%s' where sno='%s' "%("pending",s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('viewmedicines'))

@app.route("/viewses")
def viewses():
    sql="select * from filesupload where requeststofiles='accepted'"
    data=pd.read_sql_query(sql,db)
    data["Action"]="Action"
    return render_template("viewses.html",row_val=data.values.tolist())

@app.route("/key/<s1>")
def key(s1=0):
    sql = "select AES_DECRYPT(files,'rupesh') from filesupload where sno='%s' " % (s1)
    cursor.execute(sql)
    data = pd.read_sql_query(sql, db)
    return render_template("key.html", row_val=[[data.values[0][0].decode('utf8')]])


@app.route("/doctor",methods=["POST","GET"])
def doctor():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        age = request.form["age"]
        pwd=request.form["pwd"]
        cpwd=request.form["pwd"]
        gender=request.form["gender"]
        mobile=request.form["mobile"]
        role=request.form["role"]
        sql = "insert into doctor (name,email,age,pwd,cpwd,gender,mobile,role) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (name,email,age,pwd,cpwd,gender,mobile,role)
        cursor.execute(sql, values)
        db.commit()
        return render_template("doctor.html",ms="success")
    return render_template("doctor.html")

@app.route("/doctorlogin",methods=['POST','GET'])
def doctorlogin():
    if request.method=='POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        sql="select * from doctor where name=%s and pwd=%s "
        val=(name,pwd)
        X=cursor.execute(sql,val)
        Results=cursor.fetchall()
        if X>0:

            session["doctorloginid"]=Results[0][0]
            session["doctorname"]=Results[0][1]

            return render_template("doctorshome.html",msg="sucess")
        else:
            print("5555555555555")
            return render_template("doctorlogin.html",mfg="not found")
    return render_template("doctorlogin.html")


@app.route("/viewappointments")
def viewappointments():
    sql="select * from addrequesttodoctor where sno=%s"%(session["doctorloginid"])
    data=pd.read_sql_query(sql,db)
    session["s1"]=data.values[0][0]
    data.drop(["appointmentdate","status","doctorname","doctorid"],axis=1,inplace=True)
    data["Action"]="Action"
    return render_template("viewappointments.html",row_val=data.values.tolist())

@app.route("/addappointment",methods=["POST","GET"])
def addappointment():
    if request.method=="POST":
        date=request.form["date"]
        sql = "update  addrequesttodoctor set appointmentdate='%s',status='%s',doctorname='%s' where sno='%s'" %(date,"accepted",session["doctorname"],session["s1"])
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('viewappointments'))
    return render_template("addappointment.html")

@app.route("/patient",methods=["POST","GET"])
def patient():
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        pwd = request.form["pwd"]
        cpwd = request.form["pwd"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        dissease = request.form["disease"]
        if pwd==cpwd:
            sql = "insert into patient (name,email,pwd,cpwd,gender,mobile,disease) values (%s,%s,%s,%s,%s,%s,%s)"
            values = (name, email, pwd, cpwd, gender, mobile, dissease)
            cursor.execute(sql, values)
            db.commit()
            return render_template("patient.html", ms="success")
        else:
            return render_template("patient.html", m1s="fg")
    return render_template("patient.html")

@app.route("/patientlogin",methods=['POST','GET'])
def patientlogin():
    if request.method=='POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        sql="select * from patient where name=%s and pwd=%s "
        val=(name,pwd)
        X=cursor.execute(sql,val)
        Results=cursor.fetchall()
        if X>0:
            session["patientdisease"]=Results[0][8]
            session["patientname"]=Results[0][1]
            session["patientage"]=Results[0][3]
            session["patientid"]=Results[0][0]
            return render_template("patienthome.html",msg="sucess")
        else:

            return render_template("patientlogin.html",mfg="not found")
    return render_template("patientlogin.html")

@app.route("/viewaddoctors")
def viewaddoctors():
    session["patientdisease"]="card"
    sql = 'SELECT * FROM addoctors WHERE role LIKE %s'
    args = [ session["patientdisease"] + '%']
    cursor.execute(sql, args)
    data = pd.DataFrame(cursor.fetchall())
    print(data)
    data["Action"]="Action"
    return render_template("viewaddoctors.html",data=data.to_html(index=False),row_val=data.values.tolist())

@app.route("/addrequesttodoctor/<s1>")
def addrequesttodoctor(s1=0):
    sql = "insert into addrequesttodoctor (name,age,disease,doctorid,patientid) values (%s,%s,%s,%s,%s)"
    values = ( session["patientname"],  session["patientage"], session["patientdisease"], s1,session["patientid"])
    cursor.execute(sql, values)
    db.commit()
    return redirect(url_for('viewaddoctors'))

@app.route("/viewstatus")
def viewstatus():
    sql = "select * from addrequesttodoctor where sno='%s' and status='%s' "%( session["patientid"],"accepted")
    data=pd.read_sql_query(sql,db)
    data.drop(["disease","patientid","age","doctorid","sno"],axis=1,inplace=True)
    return render_template("viewstatus.html",row_val=data.values.tolist())

@app.route("/ioh",methods=["POST","GET"])
def ioh():
    if request.method == "POST":
        name = request.form["name"]
        pwd = request.form["pwd"]
        if name == "IOH" and pwd == "IOH":
            return render_template("iohhome.html", msg="success")
    return render_template("ioh.html")

@app.route("/iohviewpatients")
def iohviewpatients():
    sql="select * from adpatients"
    data=pd.read_sql_query(sql,db)
    data.drop(["sno","age"],axis=1,inplace=True)
    return render_template("iohviewpatients.html",row_val=data.values.tolist())

@app.route("/uploadmedicienes",methods=["POST","GET"])
def uploadmedicienes():
    if request.method=="POST":
        files=request.form["files"]
        dd = "D:/rupesh/Medical Data Integration/uploadfiles/" + files
        f = open(dd, "r")
        data = f.read()
        print(data)
        sql = "insert into filesupload (files) values (AES_ENCRYPT('%s','rupesh'))"%(data)
        cursor.execute(sql)
        db.commit()
    return render_template("uploadmedicienes.html")

@app.route("/viewadminrequests")
def viewadminrequests():
    return render_template("viewadminrequests.html")


@app.route("/Viewre")
def Viewre():
    sql="select * from filesupload where requeststofiles='%s'"%("pending")
    data=pd.read_sql_query(sql,db)
    data["Action"]="Action"
    return render_template("Viewre.html",row_val=data.values.tolist())

@app.route("/upd/<s1>")
def upd(s1=0):
    sql="update filesupload set requeststofiles='%s' where sno='%s' "%("accepted",s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('viewadminrequests'))

if(__name__)==("__main__"):
    app.secret_key = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'

    app.run(debug=True)
