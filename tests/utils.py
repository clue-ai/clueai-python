import os


def get_api_key() -> str:
    api_key = os.getenv('CLUAI_API_KEY')
    assert api_key, 'CLUEAI_API_KEY environment variable not set'
    return api_key
