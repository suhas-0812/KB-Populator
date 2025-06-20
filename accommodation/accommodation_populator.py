from .google_places import search_places_with_details
from .perplexity_analyzer import analyze_place_with_perplexity
from .openaicalls import format_with_azure_openai

def populate_accommodation(accommodation_name, city):
    places_api_output = search_places_with_details(accommodation_name, city)
    if "error" in places_api_output:
        return places_api_output
    
    places_context_for_llms = {
        "Formatted Address": places_api_output["Formatted Address"],
        "Description": places_api_output["Description"],
        "google_rating": places_api_output["google_rating"],
        "Category": places_api_output["Category"],
    }

    perplexity_output = analyze_place_with_perplexity(accommodation_name, city, places_context_for_llms)
    if "error" in perplexity_output:
        return {"error": "No perplexity data available"}
    
    formatted_output = format_with_azure_openai(accommodation_name, places_context_for_llms, perplexity_output)
    if "error" in formatted_output:
        return {"error": "No formatted output available"}
    
    formatted_output["website"] = places_api_output["website"]
    formatted_output["photo_urls"] = places_api_output["photo_urls"]
    formatted_output["google_maps_url"] = places_api_output["google_maps_url"]
    return formatted_output