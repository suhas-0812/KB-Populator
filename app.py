import streamlit as st
from dining.dining_populator import populate_dining
from activities.activities_populator import populate_activities
from accommodation.accommodation_populator import populate_accommodation
import pandas as pd
# Configure page
st.set_page_config(
    page_title="Metadata Populator",
    page_icon="🗺️",
    layout="wide"
)


pages = st.sidebar.selectbox(
    "Navigate to:",
    options=["Activities", "Dining", "Accommodations"]
)

if pages == "Activities":
    st.header("Activities")
    
    # Add radio button for test type
    test_type = st.radio("Select Test Type", ["Single Test", "Batch Test"])
    
    if test_type == "Single Test":
        st.write("Enter Activity name and city to get metadata")
        col1, col2 = st.columns(2)
        with col1:
            activity_name = st.text_input("Activity")
        with col2:
            city = st.text_input("City")
        
        if st.button("Get Metadata"):
            with st.spinner("Getting metadata..."):
                data = populate_activities(activity_name, city)
                if data:
                    st.success("Metadata retrieved successfully!")
                    st.write("**Country:** ", data["Country"])
                    st.write("**Destination L1 (State):** ", data["Destination L1 (State)"])
                    st.write("**Destination L2 (City):** ", data["Destination L2 (City)"])
                    st.write("**Destination L3 (Area):** ", data["Destination L3 (Area)"])
                    st.write("**Name:** ", data["Name"])
                    st.write("**Description:** ", data["Description"])
                    st.write("**Price for Adults:** ", data["Price_Adult_INR"])
                    st.write("**Price for Children:** ", data["Price_Child_INR"])
                    st.write("**Duration:** ", data["Duration"])
                    st.write("**Timings:** ", data["Timings"])
                    st.write("**Season / Operational Months:** ", data["Season_Operational_Months"])
                    st.write("**Booleans**", {
                        "Must Do": data["Must_Do"],
                        "Group Friendly": data["Group_Friendly"],
                        "Offbeat": data["Offbeat"],
                        "Historic/Cultural": data["Historic_Cultural"],
                        "Party": data["Party"],
                        "Pet Friendly": data["Pet_Friendly"],
                        "Adventurous": data["Adventurous"],
                        "Kid Friendly": data["Kid_Friendly"],
                        "Romantic": data["Romantic"],
                        "Wellness/Relaxation": data["Wellness_Relaxation"],
                        "Senior Citizen Friendly": data["Senior_Citizen_Friendly"]
                    })
                    st.write("**Inclusions:** ", data["Inclusions"])
                    st.write("**Exclusions:** ", data["Exclusions"])
                    st.write("**Google Rating:** ", data["google_rating"])
                    st.write("**Website Link:** ", data["website"])
                    st.write("**Google Maps Link:** ", data["google_maps_url"])
                    st.write("**Photos:** ")
                    # First row of 5 photos
                    col1, col2, col3, col4, col5 = st.columns(5)
                    photos = [col1, col2, col3, col4, col5]
                    
                    for i, col in enumerate(photos):
                        if data["photo_urls"][i] != "N/A":
                            col.image(data["photo_urls"][i], width=150)
                        else:
                            col.write("N/A")
                    
                    # Second row of 5 photos
                    col6, col7, col8, col9, col10 = st.columns(5)
                    photos_row2 = [col6, col7, col8, col9, col10]
                    
                    for i, col in enumerate(photos_row2):
                        photo_index = i + 5  # Photos 5-9
                        if data["photo_urls"][photo_index] != "N/A":
                            col.image(data["photo_urls"][photo_index], width=150)
                        else:
                            col.write("N/A")
                    
                    # Prepare data for CSV download
                    csv_data = {
                        "Country": [data["Country"]],
                        "Destination L1 (State)": [data["Destination L1 (State)"]],
                        "Destination L2 (City)": [data["Destination L2 (City)"]],
                        "Destination L3 (Area)": [data["Destination L3 (Area)"]],
                        "Name": [data["Name"]],
                        "Description": [data["Description"]],
                        "Price for Adults": [data["Price_Adult_INR"]],
                        "Price for Children": [data["Price_Child_INR"]],
                        "Duration": [data["Duration"]],
                        "Timings": [data["Timings"]],
                        "Season / Operational Months": [data["Season_Operational_Months"]],
                        "Must Do": [data["Must_Do"]],
                        "Group Friendly": [data["Group_Friendly"]],
                        "Offbeat": [data["Offbeat"]],
                        "Historic/Cultural": [data["Historic_Cultural"]],
                        "Party": [data["Party"]],
                        "Pet Friendly": [data["Pet_Friendly"]],
                        "Adventurous": [data["Adventurous"]],
                        "Kid Friendly": [data["Kid_Friendly"]],
                        "Romantic": [data["Romantic"]],
                        "Wellness/Relaxation": [data["Wellness_Relaxation"]],
                        "Senior Citizen Friendly": [data["Senior_Citizen_Friendly"]],
                        "Inclusions": [data["Inclusions"]],
                        "Exclusions": [data["Exclusions"]],
                        "Google Rating": [data["google_rating"]],
                        "Website Link": [data["website"]],
                        "Google Maps Link": [data["google_maps_url"]],
                        "Photo 1": [data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else ""],
                        "Photo 2": [data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else ""],
                        "Photo 3": [data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else ""],
                        "Photo 4": [data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else ""],
                        "Photo 5": [data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else ""],
                        "Photo 6": [data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else ""],
                        "Photo 7": [data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else ""],
                        "Photo 8": [data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else ""],
                        "Photo 9": [data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else ""],
                        "Photo 10": [data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""]
                    }
                    
                    df = pd.DataFrame(csv_data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{activity_name}_{city}_metadata.csv",
                        mime="text/csv",
                        key="download_activity_csv"
                    )
                    
                else:
                    st.error("No metadata found for the given activity and city.")
    else:  # Batch Test
        st.write("Upload a CSV file with activities data (should contain 'activity name' and 'city' columns)")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="activities_upload")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'activity name' not in df.columns or 'city' not in df.columns:
                    st.error("CSV file must contain 'activity name' and 'city' columns")
                else:
                    if st.button("Process Activities"):
                        total_activities = len(df)
                        progress_text = "Operation in progress. Please wait."
                        my_bar = st.progress(0, text=progress_text)
                        
                        def process_activity(row):
                            # Get metadata
                            data = populate_activities(row["activity name"], row["city"])
                            
                            result = None
                            if data:
                                result = pd.Series({
                                    "Country": data["Country"],
                                    "Destination L1 (State)": data["Destination L1 (State)"],
                                    "Destination L2 (City)": data["Destination L2 (City)"],
                                    "Destination L3 (Area)": data["Destination L3 (Area)"],
                                    "Name": data["Name"],
                                    "Description": data["Description"],
                                    "Price for Adults": data["Price_Adult_INR"],
                                    "Price for Children": data["Price_Child_INR"],
                                    "Duration": data["Duration"],
                                    "Timings": data["Timings"],
                                    "Season / Operational Months": data["Season_Operational_Months"],
                                    "Must Do": data["Must_Do"],
                                    "Group Friendly": data["Group_Friendly"],
                                    "Offbeat": data["Offbeat"],
                                    "Historic/Cultural": data["Historic_Cultural"],
                                    "Party": data["Party"],
                                    "Pet Friendly": data["Pet_Friendly"],
                                    "Adventurous": data["Adventurous"],
                                    "Kid Friendly": data["Kid_Friendly"],
                                    "Romantic": data["Romantic"],
                                    "Wellness/Relaxation": data["Wellness_Relaxation"],
                                    "Senior Citizen Friendly": data["Senior_Citizen_Friendly"],
                                    "Inclusions": data["Inclusions"],
                                    "Exclusions": data["Exclusions"],
                                    "Google Rating": data["google_rating"],
                                    "Website Link": data["website"],
                                    "Google Maps Link": data["google_maps_url"],
                                    "Photo 1": data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else "",
                                    "Photo 2": data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else "",
                                    "Photo 3": data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else "",
                                    "Photo 4": data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else "",
                                    "Photo 5": data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else "",
                                    "Photo 6": data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else "",
                                    "Photo 7": data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else "",
                                    "Photo 8": data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else "",
                                    "Photo 9": data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else "",
                                    "Photo 10": data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""
                                })
                            else:
                                # Return empty data if no metadata found
                                empty_data = {col: "" for col in df.columns}
                                empty_data["activity name"] = row["activity name"]
                                empty_data["city"] = row["city"]
                                result = pd.Series(empty_data)
                            
                            # Update progress after processing is complete
                            current_count = int(row.name) + 1
                            my_bar.progress(current_count/total_activities, 
                                          text=f"Completed {current_count}/{total_activities}: {row['activity name']}, {row['city']}")
                            
                            return result
                        
                        # Process all activities using apply
                        final_df = df.apply(process_activity, axis=1)
                        
                        # Convert to CSV
                        csv = final_df.to_csv(index=False)
                        
                        # Update progress bar to completion
                        my_bar.progress(1.0, text="Processing complete!")
                        
                        # Offer download
                        st.download_button(
                            label="Download Results CSV",
                            data=csv,
                            file_name="activities_metadata_results.csv",
                            mime="text/csv",
                            key="download_batch_activities_csv"
                        )
                        
                        st.success("Processing complete! You can now download the results.")
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

if pages == "Dining":
    st.header("Dining")
    
    # Add radio button for test type
    test_type = st.radio("Select Test Type", ["Single Test", "Batch Test"])
    
    if test_type == "Single Test":
        st.write("Enter restaurant name and city to get metadata")
        col1, col2 = st.columns(2)
        with col1:
            restaurant_name = st.text_input("Restaurant name")
        with col2:
            city = st.text_input("City")

        if st.button("Get Metadata"):
            with st.spinner("Getting metadata..."):
                data = populate_dining(restaurant_name, city)
                if data:
                    st.success("Metadata retrieved successfully!")
                    st.write("**Country:** ", data["Country"])
                    st.write("**Destination L1 (State):** ", data["Destination L1 (State)"])
                    st.write("**Destination L2 (City):** ", data["Destination L2 (City)"])
                    st.write("**Destination L3 (Area):** ", data["Destination L3 (Area)"])
                    st.write("**Name:** ", data["Name"])
                    st.write("**Description:** ", data["Description"])
                    st.write("**Recommended Dishes:** ", data["Recommended_Dishes"])
                    st.write("**Meals Served:** ", data["Meals_Served"])
                    st.write("**Timings:** ", data["opening_hours"])
                    st.write("**Can we have Private Dining?:** ", data["Private_Dining"])
                    st.write("**Can I host a Party?:** ", data["Party"])
                    st.write("**Service Style:** ", data["Service_Style"])
                    st.write("**Cuisine:** ", data["Cuisine"])
                    st.write("**Dietary:** ", data["Dietary"])
                    st.write("**Guest Persona:** ", data["Guest_Persona"])
                    st.write("**Vibe:** ", data["Vibe"])
                    st.write("**Google Rating:** ", data["google_rating"])
                    st.write("**Website Link:** ", data["website"])
                    st.write("**Google Maps Link:** ", data["google_maps_url"])
                    st.write("**Photos:** ")
                    # First row of 5 photos
                    col1, col2, col3, col4, col5 = st.columns(5)
                    photos = [col1, col2, col3, col4, col5]
                    
                    for i, col in enumerate(photos):
                        if data["photo_urls"][i] != "N/A":
                            col.image(data["photo_urls"][i], width=150)
                        else:
                            col.write("N/A")
                    
                    # Second row of 5 photos
                    col6, col7, col8, col9, col10 = st.columns(5)
                    photos_row2 = [col6, col7, col8, col9, col10]
                    
                    for i, col in enumerate(photos_row2):
                        photo_index = i + 5  # Photos 5-9
                        if data["photo_urls"][photo_index] != "N/A":
                            col.image(data["photo_urls"][photo_index], width=150)
                        else:
                            col.write("N/A")
                    
                    # Prepare data for CSV download
                    csv_data = {
                        "Country": [data["Country"]],
                        "Destination L1 (State)": [data["Destination L1 (State)"]],
                        "Destination L2 (City)": [data["Destination L2 (City)"]],
                        "Destination L3 (Area)": [data["Destination L3 (Area)"]],
                        "Name": [data["Name"]],
                        "Description": [data["Description"]],
                        "Recommended Dishes": [data["Recommended_Dishes"]],
                        "Meals Served": [data["Meals_Served"]],
                        "Timings": [data["opening_hours"]],
                        "Can we have Private Dining?": [data["Private_Dining"]],
                        "Can I host a Party?": [data["Party"]],
                        # Service Style fields as separate columns
                        "Michelin Star": [data["Service_Style"].get("Michelin_Star", False)],
                        "Fine Dining": [data["Service_Style"].get("Fine_Dining", False)],
                        "Casual Dining": [data["Service_Style"].get("Casual_Dining", False)],
                        "Bistro": [data["Service_Style"].get("Bistro", False)],
                        "Cafe": [data["Service_Style"].get("Cafe", False)],
                        "Bakery": [data["Service_Style"].get("Bakery", False)],
                        "Breweries": [data["Service_Style"].get("Breweries", False)],
                        "Farm to Table": [data["Service_Style"].get("Farm_to_Table", False)],
                        "Cocktail Bars": [data["Service_Style"].get("Cocktail_Bars", False)],
                        "Speakeasys": [data["Service_Style"].get("Speakeasys", False)],
                        "Tapas Bar": [data["Service_Style"].get("Tapas_Bar", False)],
                        "Rooftop Bar": [data["Service_Style"].get("Rooftop_Bar", False)],
                        "Dessert Spot": [data["Service_Style"].get("Dessert_Spot", False)],
                        # Cuisine fields as separate columns
                        "Fast Food": [data["Cuisine"].get("Fast_Food", False)],
                        "Modern Indian": [data["Cuisine"].get("Modern_Indian", False)],
                        "Indian": [data["Cuisine"].get("Indian", False)],
                        "Continental": [data["Cuisine"].get("Continental", False)],
                        "Finger Food": [data["Cuisine"].get("Finger_Food", False)],
                        "Burmese": [data["Cuisine"].get("Burmese", False)],
                        "Peruvian": [data["Cuisine"].get("Peruvian", False)],
                        "Lebanese": [data["Cuisine"].get("Lebanese", False)],
                        "Afghan": [data["Cuisine"].get("Afghan", False)],
                        "Malaysian": [data["Cuisine"].get("Malaysian", False)],
                        "Vietnamese": [data["Cuisine"].get("Vietnamese", False)],
                        "Pan Asian": [data["Cuisine"].get("Pan_Asian", False)],
                        "Mediterranean": [data["Cuisine"].get("Mediterranean", False)],
                        "Thai": [data["Cuisine"].get("Thai", False)],
                        "Italian": [data["Cuisine"].get("Italian", False)],
                        "Japanese": [data["Cuisine"].get("Japanese", False)],
                        "Mexican": [data["Cuisine"].get("Mexican", False)],
                        "Modern European": [data["Cuisine"].get("Modern_European", False)],
                        "Contemporary Dining": [data["Cuisine"].get("Contemporary_Dining", False)],
                        "Molecular Gastronomy": [data["Cuisine"].get("Molecular_Gastronomy", False)],
                        # Dietary fields as separate columns
                        "Vegetarian + Non Vegetarian": [data["Dietary"].get("Vegetarian_Non_Vegetarian", False)],
                        "Vegetarian": [data["Dietary"].get("Vegetarian", False)],
                        "Vegan Options": [data["Dietary"].get("Vegan_Options", False)],
                        "Seafood Speciality": [data["Dietary"].get("Seafood_Speciality", False)],
                        # Guest Persona fields as separate columns
                        "Couple Friendly": [data["Guest_Persona"].get("Couple_Friendly", False)],
                        "Family Friendly": [data["Guest_Persona"].get("Family_Friendly", False)],
                        "Especially For Kids": [data["Guest_Persona"].get("Especially_For_Kids", False)],
                        "No Kids Allowed": [data["Guest_Persona"].get("No_Kids_Allowed", False)],
                        "Senior Friendly": [data["Guest_Persona"].get("Senior_Friendly", False)],
                        "Pet Friendly": [data["Guest_Persona"].get("Pet_Friendly", False)],
                        # Vibe fields as separate columns
                        "Romantic / Intimate": [data["Vibe"].get("Romantic_Intimate", False)],
                        "Refined / Elegant": [data["Vibe"].get("Refined_Elegant", False)],
                        "Luxurious / Formal": [data["Vibe"].get("Luxurious_Formal", False)],
                        "Bohemian / Playful": [data["Vibe"].get("Bohemian_Playful", False)],
                        "Modern / Chic": [data["Vibe"].get("Modern_Chic", False)],
                        "Vibrant / Lively": [data["Vibe"].get("Vibrant_Lively", False)],
                        "Relaxed / Cozy": [data["Vibe"].get("Relaxed_Cozy", False)],
                        "Reservation Recommended": [data["Reservation_Recommended"]],
                        "Alcohol Served?": [data["Alcohol_Served"]],
                        "Google Rating": [data["google_rating"]],
                        "Website Link": [data["website"]],
                        "Google Maps Link": [data["google_maps_url"]],
                        "Photo 1": [data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else ""],
                        "Photo 2": [data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else ""],
                        "Photo 3": [data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else ""],
                        "Photo 4": [data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else ""],
                        "Photo 5": [data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else ""],
                        "Photo 6": [data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else ""],
                        "Photo 7": [data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else ""],
                        "Photo 8": [data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else ""],
                        "Photo 9": [data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else ""],
                        "Photo 10": [data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""]
                    }
                    
                    df = pd.DataFrame(csv_data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{restaurant_name}_{city}_metadata.csv",
                        mime="text/csv",
                        key="download_dining_csv"
                    )
                    
                else:
                    st.error("No metadata found for the given restaurant and city.")
    else:  # Batch Test
        st.write("Upload a CSV file with dining data (should contain 'restaurant name' and 'city' columns)")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="dining_upload")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'restaurant name' not in df.columns or 'city' not in df.columns:
                    st.error("CSV file must contain 'restaurant name' and 'city' columns")
                else:
                    if st.button("Process Restaurants"):
                        total_restaurants = len(df)
                        progress_text = "Operation in progress. Please wait."
                        my_bar = st.progress(0, text=progress_text)
                        
                        def process_restaurant(row):
                            # Get metadata
                            data = populate_dining(row["restaurant name"], row["city"])
                            
                            result = None
                            if data:
                                result = pd.Series({
                                    "Country": data["Country"],
                                    "Destination L1 (State)": data["Destination L1 (State)"],
                                    "Destination L2 (City)": data["Destination L2 (City)"],
                                    "Destination L3 (Area)": data["Destination L3 (Area)"],
                                    "Name": data["Name"],
                                    "Description": data["Description"],
                                    "Recommended Dishes": data["Recommended_Dishes"],
                                    "Meals Served": data["Meals_Served"],
                                    "Timings": data["opening_hours"],
                                    "Can we have Private Dining?": data["Private_Dining"],
                                    "Can I host a Party?": data["Party"],
                                    # Service Style fields
                                    "Michelin Star": data["Service_Style"].get("Michelin_Star", False),
                                    "Fine Dining": data["Service_Style"].get("Fine_Dining", False),
                                    "Casual Dining": data["Service_Style"].get("Casual_Dining", False),
                                    "Bistro": data["Service_Style"].get("Bistro", False),
                                    "Cafe": data["Service_Style"].get("Cafe", False),
                                    "Bakery": data["Service_Style"].get("Bakery", False),
                                    "Breweries": data["Service_Style"].get("Breweries", False),
                                    "Farm to Table": data["Service_Style"].get("Farm_to_Table", False),
                                    "Cocktail Bars": data["Service_Style"].get("Cocktail_Bars", False),
                                    "Speakeasys": data["Service_Style"].get("Speakeasys", False),
                                    "Tapas Bar": data["Service_Style"].get("Tapas_Bar", False),
                                    "Rooftop Bar": data["Service_Style"].get("Rooftop_Bar", False),
                                    "Dessert Spot": data["Service_Style"].get("Dessert_Spot", False),
                                    # Cuisine fields
                                    "Fast Food": data["Cuisine"].get("Fast_Food", False),
                                    "Modern Indian": data["Cuisine"].get("Modern_Indian", False),
                                    "Indian": data["Cuisine"].get("Indian", False),
                                    "Continental": data["Cuisine"].get("Continental", False),
                                    "Finger Food": data["Cuisine"].get("Finger_Food", False),
                                    "Burmese": data["Cuisine"].get("Burmese", False),
                                    "Peruvian": data["Cuisine"].get("Peruvian", False),
                                    "Lebanese": data["Cuisine"].get("Lebanese", False),
                                    "Afghan": data["Cuisine"].get("Afghan", False),
                                    "Malaysian": data["Cuisine"].get("Malaysian", False),
                                    "Vietnamese": data["Cuisine"].get("Vietnamese", False),
                                    "Pan Asian": data["Cuisine"].get("Pan_Asian", False),
                                    "Mediterranean": data["Cuisine"].get("Mediterranean", False),
                                    "Thai": data["Cuisine"].get("Thai", False),
                                    "Italian": data["Cuisine"].get("Italian", False),
                                    "Japanese": data["Cuisine"].get("Japanese", False),
                                    "Mexican": data["Cuisine"].get("Mexican", False),
                                    "Modern European": data["Cuisine"].get("Modern_European", False),
                                    "Contemporary Dining": data["Cuisine"].get("Contemporary_Dining", False),
                                    "Molecular Gastronomy": data["Cuisine"].get("Molecular_Gastronomy", False),
                                    # Dietary fields
                                    "Vegetarian + Non Vegetarian": data["Dietary"].get("Vegetarian_Non_Vegetarian", False),
                                    "Vegetarian": data["Dietary"].get("Vegetarian", False),
                                    "Vegan Options": data["Dietary"].get("Vegan_Options", False),
                                    "Seafood Speciality": data["Dietary"].get("Seafood_Speciality", False),
                                    # Guest Persona fields
                                    "Couple Friendly": data["Guest_Persona"].get("Couple_Friendly", False),
                                    "Family Friendly": data["Guest_Persona"].get("Family_Friendly", False),
                                    "Especially For Kids": data["Guest_Persona"].get("Especially_For_Kids", False),
                                    "No Kids Allowed": data["Guest_Persona"].get("No_Kids_Allowed", False),
                                    "Senior Friendly": data["Guest_Persona"].get("Senior_Friendly", False),
                                    "Pet Friendly": data["Guest_Persona"].get("Pet_Friendly", False),
                                    # Vibe fields
                                    "Romantic / Intimate": data["Vibe"].get("Romantic_Intimate", False),
                                    "Refined / Elegant": data["Vibe"].get("Refined_Elegant", False),
                                    "Luxurious / Formal": data["Vibe"].get("Luxurious_Formal", False),
                                    "Bohemian / Playful": data["Vibe"].get("Bohemian_Playful", False),
                                    "Modern / Chic": data["Vibe"].get("Modern_Chic", False),
                                    "Vibrant / Lively": data["Vibe"].get("Vibrant_Lively", False),
                                    "Relaxed / Cozy": data["Vibe"].get("Relaxed_Cozy", False),
                                    # Additional fields
                                    "Reservation Recommended": data["Reservation_Recommended"],
                                    "Alcohol Served?": data["Alcohol_Served"],
                                    "Google Rating": data["google_rating"],
                                    "Website Link": data["website"],
                                    "Google Maps Link": data["google_maps_url"],
                                    "Photo 1": data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else "",
                                    "Photo 2": data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else "",
                                    "Photo 3": data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else "",
                                    "Photo 4": data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else "",
                                    "Photo 5": data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else "",
                                    "Photo 6": data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else "",
                                    "Photo 7": data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else "",
                                    "Photo 8": data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else "",
                                    "Photo 9": data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else "",
                                    "Photo 10": data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""
                                })
                            else:
                                # Return empty data if no metadata found
                                empty_data = {col: "" for col in df.columns}
                                empty_data["restaurant name"] = row["restaurant name"]
                                empty_data["city"] = row["city"]
                                result = pd.Series(empty_data)
                            
                            # Update progress after processing is complete
                            current_count = int(row.name) + 1
                            my_bar.progress(current_count/total_restaurants, 
                                          text=f"Completed {current_count}/{total_restaurants}: {row['restaurant name']}, {row['city']}")
                            
                            return result
                        
                        # Process all restaurants using apply
                        final_df = df.apply(process_restaurant, axis=1)
                        
                        # Convert to CSV
                        csv = final_df.to_csv(index=False)
                        
                        # Update progress bar to completion
                        my_bar.progress(1.0, text="Processing complete!")
                        
                        # Offer download
                        st.download_button(
                            label="Download Results CSV",
                            data=csv,
                            file_name="dining_metadata_results.csv",
                            mime="text/csv",
                            key="download_batch_dining_csv"
                        )
                        
                        st.success("Processing complete! You can now download the results.")
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

if pages == "Accommodations":
    st.header("Accommodations")
    
    # Add radio button for test type
    test_type = st.radio("Select Test Type", ["Single Test", "Batch Test"])
    
    if test_type == "Single Test":
        st.write("Enter Accommodation name and city to get metadata")
        col1, col2 = st.columns(2)
        with col1:
            accommodation_name = st.text_input("Accommodation")
        with col2:
            city = st.text_input("City")
            
        if st.button("Get Metadata"):
            with st.spinner("Getting metadata..."):
                data = populate_accommodation(accommodation_name, city)
                if data:
                    st.success("Metadata retrieved successfully!")
                    
                    st.write("**Country:** ", data["Country"])
                    st.write("**Destination L1 (State):** ", data["Destination L1 (State)"])
                    st.write("**Destination L2 (City):** ", data["Destination L2 (City)"])
                    st.write("**Destination L3 (Area):** ", data["Destination L3 (Area)"])
                    st.write("**Category:** ", data["Category"])
                    st.write("**Name:** ", data["Name"])
                    st.write("**Description:** ", data["Description"])
                    st.write("**Booleans**", {
                        "Pool": data["Pool"],
                        "View": data["View"],
                        "Pet Friendly": data["Pet Friendly"],
                        "Kid Friendly": data["Kid Friendly"],
                        "Senior Citizen Friendly": data["Senior Citizen Friendly"],
                        "Romantic": data["Romantic"],
                        
                    })
                    st.write("**Google Rating:** ", data["Google Rating"])
                    st.write("**Website Link:** ", data["website"])
                    st.write("**Google Maps Link:** ", data["google_maps_url"])
                    st.write("**Photos:** ")
                    # First row of 5 photos
                    col1, col2, col3, col4, col5 = st.columns(5)
                    photos = [col1, col2, col3, col4, col5]
                    
                    for i, col in enumerate(photos):
                        if data["photo_urls"][i] != "N/A":
                            col.image(data["photo_urls"][i], width=150)
                        else:
                            col.write("N/A")
                    
                    # Second row of 5 photos
                    col6, col7, col8, col9, col10 = st.columns(5)
                    photos_row2 = [col6, col7, col8, col9, col10]
                    
                    for i, col in enumerate(photos_row2):
                        photo_index = i + 5  # Photos 5-9
                        if data["photo_urls"][photo_index] != "N/A":
                            col.image(data["photo_urls"][photo_index], width=150)
                        else:
                            col.write("N/A")
                    
                    # Prepare data for CSV download
                    csv_data = {
                        "Country": [data["Country"]],
                        "Destination L1 (State)": [data["Destination L1 (State)"]],
                        "Destination L2 (City)": [data["Destination L2 (City)"]],
                        "Destination L3 (Area)": [data["Destination L3 (Area)"]],
                        "Category": [data["Category"]],
                        "Name": [data["Name"]],
                        "Description": [data["Description"]],
                        "Pool": [data["Pool"]],
                        "View": [data["View"]],
                        "Pet Friendly": [data["Pet Friendly"]],
                        "Kid Friendly": [data["Kid Friendly"]],
                        "Senior Citizen Friendly": [data["Senior Citizen Friendly"]],
                        "Romantic": [data["Romantic"]],
                        "Google Rating": [data["Google Rating"]],
                        "Website Link": [data["website"]],
                        "Google Maps Link": [data["google_maps_url"]],
                        "Photo 1": [data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else ""],
                        "Photo 2": [data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else ""],
                        "Photo 3": [data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else ""],
                        "Photo 4": [data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else ""],
                        "Photo 5": [data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else ""],
                        "Photo 6": [data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else ""],
                        "Photo 7": [data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else ""],
                        "Photo 8": [data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else ""],
                        "Photo 9": [data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else ""],
                        "Photo 10": [data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""]
                    }
                    
                    df = pd.DataFrame(csv_data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{accommodation_name}_{city}_metadata.csv",
                        mime="text/csv",
                        key="download_accommodation_csv"
                    )
                    
                else:
                    st.error("No metadata found for the given accommodation and city.")
    else:  # Batch Test
        st.write("Upload a CSV file with accommodation data (should contain 'accommodation name' and 'city' columns)")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="accommodation_upload")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'accommodation name' not in df.columns or 'city' not in df.columns:
                    st.error("CSV file must contain 'accommodation name' and 'city' columns")
                else:
                    if st.button("Process Accommodations"):
                        total_accommodations = len(df)
                        progress_text = "Operation in progress. Please wait."
                        my_bar = st.progress(0, text=progress_text)
                        
                        def process_accommodation(row):
                            # Get metadata
                            data = populate_accommodation(row["accommodation name"], row["city"])
                            
                            result = None
                            if data:
                                result = pd.Series({
                                    "Country": data["Country"],
                                    "Destination L1 (State)": data["Destination L1 (State)"],
                                    "Destination L2 (City)": data["Destination L2 (City)"],
                                    "Destination L3 (Area)": data["Destination L3 (Area)"],
                                    "Category": data["Category"],
                                    "Name": data["Name"],
                                    "Description": data["Description"],
                                    "Pool": data["Pool"],
                                    "View": data["View"],
                                    "Pet Friendly": data["Pet Friendly"],
                                    "Kid Friendly": data["Kid Friendly"],
                                    "Senior Citizen Friendly": data["Senior Citizen Friendly"],
                                    "Romantic": data["Romantic"],
                                    "Google Rating": data["Google Rating"],
                                    "Website Link": data["website"],
                                    "Google Maps Link": data["google_maps_url"],
                                    "Photo 1": data["photo_urls"][0] if data["photo_urls"][0] != "N/A" else "",
                                    "Photo 2": data["photo_urls"][1] if data["photo_urls"][1] != "N/A" else "",
                                    "Photo 3": data["photo_urls"][2] if data["photo_urls"][2] != "N/A" else "",
                                    "Photo 4": data["photo_urls"][3] if data["photo_urls"][3] != "N/A" else "",
                                    "Photo 5": data["photo_urls"][4] if data["photo_urls"][4] != "N/A" else "",
                                    "Photo 6": data["photo_urls"][5] if data["photo_urls"][5] != "N/A" else "",
                                    "Photo 7": data["photo_urls"][6] if data["photo_urls"][6] != "N/A" else "",
                                    "Photo 8": data["photo_urls"][7] if data["photo_urls"][7] != "N/A" else "",
                                    "Photo 9": data["photo_urls"][8] if data["photo_urls"][8] != "N/A" else "",
                                    "Photo 10": data["photo_urls"][9] if data["photo_urls"][9] != "N/A" else ""
                                })
                            else:
                                # Return empty data if no metadata found
                                empty_data = {col: "" for col in df.columns}
                                empty_data["accommodation name"] = row["accommodation name"]
                                empty_data["city"] = row["city"]
                                result = pd.Series(empty_data)
                            
                            # Update progress after processing is complete
                            current_count = int(row.name) + 1
                            my_bar.progress(current_count/total_accommodations, 
                                          text=f"Completed {current_count}/{total_accommodations}: {row['accommodation name']}, {row['city']}")
                            
                            return result
                        
                        # Process all accommodations using apply
                        final_df = df.apply(process_accommodation, axis=1)
                        
                        # Convert to CSV
                        csv = final_df.to_csv(index=False)
                        
                        # Update progress bar to completion
                        my_bar.progress(1.0, text="Processing complete!")
                        
                        # Offer download
                        st.download_button(
                            label="Download Results CSV",
                            data=csv,
                            file_name="accommodation_metadata_results.csv",
                            mime="text/csv",
                            key="download_batch_accommodation_csv"
                        )
                        
                        st.success("Processing complete! You can now download the results.")
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")