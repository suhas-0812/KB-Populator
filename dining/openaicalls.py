import requests
import json
from typing import Dict, Any
import streamlit as st

def format_dining_perplexity_output(place_name: str, google_places_data: Dict, perplexity_data: str) -> Dict:
    """
    Format the combined Google Places and Perplexity data for dining establishments using Azure OpenAI into structured output
    
    Args:
        place_name: Original restaurant name from user input
        google_places_data: Output from Google Places API
        perplexity_data: Raw response string from Perplexity
        
    Returns:
        Formatted dictionary with all required dining fields or error
    """
    
    # Azure OpenAI configuration
    azure_endpoint = st.secrets["azure_openai"]["endpoint"]
    api_key = st.secrets["api_keys"]["azure_openai"]
    deployment_name = st.secrets["azure_openai"]["deployment_name"]
    api_version = st.secrets["azure_openai"]["api_version"]
    
    # Construct the formatting prompt
    prompt = f"""
You are a data formatting and validation expert specializing in restaurant and dining establishment data. Format the following dining data into a specific JSON structure with strict validation.

USER INPUT:
Restaurant Name: {place_name}

GOOGLE PLACES DATA:
{json.dumps(google_places_data, indent=2)}

PERPLEXITY DATA:
{perplexity_data if perplexity_data else 'No data available'}

FORMATTING AND VALIDATION INSTRUCTIONS:
Create a JSON object with exactly these fields and nested structures, applying strict validation rules:

1. Country: Extract from Google Places data/Perplexity data which is more accurate (Ex - India, USA, etc.)
2. State: Extract from Google Places data/Perplexity data which is more accurate (Ex - Karnataka, Maharashtra, etc.)
3. City: Extract from Google Places data/Perplexity data which is more accurate (Ex - Bengaluru, Mumbai, etc.)
4. Area: Extract from Google Places data/Perplexity data which is more accurate (Ex - Whitefield, Bandra, etc.)
5. Description: Choose the best description between Google Places and Perplexity (prioritize the more detailed one)
6. Recommended_Dishes: Extract from Perplexity data (comma-separated list of signature dishes)
7. Meals_Served: Nested object with boolean values based on opening hours and restaurant type
8. Private_Dining: MUST be exactly true or false (boolean)
9. Party: MUST be exactly true or false (boolean)
10. Service_Style: Nested object with boolean values for each service style
11. Cuisine: Nested object with boolean values for each cuisine type
12. Dietary: Nested object with boolean values for dietary options
13. Guest_Persona: Nested object with boolean values for guest suitability
14. Vibe: Nested object with boolean values for atmosphere types
15. Reservation_Recommended: MUST be exactly true or false (boolean)
16. Alcohol_Served: MUST be exactly true or false (boolean)

CRITICAL VALIDATION RULES:
- ALL boolean fields must be actual boolean values (true/false), not strings ("yes"/"no")
- Convert "Yes"/"True"/"yes" to true, "No"/"False"/"no" to false
- If a field is missing or unclear, use appropriate defaults:
  - Text fields: "N/A"
  - Boolean fields: false
- Ensure nested objects maintain their structure exactly as specified

Expected JSON structure:
{{
    "Country": "string",
    "Destination L1 (State)": "string",
    "Destination L2 (City)": "string",
    "Destination L3 (Area)": "string",
    "Description": "string",
    "Recommended_Dishes": "string",
    "Meals_Served": {{
        "Breakfast": boolean,
        "Lunch": boolean,
        "Dinner": boolean,
        "Late_Night": boolean,
        "24_Hours": boolean
    }},
    "Private_Dining": boolean,
    "Party": boolean,
    "Service_Style": {{
        "Michelin_Star": boolean,
        "Fine_Dining": boolean,
        "Casual_Dining": boolean,
        "Bistro": boolean,
        "Cafe": boolean,
        "Bakery": boolean,
        "Breweries": boolean,
        "Farm_to_Table": boolean,
        "Cocktail_Bars": boolean,
        "Speakeasys": boolean,
        "Tapas_Bar": boolean,
        "Rooftop_Bar": boolean,
        "Dessert_Spot": boolean
    }},
    "Cuisine": {{
        "Fast_Food": boolean,
        "Modern_Indian": boolean,
        "Indian": boolean,
        "Continental": boolean,
        "Finger_Food": boolean,
        "Burmese": boolean,
        "Peruvian": boolean,
        "Lebanese": boolean,
        "Afghan": boolean,
        "Malaysian": boolean,
        "Vietnamese": boolean,
        "Pan_Asian": boolean,
        "Mediterranean": boolean,
        "Thai": boolean,
        "Italian": boolean,
        "Japanese": boolean,
        "Mexican": boolean,
        "Modern_European": boolean,
        "Contemporary_Dining": boolean,
        "Molecular_Gastronomy": boolean
    }},
    "Dietary": {{
        "Vegetarian_Non_Vegetarian": boolean,
        "Vegetarian": boolean,
        "Vegan_Options": boolean,
        "Seafood_Speciality": boolean
    }},
    "Guest_Persona": {{
        "Couple_Friendly": boolean,
        "Family_Friendly": boolean,
        "Especially_For_Kids": boolean,
        "No_Kids_Allowed": boolean,
        "Senior_Friendly": boolean,
        "Pet_Friendly": boolean
    }},
    "Vibe": {{
        "Romantic_Intimate": boolean,
        "Refined_Elegant": boolean,
        "Luxurious_Formal": boolean,
        "Bohemian_Playful": boolean,
        "Modern_Chic": boolean,
        "Vibrant_Lively": boolean,
        "Relaxed_Cozy": boolean
    }},
    "Reservation_Recommended": boolean,
    "Alcohol_Served": boolean
}}

IMPORTANT NOTES:
- Base meal service determination on opening hours and restaurant type
- Be conservative with boolean values - only set to true if there's clear evidence
- Maintain exact field names and structure as specified
- All nested objects must include all specified sub-fields
- Text fields should be descriptive and informative

Return ONLY the JSON object with properly validated data types and structure, no additional text.
"""

    # Azure OpenAI API call
    url = f"{azure_endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 3000
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
            
            # Clean and parse the JSON response
            try:
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                formatted_data = json.loads(content)
                
                # Define the expected structure with defaults
                expected_structure = {
                    "Country": "N/A",
                    "Destination L1 (State)": "N/A",
                    "Destination L2 (City)": "N/A",
                    "Destination L3 (Area)": "N/A",
                    "Description": "N/A",
                    "Recommended_Dishes": "N/A",
                    "Meals_Served": {
                        "Breakfast": False,
                        "Lunch": False,
                        "Dinner": False,
                        "Late_Night": False,
                        "24_Hours": False
                    },
                    "Private_Dining": False,
                    "Party": False,
                    "Service_Style": {
                        "Michelin_Star": False,
                        "Fine_Dining": False,
                        "Casual_Dining": False,
                        "Bistro": False,
                        "Cafe": False,
                        "Bakery": False,
                        "Breweries": False,
                        "Farm_to_Table": False,
                        "Cocktail_Bars": False,
                        "Speakeasys": False,
                        "Tapas_Bar": False,
                        "Rooftop_Bar": False,
                        "Dessert_Spot": False
                    },
                    "Cuisine": {
                        "Fast_Food": False,
                        "Modern_Indian": False,
                        "Indian": False,
                        "Continental": False,
                        "Finger_Food": False,
                        "Burmese": False,
                        "Peruvian": False,
                        "Lebanese": False,
                        "Afghan": False,
                        "Malaysian": False,
                        "Vietnamese": False,
                        "Pan_Asian": False,
                        "Mediterranean": False,
                        "Thai": False,
                        "Italian": False,
                        "Japanese": False,
                        "Mexican": False,
                        "Modern_European": False,
                        "Contemporary_Dining": False,
                        "Molecular_Gastronomy": False
                    },
                    "Dietary": {
                        "Vegetarian_Non_Vegetarian": False,
                        "Vegetarian": False,
                        "Vegan_Options": False,
                        "Seafood_Speciality": False
                    },
                    "Guest_Persona": {
                        "Couple_Friendly": False,
                        "Family_Friendly": False,
                        "Especially_For_Kids": False,
                        "No_Kids_Allowed": False,
                        "Senior_Friendly": False,
                        "Pet_Friendly": False
                    },
                    "Vibe": {
                        "Romantic_Intimate": False,
                        "Refined_Elegant": False,
                        "Luxurious_Formal": False,
                        "Bohemian_Playful": False,
                        "Modern_Chic": False,
                        "Vibrant_Lively": False,
                        "Relaxed_Cozy": False
                    },
                    "Reservation_Recommended": False,
                    "Alcohol_Served": False
                }
                
                # Merge formatted data with expected structure to ensure all fields are present
                def merge_with_defaults(expected, actual):
                    result = expected.copy()
                    for key, value in actual.items():
                        if key in result:
                            if isinstance(value, dict) and isinstance(result[key], dict):
                                result[key] = merge_with_defaults(result[key], value)
                            else:
                                result[key] = value
                    return result
                
                final_data = merge_with_defaults(expected_structure, formatted_data)
                
                return final_data
                
            except json.JSONDecodeError as e:
                return {"error": f"Failed to parse Azure OpenAI response as JSON: {str(e)}"}
                
        else:
            return {"error": "No valid response received from Azure OpenAI"}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Azure OpenAI API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg += f" - Details: {error_details}"
            except:
                error_msg += f" - Response: {e.response.text}"
        return {"error": error_msg}
    except Exception as e:
        return {"error": f"Unexpected error in Azure OpenAI formatting: {str(e)}"}

