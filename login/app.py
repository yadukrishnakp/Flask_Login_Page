from flask import Flask, render_template, request
import sqlite3
import cipher

app = Flask(__name__)


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
        conn= sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute('create table logind(email text not null, name text not null,phone_number integer not null primary key,password text not null)')
        
        conn.commit()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
