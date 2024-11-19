import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from recommender import PersonalizedTrailRecommender, format_user_recommendations

# Load data
TRAILS_FILE = 'data/trails_df.csv'  # Path to trails data CSV
SURVEY_FILE = 'data/survey_df.csv'  # Path to survey data CSV

# Initialize recommender
recommender = PersonalizedTrailRecommender()
trails_df = pd.read_csv(TRAILS_FILE)
recommender.preprocess_trails(trails_df)


def format(recommendations):
    """Format the recommendations into styled cards for display."""
    cards = []
    for _, trail in recommendations.iterrows():
        card_html = f"""
        <div style="
            border: 1px solid #e1e4e8;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            background-color: inherit;">
            <h3 style="margin: 5px 0;">🏃‍♂️ {trail['Trail_name']}</h3>
            <p style="margin: 5px 0;">📍 <strong>Location:</strong> {trail['Location']}</p>
            <p style="margin: 5px 0;">💪 <strong>Difficulty:</strong> {trail['Difficulty']}</p>
            <p style="margin: 5px 0;">📏 <strong>Length:</strong> {trail['Length']} km</p>
            <p style="margin: 5px 0;">⭐ <strong>Rating:</strong> {trail['Average_rating']}/5.0</p>
            <p style="margin: 5px 0;">🏷️ <strong>Features:</strong> {', '.join(trail['Tags'])}</p>
        </div>
        """
        cards.append(card_html)
    return "".join(cards)



st.set_page_config(page_title="HikeMatch", layout="wide")

# Title and Search Bar
# Title and Search Bar
# Title and Search Bar
st.markdown("<h1 style='text-align: center; font-size: 50px'>HikeMatch</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; font-size: 20px'>Matching You to the Best Trails, Every Step of the Way.</p>
""", unsafe_allow_html=True)

st.write("---")


# Survey Section in an expander
with st.expander("Take the Survey", expanded=False):
    with st.form("user_preferences_form"):
        
        home_environment = st.selectbox(
            "Where do you live?",
            ['A big city 🌆', 'A peaceful small town 🏡', 
             'A bustling suburb just outside the city 🏘', 
             'A rural area surrounded by nature 🌾', 
             'A mountain or hilly area 🏔', 
             'A coastal area by the beach 🌊']
        )
        
        weekend_preference = st.selectbox(
            "How do you prefer to spend your weekends?",
            ['Chilling with friends', 'Exploring new places', 
             'Watching movies or gaming', 
             'Going on adventures (like hiking)']
        )
        
        fitness_level = st.selectbox(
            "How would you describe your fitness level?",
            ['Couch potato 🛋', 'Average, but could be better 🚶', 
             'Pretty active 💪', 'Athlete level 🏃‍♀️']
        )
        
        hiking_experience = st.selectbox(
            "Have you ever been on a hike?",
            ['Yes, a few times', 'No, but I\'d like to try', 
             'Yes, and I hike regularly', 'Not my thing']
        )
        
        trail_length_preference = st.selectbox(
            "What length of trail do you prefer?",
            ['Short and sweet (under 5 km)', 
             'A nice challenge (5-10 km)', 
             'Long and tough (over 10 km)']
        )
        
        hiking_companion = st.selectbox(
            "Who do you prefer to hike with?",
            ['Alone for some peace and quiet', 
             'With friends or a group', 
             'Family trips', 'My pet 🐕']
        )
        
        perfect_trail_features = st.selectbox(
            "What makes a trail perfect for you?",
            ['Great scenery 🌄', 
             'Not too difficult, but enough exercise 💦', 
             'Close to a cool destination (like a waterfall or viewpoint) 💧', 
             'Good weather ☀️']
        )
        
        dream_destination = st.selectbox(
            "What’s your dream hiking destination?",
            ['A tropical island 🏝', 
             'A snowy mountain 🏔', 
             'A peaceful forest 🌳', 
             'Anywhere with breathtaking views!']
        )
        
        music_preference = st.selectbox(
            "What’s your hiking playlist vibe?",
            ['Chill acoustic tunes 🎸', 
             'Pumped-up workout beats 🎧', 
             'Nature sounds 🌿', 
             'No music, just the sound of nature 🐦']
        )
        
        weather_preference = st.selectbox(
            "If the weather’s not great, would you still go hiking?",
            ['No way, I\'ll reschedule 🛌', 
             'Maybe if it\'s just cloudy ☁️', 
             'Rain won\'t stop me! 🌧']
        )
        
        hiking_likelihood = st.slider(
            "On a scale of 1-5, how likely are you to go hiking in the next vacation?",
            min_value=1, max_value=5, value=3
        )
        
        # Submit button
        submitted = st.form_submit_button("Get Recommendations")

# Generate recommendations
if submitted:
    # Create user response dictionary
    user_response = {
        'home_environment': home_environment,
        'weekend_preference': weekend_preference,
        'fitness_level': fitness_level,
        'hiking_experience': hiking_experience,
        'trail_length_preference': trail_length_preference,
        'hiking_companion': hiking_companion,
        'perfect_trail_features': perfect_trail_features,
        'dream_destination': dream_destination,
        'music_preference': music_preference,
        'weather_preference': weather_preference,
        'hiking_likelihood': hiking_likelihood
    }

    # Get recommendations
    recommendations = recommender.get_recommendations(user_response, n_recommendations=3)
    
    # Display recommendations
    if not recommendations.empty:
        st.subheader("Here are your top trail recommendations:")
        st.markdown(format(recommendations), unsafe_allow_html=True)

    else:
        st.warning("No suitable trails found. Try adjusting your preferences.")

##################################################################################################
# Insights Section
st.write("## Hiking Trends and Preferences")

# Sample visualization - replace with real data insights
data = pd.DataFrame({
    "Preference": ["Others", "Views", "Wildflowers", "Wildlife", "Hiking", "Walking",
                   "Forest", "Bird watching", "Historic site", "Scramble", "Rocky",
                   "River", "Lake", "Backpacking", "Waterfall", "Camping"],
    "Popularity (%)": [20.7, 9.9, 8.2, 7.6, 7.5, 7.5, 6.7, 5.7, 4.4, 4.1, 3.9, 3.8, 
                       2.9, 2.5, 2.4, 2.3]
})

# Create a pie chart
fig = px.pie(data, names="Preference", values="Popularity (%)", title="Tourist Preferences for Activities")

# Display the chart in Streamlit
st.plotly_chart(fig)

difficulty_pref = pd.DataFrame({
    "Difficulty Level": ["Hard", "Moderate", "Easy"],
    "Count": [350, 340, 130]
})

# Create a pie chart
fig_diff = px.pie(difficulty_pref, names="Difficulty Level", values="Count", title="Distribution of Trail Difficulty")

# Display the chart in Streamlit
st.plotly_chart(fig_diff)



##################################################################################################
# About the Project Section
st.write("## About the Project")
st.markdown("""
This project aims to analyze tourist behavior to help identify hiking preferences and popular trails. 
By collecting data from tourists, we use machine learning to predict and recommend personalized hiking experiences.
If interested and want to contribute to this project, please reach out to us through <a href="https://github.com/InfernoAsura/HikeMatch/tree/main">Github</a>
""", unsafe_allow_html=True)

# Footer
st.write("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>© 2024 Tourist Behavior Analysis Project</p>", unsafe_allow_html=True)
