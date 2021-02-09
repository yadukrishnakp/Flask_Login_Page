from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re
import bcrypt

app = Flask(__name__)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
pss = re.compile(reg)


# login page
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('signup.html')


@app.route('/signupsuccess', methods=["GET", "POST"])
def signupsuccess():
    if request.method == "POST":
        email = request.form["semail"]
        sname = request.form["sname"]
        sphoneno = request.form["sphoneno"]
        spassword = request.form["spassword"]
        s1password = request.form["s1password"]
        secure_password = bcrypt.hashpw(spassword.encode('utf8'), bcrypt.gensalt())
        with sqlite3.connect("database.db") as conn:
            try:
                c = conn.cursor()
                # c.execute('create table logind(email text not null, name text not null,phone_number integer not null primary key,password text not null)')
                c.execute("SELECT * FROM logind WHERE phone_number=(?)", (sphoneno,))
                rows = c.fetchone()
                if rows:
                    return render_template("results.html", commontext="phone number exist")
                elif not re.search(pss, spassword):
                    return render_template("results.html", commontext="password error")
                elif not re.search(regex, email):
                    return render_template("results.html", commontext="email error")
                elif not spassword == s1password:
                    return render_template("results.html", commontext="does not match passwords")
                else:
                    c.execute("insert into logind values(?,?,?,?)", (email, sname, sphoneno, secure_password))
                    return render_template("results.html", commontext="signup complete")
            except:
                conn.rollback()
                conn.commit()


@app.route('/back', methods=["POST"])
def signupback():
    return redirect(url_for('index'))


@app.route('/loginsuccess', methods=["POST"])
def loginsuccess():
    if request.method == "POST":
        email = request.form["email"]
        pno = request.form["pnumber"]
        password = request.form["pswd"]
        with sqlite3.connect('database.db')as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logind WHERE phone_number=?", (pno,))
            rows = c.fetchone()
            if not rows:
                return render_template("results.html", commontext="haven't account on this phone number")
            elif not rows[0] == email:
                return render_template("results.html", commontext="check email")
            elif not bcrypt.hashpw(password.encode('utf8'), rows[3]) == rows[3]:
                return render_template("results.html", commontext="error in password")
            else:
                return render_template("results.html", commontext="login complete")

if __name__ == '__main__':
    app.run(debug=True)
