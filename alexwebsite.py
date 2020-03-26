from flask import Flask, render_template
import jinja2
import trademeScraper
app = Flask(__name__)

@app.route("/")
def home():
    productlist = trademeScraper.Scrape()
    average = trademeScraper.GetAverage(productlist)
    return render_template("home.html", productlist=productlist, average=average)

if __name__ == "__main__":
    app.run(debug=True)
