# converter.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Conversion functions for length, weight, and temperature
def convert_length(value, from_unit, to_unit):
    length_units = {
        'millimeter': 0.001, 'centimeter': 0.01, 'meter': 1, 'kilometer': 1000,
        'inch': 0.0254, 'foot': 0.3048, 'yard': 0.9144, 'mile': 1609.34
    }
    return value * length_units[to_unit] / length_units[from_unit]

def convert_weight(value, from_unit, to_unit):
    weight_units = {
        'milligram': 0.001, 'gram': 1, 'kilogram': 1000,
        'ounce': 28.3495, 'pound': 453.592
    }
    return value * weight_units[to_unit] / weight_units[from_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'Celsius':
        return value + 273.15 if to_unit == 'Kelvin' else (value * 9/5) + 32
    elif from_unit == 'Fahrenheit':
        return (value - 32) * 5/9 if to_unit == 'Celsius' else ((value - 32) * 5/9) + 273.15
    elif from_unit == 'Kelvin':
        return value - 273.15 if to_unit == 'Celsius' else ((value - 273.15) * 9/5) + 32

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    value = data.get('value')
    from_unit = data.get('fromUnit')
    to_unit = data.get('toUnit')
    category = data.get('category')

    if category == 'length':
        result = convert_length(value, from_unit, to_unit)
    elif category == 'weight':
        result = convert_weight(value, from_unit, to_unit)
    elif category == 'temperature':
        result = convert_temperature(value, from_unit, to_unit)
    else:
        return jsonify({"error": "Invalid category"}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
