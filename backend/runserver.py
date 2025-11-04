from waitress import serve
from zipcab_project.wsgi import application

if __name__ == "__main__":
    print("🚀 Running ZipCab backend on http://127.0.0.1:8000")
    serve(application, host="127.0.0.1", port=8000, threads=4)