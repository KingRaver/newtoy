import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    
    @staticmethod
    def validate():
        if not all([Config.ANTHROPIC_API_KEY, Config.CHROME_DRIVER_PATH, 
                   Config.TWITTER_USERNAME, Config.TWITTER_PASSWORD]):
            raise ValueError("Missing required environment variables")
