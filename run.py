if __name__ == '__main__':
    from app import application
    application.run()
    from threading import Thread
    from app.src.email import send_emails
    try:
        thread1 = Thread(target=send_emails, args=())
        thread1.start()
    except Exception as e:
        print("Email error: ", e)