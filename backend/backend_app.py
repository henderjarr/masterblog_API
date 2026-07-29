from flask import Flask, abort, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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
    return jsonify(POSTS)


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
    post_to_update = None
    for post in POSTS:
        if post["id"] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required"}), 400

    post_to_update["title"] = data.get("title")
    post_to_update["content"] = data.get("content")

    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
