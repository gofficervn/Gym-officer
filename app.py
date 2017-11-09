from flask import *
import mlab
from mongoengine import *


app = Flask(__name__)

mlab.connect()

class BaiTap(Document):
    name = StringField()
    time = StringField()
    purpose = StringField()
    space = StringField()
    description = StringField()
    image = ListField(StringField())
    clip = StringField()
# baitap = BaiTap(
# name="Xoay khớp cổ",
# time=20,
# purpose=" Giúp bạn thả lỏng cơ xương vùng cổ, thư giãn và khôi phục trạng thái mệt mỏi.",
# space="Tại chỗ",
# description="Bạn hãy ngồi thẳng,hai tay buông thả lỏng,từ từ nghiêng toàn bộ đầu về bên trái , phải,sau đó lại từ từ về vị trí đầu thẳng,Bạn từ từ cúi đầu xuống, thật chậm. Sau đó là ngóc đầu lên về tư thế thẳng với thân người. Chú ý, không ngửa đầu ra sau, có thể làm đau hơn",
# image="https://drive.google.com/open?id=0Bxg-fKHz6ZdFeGt0RVVpUWdRQmc",
# clip="https://youtu.be/subTIsB2Ca0")
# baitap.save()


@app.route('/')
def index():

    # ex = BaiTap.objects()
    return render_template('homepage.html')

@app.route('/search', methods=['POST'])
def search():
    time = request.form["time"]
    purpose = request.form["purpose"]
    space = request.form["space"]

    if request.form["time"] == '0' and request.form["purpose"] =="0" and request.form["space"] == '0':
        listbaitap = BaiTap.objects()
    elif request.form["time"] == "0" and request.form["purpose"] =="0" and request.form["space"] != "0":
        listbaitap = BaiTap.objects(space = space)
    elif request.form["time"] == "0" and request.form["purpose"] !="0" and request.form["space"] == "0":
        listbaitap = BaiTap.objects(purpose = purpose)
    elif request.form["time"] != "0" and request.form["purpose"] =="0" and request.form["space"] == "0":
        listbaitap = BaiTap.objects(time = time)
    elif request.form["time"] != "0" and request.form["purpose"] !="0" and request.form["space"] == "0":
        listbaitap = BaiTap.objects(time = time, purpose = purpose)
    elif request.form["time"] != "0" and request.form["purpose"] =="0" and request.form["space"] != "0":
        listbaitap = BaiTap.objects(time = time, space = space)
    elif request.form["time"] == "0" and request.form["purpose"] !="0" and request.form["space"] != "0":
        listbaitap = BaiTap.objects(purpose = purpose, space = space)
    else:
        listbaitap = BaiTap.objects(time=time, purpose = purpose, space = space)

    return render_template("ketqua.html", listbaitap = listbaitap)

@app.route("/access")
def access():
    return render_template("access.html")

@app.route("/admin", methods =["POST"])
def admin():
    listbaitap = BaiTap.objects()
    if request.form["email"]== "admin" and request.form["pass"] =="admin":
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


@app.route('/baitap/<baitap_id>', methods=["GET"])
def baitap(baitap_id):
    baitap = BaiTap.objects().with_id(baitap_id)

    return render_template('baitap_new.html', baitap= baitap)

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
    return render_template("about.html")

if __name__ == '__main__':
  app.run(debug=True)
