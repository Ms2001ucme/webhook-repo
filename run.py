from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
# This script initializes the Flask application and runs it.
# It imports the create_app function from the app package, creates an app instance,