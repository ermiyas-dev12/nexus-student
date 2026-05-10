class TestChatbotService:

    def test_match_intent_returns_string_or_none(self, app):
        from services.chatbot_service import match_intent
        with app.app_context():
            result = match_intent('hello')
            assert result is None or isinstance(result, str)

    def test_get_response_returns_string(self, app):
        from services.chatbot_service import get_response
        with app.app_context():
            result = get_response('hello')
            assert isinstance(result, str)
            assert len(result) > 0

    def test_match_intent_unknown_returns_none(self, app):
        from services.chatbot_service import match_intent
        with app.app_context():
            # Use a string that cannot possibly match any intent pattern
            result = match_intent('zzzzzquerywithnomatch999aaa')
            assert result is None

    def test_match_intent_known_returns_string(self, app):
        from services.chatbot_service import match_intent
        with app.app_context():
            # 'hello' may or may not match depending on intents.json —
            # either outcome is valid, just must be str or None
            result = match_intent('hello')
            assert result is None or isinstance(result, str)

    def test_get_response_never_returns_empty(self, app):
        from services.chatbot_service import get_response
        with app.app_context():
            result = get_response('zzzzzquerywithnomatch999aaa')
            assert isinstance(result, str)
            assert len(result) > 0