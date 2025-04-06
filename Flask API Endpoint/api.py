"""
Note:
This project has already achieved the core functionality through a Streamlit app that provides an interactive UI for querying and visualizing recommendations.

While the solution does not follow a traditional full-stack architecture (separating frontend and backend layers), this file (`api.py`) serves as a simple Flask API to meet the submission requirement for an accessible API endpoint.

It wraps around the same recommendation logic to expose an HTTP endpoint that returns results in JSON format.
"""
from flask import Flask, request, jsonify
from recommendation_engine import load_data_and_model, get_top_k_recommendations

app = Flask(__name__)

# Load data + embeddings on server start
product_df, embedding_model = load_data_and_model()

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    # Get the query (from GET param or POST JSON)
    query = request.args.get('query') if request.method == 'GET' else request.json.get('query')
    
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    try:
        # Get recommendations
        results = get_top_k_recommendations(query, product_df, embedding_model, k=10)

        # Format response
        return jsonify({
            "query": query,
            "recommendations": [
                {
                    "product_name": row["Product Name"],
                    "product_id": row["Product ID"],
                    "description": row["Description"]
                }
                for _, row in results.iterrows()
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)