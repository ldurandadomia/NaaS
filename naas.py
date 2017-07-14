#!flask/bin/python

author__ = "Laurent DURAND"

from restapp.app import app

if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=8000)
    app.run(debug=True)
