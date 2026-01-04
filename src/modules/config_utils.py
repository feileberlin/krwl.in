"""Configuration and environment detection utilities"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def is_ci():
    """
    Detect if running in CI environment.
    
    Checks for common CI environment variables set by:
    - GitHub Actions (GITHUB_ACTIONS, CI)
    - GitLab CI (GITLAB_CI, CI)
    - Travis CI (TRAVIS, CI)
    - CircleCI (CIRCLECI, CI)
    - Jenkins (JENKINS_HOME, JENKINS_URL)
    - Bitbucket Pipelines (BITBUCKET_BUILD_NUMBER)
    - Azure Pipelines (TF_BUILD)
    - AWS CodeBuild (CODEBUILD_BUILD_ID)
    
    Returns:
        bool: True if running in CI, False otherwise
    """
    ci_indicators = [
        'CI',
        'GITHUB_ACTIONS',
        'GITLAB_CI',
        'TRAVIS',
        'CIRCLECI',
        'JENKINS_HOME', 'JENKINS_URL',
        'BITBUCKET_BUILD_NUMBER',
        'TF_BUILD',
        'CODEBUILD_BUILD_ID'
    ]
    
    return any(os.environ.get(var) for var in ci_indicators)


def is_production():
    """
    Detect if running in production environment.
    
    Checks for production indicators from major hosting platforms.
    
    Returns:
        bool: True if in production, False otherwise
    """
    # Explicit production setting
    env = os.environ.get('ENVIRONMENT') or os.environ.get('NODE_ENV')
    if env == 'production':
        return True
    
    # Vercel
    if os.environ.get('VERCEL_ENV') == 'production':
        return True
    
    # Netlify
    if os.environ.get('NETLIFY') == 'true' and os.environ.get('CONTEXT') == 'production':
        return True
    
    # Heroku
    if os.environ.get('DYNO'):
        return True
    
    # Railway
    if os.environ.get('RAILWAY_ENVIRONMENT') == 'production':
        return True
    
    # Render
    if os.environ.get('RENDER') == 'true' and os.environ.get('IS_PULL_REQUEST') != 'true':
        return True
    
    # Fly.io
    if os.environ.get('FLY_APP_NAME'):
        return True
    
    # Google Cloud Run
    if os.environ.get('K_SERVICE'):
        return True
    
    # AWS (non-Lambda)
    if os.environ.get('AWS_EXECUTION_ENV') and 'lambda' not in os.environ.get('AWS_EXECUTION_ENV', '').lower():
        return True
    
    return False


def is_development():
    """
    Detect if running in development environment.
    
    Returns:
        bool: True if in development (not CI and not production)
    """
    return not is_production() and not is_ci()


def validate_config(config):
    """
    Validate configuration structure.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_sections = ['app', 'map', 'scraping']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required section: {section}")
    
    return True


def load_config(base_path):
    """
    Load configuration with automatic environment detection.
    
    Args:
        base_path: Repository root path
        
    Returns:
        dict: Configuration with environment overrides applied
    """
    config_file = base_path / 'config.json'
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise
    
    # Validate base config
    validate_config(config)
    
    # Apply environment-specific overrides
    if is_development():
        logger.info("🚀 Running in development mode")
        config['debug'] = True
        config['data']['source'] = 'both'
        config['watermark']['text'] = 'DEV'
        config['performance']['cache_enabled'] = False
        config['performance']['prefetch_events'] = False
    elif is_ci() or is_production():
        mode = 'ci' if is_ci() else 'production'
        logger.info(f"🚀 Running in {mode} mode")
        config['debug'] = False
        config['data']['source'] = 'real'
        config['watermark']['text'] = 'PRODUCTION'
        config['performance']['cache_enabled'] = True
        config['performance']['prefetch_events'] = True
    
    return config
