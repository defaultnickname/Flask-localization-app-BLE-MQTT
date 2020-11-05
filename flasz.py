from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, make_response, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import main
import Target
import pickle


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class anchors(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    x = db.Column("x", db.Integer)
    y = db.Column("y", db.Integer)

    def __init__(self, x, y):
        self.x = x
        self.y = y


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("fname", db.String(100))
    lastname = db.Column("lname", db.String(100))
    tarid = db.Column("userid", db.Integer)
    target = db.Column("target",db.PickleType)

    def __init__(self, name, lastname, userid,tar):
        self.name = name
        self.lastname = lastname
        self.tarid = userid
        self.target = tar


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def hello_world():



    if request.method == "POST":
        anchor = request.get_json()

        db.session.query(anchors).delete()

        db.session.commit()

        print(anchor)

        for item in anchor:
            anch = anchors(item['x'], item['y'])
            db.session.add(anch)
        db.session.commit()
        print(anchors.query.all())

        main.letsgobaby(anchor, Target.Tar.TargetList)

    return render_template('home.html')


@app.route('/delete', methods=['POST'])
def delete_user():
    if request.method == "POST":
        deleteId = request.form["Delete"]


        usr = users.query.filter_by(_id=deleteId).first()

        print(usr.tarid)
        Target.Tar.DelWithID(usr.tarid)
        print(Target.Tar.TargetList)

        usr = users.query.filter_by(_id=deleteId)

        usr.delete()
        db.session.commit()

    return render_template('targets.html', values=users.query.all())


@app.route('/add', methods=['POST'])
def add_user():
    if request.method == "POST":
        lname = request.form["lname"]
        fname = request.form['fname']
        userid = request.form['userid']


        tar = Target.Tar(int(userid))  # Tar
        print(Target.Tar.TargetList)

        usr = users(fname, lname, userid,tar)  # dB entry on that user

        db.session.add(usr)
        db.session.commit()

    return render_template('targets.html', values=users.query.all())


@app.route('/manage-users', methods=['GET', 'POST'])
def adding_user():
    return render_template('targets.html', values=users.query.all())


@app.route('/secret')
def secret():
    return "dasd"


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    db.create_all()

    for user in users.query.all():
        Target.Tar.TargetList.append(user.target)
        print(Target.Tar.TargetList)

    app.run(debug=True, host="localhost", port="5001")

