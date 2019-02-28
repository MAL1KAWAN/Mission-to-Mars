import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

sys.setrecursionlimit(2000)
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts
#uri = "mongodb://localhost:27017/mars_db"
#mongo = PyMongo(app, uri)



@app.route('/scrape')
def scrape():
    #mars = mongo.db.mars_facts_data
    mars = scrape_mars.scrape()
    #mars.update({}, mars_data, upsert = True)
    print("\n\n\n")
    db.mars_facts.insert_one(mars)
    return redirect("/", code = 302)

@app.route("/")
def home():
    mars = list(db.mars_facts.find())
    #mars = mongo.db.mars_facts_data.find_one()
    print(mars)
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
    app.run(debug=True)





