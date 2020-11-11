from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mars_scrape

# Create an instance of Flask app
app = Flask(__name__)

#Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#mongo.db.mars.drop()

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = mars_scrape.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
