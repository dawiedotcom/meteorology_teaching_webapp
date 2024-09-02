from . import init_app

app = init_app()

if __name__ == "__main__":
    '''Flask application entry point.'''
    app.run(host='0.0.0.0', debug=True)
