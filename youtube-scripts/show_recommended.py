from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os

if __name__ == "__main__":
    args = argparser.parse_args()
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))

    recommended  = youtube_client.get_recommended()
    print(recommended)