from geopy.geocoders import Nominatim


def get_lan_and_lon(country, city):
    try:
        if not city  or not country:
            print("Invalid city or country")
            return None
        geolocator = Nominatim(user_agent="geoapi")
        result = geolocator.geocode(f"{city}, {country}", timeout=None)
        if result: return result.latitude, result.longitude
    except Exception as e:
        print(f"Error: {e}")
        return None