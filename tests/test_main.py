from main import hello


def test_hello_returns_greeting_message_with_valid_name_param():
    assert hello("John") == "Hello John!"
