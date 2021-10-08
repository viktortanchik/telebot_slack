import os
import slack
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
client.chat_postMessage(channel='#test',text="Hello world!")
