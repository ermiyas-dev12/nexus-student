from flask import request, jsonify, session
from flask_login import current_user
from database.models import db, Post, ChatHistory, Like
from services.chatbot_service import get_response
import uuid

def register_api_routes(app):

    # ---------- CHAT ----------
    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        msg = data.get('message', '')

        # Get or create session id for anonymous users
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        reply = get_response(msg)

        # Save to chat history
        try:
            history = ChatHistory(
                user_id=current_user.id if current_user.is_authenticated else None,
                session_id=session['session_id'],
                message=msg,
                response=reply
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            print(f"[Chat History Error] {e}")

        return jsonify({'reply': reply})

    # ---------- GET CHAT HISTORY ----------
    @app.route('/api/chat/history', methods=['GET'])
    def chat_history():
        if current_user.is_authenticated:
            history = ChatHistory.query.filter_by(
                user_id=current_user.id
            ).order_by(ChatHistory.created_at.desc()).limit(20).all()
        else:
            session_id = session.get('session_id')
            history = ChatHistory.query.filter_by(
                session_id=session_id
            ).order_by(ChatHistory.created_at.desc()).limit(20).all()

        return jsonify([{
            'message': h.message,
            'response': h.response,
            'created_at': h.created_at.strftime('%b %d, %H:%M')
        } for h in reversed(history)])

    # ---------- ADD POST ----------
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

        return jsonify({'success': True, 'post_id': post.id})

    # ---------- LIKE POST ----------
    @app.route('/api/post/<int:post_id>/like', methods=['POST'])
    def like_post(post_id):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Login required to like posts'}), 401

        post = Post.query.get_or_404(post_id)
        existing_like = Like.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first()

        if existing_like:
            # Unlike
            db.session.delete(existing_like)
            db.session.commit()
            liked = False
        else:
            # Like
            like = Like(user_id=current_user.id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            liked = True

        like_count = Like.query.filter_by(post_id=post_id).count()
        return jsonify({'liked': liked, 'count': like_count})

    # ---------- SEARCH POSTS ----------
    @app.route('/api/search', methods=['GET'])
    def search_posts():
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])

        posts = Post.query.filter(
            db.or_(
                Post.title.ilike(f'%{query}%'),
                Post.body.ilike(f'%{query}%')
            )
        ).order_by(Post.created_at.desc()).all()

        return jsonify([{
            'id': p.id,
            'title': p.title,
            'body': p.body,
            'author': p.author,
            'created_at': p.created_at.strftime('%b %d, %Y'),
            'likes': len(p.likes)
        } for p in posts])