import pandas as pd   
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def index(request):
    return render(request, 'index.html')

def analyze(request):
    crop = pd.read_csv("dataset/Crop_recommendation.csv")
    crop.drop_duplicates(inplace=True)
    attr = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]
    if crop.isna().any().sum() != 0:
        for col in attr:
            crop[col].fillna(0.0, inplace=True)
    crop.columns = crop.columns.str.replace(' ', '') 
    features = crop[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    target = crop['label']
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=2)
    RF = RandomForestClassifier(n_estimators=20, random_state=0)
    RF.fit(x_train, y_train)
    try:
        N = int(request.POST.get('nitrogen', 0))
        P = int(request.POST.get('phosphorous', 0))
        K = int(request.POST.get('potassium', 0))
        temp = float(request.POST.get('temperature', 0))
        humidity = float(request.POST.get('humidity', 0))
        ph = float(request.POST.get('ph', 0))
        rainfall = float(request.POST.get('rainfall', 0))
    except ValueError:
        return render(request, 'index.html', {'error': '❗ Please enter valid numeric values.'})
    if any(val == 0 for val in [N, P, K, temp, humidity, ph, rainfall]):
        return render(request, 'index.html', {'error': '❗ Please enter all values greater than 0.'})
    userInput = [N, P, K, temp, humidity, ph, rainfall]
    result = RF.predict([userInput])[0]
    params = {'purpose': 'Predicted Crop:', 'analyzed_text': result.upper()}
    return render(request, 'analyze.html', params)
def about_us(request):
    return render(request, 'About_us.html')
