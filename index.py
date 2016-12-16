from flask import Flask, abort, request, redirect, render_template, \
                  make_response, session, g
import psycopg2 as pg2
import os

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
        print user, pwd
        db = get_db()
        c = db.cursor()
        
        c.execute("SELECT password FROM users WHERE name = %s; ",(user,))

        #c.execute("SELECT password FROM users WHERE name = '%s' ;" %user)

        tmp = c.fetchone()
        print tmp
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
        return render_template("register.html", session = session)
    if request.method == "POST":
        pass

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
