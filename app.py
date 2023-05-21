from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weed.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Weed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    tgk = db.Column(db.Integer, nullable=False)
    compound = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Weed %r>" % self.id

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route("/add-weed", methods=["POST", "GET"])
def add_weed():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        count = request.form["count"]
        brand = request.form["brand"]
        tgk = request.form["tgk"]
        compound = request.form["compound"]
        img = request.form["img"]
        text = request.form["text"]

        weed = Weed(name=name, price=price, rating=0, count=count, brand=brand, tgk=tgk, compound=compound, img=img, text=text)
        try:
            db.session.add(weed)
            db.session.commit()
            return redirect("/")
        except Exception as ex:
            print(ex)
    else:
        return render_template("add-weed.html")

@app.route("/market", methods=["POST", "GET"])
def market():
    if request.method == "POST":
        print(request.form)
        return redirect("/")
    else:
        try:
            weeds = Weed.query.order_by(Weed.id).all()
        except Exception as ex:
            print(ex)
        return render_template("market.html", weeds = weeds)

if __name__ == "__main__":
    app.run(debug=True, port=9999)