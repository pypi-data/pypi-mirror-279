import subprocess
import sys
import time
from flask import Flask

# Список необходимых библиотек
required_libraries = [
    "Flask",
    "Werkzeug",
    "Flask-SQLAlchemy",
    "flask-help-tools",
    "Flask-Login",
    "Flask-WTF",
    "email-validator",
    "pandas",
    "openpyxl"
]


def check_and_run():
    # Проверка установленных библиотек
    def check_libraries(libraries):
        for lib in libraries:
            try:
                __import__(lib)
                print(f"{lib} установлена.")
            except ImportError:
                print(f"{lib} не установлена. Установка...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", lib])

    # Проверка библиотек
    check_libraries(required_libraries)

    time.sleep(10)
    # Тестовое приложение Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello, Flask!"

    app.run(debug=True)


# Если нужно, можно оставить запуск функции при запуске модуля напрямую
if __name__ == "__main__":
    check_and_run()
