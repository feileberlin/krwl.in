# PR #2: Data Structure Refactor - Implementation Plan

## Overview
Consolidate multiple pending files into unified structure with separate verified data stores.

## New File Structure

### Unified Pending Queue: `assets/json/pending.json`
```json
{
  "_schema_version": "2.0",
  "_description": "Unified pending queue for events, locations, and organizers",
  "items": [
    {
      "id": "loc_abc123",
      "type": "location",
      "name": "Freiheitshalle Hof",
      "category": "theater",
      "lat": 50.3167,
      "lon": 11.9167,
      "address": null,
      "url": null,
      "phone": null,
      "source": "osm",
      "occurrence_count": 1,
      "sources": ["osm"],
      "verified": false,
      "scraping_enabled": false,
      "notes": "",
      "created_at": "2026-01-18T13:00:00",
      "updated_at": "2026-01-18T13:00:00"
    },
    {
      "id": "org_xyz789",
      "type": "organizer",
      "name": "Stadttheater Hof",
      "url": "https://theater-hof.de",
      "phone": "+49 9281 7070",
      "email": "info@theater-hof.de",
      "category": "cultural_institution",
      "verified": false,
      "scraping_enabled": false,
      "notes": "",
      "created_at": "2026-01-18T13:00:00"
    },
    {
      "id": "evt_def456",
      "type": "event",
      "title": "Concert at Freiheitshalle",
      "description": "Classical music concert",
      "location_id": "loc_abc123",
      "organizer_id": "org_xyz789",
      "start_time": "2026-02-15T19:00:00",
      "end_time": "2026-02-15T22:00:00",
      "url": "https://example.com/event/123",
      "source": "https://example.com/event/123",
      "category": "culture",
      "status": "pending",
      "scraped_at": "2026-01-18T13:00:00"
    }
  ],
  "last_updated": "2026-01-18T13:00:00"
}
```

### Verified Locations: `assets/json/locations.json`
```json
{
  "_schema_version": "2.0",
  "_description": "Verified locations database",
  "_coordinate_precision": "4 decimal places (≈10m accuracy)",
  "locations": {
    "loc_abc123": {
      "id": "loc_abc123",
      "name": "Freiheitshalle Hof",
      "lat": 50.3167,
      "lon": 11.9167,
      "address": "Freiheitshalle, Hof",
      "url": "https://freiheitshalle-hof.de",
      "phone": "+49 9281 ...",
      "category": "venue",
      "scraping_enabled": true,
      "scraping_urls": ["https://freiheitshalle-hof.de/events"],
      "verified_at": "2026-01-18T13:00:00",
      "verified_by": "manual_review"
    }
  }
}
```

### Verified Organizers: `assets/json/organizers.json`
```json
{
  "_schema_version": "2.0",
  "_description": "Verified organizers database",
  "organizers": {
    "org_xyz789": {
      "id": "org_xyz789",
      "name": "Stadttheater Hof",
      "url": "https://theater-hof.de",
      "phone": "+49 9281 7070",
      "email": "info@theater-hof.de",
      "category": "cultural_institution",
      "scraping_enabled": true,
      "scraping_urls": ["https://theater-hof.de/programm"],
      "verified_at": "2026-01-18T13:00:00",
      "verified_by": "manual_review"
    }
  }
}
```

### Trash: `assets/json/trash.json`
```json
{
  "_schema_version": "2.0",
  "_description": "Rejected items archive",
  "items": [
    {
      "id": "loc_rejected_001",
      "type": "location",
      "name": "Invalid Location",
      "reason": "Duplicate of loc_abc123",
      "rejected_at": "2026-01-18T13:00:00",
      "rejected_by": "manual_review",
      "original_data": { }
    }
  ]
}
```

### Events (unchanged): `assets/json/events.json`
Events keep referencing locations and organizers by ID.

## Migration Steps

### Phase 1: Create Migration Script
- `scripts/migrate_to_unified_pending.py`
- Converts old structure → new structure
- Generates IDs for locations/organizers
- Preserves all data

### Phase 2: Update Core Utilities
- `src/modules/utils.py`: Add new load/save functions
- `load_pending()`, `save_pending()`
- `load_locations()`, `save_locations()`
- `load_organizers()`, `save_organizers()`
- `load_trash()`, `save_trash()`

### Phase 3: Update Scrapers
- `src/modules/scraper.py`: Save to pending.json
- `src/modules/location_tracker.py`: Use new structure

### Phase 4: Update Editor
- `src/modules/editor.py`: Review pending items by type
- Support approve/reject/trash workflow

### Phase 5: Update Event Manager
- `src/event_manager.py`: Update CLI commands
- `list-pending`, `publish`, `reject` work with types

### Phase 6: Update Location Resolver
- `src/modules/location_resolver.py`: Use locations.json
- `src/modules/event_context_aggregator.py`: Use new structure

### Phase 7: Update VGN Module
- `src/modules/vgn_transit.py`: Save discoveries to pending.json

### Phase 8: Update Tests
- All test files using old structure
- Add tests for migration script

### Phase 9: Documentation
- Update README
- Update copilot instructions
- Add migration guide

## Backward Compatibility
- Keep old files temporarily with deprecation warnings
- Migration script creates backups
- Rollback capability

## KISS Compliance
- Single pending queue (not separate files per type)
- Simple type field discrimination
- Minimal code changes
- Clear migration path
