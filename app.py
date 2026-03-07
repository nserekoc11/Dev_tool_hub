from flask import Flask, json, render_template, request, request
import re

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
            if re.search(pattern, test_string):
                result = "Match found!"
            else:
                result = "No match found."
        except Exception as e:
            error = str(e)
    return render_template('regex_tester.html', result=result, error=error) #handle regex errors

if __name__ == '__main__':
    app.run(debug=True)