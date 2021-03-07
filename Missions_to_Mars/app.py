from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def home():

    destination_data = db.data.find_one()

    return render_template("index.html", mars=destination_data)

@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()

    db.data.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)