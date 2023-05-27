import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, "instance", "weed.db")
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


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    weed_id = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<CartItem %r>" % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<User %r>" % self.id


@app.route("/")
def mainpage():
    return render_template("index.html")


@app.route("/cart", methods=["POST", "GET"])
def cart():
    if request.method == "POST":
        pass
    else:
        return render_template("cart.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        password = request.form.get("password")

        user = User.query.filter_by(nickname=nickname, password=password).first()

        if not user:
            return render_template("login.html", user=user, status=False)
        else:
            return redirect(f"/account/{user.nickname}")
    else:
        return render_template("login.html", status=True)


@app.route("/account/<string:nickname>")
def account(nickname):
    return render_template("account.html", nickname=nickname)


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
        return redirect("/market")
    else:
        try:
            weeds = Weed.query.order_by(Weed.id).all()
            cart_items = CartItem.query.filter_by(user_id="user_1").all()
        except Exception as ex:
            print(ex)
        return render_template("market.html", weeds=weeds, cart_items=cart_items)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    weed_id = request.form.get("weed_id")
    count = request.form.get("count")
    user_id = "user_1"

    if int(count) == 0:
        CartItem.query.filter_by(user_id=user_id, weed_id=weed_id).delete()
        db.session.commit()
        return jsonify({"message": "Product deleted from cart successfully."})
    existing_item = CartItem.query.filter_by(user_id=user_id, weed_id=weed_id).first()
    if existing_item:
        existing_item.count = int(count)
        db.session.commit()
        return jsonify({"message": "Product updated in cart successfully."})
    else:
        cart_item = CartItem(user_id=user_id, weed_id=weed_id, count=count)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Product added to cart successfully."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)
