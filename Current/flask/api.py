from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)

# Configure MongoDB connection
client = MongoClient(
    "mongodb+srv://joseph:FBcnrQuC46ehXdpJ@cluster.bxn70yq.mongodb.net/?retryWrites=true&w=majority"
)
db = client.webscrap
bbc = db.bbcscrap


# Define a route that seearches for articles based on a provided keyword
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
