from flask import render_template, request
from database.models import Post, Like
from flask_login import current_user

def register_main_routes(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chatbot')
    def chatbot():
        return render_template('chatbot.html')

    @app.route('/resources')
    def resources():
        return render_template('resources.html')

    @app.route('/community')
    def community():
        query = request.args.get('q', '').strip()

        if query:
            posts = Post.query.filter(
                Post.title.ilike(f'%{query}%') |
                Post.body.ilike(f'%{query}%')
            ).order_by(Post.created_at.desc()).all()
        else:
            posts = Post.query.order_by(Post.created_at.desc()).all()

        # Get liked post ids for current user
        liked_post_ids = []
        if current_user.is_authenticated:
            liked_post_ids = [
                like.post_id for like in
                Like.query.filter_by(user_id=current_user.id).all()
            ]

        return render_template('community.html',
                               posts=posts,
                               query=query,
                               liked_post_ids=liked_post_ids)

    @app.route('/emergency')
    def emergency():
        return render_template('emergency.html')
