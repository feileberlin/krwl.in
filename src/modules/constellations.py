"""
Constellation Visualization Module - ASCII Art Night Sky

This module provides ASCII art visualizations of major constellations
visible from a given location, with information about their visibility
and position in the night sky.

Historical Context:
- Medieval bell ringers used star positions to tell time at night
- Orion setting before dawn in winter signaled approaching sunrise
- The position of Polaris (North Star) was used with nocturnal instruments
- Constellations helped navigate the night hours before mechanical clocks

API Usage (wttr.in style):
    curl localhost:8080/orion            # ASCII art of Orion
    curl localhost:8080/ursa-major       # Big Dipper / Great Bear
    curl localhost:8080/:list            # List all constellations
    curl localhost:8080/:help            # Help page

Python Usage:
    from src.modules.constellations import ConstellationViewer
    viewer = ConstellationViewer(lat=50.3167, lon=11.9167)
    print(viewer.get_constellation('orion'))

Start Server:
    python3 src/modules/constellations.py --serve --port 8081

References:
- https://en.wikipedia.org/wiki/Constellation
- https://en.wikipedia.org/wiki/Nocturnal_(instrument)
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import argparse


# Constants
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi


class ConstellationViewer:
    """
    Viewer for constellation ASCII art and visibility information.
    
    Provides information about when and where constellations are visible
    from a given location, with ASCII art representations.
    """
    
    # Major constellations with their data
    CONSTELLATIONS = {
        'orion': {
            'name': 'Orion',
            'name_de': 'Orion (Der Jäger)',
            'latin': 'Orion',
            'ra_hours': 5.5,  # Right Ascension (center)
            'dec_degrees': 0,  # Declination (center, on celestial equator)
            'best_months': [12, 1, 2],  # December, January, February
            'magnitude': 0.5,  # Brightest star (Betelgeuse/Rigel)
            'description': 'The Hunter - One of the most recognizable constellations',
            'description_de': 'Der Jäger - Eine der bekanntesten Sternbilder',
            'medieval_use': 'Orion setting in the west before dawn signaled approaching sunrise in winter',
            'medieval_use_de': 'Orion im Westen untergehend vor der Morgendämmerung zeigte den nahenden Sonnenaufgang im Winter an',
            'ascii_art': r'''
                              .  Betelgeuse
                             /|\    *  (red supergiant)
                            / | \
                           /  |  \
                          /   |   \
                   Bellatrix    |    Meissa
                      *    \   |   /    *
                            \  |  /
                             \ | /
                    .---------***---------.
                   /    Orion's Belt       \
                  /   Alnitak Alnilam Mintaka  \
                 /           |                  \
                /            |                   \
               /             |                    \
              *              |                     *
           Saiph      Orion's Sword             Rigel
                          *  (blue supergiant)
                       M42 Nebula
                          ~~~
'''
        },
        'ursa-major': {
            'name': 'Ursa Major',
            'name_de': 'Großer Bär / Großer Wagen',
            'latin': 'Ursa Major',
            'ra_hours': 11.0,
            'dec_degrees': 55,
            'best_months': [3, 4, 5],  # March, April, May
            'magnitude': 1.8,
            'description': 'The Great Bear - Contains the Big Dipper asterism',
            'description_de': 'Der Große Bär - Enthält den Großen Wagen',
            'medieval_use': 'The two pointer stars show the way to Polaris (North Star)',
            'medieval_use_de': 'Die zwei Zeigersterne weisen den Weg zum Polarstern',
            'ascii_art': r'''
                    THE BIG DIPPER (Part of Ursa Major)
                    
                         *  Dubhe
                        / \
                       /   \  Merak  *
                      /     \       /
                     /       \     /
                    /         \   /
                   *-----------*-*
                 Megrez      Phecda
                   |
                   |
                   *  Alioth
                   |
                   |
                   *  Mizar (+ Alcor)
                    \
                     \
                      *  Alkaid
                      
        "Follow the arc to Arcturus, speed on to Spica"
'''
        },
        'ursa-minor': {
            'name': 'Ursa Minor',
            'name_de': 'Kleiner Bär / Kleiner Wagen',
            'latin': 'Ursa Minor',
            'ra_hours': 15.0,
            'dec_degrees': 75,
            'best_months': [6, 7, 8],  # Circumpolar, but best summer
            'magnitude': 2.0,
            'description': 'The Little Bear - Contains Polaris (North Star)',
            'description_de': 'Der Kleine Bär - Enthält den Polarstern',
            'medieval_use': 'Polaris was used with nocturnal instruments to tell time at night',
            'medieval_use_de': 'Der Polarstern wurde mit Nokturnal-Instrumenten zur Zeitbestimmung in der Nacht verwendet',
            'ascii_art': r'''
                    THE LITTLE DIPPER / URSA MINOR

                              *  POLARIS (North Star)
                             /    ← Always points north!
                            /
                           *  Yildun
                          /
                         /
                        *  Epsilon
                       / \
                      /   \
                     /     \
                    *-------*-------*
                  Zeta    Eta    Pherkad
                             \
                              \
                               *  Kochab
                               
        Medieval bell ringers used Polaris to tell time at night!
'''
        },
        'cassiopeia': {
            'name': 'Cassiopeia',
            'name_de': 'Kassiopeia',
            'latin': 'Cassiopeia',
            'ra_hours': 1.0,
            'dec_degrees': 60,
            'best_months': [10, 11, 12],
            'magnitude': 2.2,
            'description': 'The Queen - W-shaped constellation near Polaris',
            'description_de': 'Die Königin - W-förmiges Sternbild nahe dem Polarstern',
            'medieval_use': 'Opposite the Big Dipper around Polaris, helps find north',
            'medieval_use_de': 'Gegenüber dem Großen Wagen um den Polarstern, hilft bei der Nordfindung',
            'ascii_art': r'''
                    CASSIOPEIA - The Queen's Chair

                          *  Caph
                         / \
                        /   \
                       /     *  Schedar
                      /     /
                     *     /
                 Ruchbah  /
                      \  /
                       \/
                        *  Gamma Cas
                       /
                      /
                     *  Segin
                     
         The distinctive "W" shape rotates around Polaris
'''
        },
        'leo': {
            'name': 'Leo',
            'name_de': 'Löwe',
            'latin': 'Leo',
            'ra_hours': 10.5,
            'dec_degrees': 15,
            'best_months': [3, 4, 5],
            'magnitude': 1.4,
            'description': 'The Lion - Spring constellation with bright Regulus',
            'description_de': 'Der Löwe - Frühlingssternbild mit dem hellen Regulus',
            'medieval_use': 'When Leo rises in the evening, spring is arriving',
            'medieval_use_de': 'Wenn der Löwe abends aufgeht, naht der Frühling',
            'ascii_art': r'''
                    LEO - The Lion

                           * Algieba
                          /|
                         / |
                        /  *  Adhafera
                       /  /
                      /  /
                     *--*  The Sickle (Lion's Head)
                    /  Rasalas
                   /
               Regulus *-----------------------*  Denebola
                  (The King's Star)           (Lion's Tail)
                         \                   /
                          \                 /
                           \               /
                            *-------------*
                          Zosma      Chertan
'''
        },
        'scorpius': {
            'name': 'Scorpius',
            'name_de': 'Skorpion',
            'latin': 'Scorpius',
            'ra_hours': 16.5,
            'dec_degrees': -26,
            'best_months': [6, 7, 8],
            'magnitude': 1.0,
            'description': 'The Scorpion - Summer constellation with red Antares',
            'description_de': 'Der Skorpion - Sommersternbild mit dem roten Antares',
            'medieval_use': 'Low in southern sky during summer nights',
            'medieval_use_de': 'Tief am südlichen Himmel in Sommernächten',
            'ascii_art': r'''
                    SCORPIUS - The Scorpion

                                * Dschubba
                               / \
                              /   \
                             /     \
                    *-------*   ANTARES   *
                   Graffias  (Red Supergiant)  \
                                              \
                                               \
                                                *  Shaula
                                               /|
                                              / |
                                             /  * Lesath
                                            /  (The Stinger)
                                           *
                                        
        "Rival of Mars" - Antares' red color rivals the planet
'''
        },
        'cygnus': {
            'name': 'Cygnus',
            'name_de': 'Schwan',
            'latin': 'Cygnus',
            'ra_hours': 20.5,
            'dec_degrees': 42,
            'best_months': [7, 8, 9],
            'magnitude': 1.25,
            'description': 'The Swan - Northern Cross, flies along the Milky Way',
            'description_de': 'Der Schwan - Das Nördliche Kreuz, fliegt entlang der Milchstraße',
            'medieval_use': 'The Northern Cross was used to orient in summer nights',
            'medieval_use_de': 'Das Nördliche Kreuz wurde zur Orientierung in Sommernächten verwendet',
            'ascii_art': r'''
                    CYGNUS - The Swan / Northern Cross

                              * Deneb (tail)
                              |  (One of the brightest stars)
                              |
                              |
                    *---------*---------*
                 Gienah      |       Rukh
                   (wing)    |      (wing)
                              |
                              |
                              *  Sadr (heart)
                              |
                              |
                              |
                              * Albireo (head/beak)
                               (Beautiful double star!)
                               
        Part of the "Summer Triangle" with Vega and Altair
'''
        },
        'pleiades': {
            'name': 'Pleiades',
            'name_de': 'Plejaden / Siebengestirn',
            'latin': 'Pleiades (M45)',
            'ra_hours': 3.75,
            'dec_degrees': 24,
            'best_months': [11, 12, 1],
            'magnitude': 1.6,
            'description': 'The Seven Sisters - Famous open star cluster',
            'description_de': 'Das Siebengestirn - Berühmter offener Sternhaufen',
            'medieval_use': 'Pleiades rising in evening marked late autumn harvest time',
            'medieval_use_de': 'Das Aufgehen der Plejaden am Abend markierte die späte Herbsternte',
            'ascii_art': r'''
                    PLEIADES - The Seven Sisters (M45)

                                  * Alcyone
                                 /|\
                                / | \
                               /  |  \
                              *   *   *
                           Atlas |  Merope
                                 |
                              Electra
                             /       \
                            *         *
                        Maia       Taygeta
                           \       /
                            \     /
                             \   /
                              \ /
                               * Celaeno
                               |
                               * Sterope (Asterope)

        "Seven Sisters" - Actually 800+ stars, 440 light-years away
        Can you see 6 or 7 with naked eye? (test of eyesight!)
'''
        }
    }
    
    def __init__(self, lat: float, lon: float, tz_offset_hours: float = 1):
        """
        Initialize the constellation viewer.
        
        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            tz_offset_hours: Timezone offset from UTC
        """
        if not -90 <= lat <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
        if not -180 <= lon <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {lon}")
        
        self.lat = lat
        self.lon = lon
        self.tz_offset = tz_offset_hours
    
    def get_constellation(self, name: str, dt: datetime = None) -> Dict[str, Any]:
        """
        Get information about a constellation.
        
        Args:
            name: Constellation name (e.g., 'orion', 'ursa-major')
            dt: Datetime for visibility calculation (defaults to now)
            
        Returns:
            Dict with constellation info, visibility, and ASCII art
        """
        name_lower = name.lower().replace(' ', '-').replace('_', '-')
        
        if name_lower not in self.CONSTELLATIONS:
            return {'error': f"Unknown constellation: {name}. Use :list to see available constellations."}
        
        const = self.CONSTELLATIONS[name_lower]
        
        if dt is None:
            dt = datetime.now()
        
        # Calculate visibility
        visibility = self._calculate_visibility(const, dt)
        
        return {
            'name': const['name'],
            'name_de': const['name_de'],
            'latin': const['latin'],
            'description': const['description'],
            'description_de': const['description_de'],
            'medieval_use': const['medieval_use'],
            'medieval_use_de': const['medieval_use_de'],
            'best_months': const['best_months'],
            'magnitude': const['magnitude'],
            'ascii_art': const['ascii_art'],
            'visibility': visibility,
            'location': {'lat': self.lat, 'lon': self.lon},
            'timestamp': dt.isoformat()
        }
    
    def _calculate_visibility(self, const: dict, dt: datetime) -> Dict[str, Any]:
        """
        Calculate approximate visibility of a constellation.
        
        This is a simplified calculation - real astronomical software
        would use more precise algorithms.
        """
        month = dt.month
        hour = dt.hour
        
        # Check if current month is in best viewing months
        is_best_month = month in const['best_months']
        
        # Simple visibility estimate based on declination and latitude
        dec = const['dec_degrees']
        
        # Circumpolar check (always above horizon)
        is_circumpolar = (self.lat > 0 and dec > (90 - self.lat)) or \
                         (self.lat < 0 and dec < (-90 - self.lat))
        
        # Never visible check
        never_visible = (self.lat > 0 and dec < (self.lat - 90)) or \
                        (self.lat < 0 and dec > (90 + self.lat))
        
        # Estimate current position (very simplified)
        # Local Sidereal Time approximation
        day_of_year = dt.timetuple().tm_yday
        lst_hours = ((day_of_year - 80) * 0.0657 + hour + self.lon / 15) % 24
        
        # Hour angle
        ha = lst_hours - const['ra_hours']
        if ha < -12:
            ha += 24
        if ha > 12:
            ha -= 24
        
        # Estimate altitude (very simplified)
        ha_rad = ha * 15 * DEG_TO_RAD
        dec_rad = dec * DEG_TO_RAD
        lat_rad = self.lat * DEG_TO_RAD
        
        sin_alt = math.sin(lat_rad) * math.sin(dec_rad) + \
                  math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad)
        altitude = math.asin(max(-1, min(1, sin_alt))) * RAD_TO_DEG
        
        # Determine direction
        if ha < -6:
            direction = 'rising in the east'
            direction_de = 'steigt im Osten auf'
        elif ha < -2:
            direction = 'in the eastern sky'
            direction_de = 'im östlichen Himmel'
        elif ha < 2:
            direction = 'near the meridian (highest point)'
            direction_de = 'nahe dem Meridian (höchster Punkt)'
        elif ha < 6:
            direction = 'in the western sky'
            direction_de = 'im westlichen Himmel'
        else:
            direction = 'setting in the west'
            direction_de = 'geht im Westen unter'
        
        # Visibility status
        if never_visible:
            status = 'never visible from this latitude'
            status_de = 'von diesem Breitengrad nie sichtbar'
            visible_now = False
        elif is_circumpolar:
            status = 'circumpolar (always above horizon)'
            status_de = 'zirkumpolar (immer über dem Horizont)'
            visible_now = altitude > 10
        elif altitude > 10:
            status = 'visible' if is_best_month else 'visible (not optimal season)'
            status_de = 'sichtbar' if is_best_month else 'sichtbar (nicht optimale Jahreszeit)'
            visible_now = True
        elif altitude > 0:
            status = 'low on horizon'
            status_de = 'tief am Horizont'
            visible_now = True
        else:
            status = 'below horizon'
            status_de = 'unter dem Horizont'
            visible_now = False
        
        return {
            'visible_now': visible_now,
            'altitude_degrees': round(altitude, 1),
            'direction': direction,
            'direction_de': direction_de,
            'status': status,
            'status_de': status_de,
            'is_circumpolar': is_circumpolar,
            'is_best_season': is_best_month,
            'best_months': [self._month_name(m) for m in const['best_months']]
        }
    
    def _month_name(self, month: int) -> str:
        """Get month name from number."""
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return months[month] if 1 <= month <= 12 else ''
    
    def list_constellations(self) -> List[Dict[str, str]]:
        """List all available constellations."""
        result = []
        for key, const in self.CONSTELLATIONS.items():
            result.append({
                'id': key,
                'name': const['name'],
                'name_de': const['name_de'],
                'description': const['description'][:60] + '...'
            })
        return result


# =============================================================================
# HTTP API Server (wttr.in style)
# =============================================================================

class ConstellationHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for constellation API."""
    
    viewer = None  # Set by server
    
    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path.strip('/')
        query = parse_qs(parsed.query)
        
        # Get format parameter
        fmt = query.get('format', [''])[0].lower()
        
        # Route request
        if path == '' or path == 'orion':
            self._send_constellation('orion', fmt)
        elif path == ':help':
            self._send_help()
        elif path == ':list':
            self._send_list(fmt)
        elif path == ':about':
            self._send_about()
        elif path in ConstellationViewer.CONSTELLATIONS:
            self._send_constellation(path, fmt)
        else:
            # Try to match constellation name
            path_normalized = path.lower().replace(' ', '-').replace('_', '-')
            if path_normalized in ConstellationViewer.CONSTELLATIONS:
                self._send_constellation(path_normalized, fmt)
            else:
                self._send_error(404, f"Unknown constellation: {path}\n\nUse :list to see available constellations.")
    
    def _send_constellation(self, name: str, fmt: str):
        """Send constellation data."""
        result = self.viewer.get_constellation(name)
        
        if 'error' in result:
            self._send_error(404, result['error'])
            return
        
        if fmt in ['j', 'json']:
            self._send_json(result)
        else:
            self._send_plain_text(result)
    
    def _send_plain_text(self, result: dict):
        """Send as plain text ASCII art."""
        vis = result['visibility']
        
        # Visibility icon
        if vis['visible_now']:
            vis_icon = "✅"
            vis_text = f"Visible ({vis['direction']})"
        else:
            vis_icon = "❌"
            vis_text = vis['status']
        
        output = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ⭐ {result['name']:<71} ║
║     {result['name_de']:<71} ║
╠═══════════════════════════════════════════════════════════════════════════════╣
{result['ascii_art']}
╠═══════════════════════════════════════════════════════════════════════════════╣
║  📍 Visibility from {result['location']['lat']:.2f}°N, {result['location']['lon']:.2f}°E                                    ║
║                                                                               ║
║  {vis_icon} {vis_text:<72} ║
║  📐 Altitude: {vis['altitude_degrees']:>5.1f}°   {'(circumpolar)' if vis['is_circumpolar'] else '              ':<30}      ║
║  📅 Best viewing: {', '.join(vis['best_months'][:3]):<54} ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  🏛️ Medieval Use:                                                             ║
║     {result['medieval_use'][:70]:<70} ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  📖 {result['description']:<72} ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        self._send_response(200, output, 'text/plain; charset=utf-8')
    
    def _send_json(self, data: dict):
        """Send JSON response."""
        self._send_response(200, json.dumps(data, indent=2, ensure_ascii=False), 'application/json')
    
    def _send_list(self, fmt: str):
        """Send list of constellations."""
        constellations = self.viewer.list_constellations()
        
        if fmt in ['j', 'json']:
            self._send_json(constellations)
        else:
            output = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ⭐ Available Constellations ⭐                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
"""
            for const in constellations:
                output += f"║  • /{const['id']:<20} {const['name']:<15} {const['name_de']:<30}║\n"
            
            output += """║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Usage:                                                                       ║
║    curl localhost:PORT/orion           # Show Orion                           ║
║    curl localhost:PORT/ursa-major      # Show Ursa Major (Big Dipper)         ║
║    curl localhost:PORT/pleiades        # Show the Pleiades                    ║
║    curl localhost:PORT/:help           # Help page                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
            self._send_response(200, output, 'text/plain; charset=utf-8')
    
    def _send_help(self):
        """Send help page."""
        help_text = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ⭐ Constellation Viewer - Help ⭐                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  USAGE:                                                                       ║
║                                                                               ║
║    curl localhost:PORT/CONSTELLATION   # View constellation ASCII art        ║
║    curl localhost:PORT/:list           # List all constellations              ║
║    curl localhost:PORT/:help           # This help page                       ║
║    curl localhost:PORT/:about          # About this tool                      ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  CONSTELLATIONS:                                                              ║
║                                                                               ║
║    /orion              Orion the Hunter (winter)                              ║
║    /ursa-major         Big Dipper / Great Bear                                ║
║    /ursa-minor         Little Dipper / Polaris                                ║
║    /cassiopeia         The Queen (W-shape)                                    ║
║    /leo                The Lion (spring)                                      ║
║    /scorpius           The Scorpion (summer)                                  ║
║    /cygnus             The Swan / Northern Cross                              ║
║    /pleiades           Seven Sisters star cluster                             ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  OUTPUT FORMATS:                                                              ║
║                                                                               ║
║    ?format=j           JSON output                                            ║
║    (default)           ASCII art with visibility info                         ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  EXAMPLES:                                                                    ║
║                                                                               ║
║    curl localhost:PORT/orion                                                  ║
║    curl localhost:PORT/ursa-major?format=j                                    ║
║    curl localhost:PORT/pleiades                                               ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  🏛️ MEDIEVAL CONTEXT:                                                         ║
║                                                                               ║
║    Before mechanical clocks, people used constellations to tell time:         ║
║    • Orion setting before dawn → approaching sunrise (winter)                 ║
║    • Polaris + Big Dipper → night hour via nocturnal instrument               ║
║    • Pleiades rising → harvest time (autumn)                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        self._send_response(200, help_text, 'text/plain; charset=utf-8')
    
    def _send_about(self):
        """Send about page."""
        about_text = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ⭐ Constellation Viewer - About ⭐                          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  This tool displays ASCII art of major constellations with information        ║
║  about their visibility from your location.                                   ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  🏛️ HISTORICAL CONTEXT:                                                       ║
║                                                                               ║
║  Before mechanical clocks (14th century), people used the stars to tell       ║
║  time at night. Medieval bell ringers and watchmen knew the positions         ║
║  of constellations and used them to mark the night hours:                     ║
║                                                                               ║
║  • ORION: In winter, when Orion set in the west before dawn, it signaled      ║
║    that sunrise was approaching (time for Lauds, the dawn prayer)             ║
║                                                                               ║
║  • POLARIS & URSA MAJOR: The Big Dipper rotates around Polaris like a         ║
║    giant clock hand. Using a "nocturnal" instrument, one could read           ║
║    the night hour by the position of the pointer stars.                       ║
║                                                                               ║
║  • PLEIADES: When the Seven Sisters rose in the evening in late autumn,       ║
║    it marked harvest time and the approaching winter.                         ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Related Tools:                                                               ║
║    • Subjective Day API (Nürnberger Uhr) - Medieval temporal hours            ║
║                                                                               ║
║  References:                                                                  ║
║    • https://en.wikipedia.org/wiki/Nocturnal_(instrument)                     ║
║    • https://en.wikipedia.org/wiki/Canonical_hours                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        self._send_response(200, about_text, 'text/plain; charset=utf-8')
    
    def _send_error(self, code: int, message: str):
        """Send error response."""
        self._send_response(code, f"Error {code}: {message}\n", 'text/plain')
    
    def _send_response(self, code: int, body: str, content_type: str):
        """Send HTTP response with CORS headers."""
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))


def run_server(host: str = '127.0.0.1', port: int = 8081, lat: float = 50.3167, lon: float = 11.9167):
    """Run the HTTP server."""
    ConstellationHTTPHandler.viewer = ConstellationViewer(lat, lon)
    
    server = HTTPServer((host, port), ConstellationHTTPHandler)
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ⭐ Constellation Viewer API ⭐                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Server running at: http://{host}:{port}/                                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Usage (like wttr.in):                                                        ║
║                                                                               ║
║    curl {host}:{port}/orion            # Orion the Hunter                         ║
║    curl {host}:{port}/ursa-major       # Big Dipper                               ║
║    curl {host}:{port}/pleiades         # Seven Sisters                            ║
║    curl {host}:{port}/:list            # List all constellations                  ║
║    curl {host}:{port}/:help            # Help page                                ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Press Ctrl+C to stop                                                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        server.shutdown()


# =============================================================================
# Demo / CLI
# =============================================================================

def demo():
    """Demo output showing constellation ASCII art."""
    viewer = ConstellationViewer(lat=50.3167, lon=11.9167)  # Hof, Germany
    
    print("=" * 60)
    print("Constellation Viewer - Demo")
    print("=" * 60)
    
    # Show Orion
    orion = viewer.get_constellation('orion')
    print(f"\n{orion['name']} ({orion['name_de']})")
    print(orion['ascii_art'])
    print(f"\nVisibility: {orion['visibility']['status']}")
    print(f"Direction: {orion['visibility']['direction']}")
    print(f"Medieval use: {orion['medieval_use']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Constellation Viewer - ASCII Art Night Sky')
    parser.add_argument('--serve', action='store_true', help='Run HTTP server')
    parser.add_argument('--port', type=int, default=8081, help='Server port (default: 8081)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Server host')
    parser.add_argument('--lat', type=float, default=50.3167, help='Latitude (default: Hof, Germany)')
    parser.add_argument('--lon', type=float, default=11.9167, help='Longitude (default: Hof, Germany)')
    
    args = parser.parse_args()
    
    if args.serve:
        run_server(host=args.host, port=args.port, lat=args.lat, lon=args.lon)
    else:
        demo()
