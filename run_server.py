import os
if os.environ['WEB_FRAMEWORK'] == 'flask':
    from flask_ui import app
if os.environ['WEB_FRAMEWORK'] is 'django':
    from django_ui import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)