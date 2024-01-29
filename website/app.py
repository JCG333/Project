from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    data = {
        'title': 'Service for snow and ice detection',
        'header': 'Service for snow and ice detection',
        'welcome_message': 'Welcome to the service for snow and ice detection!',
        'content': 'Contents',
        'footer_text': 'Service for snow and ice detection. All rights reserved.'
    }
    return render_template('index.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
