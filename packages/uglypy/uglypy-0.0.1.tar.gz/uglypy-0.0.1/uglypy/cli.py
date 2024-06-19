import os
import argparse
import yaml
import logging
from uglypy.rss_retriever import fetch_feeds_from_list
from uglypy.filter import filter_old_items
from uglypy.aggregator import group_similar_articles
from uglypy.rss_generator import generate_rss_feed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(args):
    config = {}

    # Load from config file if specified
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as file:
            config.update(yaml.safe_load(file))
    
    # Override with environment variables if set
    config['rss_feeds'] = os.getenv('RSS_FEEDS', config.get('rss_feeds'))
    config['max_items'] = int(os.getenv('MAX_ITEMS', config.get('max_items', 50)))
    config['max_age_days'] = int(os.getenv('MAX_AGE_DAYS', config.get('max_age_days', 31)))
    config['similarity_threshold'] = float(os.getenv('SIMILARITY_THRESHOLD', config.get('similarity_threshold', 0.66)))
    config['similarity_options'] = {
        'min_samples': int(os.getenv('MIN_SAMPLES', config.get('similarity_options', {}).get('min_samples', 2))),
        'eps': float(os.getenv('EPS', config.get('similarity_options', {}).get('eps', 0.66))),
    }
    config['output_folder'] = os.getenv('OUTPUT_FOLDER', config.get('folders', {}).get('output_folder', 'output'))
    config['rewritten_folder'] = os.getenv('REWRITTEN_FOLDER', config.get('folders', {}).get('rewritten_folder', 'rewritten'))
    config['http_server_port'] = int(os.getenv('HTTP_SERVER_PORT', config.get('http_server_port', 8001)))

    # Override with command-line arguments if provided
    if args.rss_feeds:
        config['rss_feeds'] = args.rss_feeds
    if args.max_items is not None:
        config['max_items'] = args.max_items
    if args.max_age_days is not None:
        config['max_age_days'] = args.max_age_days
    if args.similarity_threshold is not None:
        config['similarity_threshold'] = args.similarity_threshold
    if args.min_samples is not None:
        config['similarity_options']['min_samples'] = args.min_samples
    if args.eps is not None:
        config['similarity_options']['eps'] = args.eps
    if args.output_folder:
        config['output_folder'] = args.output_folder
    if args.rewritten_folder:
        config['rewritten_folder'] = args.rewritten_folder
    if args.http_server_port is not None:
        config['http_server_port'] = args.http_server_port

    return config

def main():
    parser = argparse.ArgumentParser(description='UglyPy - Aggregate and process RSS feeds.')
    parser.add_argument('--rss_feeds', nargs='+', help='List of RSS feed URLs')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration YAML file')
    parser.add_argument('--max_items', type=int, help='Maximum number of items to process')
    parser.add_argument('--max_age_days', type=int, help='Maximum age of items in days to be considered')
    parser.add_argument('--similarity_threshold', type=float, help='Threshold for similarity grouping')
    parser.add_argument('--min_samples', type=int, help='Minimum number of samples in a cluster for DBSCAN')
    parser.add_argument('--eps', type=float, help='Maximum distance between two samples for clustering')
    parser.add_argument('--output_folder', type=str, help='Folder to save the final RSS feed')
    parser.add_argument('--rewritten_folder', type=str, help='Folder to save the rewritten content')
    parser.add_argument('--http_server_port', type=int, help='Port for the HTTP server')
    parser.add_argument('--skip_rewriting', action='store_true', help='Skip the content rewriting step')

    args = parser.parse_args()
    config = load_config(args)

    logger.info('Fetching RSS feeds...')
    items = fetch_feeds_from_list(config['rss_feeds'])

    logger.info(f'Total articles fetched and parsed: {len(items)}')
    logger.info(f'Filtering items older than {config["max_age_days"]} days...')
    items = filter_old_items(items, config['max_age_days'])
    logger.info(f'Filtered down to {len(items)} articles from {len(items)} based on age.')

    if len(items) == 0:
        logger.warning('No items to process after filtering.')
        return

    logger.info('Aggregating similar items...')
    aggregated_items = group_similar_articles(items, config['similarity_threshold'], config['similarity_options'])
    logger.info(f'Aggregated into {len(aggregated_items)} groups.')

    if not args.skip_rewriting:
        logger.info('Rewriting content using LLM API...')
        # Implement your LLM rewriting logic here (if applicable)
        # ...

    logger.info('Generating final RSS feed...')
    output_path = os.path.join(config['output_folder'], 'uglyfeed.xml')
    generate_rss_feed(aggregated_items, config, output_path)
    logger.info(f'RSS feed successfully generated and saved to {output_path}')

if __name__ == "__main__":
    main()

