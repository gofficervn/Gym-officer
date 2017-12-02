from flask import *
import mlab
from pagination import Pagination
from mongoengine import *
from flask_pymongo import PyMongo, pymongo
import random


app = Flask(__name__)

app.config['MONGO_DBNAME'] = "goficer"
app.config['MONGO_URI'] = 'mongodb://admin:admin@ds241395.mlab.com:41395/goficer'

mongo = PyMongo(app)

mlab.connect()

class BaiTap(Document):
    name = StringField()
    time = StringField()
    purpose = StringField()
    space = StringField()
    description = StringField()
    image = ListField(StringField())
    clip = StringField()



@app.route('/', methods = ['GET', 'POST'])
def index():
    list_bg = ['static/image/homepage/1.jpg','static/image/homepage/2.jpg', 'static/image/homepage/3.jpg','static/image/homepage/4.jpg','static/image/homepage/5.jpg', 'static/image/homepage/6.jpg','static/image/homepage/7.jpg']

    random_bg = random.choice(list_bg)

    random_baitap = random.choice(BaiTap.objects())
    random_id = random_baitap.id
    return render_template('homepage.html',random_bg = random_bg, random_id = random_id)

@app.route('/numbers', methods= ['GET'])
def numbers():

    number = mongo.db.bai_tap

    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    starting_id = number.find().sort('_id', pymongo.ASCENDING)

    last_id = starting_id[offset]['_id']

    gofficer = number.find({'_id' : {'$gte' : last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)

    output= []

    for i in gofficer:
        output.append({'time' : i['time'], 'purpose' : i['purpose'], 'name' : i['name']} )

    prev_url = '/numbers?limit=' + str(limit) + '&offset=' +str(offset-limit)
    next_url = '/numbers?limit=' + str(limit) + '&offset=' +str(offset+limit)
    return jsonify({'result' : output, 'prev_url' : prev_url, 'next_url': next_url})


@app.route('/search', methods=['GET','POST'])
def search():

    list_bg = ['/static/image/search/1.jpg','/static/image/search/2.jpg','/static/image/search/3.jpg']

    random_bg = random.choice(list_bg)
    random_baitap = random.choice(BaiTap.objects())
    random_id = random_baitap.id

    if request.method == 'POST':
        time = request.form["time"]
        purpose = request.form["purpose"]
        space = request.form["space"]

        if request.form["time"] == 'all' and request.form["purpose"] =="all" and request.form["space"] == 'all':
            listbaitap = BaiTap.objects()
        elif request.form["time"] == "all" and request.form["purpose"] =="all" and request.form["space"] != "all":
            listbaitap = BaiTap.objects(space = space)
        elif request.form["time"] == "all" and request.form["purpose"] !="all" and request.form["space"] == "all":
            listbaitap = BaiTap.objects(purpose = purpose)
        elif request.form["time"] != "all" and request.form["purpose"] =="all" and request.form["space"] == "all":
            listbaitap = BaiTap.objects(time = time)
        elif request.form["time"] != "all" and request.form["purpose"] !="all" and request.form["space"] == "all":
            listbaitap = BaiTap.objects(time = time, purpose = purpose)
        elif request.form["time"] != "all" and request.form["purpose"] =="all" and request.form["space"] != "all":
            listbaitap = BaiTap.objects(time = time, space = space)
        elif request.form["time"] == "all" and request.form["purpose"] !="all" and request.form["space"] != "all":
            listbaitap = BaiTap.objects(purpose = purpose, space = space)
        else:
            listbaitap = BaiTap.objects(time=time, purpose = purpose, space = space)


        dem = len(listbaitap)

        return render_template("ketqua_new.html", listbaitap = listbaitap,random_bg=random_bg, dem= dem, random_id= random_id)
    elif request.method == 'GET':
        listbaitap = BaiTap.objects()
        dem = len(listbaitap)
        return render_template("ketqua_new.html", listbaitap = listbaitap,random_bg=random_bg, dem= dem, random_id= random_id)
@app.route("/access")
def access():
    return render_template("access.html")

@app.route("/admin", methods =["POST"])
def admin():
    listbaitap = BaiTap.objects()
    if request.form["email"]== "admin" and request.form["pass"] =="244466666":
        return render_template('admin.html',listbaitap = listbaitap)
    else:
        return render_template("homepage.html")


@app.route('/addbaitap', methods=["GET","POST"])
def adbaitap():
    if request.method == "GET":
        return render_template('addbaitap.html')
    elif request.method =="POST":
        form = request.form
        name = form['name']
        time = form['time']
        purpose = form['purpose']
        space = form['space']
        description = form['description']
        imagestring = form['image']
        image = imagestring.split(",")
        clip = form['clip']


        baitap = BaiTap(name = name, time = time, purpose = purpose, space = space, description = description, image= image, clip= clip)
        baitap.save()
        listbaitap = BaiTap.objects()
        return render_template('admin.html', listbaitap = listbaitap)


@app.route('/baitap/<baitap_id>', methods=["GET", 'POST'])
def baitap(baitap_id):
    baitap = BaiTap.objects().with_id(baitap_id)

    time = baitap.time
    purpose = baitap.purpose

    similar_baitap = [d for d in BaiTap.objects() if d['time']==time and d['purpose']==purpose]

    for i in similar_baitap:
        if i== baitap:
            similar_baitap.remove(i)


    return render_template('baitap_final.html', baitap= baitap, similar_baitap = similar_baitap)

@app.route('/deletebaitap/<baitap_id>')
def deletebaitap(baitap_id):


    baitap = BaiTap.objects().with_id(baitap_id)
    if baitap is None:
        print("Not found")
    else:
        baitap.delete()

    listbaitap = BaiTap.objects()
    return render_template('admin.html',listbaitap = listbaitap)

@app.route('/updatebaitap/<baitap_id>',methods=['GET','POST'])
def updatebaitap(baitap_id):
    listbaitap = BaiTap.objects()
    baitap = BaiTap.objects().with_id(baitap_id)
    if request.method == "GET":
        return render_template('updatebaitap.html',baitap = baitap)
    elif request.method == "POST":

        form = request.form
        name = form['name']
        time = form['time']
        purpose = form['purpose']
        space = form['space']
        description = form['description']
        imagestring = form['image']
        image = imagestring.split(",")
        clip = form['clip']

        baitap.update(set__name = name,set__time = time, set__purpose = purpose, set__space = space
                        , set__description = description,set__image = image, set__clip = clip)

    return render_template('admin.html',listbaitap = listbaitap)

@app.route("/donate")
def donate():
    return render_template("donate.html")
@app.route("/aboutus")
def about():
    return render_template("aboutus.html")

if __name__ == '__main__':
  app.run(debug=True)
