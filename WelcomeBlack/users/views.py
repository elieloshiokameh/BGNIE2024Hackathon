# users/views.py
import os
import json
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

def load_yoruba_dataset():
    dataset_path = os.path.join(settings.BASE_DIR, '../Datasets/yorubaToEnglish.json')
    with open(dataset_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    return dataset

def load_twi_dataset():
    dataset_path = os.path.join(settings.BASE_DIR, '../Datasets/twiToEnglish.json')
    with open(dataset_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    return dataset

def questions_view(request):
    language = request.GET.get('language', None)  # Get the selected language from the URL

    if language == 'yoruba':
        dataset = load_yoruba_dataset()  # Assuming this function loads the Yoruba JSON dataset
    elif language == 'twi':
        dataset = load_twi_dataset()  # Assuming this function loads the Twi JSON dataset
    else:
        # Redirect to a welcome page or show an error if no valid language is selected
        return redirect('welcome')

    # Ensure that 'dataset' has been defined at this point before proceeding
    # Shuffle options for each question
    for question in dataset['questions']:
        options = question['options']
        random.shuffle(options)  # Randomize the options
        question['options'] = options  # Update the question with shuffled options

    return render(request, 'questions.html', {'questions': dataset['questions']})
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
