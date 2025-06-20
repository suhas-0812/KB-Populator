import json
import requests
from typing import Dict, Optional, Any, List
import streamlit as st

def get_google_places_search_params(activity_name: str, context_city: Optional[str] = None) -> Dict[str, str]:
    """
    Parse an activity name using Azure OpenAI and return place_name and city for Google Places API
    
    Args:
        activity_name: Name of the activity/place from itinerary
        context_city: Optional city context to help with location disambiguation
        
    Returns:
        Dictionary with only 'place_name' and 'city' keys
    """
    
    # Azure OpenAI configuration
    azure_endpoint = st.secrets["azure_openai"]["endpoint"]
    api_key = st.secrets["api_keys"]["azure_openai"]
    deployment_name = st.secrets["azure_openai"]["deployment_name"]
    api_version = st.secrets["azure_openai"]["api_version"]
    
    # Construct the parsing prompt
    prompt = f"""
You are an expert at parsing travel activity names and determining the best way to search for them on Google Places API.

TASK: Analyze the given activity name and return optimal search parameters for Google Places API.

ACTIVITY NAME: "{activity_name}"
CONTEXT CITY: {context_city if context_city else "Not provided"}

ANALYSIS INSTRUCTIONS:
1. Identify if this is a specific place name, generic activity, or venue type
2. Extract the most likely place name to search for
3. Determine the most appropriate city to search in

RESPONSE FORMAT:
Return a JSON object with exactly these fields:

{{
    "place_name": "Exact name to search for in Google Places",
    "city": "City name to search in"
}}

EXAMPLES:
- "Eiffel Tower" → {{"place_name": "Eiffel Tower", "city": "Paris"}}
- "Visit local markets in Bangkok" → {{"place_name": "Chatuchak Market", "city": "Bangkok"}}
- "Dinner at Michelin restaurant" → {{"place_name": "Michelin restaurant", "city": "{context_city if context_city else 'Unknown'}"}}
- "Central Park picnic" → {{"place_name": "Central Park", "city": "New York"}}
- "Museum visit" → {{"place_name": "museum", "city": "{context_city if context_city else 'Unknown'}"}}

RULES:
- If activity mentions a specific landmark, use that exact name
- If it's a generic activity, try to suggest the most famous/relevant venue
- Always provide a city, even if you have to make an educated guess
- Be specific rather than generic when possible

Return ONLY the JSON object, no additional text.
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
        "temperature": 0.3,
        "max_tokens": 500
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
                
                parsed_result = json.loads(content)
                
                return {
                    "place_name": parsed_result.get("place_name", activity_name),
                    "city": parsed_result.get("city", context_city if context_city else "Unknown")
                }
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "place_name": activity_name.strip(),
                    "city": context_city if context_city else "Unknown"
                }
                
        else:
            # Fallback if no response
            return {
                "place_name": activity_name.strip(),
                "city": context_city if context_city else "Unknown"
            }
            
    except Exception:
        # Fallback for any errors
        return {
            "place_name": activity_name.strip(),
            "city": context_city if context_city else "Unknown"
        }

def format_perplexity_output(place_name: str, google_places_data: Dict, perplexity_data: str) -> Dict:
    """
    Format the combined Google Places and Perplexity data using Azure OpenAI into structured output
    
    Args:
        place_name: Original place name from user input
        google_places_data: Output from Google Places API
        perplexity_data: Raw response string from Perplexity
        
    Returns:
        Formatted dictionary with all required fields or error
    """
    
    # Azure OpenAI configuration
    azure_endpoint = st.secrets["azure_openai"]["endpoint"]
    api_key = st.secrets["api_keys"]["azure_openai"]
    deployment_name = st.secrets["azure_openai"]["deployment_name"]
    api_version = st.secrets["azure_openai"]["api_version"]
    
    # Construct the formatting prompt
    prompt = f"""
You are a data formatting and validation expert. Format the following travel data into a specific JSON structure with strict validation.

USER INPUT:
Place Name: {place_name}

GOOGLE PLACES DATA:
{json.dumps(google_places_data, indent=2)}

PERPLEXITY DATA:
{perplexity_data if perplexity_data else 'No data available'}

FORMATTING AND VALIDATION INSTRUCTIONS:
Create a JSON object with exactly these fields, applying strict validation rules:

1. Country: Extract from Google Places data/Perplexity data which is more accurate (Ex - India, USA, etc.)
2. State: Extract from Google Places data/Perplexity data which is more accurate (Ex - Karnataka, Maharashtra, etc.)
3. City: Extract from Google Places data/Perplexity data which is more accurate (Ex - Bengaluru, Mumbai, etc.)
4. Area: Extract from Google Places data/Perplexity data which is more accurate (Ex - Whitefield, Bandra, etc.)
5. Category: Extract from Perplexity data (activity type like Historical Site, Adventure Activity, etc.)
6. Description: Choose the best description between Google Places and Perplexity (prioritize the more detailed one)
7. Price_Adult_INR: Extract from Perplexity data - MUST be a number only (e.g., 500, not "500 INR")
8. Price_Child_INR: Extract from Perplexity data - MUST be a number only (e.g., 250, not "250 INR")
9. Duration: Extract from Perplexity data - MUST be a number representing hours only (e.g., 2.5 for 2.5 hours, 0.5 for 30 minutes, 8 for full day, not "2-3 hours")
10. Timings: Extract from Perplexity data (e.g., "9:00 AM - 6:00 PM")
11. Season_Operational_Months: Extract from Perplexity data (e.g., "October to March")
12. Inclusions: Extract from Perplexity data
13. Exclusions: Extract from Perplexity data
14. Must_Do: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
15. Group_Friendly: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
16. Offbeat: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
17. Historic_Cultural: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
18. Party: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
19. Pet_Friendly: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
20. Adventurous: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
21. Kid_Friendly: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
22. Romantic: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
23. Wellness_Relaxation: MUST be exactly true or false (boolean, not "Yes"/"No" strings)
24. Senior_Citizen_Friendly: MUST be exactly true or false (boolean, not "Yes"/"No" strings)

CRITICAL VALIDATION RULES:
- Duration: Convert any text duration to numeric hours (e.g., "2-3 hours" → 2.5, "30 minutes" → 0.5, "full day" → 8, "half day" → 4)
- Prices: Remove any currency symbols, text, or formatting - return only the number
- Boolean fields: Convert "Yes"/"True"/"yes" to true, "No"/"False"/"no" to false
- If a field is missing or unclear, use appropriate defaults:
  - Text fields: "Not Available"
  - Boolean fields: false
  - Numeric fields: 0
- Ensure all boolean fields are actual boolean values (true/false), not strings
- Ensure Price_Adult_INR and Price_Child_INR are numbers, not strings
- Ensure Duration is a number, not a string

VALIDATION EXAMPLES:
- "2-3 hours" → Duration: 2.5
- "30 minutes" → Duration: 0.5
- "Full day experience" → Duration: 8
- "Half day tour" → Duration: 4
- "Yes" → true
- "No" → false
- "500 INR" → 500
- "Free entry" → 0

Return ONLY the JSON object with properly validated data types, no additional text.

Expected JSON structure:
{{
    "Country": "string",
    "Destination L1 (State)": "string",
    "Destination L2 (City)": "string",
    "Destination L3 (Area)": "string",
    "Category": "string",
    "Description": "string",
    "Price_Adult_INR": "number",
    "Price_Child_INR": "number",
    "Duration": "number",
    "Timings": "string",
    "Season_Operational_Months": "string",
    "Inclusions": "string",
    "Exclusions": "string",
    "Must_Do": "boolean",
    "Group_Friendly": "boolean",
    "Offbeat": "boolean",
    "Historic_Cultural": "boolean",
    "Party": "boolean",
    "Pet_Friendly": "boolean",
    "Adventurous": "boolean",
    "Kid_Friendly": "boolean",
    "Romantic": "boolean",
    "Wellness_Relaxation": "boolean",
    "Senior_Citizen_Friendly": "boolean",
}}  
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
        "max_tokens": 2000
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
                
                # Validate required fields exist
                required_fields = [
                    "Category", "Description", "Price_Adult_INR", "Price_Child_INR", 
                    "Duration", "Timings", "Season_Operational_Months", "Inclusions", 
                    "Exclusions", "Must_Do", "Group_Friendly", "Offbeat", 
                    "Historic_Cultural", "Party", "Pet_Friendly", "Adventurous", 
                    "Kid_Friendly", "Romantic", "Wellness_Relaxation", "Senior_Citizen_Friendly"
                ]
                
                # Ensure all required fields are present with appropriate defaults
                for field in required_fields:
                    if field not in formatted_data:
                        if field in ["Must_Do", "Group_Friendly", "Offbeat", "Historic_Cultural", 
                                   "Party", "Pet_Friendly", "Adventurous", "Kid_Friendly", 
                                   "Romantic", "Wellness_Relaxation", "Senior_Citizen_Friendly"]:
                            formatted_data[field] = False
                        elif field in ["Price_Adult_INR", "Price_Child_INR"]:
                            formatted_data[field] = 0
                        else:
                            formatted_data[field] = "Not Available"
                
                return formatted_data
                
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

