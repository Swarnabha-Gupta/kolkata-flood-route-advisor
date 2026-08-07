# 🌊 DELUGE - Waterlogging & Flood-Prone Route Advisor (Kolkata Commuters)

DELUGE is a full-stack, responsive, mobile-first web application designed specifically for commuters navigating Kolkata during the monsoon season.

## 🚀 Key Features

1. **Dynamic Header with Continuous Scrolling Advisory Ticker & Theme Switcher**:
   - Header Title: "DELUGE" with subtitle "FLOOD-ROUTE ADVISORY • KOLKATA METRO & KMC AREA".
   - Status Badge: Pulsing dot indicator displaying "MONSOON WATCH ACTIVE".
   - 3-Way Theme Switcher: Toggle between Light, Dark, and System modes with Tailwind CSS `dark:` class support and `localStorage` persistence.
   - Continuous Marquee Ticker: Full-width live advisory banner powered by CSS keyframes (`@keyframes marquee`) initialized with real-time KMC pumping station & Kolkata Metro updates.

2. **Single Natural Language AI Search Bar**:
   - Single primary input bar labeled *"Ask in natural language or search any Kolkata street, station, or landmark"*.
   - Accepts any Kolkata query: route requests (*"Safe route from Sector 5 to Howrah Station in heavy rain"*), specific area inquiries (*"Is Park Street waterlogged near Camac Street?"*), or metro status questions.

3. **Gemini AI Engine (`gemini-2.5-flash`) & OpenStreetMap Geocoding**:
   - Parses natural language input using Gemini AI with Structured JSON outputs.
   - Geocodes location names bounded to Kolkata Metropolitan Coordinates (22.30 N to 22.80 N, 88.20 E to 88.50 E).
   - Generates risk level, water depth estimates, vehicle passability indicators, direct risky route waypoints, safe bypass waypoints, and hazard hotspots.
   - Built-in local fallback intelligence engine ensures instant dynamic responses without requiring an API key.

4. **Mobile-First Layout & Leaflet Map Panel**:
   - Interactive map centered on Kolkata with custom theme matching (CartoDB Dark Matter / Positron).
   - Red dashed polyline for direct risky route vs solid green line for recommended safe bypass route.
   - Pulsing circular markers with popups at waterlogged hazard hotspots.

## 🛠️ How to Run

Run this link in you browser:

https://kolkata-flood-route-advisor.vercel.app/
