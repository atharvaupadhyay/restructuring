from api.index import app
import os

if __name__ == '__main__':
    # Watch the .env file for changes so the server reloads automatically
    extra_files = []
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        extra_files.append(dotenv_path)
    
    app.run(debug=True, use_reloader=False)
