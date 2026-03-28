from flask import render_template
from database.models import Post

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
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('community.html', posts=posts)

    @app.route('/emergency')
    def emergency():
        return render_template('emergency.html')