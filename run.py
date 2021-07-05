from app import application # Из модуля app импортируем
                    # переменную app

if __name__ == '__main__':
    """
    Если файл запускаемый, 
    то запустить сервер на 5000 порту
    """
    # , host='37.140.192.110'
    application.run(port=5000, debug=True)