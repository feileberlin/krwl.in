#!/usr/bin/env python3
"""
Migration Script: Unified Entity Management System

Extracts unique locations and organizers from existing events and creates
the locations.json and organizers.json libraries.

This script:
1. Scans events.json and pending_events.json for unique locations/organizers
2. Creates location_id and organizer_id references
3. Maintains backward compatibility by keeping embedded data
4. Supports dry-run mode for previewing changes
"""

import argparse
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.entity_models import Location, Organizer, generate_location_id, generate_organizer_id
from modules.location_manager import LocationManager
from modules.organizer_manager import OrganizerManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class EntityMigration:
    """
    Handles migration from embedded entities to reference-based system.
    """
    
    def __init__(self, base_path: Path, dry_run: bool = False, force: bool = False):
        """
        Initialize migration.
        
        Args:
            base_path: Repository root path
            dry_run: If True, preview changes without modifying files
            force: If True, overwrite existing entity libraries
        """
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        self.force = force
        
        # File paths
        self.events_file = self.base_path / 'assets' / 'json' / 'events.json'
        self.pending_file = self.base_path / 'assets' / 'json' / 'pending_events.json'
        self.locations_file = self.base_path / 'assets' / 'json' / 'locations.json'
        self.organizers_file = self.base_path / 'assets' / 'json' / 'organizers.json'
        
        # Statistics
        self.stats = {
            'events_processed': 0,
            'locations_extracted': 0,
            'organizers_extracted': 0,
            'events_updated': 0,
            'errors': 0
        }
    
    def extract_unique_locations(self, events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Extract unique locations from events.
        
        Groups locations by a unique key (name + coordinates) to avoid duplicates.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dictionary mapping location_id to location data
        """
        unique_locations = {}
        location_map = {}  # Maps (name, lat, lon) to location_id
        
        for event in events:
            location = event.get('location')
            if not location or not isinstance(location, dict):
                continue
            
            name = location.get('name')
            lat = location.get('lat')
            lon = location.get('lon')
            
            if not all([name, lat, lon]):
                logger.warning(f"Event {event.get('id')}: Incomplete location data, skipping")
                continue
            
            # Create key for deduplication
            # Round coordinates to 4 decimals for grouping
            key = (name.strip(), round(float(lat), 4), round(float(lon), 4))
            
            # Skip if we've already seen this location
            if key in location_map:
                continue
            
            # Generate location ID
            location_id = generate_location_id(name, lat, lon)
            
            # Handle ID collision
            if location_id in unique_locations:
                counter = 2
                while f"{location_id}_{counter}" in unique_locations:
                    counter += 1
                location_id = f"{location_id}_{counter}"
            
            # Store location
            now = datetime.now().isoformat()
            location_data = {
                'id': location_id,
                'name': name,
                'lat': round(float(lat), 4),
                'lon': round(float(lon), 4),
                'address': location.get('address'),
                'verified': False,
                'aliases': [],
                'created_at': now,
                'updated_at': now,
                'usage_count': 0
            }
            
            # Add optional fields if present
            if location.get('phone'):
                location_data['phone'] = location['phone']
            if location.get('website'):
                location_data['website'] = location['website']
            
            unique_locations[location_id] = location_data
            location_map[key] = location_id
        
        return unique_locations
    
    def extract_unique_organizers(self, events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Extract unique organizers from events.
        
        Groups organizers by name to avoid duplicates.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dictionary mapping organizer_id to organizer data
        """
        unique_organizers = {}
        organizer_map = {}  # Maps name to organizer_id
        
        for event in events:
            organizer = event.get('organizer')
            if not organizer or not isinstance(organizer, dict):
                continue
            
            name = organizer.get('name')
            if not name:
                continue
            
            # Skip if we've already seen this organizer
            name_key = name.strip().lower()
            if name_key in organizer_map:
                continue
            
            # Generate organizer ID
            organizer_id = generate_organizer_id(name)
            
            # Handle ID collision
            if organizer_id in unique_organizers:
                counter = 2
                while f"{organizer_id}_{counter}" in unique_organizers:
                    counter += 1
                organizer_id = f"{organizer_id}_{counter}"
            
            # Store organizer
            now = datetime.now().isoformat()
            organizer_data = {
                'id': organizer_id,
                'name': name,
                'verified': False,
                'aliases': [],
                'created_at': now,
                'updated_at': now,
                'usage_count': 0
            }
            
            # Add optional fields if present
            if organizer.get('email'):
                organizer_data['email'] = organizer['email']
            if organizer.get('phone'):
                organizer_data['phone'] = organizer['phone']
            if organizer.get('website'):
                organizer_data['website'] = organizer['website']
            
            unique_organizers[organizer_id] = organizer_data
            organizer_map[name_key] = organizer_id
        
        return unique_organizers
    
    def add_entity_references(self, events: List[Dict[str, Any]], 
                            locations: Dict[str, Dict[str, Any]],
                            organizers: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add location_id and organizer_id references to events.
        
        Keeps embedded data for backward compatibility.
        
        Args:
            events: List of event dictionaries
            locations: Dictionary of unique locations
            organizers: Dictionary of unique organizers
            
        Returns:
            List of updated event dictionaries
        """
        updated_events = []
        
        # Create reverse lookup maps
        location_lookup = {}
        for loc_id, loc_data in locations.items():
            key = (loc_data['name'].strip(), loc_data['lat'], loc_data['lon'])
            location_lookup[key] = loc_id
        
        organizer_lookup = {}
        for org_id, org_data in organizers.items():
            organizer_lookup[org_data['name'].strip().lower()] = org_id
        
        for event in events:
            updated_event = event.copy()
            
            # Add location_id if location exists
            location = event.get('location')
            if location and isinstance(location, dict):
                name = location.get('name')
                lat = location.get('lat')
                lon = location.get('lon')
                
                if all([name, lat, lon]):
                    key = (name.strip(), round(float(lat), 4), round(float(lon), 4))
                    if key in location_lookup:
                        updated_event['location_id'] = location_lookup[key]
                        # Keep embedded location for backward compatibility
            
            # Add organizer_id if organizer exists
            organizer = event.get('organizer')
            if organizer and isinstance(organizer, dict):
                name = organizer.get('name')
                if name:
                    name_key = name.strip().lower()
                    if name_key in organizer_lookup:
                        updated_event['organizer_id'] = organizer_lookup[name_key]
                        # Keep embedded organizer for backward compatibility
            
            updated_events.append(updated_event)
        
        return updated_events
    
    def run(self) -> bool:
        """
        Run the migration process.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=" * 70)
        logger.info("🔄 Entity Management System Migration")
        logger.info("=" * 70)
        
        if self.dry_run:
            logger.info("🔍 DRY RUN MODE - No files will be modified")
            logger.info("")
        
        # Check if entity libraries already exist
        if not self.force:
            if self.locations_file.exists() or self.organizers_file.exists():
                logger.error("❌ Entity libraries already exist!")
                logger.error("   Use --force to overwrite existing libraries")
                return False
        
        # Load events
        logger.info("📂 Loading events...")
        all_events = []
        
        if self.events_file.exists():
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                events = data.get('events', [])
                all_events.extend(events)
                logger.info(f"   ✓ Loaded {len(events)} published events")
        
        if self.pending_file.exists():
            with open(self.pending_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                pending = data.get('pending_events', [])
                all_events.extend(pending)
                logger.info(f"   ✓ Loaded {len(pending)} pending events")
        
        self.stats['events_processed'] = len(all_events)
        logger.info(f"   📊 Total events to process: {len(all_events)}")
        logger.info("")
        
        # Extract unique entities
        logger.info("🔍 Extracting unique entities...")
        locations = self.extract_unique_locations(all_events)
        organizers = self.extract_unique_organizers(all_events)
        
        self.stats['locations_extracted'] = len(locations)
        self.stats['organizers_extracted'] = len(organizers)
        
        logger.info(f"   ✓ Found {len(locations)} unique locations")
        logger.info(f"   ✓ Found {len(organizers)} unique organizers")
        logger.info("")
        
        # Show sample locations
        if locations:
            logger.info("📍 Sample locations:")
            for i, (loc_id, loc_data) in enumerate(list(locations.items())[:5], 1):
                logger.info(f"   {i}. {loc_data['name']} (ID: {loc_id})")
                logger.info(f"      Coordinates: ({loc_data['lat']}, {loc_data['lon']})")
            if len(locations) > 5:
                logger.info(f"   ... and {len(locations) - 5} more")
            logger.info("")
        
        # Show sample organizers
        if organizers:
            logger.info("👥 Sample organizers:")
            for i, (org_id, org_data) in enumerate(list(organizers.items())[:5], 1):
                logger.info(f"   {i}. {org_data['name']} (ID: {org_id})")
            if len(organizers) > 5:
                logger.info(f"   ... and {len(organizers) - 5} more")
            logger.info("")
        
        if self.dry_run:
            logger.info("✅ DRY RUN COMPLETE - No changes made")
            logger.info("")
            logger.info("To apply changes, run without --dry-run flag")
            return True
        
        # Save entity libraries
        logger.info("💾 Saving entity libraries...")
        
        # Save locations
        locations_data = {
            'locations': locations,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(locations)
        }
        
        with open(self.locations_file, 'w', encoding='utf-8') as f:
            json.dump(locations_data, f, indent=2, ensure_ascii=False)
        logger.info(f"   ✓ Saved {len(locations)} locations to {self.locations_file.name}")
        
        # Save organizers
        organizers_data = {
            'organizers': organizers,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(organizers)
        }
        
        with open(self.organizers_file, 'w', encoding='utf-8') as f:
            json.dump(organizers_data, f, indent=2, ensure_ascii=False)
        logger.info(f"   ✓ Saved {len(organizers)} organizers to {self.organizers_file.name}")
        logger.info("")
        
        # Update events with references
        logger.info("🔗 Adding entity references to events...")
        
        # Update published events
        if self.events_file.exists():
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated_events = self.add_entity_references(
                data.get('events', []), locations, organizers
            )
            
            data['events'] = updated_events
            data['last_updated'] = datetime.now().isoformat()
            
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"   ✓ Updated {len(updated_events)} published events")
        
        # Update pending events
        if self.pending_file.exists():
            with open(self.pending_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated_pending = self.add_entity_references(
                data.get('pending_events', []), locations, organizers
            )
            
            data['pending_events'] = updated_pending
            
            with open(self.pending_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"   ✓ Updated {len(updated_pending)} pending events")
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ MIGRATION COMPLETE!")
        logger.info("=" * 70)
        logger.info("")
        logger.info("📊 Summary:")
        logger.info(f"   • Events processed: {self.stats['events_processed']}")
        logger.info(f"   • Locations extracted: {self.stats['locations_extracted']}")
        logger.info(f"   • Organizers extracted: {self.stats['organizers_extracted']}")
        logger.info("")
        logger.info("📝 Next steps:")
        logger.info("   1. Review locations.json and verify location data")
        logger.info("   2. Review organizers.json and verify organizer data")
        logger.info("   3. Use CLI commands to manage entities:")
        logger.info("      python3 src/event_manager.py locations list")
        logger.info("      python3 src/event_manager.py organizers list")
        logger.info("")
        
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Migrate events to unified entity management system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview migration without making changes
  python3 scripts/migrate_to_entity_system.py --dry-run
  
  # Run migration
  python3 scripts/migrate_to_entity_system.py
  
  # Force overwrite existing libraries
  python3 scripts/migrate_to_entity_system.py --force
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing entity libraries'
    )
    
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Repository root directory'
    )
    
    args = parser.parse_args()
    
    # Run migration
    migration = EntityMigration(
        base_path=args.repo_root,
        dry_run=args.dry_run,
        force=args.force
    )
    
    success = migration.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
