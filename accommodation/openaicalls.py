import json
import requests
from typing import Dict, Any
import streamlit as st

def format_with_azure_openai(place_name: str, google_places_data: Dict[str, Any], perplexity_data: str) -> Dict[str, Any]:
    """
    Format the combined data using Azure OpenAI to create the final structured output
    
    Args:
        place_name: Original place name from user input
        google_places_data: Output from Google Places API
        perplexity_data: Raw response string from Perplexity
        
    Returns:
        Formatted dictionary with all 14 required fields or error
    """
    
    # Azure OpenAI configuration
    azure_endpoint = st.secrets["azure_openai"]["endpoint"]
    api_key = st.secrets["api_keys"]["azure_openai"]
    deployment_name = st.secrets["azure_openai"]["deployment_name"]
    api_version = st.secrets["azure_openai"]["api_version"]
    
    # Construct the formatting prompt
    prompt = f"""
You are a data formatting expert. Format the following travel data into a specific JSON structure.

USER INPUT:
Place Name: {place_name}

GOOGLE PLACES DATA:
{json.dumps(google_places_data, indent=2)}

PERPLEXITY RECOMMENDATION DATA:
{perplexity_data if perplexity_data else 'No data available'}

FORMATTING INSTRUCTIONS:
Create a JSON object with exactly these 14 fields:

1. Country: Extract from Google Places data/Perplexity data which is more accurate (Ex - India, USA, etc.)
2. State: Extract from Google Places data/Perplexity data which is more accurate (Ex - Karnataka, Maharashtra, etc.)
3. City: Extract from Google Places data/Perplexity data which is more accurate (Ex - Bengaluru, Mumbai, etc.)
4. Area: Extract from Google Places data/Perplexity data which is more accurate (Ex - Whitefield, Bandra, etc.)
5. Category: Extract from Perplexity data (must be one of: "Accomodation - Wellness", "Accomodation - Boutique / Villa / Homestay", "Accomodation - Haveli", "Accomodation - Hotel / Resorts")
6. Name: Use the original place name from user input
7. Description: Choose the best description between Google Places and Perplexity (prioritize the more detailed and informative one)
8. Pool: Convert to boolean true/false based on Perplexity analysis
9. Pet Friendly: Convert to boolean true/false based on Perplexity analysis
10. View: Convert to boolean true/false based on Perplexity analysis
11. Kid Friendly: Convert to boolean true/false based on Perplexity analysis
12. Romantic: Convert to boolean true/false based on Perplexity analysis
13. Senior Citizen Friendly: Convert to boolean true/false based on Perplexity analysis
14. Google Rating: Extract from Google Places data

IMPORTANT RULES:
- All boolean fields (8-13) must be exactly true or false (not "Yes"/"No" strings)
- If a field is missing or unclear, use appropriate defaults:
  - Text fields: "N/A"
  - Boolean fields: false
  - Numeric fields: "N/A"
- Category must match one of the 4 specified categories exactly
- Name should be the exact user input
- Choose the most informative description

Return ONLY the JSON object, no additional text.

Expected JSON structure:
{{
    "Country": "string",
    "Destination L1 (State)": "string",
    "Destination L2 (City)": "string",
    "Destination L3 (Area)": "string",
    "Category": "string",
    "Name": "string",
    "Description": "string",
    "Pool": "boolean",
    "Pet Friendly": "boolean",
    "View": "boolean",
    "Kid Friendly": "boolean",
    "Romantic": "boolean",
    "Senior Citizen Friendly": "boolean",
    "Google Rating": "string"
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
                
                # Validate the structure
                required_fields = [
                    "Country", "Destination L1 (State)", "Destination L2 (City)", 
                    "Destination L3 (Zone/ Area)", "Category", "Name", "Description",
                    "Pool", "Pet Friendly", "View", "Kid Friendly", "Romantic", 
                    "Senior Citizen Friendly", "Google Rating"
                ]
                
                # Ensure all required fields are present
                for field in required_fields:
                    if field not in formatted_data:
                        if field in ["Pool", "Pet Friendly", "View", "Kid Friendly", "Romantic", "Senior Citizen Friendly"]:
                            formatted_data[field] = False
                        else:
                            formatted_data[field] = "N/A"
                
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

