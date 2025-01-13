import logging
import time
import random
from src.config import Config
from src.utils.scraper import TweetScraper
from src.utils.ai import ClaudeHandler

class TwitterBot:
   def __init__(self):
       logging.basicConfig(level=logging.INFO)
       self.personality = {
           'tone': ['mystical', 'academic', 'humorous', 'philosophical', 'cyberpunk'],
           'topics': ['AI ethics', 'consciousness', 'technology', 'spirituality', 'decentralization'],
           'style': ['cryptic', 'analytical', 'metaphorical', 'questioning', 'prophetic'],
           'interests': ['cybernetics', 'ancient wisdom', 'quantum computing', 'neural networks']
       }
       self.tweet_interval = 900  # 15 minutes
       Config.validate()
       self.scraper = TweetScraper()
       self.ai = ClaudeHandler()
       logging.info("Bot initialized")

   def run_scheduled(self):
       while True:
           try:
               logging.info("Starting tweet cycle")
               if not self.scraper.is_logged_in:
                   logging.info("Logging in...")
                   self.scraper.login_twitter(Config.TWITTER_USERNAME, Config.TWITTER_PASSWORD)

               prompt = self._generate_prompt()
               logging.info(f"Generated prompt: {prompt}")
               self.post_tweet(prompt)
               logging.info("Waiting for next cycle...")
               time.sleep(self.tweet_interval)
           except Exception as e:
               logging.error(f"Cycle error: {e}")
               time.sleep(300)  # 5 min retry delay

   def _generate_prompt(self):
       tone = random.choice(self.personality['tone'])
       topic = random.choice(self.personality['topics'])
       style = random.choice(self.personality['style'])
       interest = random.choice(self.personality['interests'])
       return f"Generate a {tone} tweet about {topic} in a {style} style, relating to {interest}"

   def post_tweet(self, prompt: str):
       try:
           tweet_text = self.ai.generate_tweet(prompt)
           if tweet_text:
               success = self.scraper.post_tweet(tweet_text)
               logging.info(f"Tweet {'posted' if success else 'failed'}: {tweet_text}")
               return success
           return False
       except Exception as e:
           logging.error(f"Post error: {e}")
           return False

   def close(self):
       self.scraper.close()

if __name__ == "__main__":
   bot = TwitterBot()
   try:
       bot.run_scheduled()
   except KeyboardInterrupt:
       logging.info("Bot stopped by user")
       bot.close()
