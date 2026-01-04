"""Data I/O utilities for events"""

import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def load_events(base_path):
    """
    Load published events.
    
    Args:
        base_path: Repository root path
        
    Returns:
        dict: Events data with 'events' key
    """
    events_file = base_path / 'assets' / 'json' / 'events.json'
    
    try:
        with open(events_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Events file not found: {events_file}")
        return {'events': [], 'metadata': {'last_updated': datetime.now().isoformat()}}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in events file: {e}")
        return {'events': [], 'metadata': {'last_updated': datetime.now().isoformat()}}


def save_events(base_path, events_data):
    """
    Save published events.
    
    Args:
        base_path: Repository root path
        events_data: Events data dictionary
    """
    events_file = base_path / 'assets' / 'json' / 'events.json'
    events_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Update metadata
    if 'metadata' not in events_data:
        events_data['metadata'] = {}
    events_data['metadata']['last_updated'] = datetime.now().isoformat()
    
    with open(events_file, 'w') as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(events_data.get('events', []))} events")


def load_pending_events(base_path):
    """
    Load pending events awaiting review.
    
    Args:
        base_path: Repository root path
        
    Returns:
        dict: Pending events data with 'pending_events' key
    """
    pending_file = base_path / 'assets' / 'json' / 'pending_events.json'
    
    try:
        with open(pending_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.debug(f"Pending file not found, creating: {pending_file}")
        return {'pending_events': [], 'metadata': {'last_updated': datetime.now().isoformat()}}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in pending file: {e}")
        return {'pending_events': [], 'metadata': {'last_updated': datetime.now().isoformat()}}


def save_pending_events(base_path, pending_data):
    """
    Save pending events.
    
    Args:
        base_path: Repository root path
        pending_data: Pending events data dictionary
    """
    pending_file = base_path / 'assets' / 'json' / 'pending_events.json'
    pending_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Update metadata
    if 'metadata' not in pending_data:
        pending_data['metadata'] = {}
    pending_data['metadata']['last_updated'] = datetime.now().isoformat()
    
    with open(pending_file, 'w') as f:
        json.dump(pending_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(pending_data.get('pending_events', []))} pending events")


def load_rejected_events(base_path):
    """
    Load rejected events log.
    
    Args:
        base_path: Repository root path
        
    Returns:
        dict: Rejected events data
    """
    rejected_file = base_path / 'assets' / 'json' / 'rejected_events.json'
    
    try:
        with open(rejected_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'rejected_events': []}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in rejected file: {e}")
        return {'rejected_events': []}


def save_rejected_events(base_path, rejected_data):
    """
    Save rejected events log.
    
    Args:
        base_path: Repository root path
        rejected_data: Rejected events data dictionary
    """
    rejected_file = base_path / 'assets' / 'json' / 'rejected_events.json'
    rejected_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(rejected_file, 'w') as f:
        json.dump(rejected_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(rejected_data.get('rejected_events', []))} rejected events")


def load_historical_events(base_path):
    """
    Load archived historical events.
    
    Args:
        base_path: Repository root path
        
    Returns:
        list: Historical events
    """
    archived_file = base_path / 'assets' / 'json' / 'archived_events.json'
    
    try:
        with open(archived_file, 'r') as f:
            data = json.load(f)
            return data.get('archived_events', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
