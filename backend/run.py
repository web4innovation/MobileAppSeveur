#!flask/bin/python3

from quiz_app_server_flaskViews import app
app.run(debug=True, port=80, host='0.0.0.0')
