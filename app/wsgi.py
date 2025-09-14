from app import create_app
import gunicorn


g_app = create_app()

if __name__ == "__main__":
    g_app.run()