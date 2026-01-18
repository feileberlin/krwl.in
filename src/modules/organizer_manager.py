"""
Organizer Manager

Provides CRUD operations for managing the organizers library.
Supports search, verification, and statistics.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from .entity_models import Organizer, generate_organizer_id

# Configure module logger
logger = logging.getLogger(__name__)


class OrganizerManager:
    """
    Manages the organizers library (organizers.json).
    
    Provides CRUD operations, search, verification features.
    Automatically backs up the organizers file on save operations.
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize organizer manager.
        
        Args:
            base_path: Repository root path
        """
        self.base_path = Path(base_path)
        self.organizers_file = self.base_path / 'assets' / 'json' / 'organizers.json'
        self.backup_dir = self.base_path / 'assets' / 'json' / 'backups' / 'organizers'
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.organizers: Dict[str, Organizer] = {}
        self._load_organizers()
    
    def _load_organizers(self):
        """Load organizers from JSON file."""
        if not self.organizers_file.exists():
            logger.info("No organizers.json found, starting with empty library")
            return
        
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
            logger.error(f"Could not load organizers.json: {e}")
            raise
    
    def _save_organizers(self):
        """Save organizers to JSON file with automatic backup."""
        # Create backup
        if self.organizers_file.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f"organizers_{timestamp}.json"
            shutil.copy2(self.organizers_file, backup_file)
            logger.info(f"Created backup: {backup_file.name}")
        
        # Save organizers
        data = {
            'organizers': {
                org_id: organizer.to_dict()
                for org_id, organizer in self.organizers.items()
            },
            'last_updated': datetime.now().isoformat(),
            'total_count': len(self.organizers)
        }
        
        try:
            with open(self.organizers_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.organizers)} organizers to library")
        except Exception as e:
            logger.error(f"Failed to save organizers.json: {e}")
            raise
    
    def add(self, name: str, verified: bool = False, **kwargs) -> Organizer:
        """
        Add a new organizer to the library.
        
        Args:
            name: Organizer name
            verified: Verification status (default: False)
            **kwargs: Additional optional fields (email, phone, website, description, aliases)
            
        Returns:
            Created Organizer instance
            
        Raises:
            ValueError: If organizer with same name already exists
        """
        # Check for duplicates
        for organizer in self.organizers.values():
            if organizer.name.lower() == name.lower():
                raise ValueError(f"Organizer with name '{name}' already exists (ID: {organizer.id})")
        
        # Generate ID
        organizer_id = generate_organizer_id(name)
        
        # Handle ID collision
        if organizer_id in self.organizers:
            # Add counter to make it unique
            counter = 2
            while f"{organizer_id}_{counter}" in self.organizers:
                counter += 1
            organizer_id = f"{organizer_id}_{counter}"
        
        # Create organizer
        organizer = Organizer(
            id=organizer_id,
            name=name,
            verified=verified,
            email=kwargs.get('email'),
            phone=kwargs.get('phone'),
            website=kwargs.get('website'),
            description=kwargs.get('description'),
            aliases=kwargs.get('aliases', [])
        )
        
        self.organizers[organizer_id] = organizer
        self._save_organizers()
        
        logger.info(f"Added organizer: {name} (ID: {organizer_id})")
        return organizer
    
    def update(self, organizer_id: str, **kwargs) -> Organizer:
        """
        Update an existing organizer.
        
        Args:
            organizer_id: ID of organizer to update
            **kwargs: Fields to update (name, email, phone, website, etc.)
            
        Returns:
            Updated Organizer instance
            
        Raises:
            KeyError: If organizer_id not found
        """
        if organizer_id not in self.organizers:
            raise KeyError(f"Organizer {organizer_id} not found")
        
        organizer = self.organizers[organizer_id]
        
        # Update fields
        for field, value in kwargs.items():
            if hasattr(organizer, field):
                setattr(organizer, field, value)
        
        organizer.update_timestamp()
        self._save_organizers()
        
        logger.info(f"Updated organizer: {organizer.name} (ID: {organizer_id})")
        return organizer
    
    def delete(self, organizer_id: str) -> bool:
        """
        Delete an organizer from the library.
        
        Args:
            organizer_id: ID of organizer to delete
            
        Returns:
            True if deleted, False if not found
        """
        if organizer_id not in self.organizers:
            logger.warning(f"Organizer {organizer_id} not found for deletion")
            return False
        
        organizer_name = self.organizers[organizer_id].name
        del self.organizers[organizer_id]
        self._save_organizers()
        
        logger.info(f"Deleted organizer: {organizer_name} (ID: {organizer_id})")
        return True
    
    def get(self, organizer_id: str) -> Optional[Organizer]:
        """
        Get an organizer by ID.
        
        Args:
            organizer_id: ID of organizer to retrieve
            
        Returns:
            Organizer instance or None if not found
        """
        return self.organizers.get(organizer_id)
    
    def list(self, verified_only: bool = False) -> List[Organizer]:
        """
        List all organizers.
        
        Args:
            verified_only: If True, only return verified organizers
            
        Returns:
            List of Organizer instances
        """
        organizers = list(self.organizers.values())
        
        if verified_only:
            organizers = [org for org in organizers if org.verified]
        
        # Sort by name
        organizers.sort(key=lambda x: x.name.lower())
        return organizers
    
    def search(self, query: str) -> List[Organizer]:
        """
        Search organizers by name or alias.
        
        Case-insensitive substring matching.
        
        Args:
            query: Search query
            
        Returns:
            List of matching Organizer instances
        """
        results = []
        
        for organizer in self.organizers.values():
            if organizer.matches_name(query):
                results.append(organizer)
        
        # Sort by relevance (exact match first, then alphabetically)
        query_lower = query.lower()
        results.sort(key=lambda x: (
            x.name.lower() != query_lower,  # Exact matches first
            x.name.lower()
        ))
        
        return results
    
    def verify(self, organizer_id: str) -> bool:
        """
        Mark an organizer as verified.
        
        Args:
            organizer_id: ID of organizer to verify
            
        Returns:
            True if verified, False if not found
        """
        if organizer_id not in self.organizers:
            logger.warning(f"Organizer {organizer_id} not found for verification")
            return False
        
        organizer = self.organizers[organizer_id]
        organizer.verified = True
        organizer.update_timestamp()
        self._save_organizers()
        
        logger.info(f"Verified organizer: {organizer.name} (ID: {organizer_id})")
        return True
    
    def merge_organizers(self, source_id: str, target_id: str) -> bool:
        """
        Merge source organizer into target organizer.
        
        Combines data from source into target and deletes source.
        Useful for deduplication.
        
        Args:
            source_id: ID of organizer to merge (will be deleted)
            target_id: ID of organizer to merge into (will be kept)
            
        Returns:
            True if merged successfully, False otherwise
        """
        if source_id not in self.organizers or target_id not in self.organizers:
            logger.error(f"Cannot merge: one or both organizers not found")
            return False
        
        source = self.organizers[source_id]
        target = self.organizers[target_id]
        
        # Merge aliases
        target.aliases = list(set(target.aliases + source.aliases + [source.name]))
        
        # Merge optional fields (keep target if exists, otherwise use source)
        if not target.email and source.email:
            target.email = source.email
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
        del self.organizers[source_id]
        
        self._save_organizers()
        
        logger.info(f"Merged organizer {source.name} (ID: {source_id}) into {target.name} (ID: {target_id})")
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the organizers library.
        
        Returns:
            Dictionary with statistics
        """
        organizers = list(self.organizers.values())
        
        verified_count = sum(1 for org in organizers if org.verified)
        
        # Find most used organizers
        most_used = sorted(organizers, key=lambda x: x.usage_count, reverse=True)[:10]
        
        return {
            'total_organizers': len(organizers),
            'verified_organizers': verified_count,
            'unverified_organizers': len(organizers) - verified_count,
            'organizers_with_email': sum(1 for org in organizers if org.email),
            'organizers_with_phone': sum(1 for org in organizers if org.phone),
            'organizers_with_website': sum(1 for org in organizers if org.website),
            'most_used_organizers': [
                {'id': org.id, 'name': org.name, 'usage_count': org.usage_count}
                for org in most_used
            ]
        }
