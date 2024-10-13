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
from django.shortcuts import render, redirect
import random

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Function to load the correct sheet from the Excel file based on the selected language
def load_excel_data(language):
    file_path = os.path.join(settings.BASE_DIR, 'WelcomeBlack', 'data', 'TwiYoruba.xlsx')

    if language == 'Twi':
        df = pd.read_excel(file_path, sheet_name='Twi')
    elif language == 'Yoruba':
        df = pd.read_excel(file_path, sheet_name='Yoruba')
    else:
        return None
    return df

# Main quiz view for displaying and handling the quiz logic
# Main quiz view for displaying and handling the quiz logic
def quiz_view(request, language, level):
    df = load_excel_data(language)
    if df is None:
        return redirect('select_language')  # Redirect if language is not valid

    filtered_df = df[df['Level'] == level]
    questions = filtered_df.to_dict('records')
    random.shuffle(questions)
    questions = questions[:8]  # Limit the number of questions to 8

    current_question = request.session.get('current_question', 0)
    correct_answers = request.session.get('correct_answers', 0)

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

    # Generate correct and wrong options
    if current_question < 8:
        question = questions[current_question]
        correct_translation = question[language]

        # Generate three wrong options
        wrong_options = df[df[language] != correct_translation][language].sample(3).tolist()
        options = wrong_options + [correct_translation]
        random.shuffle(options)

        request.session['correct_answer'] = correct_translation

        # Generate paths to the correct audio files for each option
        options_audio_files = []
        for idx, option in enumerate(options):
            option_audio_file = f"{settings.MEDIA_URL}audio/{language}_{df[df[language] == option].index[0]}.mp3"
            options_audio_files.append(option_audio_file)

        question_audio_file = f"{settings.MEDIA_URL}audio/{language}_{current_question}.mp3"

        return render(request, 'quiz.html', {
            'question': question['English'],  # Question in English
            'options_with_audio': zip(options, options_audio_files),
            'level': level,
            'language': language,
            'current_question': current_question + 1,
            'total_questions': 8,
            'correct_answers': correct_answers,  # For progress bar
            'audio_file': question_audio_file
        })

def welcome_view(request):
    return render(request, 'home.html')

def home_view(request):
    return render(request, 'landing.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('welcome')  # Redirect to welcome page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('welcome')  # Redirect to welcome page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')