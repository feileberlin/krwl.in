"""
Entity Data Models

Defines data models for locations and organizers used in the unified entity system.
Provides ID generation helpers and JSON serialization methods.
"""

import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, Optional, List


def generate_location_id(name: str, lat: Optional[float] = None, lon: Optional[float] = None) -> str:
    """
    Generate a unique ID for a location.
    
    Creates a consistent ID based on the location's name and coordinates.
    Uses a hash-based approach to ensure uniqueness while maintaining consistency.
    
    Args:
        name: Location name
        lat: Latitude (optional)
        lon: Longitude (optional)
        
    Returns:
        Unique location ID in format 'loc_<hash>'
        
    Examples:
        >>> generate_location_id("Theater Hof", 50.3200, 11.9180)
        'loc_theater_hof'
        >>> generate_location_id("Freiheitshalle")
        'loc_freiheitshalle'
    """
    if not name:
        return "loc_unknown"
    
    # Create a clean slug from the name
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    
    # For common venues, use simple slug
    if len(slug) <= 30:
        return f"loc_{slug}"
    
    # For longer names, use hash
    hash_input = f"{name}_{lat}_{lon}".encode('utf-8')
    hash_hex = hashlib.md5(hash_input).hexdigest()[:8]
    short_slug = slug[:20]
    return f"loc_{short_slug}_{hash_hex}"


def generate_organizer_id(name: str) -> str:
    """
    Generate a unique ID for an organizer.
    
    Creates a consistent ID based on the organizer's name.
    
    Args:
        name: Organizer name
        
    Returns:
        Unique organizer ID in format 'org_<hash>'
        
    Examples:
        >>> generate_organizer_id("Theater Hof")
        'org_theater_hof'
        >>> generate_organizer_id("Kulturverein Hof e.V.")
        'org_kulturverein_hof_e_v'
    """
    if not name:
        return "org_unknown"
    
    # Create a clean slug from the name
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    
    # For common organizers, use simple slug
    if len(slug) <= 30:
        return f"org_{slug}"
    
    # For longer names, use hash
    hash_hex = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
    short_slug = slug[:20]
    return f"org_{short_slug}_{hash_hex}"


@dataclass
class Location:
    """
    Location data model for the entity system.
    
    Represents a physical venue where events can take place.
    Supports verification status and usage tracking.
    """
    
    id: str
    name: str
    lat: float
    lon: float
    address: Optional[str] = None
    verified: bool = False
    aliases: List[str] = field(default_factory=list)
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    usage_count: int = 0
    
    def __post_init__(self):
        """Set timestamps if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert location to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the location
        """
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        """
        Create a Location instance from a dictionary.
        
        Args:
            data: Dictionary containing location data
            
        Returns:
            Location instance
        """
        # Extract known fields
        known_fields = {
            'id', 'name', 'lat', 'lon', 'address', 'verified', 
            'aliases', 'phone', 'website', 'description',
            'created_at', 'updated_at', 'usage_count'
        }
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        
        # Ensure aliases is a list
        if 'aliases' in filtered_data and not isinstance(filtered_data['aliases'], list):
            filtered_data['aliases'] = []
        
        return cls(**filtered_data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now().isoformat()
    
    def matches_name(self, query: str) -> bool:
        """
        Check if location matches a name query.
        
        Matches against the main name and all aliases (case-insensitive).
        
        Args:
            query: Search query string
            
        Returns:
            True if the query matches the name or any alias
        """
        query_lower = query.lower()
        
        # Check main name
        if query_lower in self.name.lower():
            return True
        
        # Check aliases
        for alias in self.aliases:
            if query_lower in alias.lower():
                return True
        
        return False


@dataclass
class Organizer:
    """
    Organizer data model for the entity system.
    
    Represents an organization or person that organizes events.
    Supports verification status and contact information.
    """
    
    id: str
    name: str
    verified: bool = False
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    usage_count: int = 0
    
    def __post_init__(self):
        """Set timestamps if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert organizer to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the organizer
        """
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Organizer':
        """
        Create an Organizer instance from a dictionary.
        
        Args:
            data: Dictionary containing organizer data
            
        Returns:
            Organizer instance
        """
        # Extract known fields
        known_fields = {
            'id', 'name', 'verified', 'email', 'phone', 'website',
            'description', 'aliases', 'created_at', 'updated_at', 'usage_count'
        }
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        
        # Ensure aliases is a list
        if 'aliases' in filtered_data and not isinstance(filtered_data['aliases'], list):
            filtered_data['aliases'] = []
        
        return cls(**filtered_data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now().isoformat()
    
    def matches_name(self, query: str) -> bool:
        """
        Check if organizer matches a name query.
        
        Matches against the main name and all aliases (case-insensitive).
        
        Args:
            query: Search query string
            
        Returns:
            True if the query matches the name or any alias
        """
        query_lower = query.lower()
        
        # Check main name
        if query_lower in self.name.lower():
            return True
        
        # Check aliases
        for alias in self.aliases:
            if query_lower in alias.lower():
                return True
        
        return False
