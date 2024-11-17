import pandas as pd
import MySQLdb

# MySQL Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "" #WRITE YOUR PASS
DB_NAME = "hiking_db"

# Connect to the MySQL Database
def get_db_connection():
    return MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)

# Load Data into MySQL
def load_data():
    trails_df = pd.read_csv("data/trails_df.csv")
    survey_df = pd.read_csv("data/survey_df.csv")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert Trails Data
    create_table_query1 = """
        CREATE TABLE IF NOT EXISTS trails (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trail_name VARCHAR(255) NOT NULL,
            link_alltrails TEXT,
            image TEXT,
            difficulty VARCHAR(50),
            average_rating FLOAT,
            number_of_reviews INT,
            location TEXT,
            length VARCHAR(50),
            description TEXT,
            tags TEXT,
            scaled_reviews FLOAT,
            scaled_rating FLOAT,
            combined_score FLOAT,
            difficulty_encoded INT
        );
    """
    create_table_query2 = """
        CREATE TABLE IF NOT EXISTS survey_responses (
            response_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            hometown VARCHAR(100),
            home_place VARCHAR(100),
            weekend_preference TEXT,
            fitness_level VARCHAR(50),
            hiking_experience VARCHAR(50),
            preferred_trail_types TEXT,
            hiking_group TEXT,
            trail_ideal_features TEXT,
            dream_destination TEXT,
            music_preference TEXT,
            bad_weather_hiking TEXT,
            vacation_hiking_likelihood INT
        );
    """
    cursor.execute(create_table_query1)
    cursor.execute(create_table_query2)

    for _, row in trails_df.iterrows():
        cursor.execute("""
            INSERT INTO trails (
                trail_name, link_alltrails, image, difficulty, average_rating,
                number_of_reviews, location, length, description, tags,
                scaled_reviews, scaled_rating, combined_score, difficulty_encoded
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Trail_name'], row['link_AllTrails'], row['image'], row['Difficulty'],
            row['Average_rating'], row['number_of_reviews'], row['Location'],
            row['Length'], row['description'], row['Tags'], row['scaled_reviews'],
            row['scaled_rating'], row['combined_score'], row['Difficulty_encoded']
        ))

    # Insert Survey Data
    for _, row in survey_df.iterrows():
        cursor.execute("""
            INSERT INTO survey_responses (
                name, hometown, home_place, weekend_preference,
                fitness_level, hiking_experience, preferred_trail_types, hiking_group,
                trail_ideal_features, dream_destination, music_preference,
                bad_weather_hiking, vacation_hiking_likelihood
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Your name'], row['Hometown'],
            row['Which best describes your home place?'],
            row['How do you prefer to spend your weekends?'],
            row['How would you describe your fitness level?'],
            row['Have you ever been on a hike ?'],
            row['What kind of hiking trail would you try (or have tried)? (Choose up to 3)'],
            row['Who would you go hiking with?'], row['What would make a hiking trail perfect for you?'],
            row['What’s your dream hiking destination?'], row['What’s your hiking playlist vibe?'],
            row['If the weather’s not great, would you still go hiking?'],
            row['On a scale of 1-5, how likely are you to go hiking in the next vacation?']
        ))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_data()