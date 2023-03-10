from flask import *
from app_utils import *
from dotenv import load_dotenv
import os
import db_utils as dbu

load_dotenv()

app = Flask(__name__)
app.secret_key = "SJCE2023"
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

@app.route('/')
def index():
    if is_logged_in():
        data = dbu.get_student_detail(session["roll_no"])
        leave_data = dbu.get_number_of_leaves(session["roll_no"])
        return render_template("dashboard.html",data=data, leave_data = leave_data)
    
    return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form
        
        if dbu.is_login_correct(data["username"],data["password"]):
            session["roll_no"] = data["username"]
            return redirect(url_for("index"))
    
    if is_logged_in():
        return redirect(url_for("index"))
    
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    if is_logged_in():
        session.pop("roll_no")
        try:
            session.pop("status")
        except:
            pass
        return redirect(url_for("login"))
    
    return redirect(url_for("login"))

@app.route("/form", methods=["GET","POST"])
def leave_form():
    if request.method=="POST":
        
        data = request.form
        print(data)

        dbu.add_leave_form_student(session["roll_no"],data)
        
        return render_template("form.html")
    
    return render_template("form.html")

@app.route("/admin",methods=["GET","POST"])
def admin():
    return render_template("admin.html")

@app.route("/admin/login",methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        data = request.form
        
        con, value = dbu.is_admin_login_correct(data["username"],data["password"])
        if con:
            session["roll_no"] = "admin"
            session["status"] = value
            
            return redirect(url_for("admin"))
        
    return render_template("admin-login.html")

@app.route("/admin/approve",methods=["GET","POST"])
def approve():
    if request.method == "POST":
        row_index = int(request.form['button-name'])
        data = dbu.admin_get_leave_details(session["status"])
        row_data = data[row_index]
        
        dbu.approve_leave_detail(row_data["leave_id"])
    
    data = dbu.admin_get_leave_details(session["status"])
    return render_template("approve.html",data=data)

if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = 8080)