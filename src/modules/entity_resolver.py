"""
Entity Resolver

Implements three-tier override system for resolving event locations and organizers:
- Tier 1: Reference only (location_id → loads from locations.json)
- Tier 2: Partial override (location_id + location_override → merges fields)
- Tier 3: Full override (location dict → uses embedded data as-is)

This enables flexible event configuration while maintaining a single source of truth.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict

from .entity_models import Location, Organizer

# Configure module logger
logger = logging.getLogger(__name__)


class EntityResolver:
    """
    Resolves entity references in events using a three-tier override system.
    
    The three-tier system allows events to:
    1. Reference entities from the library (DRY principle)
    2. Override specific fields for special cases (flexibility)
    3. Use fully embedded data for one-off events (backward compatibility)
    
    Examples:
        # Tier 1: Reference only
        event = {"location_id": "loc_theater_hof"}
        # → Loads complete location from locations.json
        
        # Tier 2: Partial override
        event = {
            "location_id": "loc_theater_hof",
            "location_override": {
                "name": "Theater Hof - VIP Lounge",
                "address": "Side entrance"
            }
        }
        # → Merges override into base location (lat/lon from base, name/address overridden)
        
        # Tier 3: Full override
        event = {
            "location": {
                "name": "Pop-Up Stage",
                "lat": 50.3250,
                "lon": 11.9200
            }
        }
        # → Uses embedded location as-is (no reference needed)
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
        
        self.locations: Dict[str, Location] = {}
        self.organizers: Dict[str, Organizer] = {}
        
        self._load_entities()
    
    def _load_entities(self):
        """Load locations and organizers from JSON files."""
        # Load locations
        if self.locations_file.exists():
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
                logger.warning(f"Could not load locations.json: {e}")
        
        # Load organizers
        if self.organizers_file.exists():
            try:
                with open(self.organizers_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    organizers_dict = data.get('organizers', {})
                    
                    for org_id, org_data in organizers_dict.items():
                        try:
                            self.organizers[org_id] = Organizer.from_dict(org_data)
                        except Exception as e:
                            logger.warning(f"Failed to load organizer {org_id}: {e}")
                
                logger.info(f"Loaded {len(self.organizers)} organizers from library")
            except Exception as e:
                logger.warning(f"Could not load organizers.json: {e}")
    
    def resolve_event_location(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Resolve event location using three-tier override system.
        
        Resolution priority:
        1. If 'location' dict exists → Tier 3: Use embedded location
        2. If 'location_id' + 'location_override' → Tier 2: Merge override into base
        3. If 'location_id' only → Tier 1: Load from library
        4. Otherwise → None
        
        Args:
            event: Event dictionary
            
        Returns:
            Resolved location dictionary or None if not resolvable
        """
        # Tier 3: Full override (embedded location)
        if 'location' in event and event['location']:
            logger.debug(f"Event {event.get('id')}: Using embedded location (Tier 3)")
            return event['location']
        
        # Check for location_id reference
        location_id = event.get('location_id')
        if not location_id:
            logger.debug(f"Event {event.get('id')}: No location reference found")
            return None
        
        # Get base location from library
        if location_id not in self.locations:
            logger.warning(f"Event {event.get('id')}: Location {location_id} not found in library")
            return None
        
        base_location = self.locations[location_id].to_dict()
        
        # Tier 2: Partial override
        if 'location_override' in event and event['location_override']:
            logger.debug(f"Event {event.get('id')}: Merging location override (Tier 2)")
            resolved_location = base_location.copy()
            resolved_location.update(event['location_override'])
            return resolved_location
        
        # Tier 1: Reference only
        logger.debug(f"Event {event.get('id')}: Using library location (Tier 1)")
        return base_location
    
    def resolve_event_organizer(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Resolve event organizer using three-tier override system.
        
        Resolution priority:
        1. If 'organizer' dict exists → Tier 3: Use embedded organizer
        2. If 'organizer_id' + 'organizer_override' → Tier 2: Merge override into base
        3. If 'organizer_id' only → Tier 1: Load from library
        4. Otherwise → None
        
        Args:
            event: Event dictionary
            
        Returns:
            Resolved organizer dictionary or None if not resolvable
        """
        # Tier 3: Full override (embedded organizer)
        if 'organizer' in event and event['organizer']:
            logger.debug(f"Event {event.get('id')}: Using embedded organizer (Tier 3)")
            return event['organizer']
        
        # Check for organizer_id reference
        organizer_id = event.get('organizer_id')
        if not organizer_id:
            logger.debug(f"Event {event.get('id')}: No organizer reference found")
            return None
        
        # Get base organizer from library
        if organizer_id not in self.organizers:
            logger.warning(f"Event {event.get('id')}: Organizer {organizer_id} not found in library")
            return None
        
        base_organizer = self.organizers[organizer_id].to_dict()
        
        # Tier 2: Partial override
        if 'organizer_override' in event and event['organizer_override']:
            logger.debug(f"Event {event.get('id')}: Merging organizer override (Tier 2)")
            resolved_organizer = base_organizer.copy()
            resolved_organizer.update(event['organizer_override'])
            return resolved_organizer
        
        # Tier 1: Reference only
        logger.debug(f"Event {event.get('id')}: Using library organizer (Tier 1)")
        return base_organizer
    
    def resolve_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve all entity references in an event.
        
        Creates a new event dict with resolved location and organizer.
        Original event is not modified.
        
        Args:
            event: Event dictionary
            
        Returns:
            Event dictionary with resolved entities
        """
        resolved_event = event.copy()
        
        # Resolve location
        resolved_location = self.resolve_event_location(event)
        if resolved_location:
            resolved_event['location'] = resolved_location
        
        # Resolve organizer
        resolved_organizer = self.resolve_event_organizer(event)
        if resolved_organizer:
            resolved_event['organizer'] = resolved_organizer
        
        return resolved_event
    
    def resolve_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Resolve entity references for a list of events.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            List of events with resolved entities
        """
        return [self.resolve_event(event) for event in events]
    
    def get_location_usage_stats(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get usage statistics for locations.
        
        Counts how many events reference each location_id.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dictionary mapping location_id to usage count
        """
        usage_counts = defaultdict(int)
        
        for event in events:
            location_id = event.get('location_id')
            if location_id:
                usage_counts[location_id] += 1
        
        return dict(usage_counts)
    
    def get_organizer_usage_stats(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get usage statistics for organizers.
        
        Counts how many events reference each organizer_id.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dictionary mapping organizer_id to usage count
        """
        usage_counts = defaultdict(int)
        
        for event in events:
            organizer_id = event.get('organizer_id')
            if organizer_id:
                usage_counts[organizer_id] += 1
        
        return dict(usage_counts)
    
    def analyze_entity_coverage(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze entity reference coverage in events.
        
        Provides statistics on how events use the entity system:
        - How many use references vs embedded data
        - How many use overrides
        - Which entities are most/least used
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dictionary with coverage statistics
        """
        stats = {
            'total_events': len(events),
            'locations': {
                'tier_1_reference': 0,  # location_id only
                'tier_2_override': 0,   # location_id + location_override
                'tier_3_embedded': 0,   # location dict
                'no_location': 0
            },
            'organizers': {
                'tier_1_reference': 0,  # organizer_id only
                'tier_2_override': 0,   # organizer_id + organizer_override
                'tier_3_embedded': 0,   # organizer dict
                'no_organizer': 0
            }
        }
        
        for event in events:
            # Analyze location usage
            if 'location' in event and event['location']:
                stats['locations']['tier_3_embedded'] += 1
            elif 'location_id' in event:
                if 'location_override' in event and event['location_override']:
                    stats['locations']['tier_2_override'] += 1
                else:
                    stats['locations']['tier_1_reference'] += 1
            else:
                stats['locations']['no_location'] += 1
            
            # Analyze organizer usage
            if 'organizer' in event and event['organizer']:
                stats['organizers']['tier_3_embedded'] += 1
            elif 'organizer_id' in event:
                if 'organizer_override' in event and event['organizer_override']:
                    stats['organizers']['tier_2_override'] += 1
                else:
                    stats['organizers']['tier_1_reference'] += 1
            else:
                stats['organizers']['no_organizer'] += 1
        
        # Add most/least used entities
        location_usage = self.get_location_usage_stats(events)
        organizer_usage = self.get_organizer_usage_stats(events)
        
        if location_usage:
            stats['locations']['most_used'] = sorted(
                location_usage.items(), key=lambda x: x[1], reverse=True
            )[:5]
            stats['locations']['least_used'] = sorted(
                location_usage.items(), key=lambda x: x[1]
            )[:5]
        
        if organizer_usage:
            stats['organizers']['most_used'] = sorted(
                organizer_usage.items(), key=lambda x: x[1], reverse=True
            )[:5]
            stats['organizers']['least_used'] = sorted(
                organizer_usage.items(), key=lambda x: x[1]
            )[:5]
        
        return stats
