import json


class TestAPIRoutes:

    def test_add_post_success(self, client):
        response = client.post('/api/post',
            data=json.dumps({'title': 'API Post', 'body': 'Body text', 'author': 'Tester'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'post_id' in data

    def test_add_post_missing_title(self, client):
        response = client.post('/api/post',
            data=json.dumps({'title': '', 'body': 'No title'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_search_posts_empty_query(self, client):
        response = client.get('/api/search?q=')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_search_posts_with_results(self, client, sample_post):
        response = client.get('/api/search?q=Test')
        assert response.status_code == 200
        results = response.get_json()
        assert isinstance(results, list)
        assert len(results) >= 1
        assert results[0]['title'] == 'Test Post'

    def test_search_posts_no_match(self, client):
        response = client.get('/api/search?q=xyznotfound')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_like_post_requires_login(self, client, sample_post):
        response = client.post(f'/api/post/{sample_post}/like',
            content_type='application/json'
        )
        assert response.status_code == 401
        assert 'error' in response.get_json()

    def test_like_post_authenticated(self, client, login, regular_user, sample_post):
        login('test@example.com', 'password123')
        response = client.post(f'/api/post/{sample_post}/like',
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['liked'] is True
        assert data['count'] == 1

    def test_unlike_post(self, client, login, regular_user, sample_post):
        login('test@example.com', 'password123')
        client.post(f'/api/post/{sample_post}/like', content_type='application/json')
        response = client.post(f'/api/post/{sample_post}/like', content_type='application/json')
        data = response.get_json()
        assert data['liked'] is False
        assert data['count'] == 0

    def test_chat_history_anonymous(self, client):
        response = client.get('/api/chat/history')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_chat_history_authenticated(self, client, login, regular_user):
        login('test@example.com', 'password123')
        response = client.get('/api/chat/history')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)