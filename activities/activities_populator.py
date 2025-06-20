from .openaicalls import get_google_places_search_params, format_perplexity_output
from .google_places import search_places_with_details
from .perplexity_analyzer import analyze_activity_with_perplexity

def populate_activities(activity_name: str, city: str):
    search_params = get_google_places_search_params(activity_name, city)
    if "error" in search_params:
        return search_params
    print("[ACTIVITIES] Azure OpenAI API call successful for search params")
    place_details = search_places_with_details(search_params["place_name"], search_params["city"])
    print("[ACTIVITIES] Google Places API call successful for place details")
    perplexity_analysis = analyze_activity_with_perplexity(activity_name, city, place_details)
    print("[ACTIVITIES] Perplexity API call successful for activity info")
    formatted_output = format_perplexity_output(activity_name, place_details, perplexity_analysis)
    print("[ACTIVITIES] Azure OpenAI API call successful for formatting final output")
    
    # Append all other fields from place_details except Category and Description
    if isinstance(place_details, dict) and isinstance(formatted_output, dict) and "error" not in formatted_output:
        for key, value in place_details.items():
            # Skip Category and Description as they're already handled in formatted_output
            if key not in ['Category', 'Description', 'reviews', 'Formatted Address']:
                formatted_output[key] = value
    
    formatted_output['Name'] = activity_name
    
    print("[ACTIVITIES] Final output returned")
    return formatted_output