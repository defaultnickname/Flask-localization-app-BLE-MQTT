from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, make_response, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import main
import os
import Target

UPLOAD_FOLDER = '/static/images',
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    target = db.Column("target", db.PickleType)

    def __init__(self, name, lastname, userid, tar):
        self.name = name
        self.lastname = lastname
        self.tarid = userid
        self.target = tar




def sensor():

    _anchor = anchors.query.all()
    message = []
    print("i am in scheduled function")
    for a in _anchor:
        message.append({'x': a.x, 'y': a.y})

    main.letsgobaby(message, Target.Tar.TargetList)
    print("i am after script")


sched = BackgroundScheduler(daemon=True)
job = sched.add_job(sensor, 'interval', seconds=3)
sched.start(paused=True)



@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def hello_world():



    _anchor = anchors.query.all()
    targets=[]
    message = []
    for a in _anchor:
        message.append({'x': a.x, 'y': a.y})

    if sched.running:
        sched.pause()


    if request.method == "POST":


        sched.resume()

        print('homepage request', request)

        anchor = request.get_json()

        print('Anchor before key select', anchor)
        scheduleTaskFlag = anchor['checkbox']
        print(scheduleTaskFlag)

        anchor = anchor['anchor']
        print('Anchor after key select', anchor)

        db.session.query(anchors).delete()

        db.session.commit()

        for item in anchor:
            anch = anchors(item['x'], item['y'])
            db.session.add(anch)
        db.session.commit()


        return render_template('home.html', anchors=message)

    for target in Target.Tar.TargetList:
        targets.append({'x': target.x, 'y': target.y})

    #obiekty target muszą mieć w tym miejscu update x and y w dB
    print('Targets passed', targets)

    print("Anchor from request X and Y", message)
    return render_template('home.html', anchors=message,targets=targets)


@app.route('/delete', methods=['POST'])
def delete_user():
    if request.method == "POST":
        deleteId = request.form["Delete"]

        usr = users.query.filter_by(_id=deleteId).first()

        print('Datagase User ID to be deleted', usr.tarid)
        Target.Tar.DelWithID(usr.tarid)
        print('Server user tab entry stored in RAM to be removed', Target.Tar.TargetList)

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
        print('Server RAM table entry to be added', Target.Tar.TargetList)

        usr = users(fname, lname, userid, tar)  # dB entry on that user

        db.session.add(usr)
        db.session.commit()

    return render_template('targets.html', values=users.query.all())


@app.route('/manage-users', methods=['GET', 'POST'])
def adding_user():
    return render_template('targets.html', values=users.query.all())


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    db.create_all()

    for user in users.query.all():
        Target.Tar.TargetList.append(user.target)
        print('Server reboot target creation', Target.Tar.TargetList)
        print(user.target.x, user.target.y)

    app.run(debug=False, host="localhost", port="5001")
