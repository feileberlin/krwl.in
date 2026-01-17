"""Shared date parsing utilities for custom scrapers."""

from datetime import datetime, timedelta
from typing import Optional
import re
import hashlib


def extract_date_from_text(text: str, default_hour: int = 18) -> str:
    """
    Extract date from text using German date patterns.
    
    Args:
        text: Text containing date information
        default_hour: Default hour to use if only date is found (default: 18:00)
        
    Returns:
        ISO format datetime string, or future date if no valid date found
    """
    patterns = [
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'DMY'),  # DD.MM.YYYY
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', 'DMY_SHORT'),  # DD.MM.YY
        (r'(\d{4})-(\d{2})-(\d{2})', 'YMD'),  # YYYY-MM-DD
        (r'ab\s+(\d{1,2})\.(\d{1,2})\.(\d{4})', 'DMY'),  # ab DD.MM.YYYY
    ]
    
    for pattern, format_type in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                groups = match.groups()
                if format_type == 'DMY':
                    day, month, year = groups[-3:]
                    day, month, year = int(day), int(month), int(year)
                elif format_type == 'DMY_SHORT':
                    day, month, year = groups[-3:]
                    day, month = int(day), int(month)
                    year = int(year)
                    # Use dynamic cutoff based on current year
                    current_year = datetime.now().year
                    current_century = (current_year // 100) * 100
                    # If year is more than 50 years in the future, assume previous century
                    full_year = current_century + year
                    if full_year > current_year + 50:
                        full_year -= 100
                    year = full_year
                elif format_type == 'YMD':
                    year, month, day = groups[-3:]
                    day, month, year = int(day), int(month), int(year)
                
                # Validate date components before creating datetime
                if not (1 <= day <= 31 and 1 <= month <= 12):
                    continue
                    
                date = datetime(year, month, day, default_hour, 0)
                
                # Only return dates in the future
                if date > datetime.now():
                    return date.isoformat()
            except (ValueError, TypeError):
                continue
    
    # Default to next week if no valid date found
    return (datetime.now() + timedelta(days=7)).replace(
        hour=default_hour, minute=0
    ).isoformat()


def generate_stable_event_id(prefix: str, *components: str) -> str:
    """
    Generate a stable, deterministic event ID using MD5 hashing.
    
    Args:
        prefix: Prefix for the ID (e.g., 'freiheitshalle', 'vhs')
        *components: Components to hash (title, start_time, etc.)
        
    Returns:
        Stable event ID string
    """
    # Join components and create deterministic hash
    content = '|'.join(str(c) for c in components)
    hash_value = hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
    return f"{prefix}_{hash_value}"
