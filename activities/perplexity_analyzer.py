import requests
import json
from typing import Dict, Any
import streamlit as st

def analyze_activity_with_perplexity(place_name: str, city: str, places_api_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze activity/attraction information using Perplexity Sonar Pro model
    
    Args:
        place_name: Name of the place/activity to analyze
        city: City where the place is located
        places_api_output: Single place dictionary from Google Places API
        
    Returns:
        Dictionary with comprehensive activity information
    """
    api_key = st.secrets["api_keys"]["perplexity"]
    
    # Validate API key format
    if not api_key.startswith('pplx-'):
        return {"error": "Invalid API key format"}
    
    # Handle the case where no place data is provided
    if not places_api_output:
        return {"error": "No places data provided"}
    
    # Extract relevant information from places API output
    google_description = places_api_output.get('Description', 'N/A')
    google_category = places_api_output.get('Category', 'N/A')
    google_rating = places_api_output.get('google_rating', 'N/A')
    reviews = places_api_output.get('reviews', [])
    formatted_address = places_api_output.get('Formatted Address', 'N/A')
    
    # Prepare reviews text for analysis (first 5 reviews)
    reviews_text = ""
    if reviews:
        reviews_sample = reviews[:5]  # Take first 5 reviews
        reviews_text = " | ".join([review.get('text', '') if isinstance(review, dict) else str(review) for review in reviews_sample])
    
    # Construct the comprehensive prompt
    prompt = f"""
Please research and provide comprehensive information for the following place/activity using reliable and up-to-date sources such as official websites, travel guides, booking platforms, review sites, and tourism authorities:

Place/Activity Name: {place_name}
City: {city}
Google Category: {google_category}
Google Description: {google_description}
Google Rating: {google_rating}
Sample Reviews: {reviews_text}
Formatted Address: {formatted_address}

RESEARCH INSTRUCTIONS:
1. Research through multiple reliable sources including:
   - Official website and booking platforms
   - TripAdvisor, GetYourGuide, Viator, Klook
   - Local tourism authority websites
   - Travel blogs and professional guides
   - Recent visitor reviews and pricing information
   - Official government tourism sites

2. Focus on gathering accurate, current information about:
   - Exact pricing in Indian Rupees (INR)
   - Operating hours and seasonal information
   - Duration and what's included/excluded
   - Specific characteristics and suitability for different travelers

3. For pricing: Convert international prices to INR using current exchange rates. If pricing varies, provide typical/average pricing.

4. For boolean fields: Answer true only if there is clear evidence/proof. If uncertain or no evidence, answer false.

Based on your comprehensive research, provide information in JSON format:

{{
    "Country": "The country of the place, extracted from the Formatted Address if it accurately describes the country of the place, else populate it with the accurate country",
    "State": "The state of the place, extracted from the Formatted Address if it accurately describes the state of the place, else populate it with the accurate state",
    "City": "The city of the place, extracted from the Formatted Address if it accurately describes the city of the place, else populate it with the accurate city",
    "Area": "The area of the place, extracted from the Formatted Address if it accurately describes the area of the place, else populate it with the accurate area",
    "Category": "Primary category of this attraction/activity (e.g., Historical Site, Adventure Activity, Cultural Experience, Entertainment, Nature/Wildlife, Religious Site, Museum, Theme Park, etc.)",
    "Description": "A detailed description of what visitors can expect, what makes this place special, and key highlights of the experience",
    "Price_Adult_INR": "Adult ticket price in Indian Rupees (number only, e.g., 500). If free, write 0. If pricing varies significantly, provide average price.",
    "Price_Child_INR": "Child ticket price in Indian Rupees (number only, e.g., 250). If same as adult or no child pricing, write same as adult price.",
    "Duration": "Average time required to cover the activity in hours (number only, e.g., 2.5 for 2.5 hours, 0.5 for 30 minutes, 8 for full day)",
    "Timings": "Operational timings (e.g., '9:00 AM - 6:00 PM', '24 hours', 'Sunrise to Sunset')",
    "Season_Operational_Months": "Best season or operational months (e.g., 'Year-round', 'October to March', 'Closed during monsoon')",
    "Inclusions": "What is included in the basic entry/experience (e.g., 'Entry ticket, Basic guided tour', 'Access to all exhibits')",
    "Exclusions": "What is not included and costs extra (e.g., 'Food and beverages, Photography charges, Special exhibitions')",
    "Must_Do": "true/false - Is this considered a must-visit attraction in the city? true only if it's widely recommended as essential.",
    "Group_Friendly": "true/false - Suitable for group visits? true only if there's evidence of group facilities/discounts.",
    "Offbeat": "true/false - Is this an offbeat/lesser-known attraction? true only if it's not mainstream/touristy.",
    "Historic_Cultural": "true/false - Does this have historical or cultural significance? true only with clear evidence.",
    "Party": "true/false - Suitable for parties/celebrations? true only if there's evidence of party facilities/nightlife.",
    "Pet_Friendly": "true/false - Are pets allowed? true only if there's clear evidence pets are welcome.",
    "Adventurous": "true/false - Involves adventure/thrill activities? true only if there are adventure elements.",
    "Kid_Friendly": "true/false - Suitable for children? true only if there's evidence of kid-friendly features.",
    "Romantic": "true/false - Suitable for couples/romantic visits? true only if there's evidence of romantic appeal.",
    "Wellness_Relaxation": "true/false - Focused on wellness/relaxation? true only if it offers wellness/spa/meditation facilities.",
    "Senior_Citizen_Friendly": "true/false - Accessible and suitable for senior citizens? true only if there's evidence of senior-friendly facilities."
}}

IMPORTANT: 
- Provide specific, accurate information based on current data
- For pricing, ensure amounts are in INR and realistic
- For booleans, be conservative - only answer true with clear evidence
- Use exactly true or false (lowercase) for boolean fields
- If information is not available, use "Not Available" for text fields and false for booleans

Please respond with ONLY the JSON object, no additional text.
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
        "model": "sonar-pro",
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
            
            # Try to parse as JSON for structured output
            try:
                # Clean the content
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                # Parse JSON
                parsed_data = json.loads(content)
                
                return {
                    "parsed_data": parsed_data,
                    "raw_response": content,
                    "status": "success"
                }
                
            except json.JSONDecodeError:
                # Return raw response if JSON parsing fails
                return {
                    "raw_response": content,
                    "status": "success_raw_only"
                }
                
        else:
            return {"error": "No valid response from Perplexity API"}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg += f" - Details: {error_details}"
            except:
                error_msg += f" - Response: {e.response.text}"
        return {"error": error_msg}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_activity_info(place_name: str, city: str, places_api_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simplified function to get activity information
    
    Args:
        place_name: Name of the place/activity
        city: City where the place is located
        places_api_output: Google Places API output
        
    Returns:
        Dictionary with activity information or error
    """
    result = analyze_activity_with_perplexity(place_name, city, places_api_output)
    
    if "error" in result:
        return result
    
    # Return parsed data if available, otherwise raw response
    if "parsed_data" in result:
        return result["parsed_data"]
    else:
        return {"raw_response": result.get("raw_response", "No data available")} 