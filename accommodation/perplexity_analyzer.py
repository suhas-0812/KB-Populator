import requests
from typing import Dict, Any
import streamlit as st

def analyze_place_with_perplexity(place_name: str, city: str, places_api_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze place information using Perplexity Sonar Pro model
    
    Args:
        place_name: Name of the place to search for
        city: City where the place is located
        places_api_output: Single place dictionary from Google Places API
        
    Returns:
        Dictionary with analyzed place information
    """
    api_key = st.secrets["api_keys"]["perplexity"]
    
    # Validate API key format
    if not api_key.startswith('pplx-'):
        return {"error": "Invalid Perplexity API key format"}
    
    # Handle the case where no place data is provided
    if not places_api_output:
        return {"error": "No places data provided"}
    
    # Extract relevant information from places API output (now a single dict)
    google_description = places_api_output.get('Description', 'N/A')
    google_category = places_api_output.get('Category', 'N/A')
    google_rating = places_api_output.get('google_rating', 'N/A')
    reviews = places_api_output.get('reviews', [])
    formatted_address = places_api_output.get('Formatted Address', 'N/A')
    
    # Prepare reviews text for analysis (first 5 reviews)
    reviews_text = ""
    if reviews:
        reviews_sample = reviews[:5]  # Take first 5 reviews
        reviews_text = " | ".join(reviews_sample)
    
    # Construct the prompt
    prompt = f"""
Please research and provide comprehensive recommendations for the following place using reliable and up-to-date sources such as official websites, travel guides, booking platforms, review sites, and hospitality industry reports:

Place Name: {place_name}
City: {city}
Google Category: {google_category}
Google Description: {google_description}
Google Rating: {google_rating}
Sample Reviews: {reviews_text}
Formatted Address: {formatted_address}

RECOMMENDATION RESEARCH INSTRUCTIONS:
1. Research through multiple reliable sources including:
   - Official website of the establishment
   - TripAdvisor, Booking.com, Hotels.com, Expedia
   - Travel blogs and professional travel guides
   - Local tourism websites and recommendation sites
   - Recent visitor reviews and testimonials
   - Travel recommendation articles and "best of" lists

2. Focus on recommendation aspects:
   - Who should visit this place and why
   - What makes this place worth recommending
   - Best times to visit or specific experiences to have
   - What type of travelers would most enjoy this place
   - Unique selling points and standout features

3. Consider different traveler types:
   - Families with children
   - Couples seeking romance
   - Solo travelers
   - Senior citizens
   - Pet owners
   - Adventure seekers vs. relaxation seekers

Based on your comprehensive research, provide recommendations in JSON format:

{{
    "Country": "The country of the place, extracted from the Formatted Address if it accurately describes the country of the place, else populate it with the accurate country",
    "State": "The state of the place, extracted from the Formatted Address if it accurately describes the state of the place, else populate it with the accurate state",
    "City": "The city of the place, extracted from the Formatted Address if it accurately describes the city of the place, else populate it with the accurate city",
    "Area": "The area of the place, extracted from the Formatted Address if it accurately describes the area of the place, else populate it with the accurate area",
    "Category": "Primary category with recommendation context. It must always be one of - [Accomodation - Wellness, Accomodation - Boutique / Villa / Homestay,  Accomodation - Haveli, Accomodation - Hotel / Resorts]",
    "Description": "A short single line description of the place. Recommendation-focused description explaining why visitors should choose this place, what unique experiences it offers, and what makes it special. Include specific recommendations about what to do, see, or experience here.",
    "Pool": "Yes/No - Recommended for pool lovers? Include details about pool experience if this is a highlight.",
    "Pet_Friendly": "Yes/No - Recommended for pet owners? Yes only if there is a proof about it else no. Include specific pet amenities and policies that make it pet-friendly. If it is not suitable for pets, say no and state the reason.",
    "View": "Yes/No - Recommended for scenic views? Yes only if there is a proof about it else no. Specify what types of views and why they're worth visiting for. If it is not suitable for views, say no and state the reason.",
    "Kid_Friendly": "Yes/No - Recommended for families with children? Yes only if there is a proof about it else no. Include specific kid-friendly features and experiences. If it is not suitable for kids, say no and state the reason.",
    "Romantic": "Yes/No - Recommended for couples and romantic occasions? Yes only if there is a proof about it else no. Include what makes it romantic and special experiences for couples. If it is not suitable for couples, say no and state the reason.",
    "Senior_Citizen_Friendly": "Yes/No - Recommended for senior travelers? Say yes only if there is a proof about it and state the proof, else say no stating that it is not suitable for senior travelers. Include specific senior-friendly features and experiences."
}}

IMPORTANT: Frame your response as recommendations. Focus on who should visit, why they should visit, and what they can expect. Base recommendations on current, verified information from reputable sources.

Please respond with ONLY the JSON object, no additional text or source citations.
"""

    # Perplexity API endpoint
    url = "https://api.perplexity.ai/chat/completions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "model": "sonar-pro",  # Updated model name
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 4000
    }
    
    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse response
        response_data = response.json()
        
        # Extract the content from the response
        if 'choices' in response_data and len(response_data['choices']) > 0:
            content = response_data['choices'][0]['message']['content']
            
            # Return the raw content without parsing
            return {
                "raw_response": content,
                "status": "success"
            }
                
        else:
            print("No valid response from Perplexity API")
            return {"error": "No valid response from Perplexity API"}
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perplexity API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                print(f"API Error Details: {error_details}")
            except:
                print(f"Response content: {e.response.text}")
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {str(e)}"}
