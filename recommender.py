
import pandas as pd
import numpy as np

df = pd.read_csv('data/trails_df.csv')

class PersonalizedTrailRecommender:
    def __init__(self):
        self.trails_df = None

    def preprocess_trails(self, trails_data):
        """Preprocess trail data to clean and structure it."""
        self.trails_df = pd.DataFrame(trails_data)
        self.trails_df['Tags'] = self.trails_df['Tags'].str.split(', ')
        # Extract numeric part of length and convert to float
        self.trails_df['Length'] = self.trails_df['Length'].str.extract(r'([\d.]+)').astype(float)

    def process_user_preferences(self, user_response):
        """Convert user preferences into feature vectors and tags."""
        features = {}
        preferred_tags = []

        # Mappings for user preferences to tags and features
        mappings = {
            'home_environment': {
                'A big city 🌆': ['Urban', 'Accessible'],
                'A peaceful small town 🏡': ['Accessible', 'Quiet'],
                'A bustling suburb just outside the city 🏘': ['Urban', 'Accessible'],
                'A rural area surrounded by nature 🌾': ['Nature', 'Rural'],
                'A mountain or hilly area 🏔': ['Mountain', 'Elevation'],
                'A coastal area by the beach 🌊': ['Coastal', 'Beach'],
            },
            'weekend_preference': {
                'Chilling with friends': ['Social', 'Easy'],
                'Exploring new places': ['Adventure', 'Scenic'],
                'Watching movies or gaming': ['Easy', 'Beginner'],
                'Going on adventures (like hiking)': ['Adventure', 'Challenge'],
            },
            'trail_length_preference': {
                'Short and sweet (under 5 km)': ['Short', 'Easy'],
                'A nice challenge (5-10 km)': ['Medium', 'Moderate'],
                'Long and tough (over 10 km)': ['Long', 'Hard'],
            },
            'hiking_companion': {
                'Alone for some peace and quiet': ['Solo', 'Quiet'],
                'With friends or a group': ['Group', 'Social'],
                'Family trips': ['Family', 'Easy'],
                'My pet 🐕': ['Pet-friendly', 'Accessible'],
            },
            'perfect_trail_features': {
                'Great scenery 🌄': ['Scenic', 'Views'],
                'Not too difficult, but enough exercise 💦': ['Moderate', 'Exercise'],
                'Close to a cool destination (like a waterfall or viewpoint) 💧': ['Destination', 'Feature'],
                'Good weather ☀️': ['Fair_weather'],
            },
            'dream_destination': {
                'A tropical island 🏝': ['Tropical', 'Coastal'],
                'A snowy mountain 🏔': ['Mountain', 'Snow'],
                'A peaceful forest 🌳': ['Forest', 'Peaceful'],
                'Anywhere with breathtaking views!': ['Scenic', 'Views'],
            },
            'music_preference': {
                'Chill acoustic tunes 🎸': ['Moderate', 'Peaceful'],
                'Pumped-up workout beats 🎧': ['Hard', 'Challenge'],
                'Nature sounds 🌿': ['Nature', 'Quiet'],
                'No music, just the sound of nature 🐦': ['Nature', 'Peaceful'],
            }
        }

        # Feature mappings for numeric values
        fitness_map = {'Couch potato 🛋': 0.2, 'Average, but could be better 🚶': 0.5, 'Pretty active 💪': 0.8, 'Athlete level 🏃‍♀️': 1.0}
        weather_map = {'No way, I\'ll reschedule 🛌': 0.2, 'Maybe if it\'s just cloudy ☁️': 0.5, 'Rain won\'t stop me! 🌧': 1.0}
        experience_map = {'Yes, a few times': 0.6, 'No, but I\'d like to try': 0.3, 'Yes, and I hike regularly': 1.0, 'Not my thing': 0.1}

        # Extract numeric features
        features['fitness_level'] = fitness_map.get(user_response.get('fitness_level', 'Average, but could be better 🚶'), 0.5)
        features['weather_tolerance'] = weather_map.get(user_response.get('weather_preference', 'Maybe if it\'s just cloudy ☁️'), 0.5)
        features['experience'] = experience_map.get(user_response.get('hiking_experience', 'No, but I\'d like to try'), 0.3)
        features['hiking_likelihood'] = int(user_response.get('hiking_likelihood', 3)) / 5.0

        # Collect preferred tags from mappings
        for category, tag_mapping in mappings.items():
            user_choice = user_response.get(category)
            if isinstance(user_choice, list):
                for choice in user_choice:
                    preferred_tags.extend(tag_mapping.get(choice, []))
            elif user_choice in tag_mapping:
                preferred_tags.extend(tag_mapping[user_choice])

        return features, list(set(preferred_tags))

    def get_recommendations(self, user_response, n_recommendations=3):
        """Get personalized trail recommendations based on user preferences."""
        features, preferred_tags = self.process_user_preferences(user_response)

        # Calculate trail scores
        scores = []
        for _, trail in self.trails_df.iterrows():
            score = 0

            # Match difficulty with fitness and experience
            difficulty_score = (features['fitness_level'] + features['experience']) / 2
            if trail['Difficulty'] == 'Hard':
                score += difficulty_score * 2 if difficulty_score > 0.6 else difficulty_score * 0.5
            elif trail['Difficulty'] == 'Moderate':
                score += difficulty_score * 1.5
            else:
                score += (1 - difficulty_score) * 1.5

            # Tag matching
            trail_tags = set(trail['Tags'])
            tag_match = len(trail_tags.intersection(preferred_tags)) / max(len(preferred_tags), 1)
            score += tag_match * 3

            # Length adjustment
            trail_length = trail['Length']
            if trail_length <= 5:
                score *= 1.2 if 'Short' in preferred_tags else 0.9
            elif trail_length <= 10:
                score *= 1.2 if 'Medium' in preferred_tags else 0.9
            else:
                score *= 1.2 if 'Long' in preferred_tags else 0.8

            # Weather adjustment
            if 'all_weather' in trail_tags:
                score *= (1 + features['weather_tolerance'])
            elif 'fair_weather' in trail_tags and features['weather_tolerance'] < 0.5:
                score *= 1.1

            # Hiking likelihood impact
            score *= (0.5 + features['hiking_likelihood'])
            scores.append(score)

        # Get top recommendations
        recommendations_idx = np.argsort(scores)[::-1][:n_recommendations]
        recommendations = self.trails_df.iloc[recommendations_idx].copy()
        recommendations['Match_Score'] = [scores[i] for i in recommendations_idx]

        return recommendations


def format_user_recommendations(recommendations):
    """Format the recommendations for display."""
    output = []
    for _, trail in recommendations.iterrows():
        output.append(
            f"🏃‍♂️ {trail['Trail_name']}\n"
            f"📍 Location: {trail['Location']}\n"
            f"💪 Difficulty: {trail['Difficulty']}\n"
            f"📏 Length: {trail['Length']} km\n"
            f"⭐ Rating: {trail['Average_rating']}/5.0\n"
            f"🎯 Match Score: {trail['Match_Score']:.2f}\n"
            f"🏷️ Features: {', '.join(trail['Tags'])}\n"
        )
    return "\n".join(output)