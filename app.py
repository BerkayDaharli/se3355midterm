import sqlite3 as sql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def initDB():
    conn = sql.connect('database.db')
    print("Opened database successfully")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    initDB()
    app.run(debug=True)
