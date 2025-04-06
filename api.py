"""
Note:
This project has already achieved the core functionality through a Streamlit app that provides an interactive UI for querying and visualizing recommendations.

While the solution does not follow a traditional full-stack architecture (separating frontend and backend layers), this file (`api.py`) serves as a simple Flask API to meet the submission requirement for an accessible API endpoint.

It wraps around the same recommendation logic to expose an HTTP endpoint that returns results in JSON format.
"""

from flask import Flask, request, jsonify
from recommendation_engine import recommend_assessments
import os

app = Flask(__name__)

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    query = request.args.get('query') if request.method == 'GET' else request.json.get('query')
    is_url = request.args.get('is_url', 'false').lower() == 'true'

    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    try:
        recommendations = recommend_assessments(query, is_url=is_url, top_k=10)

        return jsonify({
            "query": query,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # using Render-provided PORT
    app.run(host="0.0.0.0", port=port)        # binding to 0.0.0.0 for external access