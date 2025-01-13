       *****DOES NOT WORK CURRENTLY*****

import pytest
from unittest.mock import Mock, patch
from src.bot import TwitterBot

@pytest.fixture
def mocked_bot():
    with patch('src.utils.scraper.TweetScraper') as MockTweetScraper:
        # Setup mock scraper with is_logged_in property
        mock_scraper = Mock()
        mock_scraper.is_logged_in = True
        MockTweetScraper.return_value = mock_scraper
        
        bot = TwitterBot()
        bot.scraper = mock_scraper
        return bot

def test_generate_prompt(mocked_bot):
    prompt = mocked_bot._generate_prompt()
    assert isinstance(prompt, str)
    assert 'Generate a' in prompt
    assert 'tweet about' in prompt
    assert 'style' in prompt
    assert 'relating to' in prompt

def test_post_tweet_success(mocked_bot):
    with patch('src.utils.ai.ClaudeHandler.generate_tweet') as mock_generate:
        with patch.object(mocked_bot.scraper, 'post_tweet') as mock_post:
            # Setup
            mock_generate.return_value = "Test tweet"
            mock_post.return_value = True
            
            # Run
            result = mocked_bot.post_tweet("test prompt")
            
            # Verify
            mock_generate.assert_called_once()
            mock_post.assert_called_once_with("Test tweet")

def test_tweet_cycle(mocked_bot):
    with patch.object(mocked_bot.scraper, 'login_twitter') as mock_login:
        with patch.object(mocked_bot, 'post_tweet') as mock_post:
            with patch('time.sleep') as mock_sleep:  # Prevent actual sleeping
                # Setup
                mock_login.return_value = True
                mock_post.return_value = True
                
                # Run
                try:
                    mocked_bot.run_scheduled()
                except KeyboardInterrupt:  # Simulate stopping the bot
                    pass
                
                # Verify
                mock_post.assert_called()

def test_ai_handler(mocked_bot):
    with patch('anthropic.Anthropic'):
        handler = mocked_bot.ai
        assert handler is not None

def test_error_handling(mocked_bot):
    with patch('src.utils.ai.ClaudeHandler.generate_tweet') as mock_generate:
        mock_generate.side_effect = Exception("Test error")
        result = mocked_bot.post_tweet("test prompt")
        assert isinstance(result, str)  # Should return error message string
