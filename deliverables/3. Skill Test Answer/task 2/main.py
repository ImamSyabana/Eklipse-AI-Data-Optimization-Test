import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from dotenv import find_dotenv, load_dotenv
import sys
import time

# search  .env file location automaticaly 
dotenv_path = find_dotenv()

# load the entries as environtment variables
load_dotenv(dotenv_path)

def setup_api():
    """
    Sets up the Google AI Studio API using a key from environment variables.
    
    Returns:
        A configured generative model object or None if the key is not found.
    """
    try:
        # stored the env variables within a python variable
        API_KEY = os.getenv("Eklipse_genai")
        if API_KEY == "None":
            print("Error: GOOGLE_API_KEY environment variable not found.")
            return None
        
        # Configure the library with Google AI Studio API key
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        return model
    except Exception as msg:
        print(f"An error occurred during API setup: {msg}")
        return None


def get_ai_response(model, prompt, safety_settings):
    """
    Calls the Gemini API with a specific prompt and handles potential errors. [cite: 48]
    
    Args:
        model: The configured generative model object.
        prompt (str): The prompt to send to the AI.
        
    Returns:
        The text response from the AI or a default error message.
    """
    try:
        # make a request using prompt to the model and save the response in the variable
        # the safety _setting is used to make sure the model give a response even if the game title
        # contains a word that triggered the safety filter. 
        response = model.generate_content(prompt, safety_settings=safety_settings)

        
        # NEW CHECK: Before trying to access .text, check if the response was blocked.
        if response.parts:
            # Clean up the response text by removing potential markdown or extra spaces.
            return response.text.strip().replace("*", "")
        else:
            # This part now executes if the response was empty (blocked)
            print("  [!] Response was blocked by safety filters.")
            return "Blocked by safety filter"
        
    except Exception as msg:
        print(f"  [!] An error occurred while calling the API: {msg}")
        return "Error generating response"
    
#################### MAIN SCRIPT CODE #############################
# 1. Setup the Gemini API
model = setup_api()
if not model:
    print("Process aborted due to API setup failure.")
    # break from the rest of the program and stop the process
    sys.exit()
    
# 2. Load the CSV file into a pandas DataFrame [cite: 34]
try:
    df = pd.read_csv("task 2/Game Thumbnail.csv")
except FileNotFoundError:
    print("Error: 'Game Thumbnail.csv' not found. Make sure the file is in the same directory.")
    # break from the rest of the program and stop the process
    sys.exit()

# 3. Create new columns to store the added data property
df['genre'] = ""
df['short_description'] = ""
df['player_mode'] = ""


# --- DEFINING SAFETY SETTINGS ---
# Set the parameter of the safety settings so that the API won't block content for these categories.
safety_settings = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}


# 4. Iterate through each game and call the API
for index, row in df.iterrows():
    game_title = row['game_title']
    print(f"\nProcessing game {index + 1}/{len(df)}: {game_title}")

    # Create the prompts as an input to the generative AI model
    # a. Genre Classification Prompt
    genre_prompt = f"Classify the video game '{game_title}' into a single, common genre (e.g., 'RPG', 'Shooter', 'Strategy'). Respond with only the single-word genre."
    # b. Short Description Prompt
    description_prompt = f"In your own words, write a unique and creative short description for the video game '{game_title}'. The description must be under 30 words."
    # c. Player Mode Prompt 
    player_mode_prompt = f"Is the video game '{game_title}' primarily 'Singleplayer', 'Multiplayer', or 'Both'? Answer with only one of these three options."


    # --- Calling the API for each piece of information ---
    print("Prompting genre...")
    genre = get_ai_response(model, genre_prompt, safety_settings)
    df.at[index, 'genre'] = genre
    time.sleep(6) # Add a small delay to avoid hitting API rate limits
    print(genre)

    print("Prompting description...")
    description = get_ai_response(model, description_prompt, safety_settings)
    df.at[index, 'short_description'] = description
    time.sleep(6)
    print(description)

    print("Prompting player mode...")
    player_mode = get_ai_response(model, player_mode_prompt, safety_settings)
    df.at[index, 'player_mode'] = player_mode
    time.sleep(6)
    print(player_mode)

# 5. Save the enhanced DataFrame to a new CSV file [cite: 46, 53]
output_filename = "task 2/enhanced_games_data.csv"
df.to_csv(output_filename, index=False)

print(f"\nProcess complete. Enhanced data saved to '{output_filename}'.")