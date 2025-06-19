import requests
import json
from typing import Dict, Any
import streamlit as st

def analyze_dining_with_perplexity(place_name: str, city: str, places_api_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze dining establishment information using Perplexity Sonar Pro model
    
    Args:
        place_name: Name of the restaurant/dining place to analyze
        city: City where the restaurant is located
        places_api_output: Single place dictionary from Google Places API
        
    Returns:
        Dictionary with comprehensive dining establishment information
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
    opening_hours = places_api_output.get('opening_hours', 'N/A')
    reviews = places_api_output.get('reviews', [])
    website = places_api_output.get('website', 'N/A')
    
    # Prepare reviews text for analysis (Google Places API returns max 5 reviews by default)
    reviews_text = ""
    if reviews:
        reviews_text = " | ".join([review.get('text', '') if isinstance(review, dict) else str(review) for review in reviews])
    
    # Prepare opening hours text
    hours_text = ""
    if opening_hours != 'N/A' and isinstance(opening_hours, list):
        hours_text = " | ".join(opening_hours)
    elif opening_hours != 'N/A':
        hours_text = str(opening_hours)
    
    # Construct the comprehensive prompt
    prompt = f"""
Please research and provide comprehensive information for the following dining establishment using reliable and up-to-date sources such as official websites, food review platforms, dining guides, and restaurant directories:

Restaurant/Dining Place: {place_name}
City: {city}
Google Category: {google_category}
Google Description: {google_description}
Google Rating: {google_rating}
Opening Hours: {hours_text}
Website: {website}
Sample Reviews: {reviews_text}

RESEARCH INSTRUCTIONS:
1. Research through multiple reliable sources including:
   - Official restaurant website and social media
   - Zomato, Swiggy, EazyDiner, OpenTable
   - TripAdvisor restaurant reviews
   - Food blogs and professional restaurant reviews
   - Local dining guides and food critics
   - Recent customer reviews and menu information

2. Focus on gathering accurate, current information about:
   - Menu highlights and signature dishes
   - Service style and dining experience
   - Cuisine types and dietary options
   - Ambiance and target audience
   - Operating hours and meal service times
   - Reservation policies and special features

3. For boolean fields: Answer true only if there is clear evidence/proof from reliable sources. If uncertain or no evidence, answer false.

4. For "Meals Served": Based on opening hours and restaurant type, determine which meals are typically served (B=Breakfast, L=Lunch, D=Dinner, Late Night, 24 Hours).

Based on your comprehensive research, provide information in JSON format:

{{
    "Area": "string - The area of the restaurant, extracted from the Google Places API if it accurately describes the area of the restaurant, else populate it with the accurate area",
    "Description": "Detailed description of the dining establishment, its concept, ambiance, and what makes it special",
    "Recommended_Dishes": "List of signature dishes, popular items, or chef's recommendations (comma-separated)",
    "Meals_Served": {{ 
        "Breakfast": "true/false - Does the restaurant serve breakfast?" (Choose based on the opening hours and the type of restaurant),
        "Lunch": "true/false - Does the restaurant serve lunch?" (Choose based on the opening hours and the type of restaurant),
        "Dinner": "true/false - Does the restaurant serve dinner?" (Choose based on the opening hours and the type of restaurant),
        "Late_Night": "true/false - Does the restaurant serve late night meals (after 11 PM)?" (Choose based on the opening hours and the type of restaurant),
        "24_Hours": "true/false - Is the restaurant open 24 hours?" (Choose based on the opening hours and the type of restaurant)
    }},
    "Private_Dining": "true/false - Does the restaurant offer private dining rooms or exclusive dining experiences?",
    "Party": "true/false - Is the restaurant suitable for parties, celebrations, or group events?",
    "Service_Style": {{
        "Michelin_Star": "true/false - Is this a Michelin starred restaurant?",
        "Fine_Dining": "true/false - Is this a fine dining establishment with formal service?",
        "Casual_Dining": "true/false - Is this a casual dining restaurant?",
        "Bistro": "true/false - Is this a bistro-style establishment?",
        "Cafe": "true/false - Is this primarily a cafe?",
        "Bakery": "true/false - Is this a bakery or includes significant baking offerings?",
        "Breweries": "true/false - Is this a brewery or brewpub?",
        "Farm_to_Table": "true/false - Does this restaurant focus on farm-to-table dining?",
        "Cocktail_Bars": "true/false - Is this primarily a cocktail bar or has an extensive cocktail program?",
        "Speakeasys": "true/false - Is this a speakeasy-style establishment?",
        "Tapas_Bar": "true/false - Is this a tapas bar or focuses on small plates?",
        "Rooftop_Bar": "true/false - Is this a rooftop bar or restaurant?",
        "Dessert_Spot": "true/false - Is this primarily known for desserts?"
    }},
    "Cuisine": {{
        "Fast_Food": "true/false - Does this serve fast food?",
        "Modern_Indian": "true/false - Does this serve modern Indian cuisine?",
        "Indian": "true/false - Does this serve traditional Indian cuisine?",
        "Continental": "true/false - Does this serve continental cuisine?",
        "Finger_Food": "true/false - Does this specialize in finger foods/appetizers?",
        "Burmese": "true/false - Does this serve Burmese cuisine?",
        "Peruvian": "true/false - Does this serve Peruvian cuisine?",
        "Lebanese": "true/false - Does this serve Lebanese cuisine?",
        "Afghan": "true/false - Does this serve Afghan cuisine?",
        "Malaysian": "true/false - Does this serve Malaysian cuisine?",
        "Vietnamese": "true/false - Does this serve Vietnamese cuisine?",
        "Pan_Asian": "true/false - Does this serve Pan Asian cuisine?",
        "Mediterranean": "true/false - Does this serve Mediterranean cuisine?",
        "Thai": "true/false - Does this serve Thai cuisine?",
        "Italian": "true/false - Does this serve Italian cuisine?",
        "Japanese": "true/false - Does this serve Japanese cuisine?",
        "Mexican": "true/false - Does this serve Mexican cuisine?",
        "Modern_European": "true/false - Does this serve modern European cuisine?",
        "Contemporary_Dining": "true/false - Does this offer contemporary dining experiences?",
        "Molecular_Gastronomy": "true/false - Does this restaurant practice molecular gastronomy?"
    }},
    "Dietary": {{
        "Vegetarian_Non_Vegetarian": "true/false - Does this restaurant serve both vegetarian and non-vegetarian options?",
        "Vegetarian": "true/false - Is this a vegetarian-only restaurant?",
        "Vegan_Options": "true/false - Does this restaurant offer vegan options?",
        "Seafood_Speciality": "true/false - Does this restaurant specialize in seafood?"
    }},
    "Guest_Persona": {{
        "Couple_Friendly": "true/false - Is this restaurant suitable for couples/romantic dining?",
        "Family_Friendly": "true/false - Is this restaurant suitable for families with children?",
        "Especially_For_Kids": "true/false - Does this restaurant have special features or menu for kids?",
        "No_Kids_Allowed": "true/false - Does this restaurant have age restrictions or discourage children?",
        "Senior_Friendly": "true/false - Is this restaurant accessible and suitable for senior citizens?",
        "Pet_Friendly": "true/false - Are pets allowed in this restaurant?"
    }},
    "Vibe": {{
        "Romantic_Intimate": "true/false - Does this restaurant have a romantic or intimate atmosphere?",
        "Refined_Elegant": "true/false - Does this restaurant have a refined or elegant atmosphere?",
        "Luxurious_Formal": "true/false - Does this restaurant have a luxurious or formal atmosphere?",
        "Bohemian_Playful": "true/false - Does this restaurant have a bohemian or playful atmosphere?",
        "Modern_Chic": "true/false - Does this restaurant have a modern or chic atmosphere?",
        "Vibrant_Lively": "true/false - Does this restaurant have a vibrant or lively atmosphere?",
        "Relaxed_Cozy": "true/false - Does this restaurant have a relaxed or cozy atmosphere?"
    }},
    "Reservation_Recommended": "true/false - Is it recommended to make reservations at this restaurant?",
    "Alcohol_Served": "true/false - Does this restaurant serve alcoholic beverages?"
}}

IMPORTANT: 
- Base your analysis on factual information from reliable sources
- For boolean fields, be conservative - only answer true with clear evidence
- Use exactly true or false (lowercase) for all boolean fields
- If information is not available, use "Not Available" for text fields and false for booleans
- Do not hallucinate or make assumptions - stick to verifiable facts
- Pay special attention to opening hours to determine meal service times accurately

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

def get_dining_info(place_name: str, city: str, places_api_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simplified function to get dining establishment information
    
    Args:
        place_name: Name of the restaurant/dining place
        city: City where the restaurant is located
        places_api_output: Google Places API output from search_places_with_details function
        
    Returns:
        Dictionary with dining information or error
    """
    result = analyze_dining_with_perplexity(place_name, city, places_api_output)
    
    if "error" in result:
        return result
    
    # Return parsed data if available, otherwise raw response
    if "parsed_data" in result:
        return result["parsed_data"]
    else:
        return {"raw_response": result.get("raw_response", "No data available")}