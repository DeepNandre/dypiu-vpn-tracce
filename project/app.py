from flask import Flask, request, render_template
import requests
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Set the API token
api_token = "9132ca51f7b23e"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    # Get the IP address from the form
    ip_address = request.form["ip_address"]

    # Retrieve the IP address information
    response = requests.get("https://ipinfo.io/" + ip_address + "?token=" + api_token)
    data = response.json()
    region = data["region"]
    city = data["city"]
    country = data["country"]

    # Convert the IP address to a numerical format
    ip_array = np.array([int(x) for x in ip_address.split('.')])

    # Perform anomaly detection using K-means clustering
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(ip_array.reshape(-1,1))
    anomaly_score = abs(kmeans.score(ip_array.reshape(-1,1)))

    # Return the results to the template
    return render_template("result.html", ip_address=ip_address, region=region, city=city, country=country, anomaly_score=anomaly_score)

if __name__ == "__main__":
    app.run(debug=True)
