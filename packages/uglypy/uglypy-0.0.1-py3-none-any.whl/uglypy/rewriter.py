import re
import json
import requests
import logging
import argparse
import yaml
import time
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Maximum token count for content truncation
MAX_TOKENS = 32768

# Setup retry strategy for HTTP requests
def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Estimate token count for a given text
def estimate_token_count(text):
    return len(text) // 4  # Simple estimation: 1 token per 4 characters

# Truncate content to fit within the max token limit
def truncate_content(content, max_tokens):
    tokens = content.split()
    truncated_content = []
    current_tokens = 0

    for token in tokens:
        current_tokens += len(token) // 4
        if current_tokens > max_tokens:
            break
        truncated_content.append(token)

    return ' '.join(truncated_content)

# Call OpenAI API for rewriting content
def call_openai_api(api_url, combined_content, model, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'messages': [
            {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
            {"role": "user", "content": combined_content}
        ]
    }
    try:
        response = requests_retry_session().post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        logger.error(f"OpenAI API request failed: {e}")
        return None

# Call Groq API for rewriting content
def call_groq_api(api_url, combined_content, model, api_key):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests_retry_session().post(api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        logger.error(f"Groq API request failed: {e}")
        return None

# Call Ollama API for rewriting content
def call_ollama_api(api_url, combined_content, model):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    }
    try:
        response = requests_retry_session().post(api_url, json=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.RequestException as e:
        logger.error(f"Ollama API request failed: {e}")
        return None

# Ensure text ends with proper punctuation
def ensure_proper_punctuation(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    corrected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        corrected_sentences.append(sentence)

    return ' '.join(corrected_sentences)

# Process each JSON file and rewrite content using the selected API
def process_json_file(filepath, api_url, model, api_key, content_prefix, rewritten_folder, api_type):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error reading JSON from {filepath}: {e}")
        return

    combined_content = content_prefix + "\n".join(
        f"[source {idx + 1}] {item['content']}" for idx, item in enumerate(json_data))

    logger.info(f"Processing {filepath} - combined content prepared.")
    logger.debug(f"Combined content: {combined_content}")

    if estimate_token_count(combined_content) > MAX_TOKENS:
        logger.info(f"Truncating content to fit within {MAX_TOKENS} tokens.")
        combined_content = truncate_content(combined_content, MAX_TOKENS)

    if api_type == "openai":
        rewritten_content = call_openai_api(api_url, combined_content, model, api_key)
    elif api_type == "groq":
        rewritten_content = call_groq_api(api_url, combined_content, model, api_key)
    else:
        rewritten_content = call_ollama_api(api_url, combined_content, model)

    if rewritten_content:
        cleaned_content = re.sub(r'\*\*', '', rewritten_content)
        cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
        cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)

        cleaned_content = ensure_proper_punctuation(cleaned_content)

        links = [item.get('link') for item in json_data if 'link' in item]

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_data = {
            'title': json_data[0].get('title', 'No Title'),
            'content': cleaned_content,
            'processed_at': current_datetime,
            'links': links,
            'api': api_type,
            'model': model
        }

        new_filename = Path(rewritten_folder) / (Path(filepath).stem + '_rewritten.json')
        try:
            with open(new_filename, 'w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, ensure_ascii=False, indent=4)
            logger.info(f"Rewritten file saved to {new_filename}")
        except IOError as e:
            logger.error(f"Error writing to {new_filename}: {e}")
    else:
        logger.error("Failed to get rewritten content from LLM API.")

# Validate API configuration
def validate_config(api_config):
    selected_api = api_config.get('selected_api')

    if selected_api == "OpenAI":
        required_keys = ['openai_api_url', 'openai_api_key', 'openai_model']
    elif selected_api == "Groq":
        required_keys = ['groq_api_url', 'groq_api_key', 'groq_model']
    elif selected_api == "Ollama":
        required_keys = ['ollama_api_url', 'ollama_model']
    else:
        raise ValueError("Invalid API selection. Please choose OpenAI, Groq, or Ollama.")

    missing_keys = [key for key in required_keys if not api_config.get(key)]
    if missing_keys:
        raise ValueError(f"The selected API configuration is incomplete. Missing keys: {', '.join(missing_keys)}")

# Main function to read the config and process files
def main(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        logger.error(f"Error reading config file {config_path}: {e}")
        return

    api_config = config.get('api_config', {})
    folder_config = config.get('folders', {})
    content_prefix = config.get('content_prefix', "")

    validate_config(api_config)

    selected_api = api_config['selected_api']

    if selected_api == 'OpenAI':
        api_url = api_config['openai_api_url']
        model = api_config['openai_model']
        api_key = api_config['openai_api_key']
        api_type = 'openai'
    elif selected_api == 'Groq':
        api_url = api_config['groq_api_url']
        model = api_config['groq_model']
        api_key = api_config['groq_api_key']
        api_type = 'groq'
    else:  # Ollama
        api_url = api_config['ollama_api_url']
        model = api_config['ollama_model']
        api_key = None  # Ollama does not need an API key
        api_type = 'ollama'

    output_folder = folder_config.get('output_folder', 'output')
    rewritten_folder = folder_config.get('rewritten_folder', 'rewritten')

    Path(rewritten_folder).mkdir(parents=True, exist_ok=True)

    json_files = Path(output_folder).glob('*.json')
    for json_file in json_files:
        process_json_file(json_file, api_url, model, api_key, content_prefix, rewritten_folder, api_type)

# Command line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files with LLM API')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration YAML file (default: config.yaml in current directory)')
    args = parser.parse_args()

    config_path = args.config if args.config else 'config.yaml'
    main(config_path)

