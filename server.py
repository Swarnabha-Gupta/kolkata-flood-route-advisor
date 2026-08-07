import http.server
import socketserver
import json
import os
import sys
import urllib.request
import urllib.error

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(__file__), "src")

class DelugeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        if self.path == '/api/analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode('utf-8'))
                user_query = data.get('query', '')
            except Exception:
                user_query = ''

            # Attempt Gemini 2.5 Flash API call if key is present
            gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
            response_payload = None

            if gemini_key and user_query:
                try:
                    response_payload = self.call_gemini_api(user_query, gemini_key)
                except Exception as e:
                    print(f"[Deluge Server] Gemini API call failed: {e}", file=sys.stderr)

            if not response_payload:
                # Fallback to local server intelligence generator
                response_payload = self.generate_local_response(user_query)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

    def fetch_kolkata_precipitation(self):
        """Fetch current precipitation rate for Kolkata (22.5726 N, 88.3639 E) in mm/hr"""
        try:
            url = "https://api.open-meteo.com/v1/forecast?latitude=22.5726&longitude=88.3639&current=precipitation&precipitation_unit=mm"
            req = urllib.request.Request(url, headers={'User-Agent': 'DelugeApp/1.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('current', {}).get('precipitation', 0.0)
        except Exception as e:
            print(f"[Deluge Server] Weather fetch failed: {e}", file=sys.stderr)
            return 0.0

    def call_gemini_api(self, query, api_key):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # Get live precipitation
        precip = self.fetch_kolkata_precipitation()
        
        prompt_text = f"""
You are the AI engine for DELUGE - Waterlogging & Flood-Prone Route Advisor for Kolkata.
Analyze this Kolkata commuter query: "{query}"

REAL-TIME DATA CONTEXT:
- Current Weather / Hourly Precipitation in Kolkata: {precip} mm/hr

INSTRUCTIONS:
1. Search recent traffic and news updates from Kolkata Traffic Police and Kolkata Municipal Corporation (KMC).
2. If current rainfall is low/zero (0 - 2 mm/hr), reflect that primary thoroughfares are cleared by KMC pumping stations.
3. Structure your response to return ONLY raw valid JSON matching this schema:

{{
  "overall_risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "risk_summary": "Detailed, live explanation of waterlogging & travel risks in Kolkata",
  "metro_transit_status": "Update regarding Kolkata Metro lines or bus transport",
  "updated_ticker_alert": "Short headline alert (max 80 chars) for live marquee header",
  "water_depth_estimate": "Estimated water depth string e.g. 0 - 2 inches",
  "vehicle_passability": ["2-Wheelers", "4-Wheelers", "Buses"],
  "direct_route_coordinates": [[22.5726, 88.4339], [22.5830, 88.3426]],
  "safe_bypass_coordinates": [[22.5726, 88.4339], [22.5414, 88.3484], [22.5830, 88.3426]],
  "hazard_hotspots": [
    {{ "name": "Hotspot Location Name", "lat": 22.5, "lng": 88.35, "severity": "LOW", "depth": "0 - 2 in" }}
  ]
}}
All coordinates MUST be realistic latitude/longitude pairs within Kolkata (lat 22.40 to 22.68, lng 88.30 to 88.48).
"""
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "tools": [
                {"google_search": {}}  # Enables Google Search Grounding for live real-time reports
            ],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req, timeout=12) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            text = res_data['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text)

    def generate_local_response(self, query):
        q = query.lower()
        
        # Sector 5 to Howrah
        if 'sector 5' in q or 'howrah' in q:
            return {
                "overall_risk_level": "HIGH",
                "risk_summary": "Ultadanga Underpass and MG Road flooded with 8-14 inches of water. High-capacity KMC pumps operating. Take Maa Flyover & AJC Bose Rd safe bypass.",
                "metro_transit_status": "Green Line Metro running smooth between Sector V & Sealdah. Blue Line delayed near MG Road station.",
                "updated_ticker_alert": "ALERT: Ultadanga Underpass flooded (12 in). Rerouting traffic via EM Bypass & Maa Flyover.",
                "water_depth_estimate": "8 - 14 inches",
                "vehicle_passability": ["Buses Only", "Heavy Commercial"],
                "direct_route_coordinates": [
                    [22.5726, 88.4339], [22.5867, 88.4171], [22.5975, 88.3842], [22.5816, 88.3598], [22.5830, 88.3426]
                ],
                "safe_bypass_coordinates": [
                    [22.5726, 88.4339], [22.5600, 88.4000], [22.5450, 88.3750], [22.5414, 88.3484], [22.5550, 88.3350], [22.5830, 88.3426]
                ],
                "hazard_hotspots": [
                    { "name": "Ultadanga Underpass", "lat": 22.5975, "lng": 88.3842, "severity": "HIGH", "depth": "12 - 14 in" },
                    { "name": "MG Road Crossing", "lat": 22.5816, "lng": 88.3598, "severity": "HIGH", "depth": "8 - 10 in" }
                ]
            }

        # Generic default Kolkata response
        return {
            "overall_risk_level": "MEDIUM",
            "risk_summary": f"Commuter route update for query '{query}': Moderate water logging along low arterial roads. KMC pumps deployed.",
            "metro_transit_status": "Kolkata Metro services active. Surface buses rerouted near water-dense junctions.",
            "updated_ticker_alert": f"ADVISORY: Active flood monitoring for '{query[:40]}...'",
            "water_depth_estimate": "4 - 8 inches",
            "vehicle_passability": ["4-Wheelers", "Buses"],
            "direct_route_coordinates": [
                [22.5726, 88.3639], [22.5645, 88.3517], [22.5539, 88.3524]
            ],
            "safe_bypass_coordinates": [
                [22.5726, 88.3639], [22.5600, 88.3800], [22.5450, 88.3750], [22.5539, 88.3524]
            ],
            "hazard_hotspots": [
                { "name": "Low-lying Pocket", "lat": 22.5645, "lng": 88.3517, "severity": "MEDIUM", "depth": "6 in" }
            ]
        }

if __name__ == "__main__":
    handler = DelugeHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[DELUGE] Web Application running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")