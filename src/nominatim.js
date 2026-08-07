/**
 * OpenStreetMap Nominatim Geocoding API helper
 * Bounded strictly to the Kolkata Metropolitan Region:
 * Latitude: 22.30 N to 22.80 N
 * Longitude: 88.20 E to 88.50 E
 */

// Comprehensive fallback coordinates dictionary for major Kolkata landmarks
export const KOLKATA_LANDMARKS = {
  "sector 5": [22.5726, 88.4339],
  "sector v": [22.5726, 88.4339],
  "salt lake sector 5": [22.5726, 88.4339],
  "salt lake": [22.5867, 88.4171],
  "howrah": [22.5830, 88.3426],
  "howrah station": [22.5830, 88.3426],
  "howrah bridge": [22.5851, 88.3468],
  "park street": [22.5539, 88.3524],
  "camac street": [22.5489, 88.3541],
  "esplanade": [22.5645, 88.3517],
  "dharmatala": [22.5645, 88.3517],
  "ultadanga": [22.5975, 88.3842],
  "ultadanga underpass": [22.5975, 88.3842],
  "gariahat": [22.5195, 88.3697],
  "gariahat crossing": [22.5195, 88.3697],
  "behala": [22.4975, 88.3180],
  "behala chowrasta": [22.4930, 88.3160],
  "mg road": [22.5816, 88.3598],
  "mahathma gandhi road": [22.5816, 88.3598],
  "college street": [22.5744, 88.3639],
  "sealdah": [22.5670, 88.3711],
  "sealdah station": [22.5670, 88.3711],
  "airport": [22.6547, 88.4467],
  "ccu": [22.6547, 88.4467],
  "dum dum": [22.6220, 88.3830],
  "tollygunge": [22.4925, 88.3470],
  "rabindra sadan": [22.5414, 88.3484],
  "exide crossing": [22.5414, 88.3484],
  "ruby": [22.5133, 88.3989],
  "ruby crossing": [22.5133, 88.3989],
  "em bypass": [22.5450, 88.3990],
  "new town": [22.5850, 88.4720],
  "chinar park": [22.6175, 88.4380],
  "chetla": [22.5200, 88.3400],
  "dhapa": [22.5400, 88.4100],
  "palmer bazar": [22.5600, 88.3800],
  "ballygunge": [22.5280, 88.3650],
  "shyambazar": [22.6010, 88.3710],
  "shyambazar five-point": [22.6010, 88.3710],
};

/**
 * Geocode a Kolkata location string using Nominatim API with fallback
 */
export async function geocodeKolkataLocation(placeName) {
  if (!placeName || typeof placeName !== 'string') return null;

  const normalized = placeName.toLowerCase().trim();

  // Direct lookup in known landmarks
  for (const [key, coords] of Object.entries(KOLKATA_LANDMARKS)) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return {
        name: placeName,
        lat: coords[0],
        lng: coords[1],
        source: 'Kolkata Geo Registry'
      };
    }
  }

  // Attempt live Nominatim geocoding bounded to Kolkata
  try {
    const query = encodeURIComponent(`${placeName}, Kolkata, West Bengal, India`);
    // Bounded viewbox: min lon 88.20, max lat 22.80, max lon 88.50, min lat 22.30
    const url = `https://nominatim.openstreetmap.org/search?q=${query}&format=json&bounded=1&viewbox=88.20,22.80,88.50,22.30&limit=1`;
    
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'DELUGE-Kolkata-Flood-Advisor/1.0'
      }
    });

    if (response.ok) {
      const data = await response.json();
      if (data && data.length > 0) {
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        // Verify coordinates lie within Kolkata bounds
        if (lat >= 22.30 && lat <= 22.80 && lon >= 88.20 && lon <= 88.50) {
          return {
            name: data[0].display_name.split(',')[0],
            lat: lat,
            lng: lon,
            source: 'OpenStreetMap Nominatim'
          };
        }
      }
    }
  } catch (error) {
    console.warn("Nominatim geocoding request failed or timed out:", error);
  }

  // Default Kolkata central location if unresolved
  return {
    name: placeName,
    lat: 22.5726,
    lng: 88.3639,
    source: 'Kolkata Metropolitan Area'
  };
}
