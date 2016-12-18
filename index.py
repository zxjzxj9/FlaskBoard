from flask import Flask, abort, request, redirect, render_template, \
                  make_response, session, g
import psycopg2 as pg2
import os
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db():
    if not hasattr(g,'pgdb'):
        g.pgdb = pg2.connect(dbname = "forum")
    return g.pgdb

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'pgdb'):
        g.pgdb.close()

@app.route("/")
def index():
    username = request.cookies.get("username")
    if not username:
        resp = make_response(render_template("index.html", session = session))
        return resp
    else:
        resp = make_response(render_template("index.html", session = session))
        return resp

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form.get('username')
        pwd = request.form.get('password')
        #print user, pwd
        db = get_db()
        c = db.cursor()
        
        c.execute("SELECT password FROM users WHERE name = %s; ",(user,))

        #c.execute("SELECT password FROM users WHERE name = '%s' ;" %user)

        tmp = c.fetchone()
        #print tmp
        pwd1 = tmp[0] if tmp else None

        if user and pwd == pwd1:
            resp = make_response("Login Success!")
            #resp.set_cookie('username', user)
            session['logged_in'] = True
            session['username'] = user
            resp.headers['login_success'] = '1'
            #print resp
            return resp
        else:
            resp = make_response("Login Failure...")
            resp.headers['login_success'] = '0'
            return resp
        db.commit()
        c.close()
    else:
        return make_response(redirect('/'))

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    if request.method == "POST":
        session['logged_in'] = False
        return redirect('/')
    else:
        return redirect('/')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "GET":

        if request.args.get("username"):
            uname = request.args.get("username")
            email = request.args.get("email")
            db = get_db()
            c = db.cursor()
            c.execute("SELECT * FROM users WHERE name = %s;", (uname,))
            res = c.fetchone()
            #print res
            resp = make_response("") #render_template("register.html", session = session))
            resp.headers['user_exists'] = "0" if not res else "1"

            c.execute("SELECT * FROM users WHERE email = %s;", (email,))
            res = c.fetchone()
            resp.headers['user_exists'] = resp.headers['user_exists'] if not res else "2"

            c.close()
            return resp

        resp = make_response(render_template("register.html", session = session))
        return resp
        
    if request.method == "POST":
        print request.form
        try:
            linkurl = "".join(random.sample(string.ascii_letters,16))
            db = get_db()
            c = db.cursor()
            c.execute("INSERT INTO users(name, nickname, salt, password, email, verilink, verified)" + \
                      "VALUES (%s,%s,%s,%s,%s,%s,%s)", (request.form.get("username"),  
                        request.form.get("nickname"),request.form.get("salt"), request.form.get("passwd"), 
                        request.form.get("email"), linkurl, False,
                        )
                     )
            db.commit()
            c.close()
            resp = make_response("")
            resp.headers["reg_success"] = "0"
            return resp
        except Exception as e:
            print e
            resp = make_response("")
            resp.headers["reg_success"] = "1"
            return resp
            

@app.route("/forum", methods = ['GET', 'POST'])
def forum():
    return make_response(render_template("forum.html", session = session))

@app.route("/forum/<topic>", methods = ['GET', 'POST'])
def forumtopic():
    pass    


@app.route("/salt", methods = ['GET', 'POST'])
def salt():
    if methods == "GET":
        db = get_db()
        c = db.cursor()
        uname = request.args['username']
        cursor.execute("SELECT salt FROM users WHERE name = %s", (uname,))
        res = cursor.fetchone()
        resp = redirect('/')
        if not res:
            resp.headers['user_exist'] = '0'
        else:
            resp.headers['user_exist'] = '1'
            resp.headers['user_salt'] = res[0]
        c.close()
        return resp

if __name__ == "__main__":
    app.run(host="10.35.22.98", debug=False)
