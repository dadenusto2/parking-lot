import http
import json

from flask import render_template, Response, request  # Remove: import Flask
import connexion

from colors import *


from coordinates_generator import CoordinatesGenerator

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    parkings = ['parking']
    if request.method == 'POST':
        # проверка логина и пароля
        print(request.form.get('comp_select'))
        conn = http.client.HTTPSConnection("localhost", 4565)
        payload = json.dumps({
            "chargePointId": "parking"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/parking", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    else:
        return render_template('login.html', parkings=parkings)


if __name__ == "__main__":
    from waitress import serve
    app.run(host="0.0.0.0", port=4565, debug=True)

