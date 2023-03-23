# Import Flask module and necessary classes from forex_python.converter module
from flask import Flask, render_template, redirect, url_for, request
from forex_python.converter import CurrencyRates, CurrencyCodes

# Create a Flask application instance
app = Flask(__name__)

# Define a function to check if a given currency code is valid
def is_valid_currency(currency_code):
    # Create a CurrencyCodes instance to check for valid currency codes
    currency_codes = CurrencyCodes()
    # Use the get_currency_name method to check if the currency code is valid
    # If the code is valid, the method will return the currency name, otherwise it will return None
    return currency_codes.get_currency_name(currency_code.upper()) is not None

# Define a route for the home page
@app.route('/')
def welcome():
    # Render a template called 'welcome.html'
    return render_template('welcome.html')

# Define a route for the currency converter page
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    # If the user submits the form with POST request method
    if request.method == 'POST':
        # Get the amount, from_currency, and to_currency values from the form
        amount = request.form['amount']
        from_currency = request.form['from_currency'].upper()
        to_currency = request.form['to_currency'].upper()
        
        # Check if the entered currencies are valid
        if not is_valid_currency(from_currency) or not is_valid_currency(to_currency):
            # If one or both of the currencies are invalid, display an error message
            error = f"Invalid currency code(s). Please consult the list of valid currencies."
            # Render the 'calculator.html' template with the error message
            return render_template('calculator.html', error=error)
        
        # Check if the 'From Currency' and 'To Currency' options are the same
        if from_currency == to_currency:
            # If they are the same, display an error message
            error = f"The 'From Currency' and 'To Currency' options cannot be the same. Please select different currencies from the list."
            # Render the 'calculator.html' template with the error message
            return render_template('calculator.html', error=error)
        
        # If both currencies are valid and not the same, create a CurrencyRates instance
        c = CurrencyRates()
        # Get the exchange rate between the two currencies using the get_rate method
        rate = c.get_rate(from_currency, to_currency)
        # Calculate the result by multiplying the amount by the exchange rate and rounding to 2 decimal places
        result = round(float(amount) * rate, 2)
        # Create a result_text string to display the result
        result_text = f"{amount} {from_currency} = {result} {to_currency}"
        # Render the 'calculator.html' template with the result
        return render_template('calculator.html', result=result_text)
    
    # If the user requests the page with GET request method
    return render_template('calculator.html')

# If the script is run directly, start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)
