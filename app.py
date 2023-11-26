from flask import render_template # Remove: import Flask
import connexion
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    from waitress import serve
    app.run(host="212.233.88.0", port=22, debug=True)

