import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained linear regression model
model_filename = 'Medical_linear2.pkl'
try:
  with open(model_filename, 'rb') as file:
    model = pickle.load(file)
except Exception as e:
  model = None
  print(f'Error loading model: {e}')

# HTML template with an attractive, modern UI using Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Cost Prediction</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 via-indigo-50 to-slate-100 min-h-screen flex flex-col justify-between">

    <!-- Header -->
    <header class="bg-white shadow-sm py-4 px-6 mb-8">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="bg-blue-600 text-white p-2 rounded-xl shadow-md">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                    </svg>
                </div>
                <h1 class="text-xl font-bold text-slate-800">HealthCost Predictor v2</h1>
            </div>
            <span class="text-xs font-semibold uppercase tracking-wider bg-blue-100 text-blue-800 px-3 py-1 rounded-full">AI Powered</span>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-2xl mx-auto px-4 w-full mb-12">
        <div class="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden p-8">
            <div class="text-center mb-8">
                <h2 class="text-2xl font-bold text-slate-900">Medical Insurance Cost Estimation</h2>
                <p class="text-slate-500 text-sm mt-1">Enter your details below to calculate projected medical expenses based on your profile.</p>
            </div>

            {% if prediction_text %}
            <div class="mb-8 p-6 bg-emerald-50 border border-emerald-200 rounded-2xl text-center">
                <span class="text-xs font-bold uppercase tracking-widest text-emerald-600 block mb-1">Estimated Cost</span>
                <div class="text-4xl font-extrabold text-emerald-700">{{ prediction_text }}</div>
            </div>
            {% endif %}

            <form action="/predict" method="POST" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Age -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Age</label>
                        <input type="number" name="age" required min="1" max="120" value="{{ request.form.age if request.form.age else '30' }}"
                            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-slate-700">
                    </div>

                    <!-- BMI -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">BMI (Body Mass Index)</label>
                        <input type="number" step="0.1" name="bmi" required min="10" max="60" value="{{ request.form.bmi if request.form.bmi else '25.0' }}"
                            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-slate-700">
                    </div>

                    <!-- Children -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Number of Children</label>
                        <input type="number" name="children" required min="0" max="10" value="{{ request.form.children if request.form.children else '0' }}"
                            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-slate-700">
                    </div>

                    <!-- Smoker -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Smoker Status</label>
                        <select name="smoker" class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-slate-700 bg-white">
                            <option value="0" {% if request.form.smoker == '0' %}selected{% endif %}>No (Non-Smoker)</option>
                            <option value="1" {% if request.form.smoker == '1' %}selected{% endif %}>Yes (Smoker)</option>
                        </select>
                    </div>
                </div>

                <!-- Region -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-2">Region</label>
                    <select name="region" class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-slate-700 bg-white">
                        <option value="0" {% if request.form.region == '0' %}selected{% endif %}>Northeast</option>
                        <option value="1" {% if request.form.region == '1' %}selected{% endif %}>Northwest</option>
                        <option value="2" {% if request.form.region == '2' %}selected{% endif %}>Southeast</option>
                        <option value="3" {% if request.form.region == '3' %}selected{% endif %}>Southwest</option>
                    </select>
                </div>

                <!-- Submit Button -->
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 px-6 rounded-xl shadow-lg shadow-blue-500/30 transition duration-200 cursor-pointer">
                    Calculate Prediction
                </button>
            </form>
        </div>
    </main>

    <!-- Footer -->
    <footer class="text-center py-6 text-slate-400 text-xs">
        &copy; 2026 HealthCost Predictor. Deployed on Render.
    </footer>

</body>
</html>
"""


@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)


@app.route('/predict', methods=['POST'])
def predict():
  if model is None:
    return render_template_string(
        HTML_TEMPLATE,
        prediction_text='Error: Model not loaded properly.',
    )

  try:
    # Extract features matching the model definition: age, bmi, children, smoker, region
    age = float(request.form['age'])
    bmi = float(request.form['bmi'])
    children = float(request.form['children'])
    smoker = float(request.form['smoker'])
    region = float(request.form['region'])

    # Format into numpy array matching model expectation
    features = np.array([[age, bmi, children, smoker, region]])

    # Make prediction
    prediction = model.predict(features)[0]
    formatted_prediction = f'${prediction:,.2f}'

    return render_template_string(
        HTML_TEMPLATE, prediction_text=formatted_prediction
    )
  except Exception as e:
    return render_template_string(
        HTML_TEMPLATE, prediction_text=f'Error in prediction: {str(e)}'
    )


if __name__ == '__main__':
  app.run(debug=True)
