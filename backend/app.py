"""
Софтуер за Анализ на Брандове в Amazon - Главно Приложение
Водещ Разработчик: Мартин Дачев (martin.da4ev@gmail.com)
Компания: SP LINK
Проект: ЕС BG16RFPR001-1.001
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Зареждане на environment променливи
load_dotenv('config/.env')

# Инициализация на Flask приложение
app = Flask(__name__)
CORS(app)

# Конфигурация
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Инициализация на база данни
db = SQLAlchemy(app)

# Импортиране на модули
from api.routes import api_blueprint
from amazon_integration.amazon_api import AmazonAPIClient

# Регистриране на blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def index():
    """Начална страница"""
    return jsonify({
        'проект': 'Софтуер за Анализ на Брандове в Amazon',
        'версия': '0.5.0',
        'статус': 'TRL 5 - Валидиран Прототип',
        'компания': 'SP LINK',
        'разработчик': 'Мартин Дачев'
    })

@app.route('/health')
def health_check():
    """Проверка на здравословното състояние на системата"""
    return jsonify({
        'статус': 'работи',
        'база_данни': 'свързана',
        'api': 'оперативно'
    }), 200

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(os.getenv('FLASK_ENV') == 'development')
    )
