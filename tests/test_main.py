class TestMainRoutes:

    def test_home_page_loads(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_chatbot_page_loads(self, client):
        response = client.get('/chatbot')
        assert response.status_code == 200

    def test_resources_page_loads(self, client):
        response = client.get('/resources')
        assert response.status_code == 200

    def test_emergency_page_loads(self, client):
        response = client.get('/emergency')
        assert response.status_code == 200

    def test_community_page_loads(self, client):
        response = client.get('/community')
        assert response.status_code == 200

    def test_community_search(self, client, sample_post):
        response = client.get('/community?q=Test')
        assert response.status_code == 200
        assert b'Test' in response.data

    def test_community_search_no_results(self, client):
        response = client.get('/community?q=xyznonexistent')
        assert response.status_code == 200