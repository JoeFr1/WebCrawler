from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)

# Configure MongoDB connection
uri = "mongodb+srv://cluster0.hq133qf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
print("Connecting to MongoDB...")
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-7954788920278394582.pem')
db = client.webscrap
bbc = db.bbcscrap


# Define a route that searches for articles based on a provided keyword
@app.route('/search', methods=['Get'])
def search_articles():
    # Get the keyword from request parameters
    keyword = request.args.get('keyword')

    # Check if the keyword is provided, return error if not
    if not keyword:
        return jsonify({"error: keyword not provided"}), 400

    # Search for articles in the MongoDB collection using the provided keyword
    results = list(bbc.find({
        "$or": [
            {"Content": {"$regex": keyword, "$options": "i"}},
            {"title": {"$regex": keyword, "$options": "i"}},
            {"Author": {"$regex": keyword, "$options": "i"}},

        ]
    }))

    # Convert MongoDB object IDS to strings for JSON serialization
    for result in results:
        result['_id'] = str(result['_id'])

    return jsonify({"results": results})


# Start Flask app on script execution
if __name__ == '__main__':
    app.run(debug=True)
