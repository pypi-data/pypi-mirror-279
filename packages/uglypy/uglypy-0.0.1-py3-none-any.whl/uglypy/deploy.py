import os
import yaml
import requests
import base64
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to load configuration from YAML or environment variables
def load_config(config_path=None):
    config = {}

    # Load configuration from file if provided
    if config_path and os.path.exists(config_path):
        logging.info(f"Loading configuration from {config_path}...")
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

    # Overwrite with environment variables if they exist
    config['github_token'] = config.get('github_token', os.getenv('GITHUB_TOKEN'))
    config['gitlab_token'] = config.get('gitlab_token', os.getenv('GITLAB_TOKEN'))
    config['github_repo'] = config.get('github_repo', os.getenv('GITHUB_REPO', 'user/uglyfeed'))
    config['gitlab_repo'] = config.get('gitlab_repo', os.getenv('GITLAB_REPO', 'user/uglyfeed'))
    config['enable_github'] = config.get('enable_github', str(os.getenv('ENABLE_GITHUB', 'true')).lower() == 'true')
    config['enable_gitlab'] = config.get('enable_gitlab', str(os.getenv('ENABLE_GITLAB', 'true')).lower() == 'true')

    return config

# Function to deploy to GitHub
def deploy_to_github(file_path, repo, token):
    logging.info("Deploying to GitHub...")
    file_name = os.path.basename(file_path)
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo}/contents/{file_name}'

    # Read the file content
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Check if the file exists in the repository
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # File exists, retrieve its SHA
        sha = response.json()['sha']
        data = {
            'message': 'Update uglyfeed.xml',
            'content': content,
            'sha': sha,
            'branch': 'main'
        }
        method = requests.put
        logging.info(f"File {file_name} exists in GitHub repo, updating it.")
    elif response.status_code == 404:
        # File does not exist, create it
        data = {
            'message': 'Add uglyfeed.xml',
            'content': content,
            'branch': 'main'
        }
        method = requests.put
        logging.info(f"File {file_name} does not exist in GitHub repo, creating it.")
    else:
        logging.error(f"GitHub file check failed: {response.text}")
        raise Exception(f"GitHub file check failed: {response.text}")

    # Upload or update the file
    response = method(url, json=data, headers=headers)
    if response.status_code in (200, 201):
        download_url = response.json()['content']['download_url']
        return download_url
    else:
        logging.error(f"GitHub upload failed: {response.text}")
        raise Exception(f"GitHub upload failed: {response.text}")

# Function to deploy to GitLab
def deploy_to_gitlab(file_path, repo, token):
    logging.info("Deploying to GitLab...")
    file_name = os.path.basename(file_path)
    headers = {
        'PRIVATE-TOKEN': token
    }
    url = f'https://gitlab.com/api/v4/projects/{repo}/repository/files/{file_name}'

    with open(file_path, 'r') as file:
        content = file.read()

    data = {
        'branch': 'main',
        'content': content,
        'commit_message': 'Add uglyfeed.xml'
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        download_url = f'https://gitlab.com/{repo}/-/raw/main/{file_name}'
        return download_url
    elif response.status_code == 400 and 'already exists' in response.text:
        # Update file if it already exists
        logging.info("File already exists on GitLab, attempting to update...")
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            download_url = f'https://gitlab.com/{repo}/-/raw/main/{file_name}'
            return download_url
        else:
            logging.error(f"GitLab update failed: {response.text}")
            raise Exception(f"GitLab update failed: {response.text}")
    else:
        logging.error(f"GitLab upload failed: {response.text}")
        raise Exception(f"GitLab upload failed: {response.text}")

# Main function to deploy XML file
def deploy_xml(file_path, github_token, gitlab_token, github_repo, gitlab_repo, enable_github, enable_gitlab):
    urls = {}

    if enable_github:
        try:
            github_url = deploy_to_github(file_path, github_repo, github_token)
            urls['github'] = github_url
        except Exception as e:
            logging.error(f"GitHub upload error: {e}")

    if enable_gitlab:
        try:
            gitlab_url = deploy_to_gitlab(file_path, gitlab_repo, gitlab_token)
            urls['gitlab'] = gitlab_url
        except Exception as e:
            logging.error(f"GitLab upload error: {e}")

    return urls

# Command line interface
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy XML file to GitHub or GitLab')
    parser.add_argument('--config', type=str, help='Path to the configuration YAML file')
    parser.add_argument('--file', type=str, default='uglyfeeds/uglyfeed.xml', help='Path to the XML file to deploy')
    parser.add_argument('--github_token', type=str, help='GitHub token')
    parser.add_argument('--gitlab_token', type=str, help='GitLab token')
    parser.add_argument('--github_repo', type=str, help='GitHub repository name')
    parser.add_argument('--gitlab_repo', type=str, help='GitLab repository name')
    parser.add_argument('--enable_github', action='store_true', help='Enable deployment to GitHub')
    parser.add_argument('--enable_gitlab', action='store_true', help='Enable deployment to GitLab')
    args = parser.parse_args()

    # Load configuration from file, environment variables, and arguments
    config = load_config(args.config)

    # Override config with command line arguments if provided
    github_token = args.github_token or config.get('github_token')
    gitlab_token = args.gitlab_token or config.get('gitlab_token')
    github_repo = args.github_repo or config.get('github_repo')
    gitlab_repo = args.gitlab_repo or config.get('gitlab_repo')
    enable_github = args.enable_github or config.get('enable_github', False)
    enable_gitlab = args.enable_gitlab or config.get('enable_gitlab', False)

    # Deploy the XML file
    urls = deploy_xml(args.file, github_token, gitlab_token, github_repo, gitlab_repo, enable_github, enable_gitlab)

    # Print the URLs
    if urls:
        logging.info("File deployed to the following URLs:")
        for platform, url in urls.items():
            print(f"{platform.capitalize()}: {url}")
    else:
        logging.info("No deployments were made.")

