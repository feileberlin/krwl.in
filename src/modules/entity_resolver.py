"""
Entity Resolver - Three-Tier Override System

Implements flexible event entity resolution:
- Tier 1: Reference only (location_id) → load from locations.json
- Tier 2: Partial override (location_id + location_override) → merge
- Tier 3: Full override (embedded location) → use as-is

This allows events to share common locations while supporting event-specific
customizations when needed (e.g., VIP entrance, temporary stage).
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from copy import deepcopy

logger = logging.getLogger(__name__)


class EntityResolver:
    """
    Resolves entity references with three-tier override support.
    
    Usage:
        resolver = EntityResolver(base_path)
        resolved_event = resolver.resolve_event(event)
        resolved_events = resolver.resolve_events(events)
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize entity resolver.
        
        Args:
            base_path: Repository root path
        """
        self.base_path = Path(base_path)
        self.locations_file = self.base_path / 'assets' / 'json' / 'locations.json'
        self.organizers_file = self.base_path / 'assets' / 'json' / 'organizers.json'
        
        # Load libraries
        self.locations = self._load_locations()
        self.organizers = self._load_organizers()
        
        # Track usage statistics
        self.stats = {
            'location_tier1': 0,  # Reference only
            'location_tier2': 0,  # Partial override
            'location_tier3': 0,  # Full override
            'organizer_tier1': 0,
            'organizer_tier2': 0,
            'organizer_tier3': 0,
        }
    
    def _load_locations(self) -> Dict[str, dict]:
        """Load locations library from JSON"""
        if not self.locations_file.exists():
            logger.warning(f"Locations file not found: {self.locations_file}")
            return {}
        
        try:
            with open(self.locations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                locations = data.get('locations', [])
                # Convert list to dict keyed by ID for fast lookup
                return {loc['id']: loc for loc in locations}
        except Exception as e:
            logger.error(f"Failed to load locations: {e}")
            return {}
    
    def _load_organizers(self) -> Dict[str, dict]:
        """Load organizers library from JSON"""
        if not self.organizers_file.exists():
            logger.warning(f"Organizers file not found: {self.organizers_file}")
            return {}
        
        try:
            with open(self.organizers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                organizers = data.get('organizers', [])
                # Convert list to dict keyed by ID for fast lookup
                return {org['id']: org for org in organizers}
        except Exception as e:
            logger.error(f"Failed to load organizers: {e}")
            return {}
    
    def resolve_event_location(self, event: dict) -> dict:
        """
        Resolve event location with three-tier system.
        
        Tier 1 (Reference only):
            event = {"location_id": "loc_theater_hof"}
            → Load complete location from locations.json
        
        Tier 2 (Partial override):
            event = {
                "location_id": "loc_theater_hof",
                "location_override": {"name": "Theater Hof - VIP Lounge"}
            }
            → Load base, merge override fields
        
        Tier 3 (Full override):
            event = {"location": {"name": "Temporary Stage", "lat": 50.32, "lon": 11.92}}
            → Use embedded location as-is
        
        Args:
            event: Event dictionary
            
        Returns:
            Resolved location dictionary
        """
        # Tier 3: Full override (embedded location)
        if 'location' in event and isinstance(event['location'], dict):
            if 'lat' in event['location'] and 'lon' in event['location']:
                self.stats['location_tier3'] += 1
                return deepcopy(event['location'])
        
        # Tier 1 & 2: Reference-based
        location_id = event.get('location_id')
        if not location_id:
            # Fallback: If no location_id but embedded location exists
            if 'location' in event:
                return deepcopy(event['location'])
            # No location at all
            logger.warning(f"Event {event.get('id')} has no location_id or location")
            return {}
        
        # Load base location
        base_location = self.locations.get(location_id)
        if not base_location:
            logger.warning(f"Location ID not found: {location_id}")
            # Fallback to embedded location if exists
            if 'location' in event:
                return deepcopy(event['location'])
            return {'name': f'Unknown Location ({location_id})'}
        
        # Tier 1: Reference only (no override)
        if 'location_override' not in event:
            self.stats['location_tier1'] += 1
            return deepcopy(base_location)
        
        # Tier 2: Partial override
        self.stats['location_tier2'] += 1
        resolved = deepcopy(base_location)
        override = event['location_override']
        
        # Merge override fields into base
        for key, value in override.items():
            resolved[key] = value
        
        return resolved
    
    def resolve_event_organizer(self, event: dict) -> Optional[dict]:
        """
        Resolve event organizer with three-tier system.
        
        Same logic as location resolution but for organizers.
        
        Args:
            event: Event dictionary
            
        Returns:
            Resolved organizer dictionary or None
        """
        # Tier 3: Full override (embedded organizer)
        if 'organizer' in event and isinstance(event['organizer'], dict):
            if 'name' in event['organizer']:
                self.stats['organizer_tier3'] += 1
                return deepcopy(event['organizer'])
        
        # Tier 1 & 2: Reference-based
        organizer_id = event.get('organizer_id')
        if not organizer_id:
            # Fallback: If no organizer_id but embedded organizer exists
            if 'organizer' in event:
                return deepcopy(event['organizer'])
            # No organizer
            return None
        
        # Load base organizer
        base_organizer = self.organizers.get(organizer_id)
        if not base_organizer:
            logger.warning(f"Organizer ID not found: {organizer_id}")
            # Fallback to embedded organizer if exists
            if 'organizer' in event:
                return deepcopy(event['organizer'])
            return {'name': f'Unknown Organizer ({organizer_id})'}
        
        # Tier 1: Reference only (no override)
        if 'organizer_override' not in event:
            self.stats['organizer_tier1'] += 1
            return deepcopy(base_organizer)
        
        # Tier 2: Partial override
        self.stats['organizer_tier2'] += 1
        resolved = deepcopy(base_organizer)
        override = event['organizer_override']
        
        # Merge override fields into base
        for key, value in override.items():
            resolved[key] = value
        
        return resolved
    
    def resolve_event(self, event: dict, clean_refs: bool = True) -> dict:
        """
        Resolve all entity references in an event.
        
        Args:
            event: Event dictionary
            clean_refs: If True, remove *_id and *_override fields after resolution
            
        Returns:
            Fully resolved event with embedded entities
        """
        resolved = deepcopy(event)
        
        # Resolve location
        resolved['location'] = self.resolve_event_location(event)
        
        # Resolve organizer (optional)
        organizer = self.resolve_event_organizer(event)
        if organizer:
            resolved['organizer'] = organizer
        
        # Clean up reference fields if requested
        if clean_refs:
            resolved.pop('location_id', None)
            resolved.pop('location_override', None)
            resolved.pop('organizer_id', None)
            resolved.pop('organizer_override', None)
        
        return resolved
    
    def resolve_events(self, events: List[dict]) -> List[dict]:
        """
        Batch resolve multiple events.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            List of resolved events
        """
        return [self.resolve_event(event) for event in events]
    
    def get_location_usage_stats(self, location_id: str, events: List[dict]) -> Dict[str, Any]:
        """
        Get usage statistics for a specific location.
        
        Args:
            location_id: Location ID to check
            events: List of events to analyze
            
        Returns:
            Dict with usage stats (total_uses, override_count, events_list)
        """
        uses = []
        override_count = 0
        
        for event in events:
            if event.get('location_id') == location_id:
                uses.append(event['id'])
                if 'location_override' in event:
                    override_count += 1
        
        return {
            'location_id': location_id,
            'total_uses': len(uses),
            'override_count': override_count,
            'events': uses
        }
    
    def get_organizer_usage_stats(self, organizer_id: str, events: List[dict]) -> Dict[str, Any]:
        """
        Get usage statistics for a specific organizer.
        
        Args:
            organizer_id: Organizer ID to check
            events: List of events to analyze
            
        Returns:
            Dict with usage stats (total_uses, override_count, events_list)
        """
        uses = []
        override_count = 0
        
        for event in events:
            if event.get('organizer_id') == organizer_id:
                uses.append(event['id'])
                if 'organizer_override' in event:
                    override_count += 1
        
        return {
            'organizer_id': organizer_id,
            'total_uses': len(uses),
            'override_count': override_count,
            'events': uses
        }
    
    def get_stats(self) -> Dict[str, int]:
        """Get resolution statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset resolution statistics"""
        self.stats = {
            'location_tier1': 0,
            'location_tier2': 0,
            'location_tier3': 0,
            'organizer_tier1': 0,
            'organizer_tier2': 0,
            'organizer_tier3': 0,
        }
