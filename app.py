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
    image = StringField()
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

    return render_template("baitap.html", listbaitap = listbaitap)

if __name__ == '__main__':
  app.run(debug=True)
