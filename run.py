if __name__ == '__main__':
    from threading import Thread
    from app import application
    from app.src.email import send_emails

    # try:
    #     thread1 = Thread(target=send_emails, args=('asd',))
    #     thread1.start()
    # except Exception as e:
    #     print("Email error: ", e)

    application.run()