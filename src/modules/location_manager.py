"""
Location Manager

Provides CRUD operations for managing the locations library.
Supports search, verification, deduplication, and statistics.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from .entity_models import Location, generate_location_id

# Configure module logger
logger = logging.getLogger(__name__)


class LocationManager:
    """
    Manages the locations library (locations.json).
    
    Provides CRUD operations, search, verification, and deduplication features.
    Automatically backs up the locations file on save operations.
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize location manager.
        
        Args:
            base_path: Repository root path
        """
        self.base_path = Path(base_path)
        self.locations_file = self.base_path / 'assets' / 'json' / 'locations.json'
        self.backup_dir = self.base_path / 'assets' / 'json' / 'backups' / 'locations'
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.locations: Dict[str, Location] = {}
        self._load_locations()
    
    def _load_locations(self):
        """Load locations from JSON file."""
        if not self.locations_file.exists():
            logger.info("No locations.json found, starting with empty library")
            return
        
        try:
            with open(self.locations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                locations_dict = data.get('locations', {})
                
                for loc_id, loc_data in locations_dict.items():
                    try:
                        self.locations[loc_id] = Location.from_dict(loc_data)
                    except Exception as e:
                        logger.warning(f"Failed to load location {loc_id}: {e}")
            
            logger.info(f"Loaded {len(self.locations)} locations from library")
        except Exception as e:
            logger.error(f"Could not load locations.json: {e}")
            raise
    
    def _save_locations(self):
        """Save locations to JSON file with automatic backup."""
        # Create backup
        if self.locations_file.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f"locations_{timestamp}.json"
            shutil.copy2(self.locations_file, backup_file)
            logger.info(f"Created backup: {backup_file.name}")
        
        # Save locations
        data = {
            'locations': {
                loc_id: location.to_dict()
                for loc_id, location in self.locations.items()
            },
            'last_updated': datetime.now().isoformat(),
            'total_count': len(self.locations)
        }
        
        try:
            with open(self.locations_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.locations)} locations to library")
        except Exception as e:
            logger.error(f"Failed to save locations.json: {e}")
            raise
    
    def add(self, name: str, lat: float, lon: float, address: Optional[str] = None,
            verified: bool = False, **kwargs) -> Location:
        """
        Add a new location to the library.
        
        Args:
            name: Location name
            lat: Latitude
            lon: Longitude
            address: Street address (optional)
            verified: Verification status (default: False)
            **kwargs: Additional optional fields (phone, website, description, aliases)
            
        Returns:
            Created Location instance
            
        Raises:
            ValueError: If location with same name already exists
        """
        # Check for duplicates
        for location in self.locations.values():
            if location.name.lower() == name.lower():
                raise ValueError(f"Location with name '{name}' already exists (ID: {location.id})")
        
        # Generate ID
        location_id = generate_location_id(name, lat, lon)
        
        # Handle ID collision
        if location_id in self.locations:
            # Add counter to make it unique
            counter = 2
            while f"{location_id}_{counter}" in self.locations:
                counter += 1
            location_id = f"{location_id}_{counter}"
        
        # Create location
        location = Location(
            id=location_id,
            name=name,
            lat=lat,
            lon=lon,
            address=address,
            verified=verified,
            aliases=kwargs.get('aliases', []),
            phone=kwargs.get('phone'),
            website=kwargs.get('website'),
            description=kwargs.get('description')
        )
        
        self.locations[location_id] = location
        self._save_locations()
        
        logger.info(f"Added location: {name} (ID: {location_id})")
        return location
    
    def update(self, location_id: str, **kwargs) -> Location:
        """
        Update an existing location.
        
        Args:
            location_id: ID of location to update
            **kwargs: Fields to update (name, lat, lon, address, etc.)
            
        Returns:
            Updated Location instance
            
        Raises:
            KeyError: If location_id not found
        """
        if location_id not in self.locations:
            raise KeyError(f"Location {location_id} not found")
        
        location = self.locations[location_id]
        
        # Update fields
        for field, value in kwargs.items():
            if hasattr(location, field):
                setattr(location, field, value)
        
        location.update_timestamp()
        self._save_locations()
        
        logger.info(f"Updated location: {location.name} (ID: {location_id})")
        return location
    
    def delete(self, location_id: str) -> bool:
        """
        Delete a location from the library.
        
        Args:
            location_id: ID of location to delete
            
        Returns:
            True if deleted, False if not found
        """
        if location_id not in self.locations:
            logger.warning(f"Location {location_id} not found for deletion")
            return False
        
        location_name = self.locations[location_id].name
        del self.locations[location_id]
        self._save_locations()
        
        logger.info(f"Deleted location: {location_name} (ID: {location_id})")
        return True
    
    def get(self, location_id: str) -> Optional[Location]:
        """
        Get a location by ID.
        
        Args:
            location_id: ID of location to retrieve
            
        Returns:
            Location instance or None if not found
        """
        return self.locations.get(location_id)
    
    def list(self, verified_only: bool = False) -> List[Location]:
        """
        List all locations.
        
        Args:
            verified_only: If True, only return verified locations
            
        Returns:
            List of Location instances
        """
        locations = list(self.locations.values())
        
        if verified_only:
            locations = [loc for loc in locations if loc.verified]
        
        # Sort by name
        locations.sort(key=lambda x: x.name.lower())
        return locations
    
    def search(self, query: str) -> List[Location]:
        """
        Search locations by name or alias.
        
        Case-insensitive substring matching.
        
        Args:
            query: Search query
            
        Returns:
            List of matching Location instances
        """
        results = []
        
        for location in self.locations.values():
            if location.matches_name(query):
                results.append(location)
        
        # Sort by relevance (exact match first, then alphabetically)
        query_lower = query.lower()
        results.sort(key=lambda x: (
            x.name.lower() != query_lower,  # Exact matches first
            x.name.lower()
        ))
        
        return results
    
    def verify(self, location_id: str) -> bool:
        """
        Mark a location as verified.
        
        Args:
            location_id: ID of location to verify
            
        Returns:
            True if verified, False if not found
        """
        if location_id not in self.locations:
            logger.warning(f"Location {location_id} not found for verification")
            return False
        
        location = self.locations[location_id]
        location.verified = True
        location.update_timestamp()
        self._save_locations()
        
        logger.info(f"Verified location: {location.name} (ID: {location_id})")
        return True
    
    def merge_locations(self, source_id: str, target_id: str) -> bool:
        """
        Merge source location into target location.
        
        Combines data from source into target and deletes source.
        Useful for deduplication.
        
        Args:
            source_id: ID of location to merge (will be deleted)
            target_id: ID of location to merge into (will be kept)
            
        Returns:
            True if merged successfully, False otherwise
        """
        if source_id not in self.locations or target_id not in self.locations:
            logger.error(f"Cannot merge: one or both locations not found")
            return False
        
        source = self.locations[source_id]
        target = self.locations[target_id]
        
        # Merge aliases
        target.aliases = list(set(target.aliases + source.aliases + [source.name]))
        
        # Merge optional fields (keep target if exists, otherwise use source)
        if not target.address and source.address:
            target.address = source.address
        if not target.phone and source.phone:
            target.phone = source.phone
        if not target.website and source.website:
            target.website = source.website
        if not target.description and source.description:
            target.description = source.description
        
        # Update usage count
        target.usage_count += source.usage_count
        
        # Mark as verified if either was verified
        target.verified = target.verified or source.verified
        
        target.update_timestamp()
        
        # Delete source
        del self.locations[source_id]
        
        self._save_locations()
        
        logger.info(f"Merged location {source.name} (ID: {source_id}) into {target.name} (ID: {target_id})")
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the locations library.
        
        Returns:
            Dictionary with statistics
        """
        locations = list(self.locations.values())
        
        verified_count = sum(1 for loc in locations if loc.verified)
        
        # Find most used locations
        most_used = sorted(locations, key=lambda x: x.usage_count, reverse=True)[:10]
        
        return {
            'total_locations': len(locations),
            'verified_locations': verified_count,
            'unverified_locations': len(locations) - verified_count,
            'locations_with_address': sum(1 for loc in locations if loc.address),
            'locations_with_phone': sum(1 for loc in locations if loc.phone),
            'locations_with_website': sum(1 for loc in locations if loc.website),
            'most_used_locations': [
                {'id': loc.id, 'name': loc.name, 'usage_count': loc.usage_count}
                for loc in most_used
            ]
        }
