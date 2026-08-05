from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data = request.get_json()

        if not data or not data.get("title") or not data.get("content"):
            return jsonify({"error": "Title and content are required"}), 400

        new_post = {
            "id": len(POSTS) + 1,
            "title": data.get("title"),
            "content": data.get("content")
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201

    sort_posts = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    results_to_be_displayed = POSTS

    if sort_posts is not None:
        if sort_posts not in ("title", "content"):
            return jsonify({"error": "Invalid sort parameter"}), 400
        if direction not in ("asc", "desc"):
            return jsonify({"error": "Invalid direction parameter"}), 400
        results_to_be_displayed = sorted(
            POSTS, key=lambda x: x[sort_posts].lower(), reverse=(direction == "desc"))

    return jsonify(results_to_be_displayed)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_filter = request.args.get('title')
    content_filter = request.args.get('content')

    def matches(post):
        if title_filter and title_filter.lower() not in post["title"].lower():
            return False
        if content_filter and content_filter.lower() not in post["content"].lower():
            return False
        return True

    filtered_posts = []
    for post in POSTS:
        if matches(post):
            filtered_posts.append(post)

    return jsonify(filtered_posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_delete = None
    for post in POSTS:
        if post["id"] == post_id:
            post_to_delete = post
            break

    if post_to_delete is None:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    updated_post = None
    for post in POSTS:
        if post["id"] == post_id:
            updated_post = post
            break

    if updated_post is None:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required"}), 400

    updated_post["title"] = data.get("title")
    updated_post["content"] = data.get("content")

    return jsonify(updated_post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
