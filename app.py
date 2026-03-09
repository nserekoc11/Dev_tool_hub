from flask import Flask, json, render_template, request
import re
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#JSON Formatter Route
@app.route('/json', methods=['GET', 'POST'])
def json_formatter():
    formatted = ""
    error = ""
    if request.method == 'POST':
        data = request.form['json_input'] #get user input
        try:
            parsed = json.loads(data) #parse the JSON data
            formatted = json.dumps(parsed, indent=4) #format the JSON data
        except Exception as e:
            error = str(e)
    return render_template('json_formatter.html', formatted=formatted, error=error) #handle JSON parsing errors

#Regex Tester Route
@app.route('/regex', methods=['GET', 'POST'])
def regex_tester():
    result = ""
    error = ""
    if request.method == 'POST':
        pattern = request.form.get('regex_pattern') #get regex pattern from user input
        test_string = request.form.get('test_string') #get test string from user input
        try:
            if not pattern or not test_string:
                error = "Both fields are required."
            else:
                matches = re.findall(pattern, test_string)
                normalized = [m if isinstance(m, str) else "".join(m) for m in matches]
                result = "\n".join(normalized) if normalized else "No matches found."

        except re.error as e:
            error = f"Regex error: {str(e)}"
    return render_template('regex.html', result=result, error=error) #handle regex errors

#Password generator
@app.route('/password', methods=['GET', 'POST'])
def password_gen():
    password = ""
    error = ""
    if request.method == 'POST':
        length = int(request.form.get('length', 12)) #get desired password length from user input
        include_uppercase = 'uppercase' in request.form #check if uppercase letters should be included
        include_lowercase = 'lowercase' in request.form #check if lowercase letters should be included
        include_digits = 'digits' in request.form #check if digits should be included
        include_special = 'special' in request.form #check if special characters should be included

        charset = ""
        if include_uppercase:
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if include_lowercase:
            charset += "abcdefghijklmnopqrstuvwxyz"
        if include_digits:
            charset += "0123456789"
        if include_special:
            charset += "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

        if charset:
            password = ''.join(random.choice(charset) for _ in range(length)) #generate random password based on selected criteria
        
        try:
            if len(password) <= 4:
                error = "Password length must be at least 4 characters."
        except Exception as e:
            error = str(e)
    return render_template('password_generator.html', password=password, error=error) #display generated password

if __name__ == '__main__':
    app.run(debug=True)