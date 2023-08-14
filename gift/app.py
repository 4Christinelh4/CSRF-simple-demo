from flask import Flask, Response, abort, redirect, render_template, request, url_for, jsonify

app = Flask(__name__)

emails = []
gift_quantity = {"Iphone14": 3, "Apple gift card": 10, "Starbuck gift card": 20, "Macbook Air": 1}

@app.route("/", methods=["GET", "POST"])
def show_gifts():
    return jsonify(gift_quantity)

@app.route("/receive-gift", methods=["GET", "POST"])
def receive_gift():
    gift_requested = request.args.get('gift')
    if gift_requested in gift_quantity:
        if gift_quantity[gift_requested] > 0:
            gift_quantity[gift_requested]-=1
            return jsonify({"msg": f"you have received {gift_requested}"})
    return jsonify({"msg": ":( try another gift"})


if __name__ == "__main__":
    app.run(port=6677, debug=True)