import openai
import os
import pandas as pd
from pathlib import Path

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set correctly

# Path to your TwiYoruba.xlsx file
data_file_path = Path(__file__).resolve().parent / "WelcomeBlack" / "data" / "TwiYoruba.xlsx"

# Create a folder to store audio files if it doesn't exist
audio_output_path = Path(__file__).resolve().parent / "WelcomeBlack"/ "audio_files"
audio_output_path.mkdir(parents=True, exist_ok=True)

# Load the Excel file
try:
    df = pd.read_excel(data_file_path, sheet_name=None)  # Read all sheets
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# OpenAI TTS Model and Voice Settings
model = "tts-1"  # Use either 'tts-1' or 'tts-1-hd' based on the model quality you want
voice = "alloy"  # Supported voices: alloy, echo, fable, onyx, nova, shimmer

# Function to generate audio for each word
def generate_audio(text, language, row_index):
    try:
        print(f"Generating audio for '{text}' ({language})...")

        # Define the output file path
        speech_file_path = audio_output_path / f"{language}_{row_index}.mp3"

        # Generate the audio file via OpenAI API
        client = openai.OpenAI()
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        # Save the audio content to file
        response.stream_to_file(speech_file_path)

        print(f"Audio saved: {speech_file_path}")

    except Exception as e:
        print(f"Error generating speech for '{text}': {e}")

# Loop through each sheet (Twi and Yoruba) and generate audio
for language, data in df.items():
    for index, row in data.iterrows():
        text = row[language]  # Assuming each sheet has a column named after the language
        generate_audio(text, language, index)
