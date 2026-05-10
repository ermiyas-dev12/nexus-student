from database.models import db, User


class TestProfileRoutes:
    def test_profile_requires_login(self, client):
        response = client.get("/profile", follow_redirects=True)
        assert response.status_code == 200
        assert b"log in" in response.data.lower()

    def test_profile_page_loads_when_logged_in(self, client, login, regular_user):
        login("test@example.com", "password123")
        response = client.get("/profile")
        assert response.status_code == 200

    def test_edit_profile_username(self, client, login, regular_user, app):
        login("test@example.com", "password123")
        response = client.post("/profile/edit", data={"username": "updatedname"}, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            user = User.query.filter_by(email="test@example.com").first()
            assert user.username == "updatedname"

    def test_change_password_success(self, client, login, regular_user):
        login("test@example.com", "password123")
        response = client.post(
            "/profile/change-password",
            data={
                "old_password": "password123",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"changed" in response.data.lower()

    def test_change_password_wrong_old(self, client, login, regular_user):
        login("test@example.com", "password123")
        response = client.post(
            "/profile/change-password",
            data={"old_password": "wrongold", "new_password": "newpassword456", "confirm_password": "newpassword456"},
            follow_redirects=True,
        )
        assert b"incorrect" in response.data.lower()

    def test_change_password_mismatch(self, client, login, regular_user):
        login("test@example.com", "password123")
        response = client.post(
            "/profile/change-password",
            data={"old_password": "password123", "new_password": "newpassword456", "confirm_password": "differentpass"},
            follow_redirects=True,
        )
        assert b"match" in response.data.lower()

    def test_change_password_too_short(self, client, login, regular_user):
        login("test@example.com", "password123")
        response = client.post(
            "/profile/change-password",
            data={"old_password": "password123", "new_password": "123", "confirm_password": "123"},
            follow_redirects=True,
        )
        assert b"6" in response.data or b"characters" in response.data.lower()
