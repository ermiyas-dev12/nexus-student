from flask import request, jsonify
from database.models import db, Post
from services.chatbot_service import get_response

def register_api_routes(app):

    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        msg = data.get('message', '')

        reply = get_response(msg)

        return jsonify({'reply': reply})

    @app.route('/api/post', methods=['POST'])
    def add_post():
        data = request.get_json()

        title = data.get('title', '').strip()
        body = data.get('body', '').strip()
        author = data.get('author', 'Anonymous').strip()

        if not title:
            return jsonify({'error': 'Title required'}), 400

        post = Post(title=title, body=body, author=author)

        db.session.add(post)
        db.session.commit()

        return jsonify({'success': True})