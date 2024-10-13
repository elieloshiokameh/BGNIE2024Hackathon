import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render, redirect
from random import sample

# Function to load the correct sheet from the Excel file based on the selected language

def select_language(request):
    # Reference the template directly from the global templates/ directory
    return render(request, 'select_language.html')

import random
import pandas as pd
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render
import random

# Function to load Excel data based on the language ('Twi' or 'Yoruba')
def load_excel_data(sheet_name):
    file_path = os.path.join(settings.BASE_DIR, 'WelcomeBlack', 'data', 'TwiYoruba.xlsx')

    # Load the appropriate sheet ('Twi' or 'Yoruba')
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# Main quiz view
def quiz_view(request, language, level):
    # Load data from the Excel file based on the selected language (Twi or Yoruba)
    df = load_excel_data(language)
    if df is None:
        return render(request, 'error.html', {'message': 'Unable to load quiz data.'})

    # Filter questions by level (assuming there's a "Level" column in the Excel file)
    filtered_df = df[df['Level'] == level]
    questions = filtered_df.to_dict('records')

    # Shuffle and pick the first 8 questions
    random.shuffle(questions)
    questions = questions[:8]

    current_question = request.session.get('current_question', 0)
    correct_answers = request.session.get('correct_answers', 0)

    # Handle form submission
    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        correct_answer = request.session['correct_answer']

        if selected_answer == correct_answer:
            correct_answers += 1

        request.session['current_question'] = current_question + 1
        request.session['correct_answers'] = correct_answers

        if current_question + 1 == 8:
            del request.session['current_question']
            del request.session['correct_answers']

            if correct_answers >= 6:
                return render(request, 'congratulations.html', {'level': level, 'language': language})
            else:
                return render(request, 'try_again.html', {'level': level, 'language': language})

    # Load next question
    if current_question < 8:
        question = questions[current_question]
        correct_translation = question[language]  # Get the word in the selected language column

        # Generate 3 random wrong options
        wrong_options = df[df[language] != correct_translation][language].sample(3).tolist()
        options = wrong_options + [correct_translation]
        random.shuffle(options)

        # Store the correct answer in the session
        request.session['correct_answer'] = correct_translation

        # Create a list of tuples with options and their corresponding audio files
        options_with_audio = []
        for option in options:
            word_index = df[df[language] == option].index[0]  # Get the index of the word in the Excel file
            audio_file = f"{settings.MEDIA_URL}audio/{language}_{word_index}.mp3"
            options_with_audio.append((option, audio_file))

        return render(request, 'quiz.html', {
            'question': question['English'],  # Display the English word
            'options_with_audio': options_with_audio,  # Options paired with their audio files
            'level': level,  # The quiz level
            'language': language,  # The chosen language (Twi or Yoruba)
            'current_question': current_question + 1,  # Current question number
            'total_questions': 8,  # Total questions
        })
