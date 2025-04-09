from django.http import HttpResponse
from django.shortcuts import redirect, render
import joblib
import numpy as np

# Load all models
xgb_model = joblib.load("xgb_model.pkl")  # XGBoost model
lgbm_model = joblib.load("lgbm_model.pkl")  # LightGBM model
ann_model = joblib.load("lgbm_model.pkl")  # ANN model

def home(request):
    return render(request, 'index.html')

def input(request):
    file_name = 'account.txt'
    name = request.POST.get('name')
    password = request.POST.get('password')
    with open(file_name, 'r') as file:
        account_list = [line.split() for line in file]
    for account in account_list:
        if account[0] == name and account[1] == password:
            return render(request, 'location_input.html')
    return HttpResponse('Wrong Password or Name', content_type='text/plain')

def city_input(request):
    if request.method == "POST":
        city = request.POST.get("city")
        return render(request, "input.html", {"city": city})
    return redirect("input")  # fallback if someone opens this page directly

def output(request):
    if request.method == 'POST':
        # Get input values from the form
        wind_speed = float(request.POST['WindSpeed'])
        sunshine = float(request.POST['Sunshine'])
        air_pressure = float(request.POST['AirPressure'])
        radiation = float(request.POST['Radiation'])
        air_temp = float(request.POST['AirTemperature'])
        humidity = float(request.POST['RelativeAirHumidity'])
        hour = int(request.POST['Hour'])
        day_of_week = int(request.POST['DayOfWeek'])
        month = int(request.POST['Month'])
        day_of_year = int(request.POST['DayOfYear'])
        model_choice = request.POST['model']  # Get selected model from user

        # Convert input to numpy array
        input_data = np.array([[wind_speed, sunshine, air_pressure, radiation, air_temp, humidity, hour, day_of_week, month, day_of_year]])

        # Select model based on user choice
        if model_choice == 'XGBoost':
            model = xgb_model
        elif model_choice == 'LGBM':
            model = lgbm_model
        else:
            model = ann_model  # Default to ANN

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Pass prediction to output.html
        return render(request, 'output.html', {'prediction': round(prediction, 2), 'model': model_choice})

    return render(request, 'output.html', {'prediction': None})
