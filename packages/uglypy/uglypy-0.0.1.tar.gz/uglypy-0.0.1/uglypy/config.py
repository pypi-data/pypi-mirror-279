import os
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    """Load configuration from a YAML file, environment variables, and merge them."""
    config = {}
    
    # Load YAML config
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    else:
        logger.warning(f"Configuration file {config_path} not found. Falling back to environment variables.")

    # Override with environment variables if available
    config['similarity_threshold'] = float(os.getenv('SIMILARITY_THRESHOLD', config.get('similarity_threshold', 0.66)))
    config['similarity_options'] = {
        'min_samples': int(os.getenv('SIMILARITY_MIN_SAMPLES', config.get('similarity_options', {}).get('min_samples', 2))),
        'eps': float(os.getenv('SIMILARITY_EPS', config.get('similarity_options', {}).get('eps', 0.66)))
    }

    config['api_config'] = {
        'selected_api': os.getenv('API_SELECTED', config.get('api_config', {}).get('selected_api', 'Groq')),
        'openai_api_url': os.getenv('OPENAI_API_URL', config.get('api_config', {}).get('openai_api_url')),
        'openai_api_key': os.getenv('OPENAI_API_KEY', config.get('api_config', {}).get('openai_api_key')),
        'openai_model': os.getenv('OPENAI_MODEL', config.get('api_config', {}).get('openai_model')),
        'groq_api_url': os.getenv('GROQ_API_URL', config.get('api_config', {}).get('groq_api_url')),
        'groq_api_key': os.getenv('GROQ_API_KEY', config.get('api_config', {}).get('groq_api_key')),
        'groq_model': os.getenv('GROQ_MODEL', config.get('api_config', {}).get('groq_model')),
        'ollama_api_url': os.getenv('OLLAMA_API_URL', config.get('api_config', {}).get('ollama_api_url')),
        'ollama_model': os.getenv('OLLAMA_MODEL', config.get('api_config', {}).get('ollama_model'))
    }

    config['folders'] = {
        'output_folder': os.getenv('OUTPUT_FOLDER', config.get('folders', {}).get('output_folder', 'output')),
        'rewritten_folder': os.getenv('REWRITTEN_FOLDER', config.get('folders', {}).get('rewritten_folder', 'rewritten'))
    }

    config['content_prefix'] = os.getenv('CONTENT_PREFIX', config.get('content_prefix', ''))

    config['max_items'] = int(os.getenv('MAX_ITEMS', config.get('max_items', 50)))
    config['max_age_days'] = int(os.getenv('MAX_AGE_DAYS', config.get('max_age_days', 10)))
    config['feed_title'] = os.getenv('FEED_TITLE', config.get('feed_title', 'UglyFeed RSS'))
    config['feed_link'] = os.getenv('FEED_LINK', config.get('feed_link', 'https://github.com/fabriziosalmi/UglyFeed'))
    config['feed_description'] = os.getenv('FEED_DESCRIPTION', config.get('feed_description', 'A dynamically generated feed using UglyFeed.'))
    config['feed_language'] = os.getenv('FEED_LANGUAGE', config.get('feed_language', 'it'))
    config['feed_self_link'] = os.getenv('FEED_SELF_LINK', config.get('feed_self_link', 'https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml'))
    config['author'] = os.getenv('AUTHOR', config.get('author', 'UglyFeed'))
    config['category'] = os.getenv('CATEGORY', config.get('category', 'Technology'))
    config['copyright'] = os.getenv('COPYRIGHT', config.get('copyright', 'UglyFeed'))

    config['scheduling_enabled'] = bool(os.getenv('SCHEDULING_ENABLED', config.get('scheduling_enabled', True)))
    config['scheduling_interval'] = int(os.getenv('SCHEDULING_INTERVAL', config.get('scheduling_interval', 4)))
    config['scheduling_period'] = os.getenv('SCHEDULING_PERIOD', config.get('scheduling_period', 'hours'))

    config['http_server_port'] = int(os.getenv('HTTP_SERVER_PORT', config.get('http_server_port', 8001)))

    config['github_token'] = os.getenv('GITHUB_TOKEN', config.get('github_token'))
    config['gitlab_token'] = os.getenv('GITLAB_TOKEN', config.get('gitlab_token'))
    config['github_repo'] = os.getenv('GITHUB_REPO', config.get('github_repo'))
    config['gitlab_repo'] = os.getenv('GITLAB_REPO', config.get('gitlab_repo'))
    config['enable_github'] = bool(os.getenv('ENABLE_GITHUB', config.get('enable_github', False)))
    config['enable_gitlab'] = bool(os.getenv('ENABLE_GITLAB', config.get('enable_gitlab', False)))

    return config

