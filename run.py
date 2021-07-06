from app import application # Из модуля app импортируем
                    # переменную app

if __name__ == '__main__':
    application.run(port=5000, debug=True)