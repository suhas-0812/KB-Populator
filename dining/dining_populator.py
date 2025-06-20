from .google_places import search_places_with_details
from .perplexity_analyzer import get_dining_info
from .openaicalls import format_dining_perplexity_output

def populate_dining(place_name: str, city: str):
    place_data = search_places_with_details(place_name, city)
    if "error" in place_data:
        return place_data
    print("[DINING] Google places API call successful for place details")
    dining_info = get_dining_info(place_name, city, place_data)
    print("[DINING] Perplexity API call successful for dining info")
    formatted_output = format_dining_perplexity_output(place_name, place_data, dining_info)
    print("[DINING] Azure OpenAI API call successful for formatting final output")
    # Append all other fields from place_details except Category and Description
    if isinstance(place_data, dict) and isinstance(formatted_output, dict) and "error" not in formatted_output:
        for key, value in place_data.items():
            # Skip Category and Description as they're already handled in formatted_output
            if key not in ['Category', 'Description', 'reviews', 'Formatted Address']:
                formatted_output[key] = value
    
    formatted_output['Name'] = place_name
    print("[DINING] Final output returned")

    return formatted_output