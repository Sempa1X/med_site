if __name__ == '__main__':
    # from threading import Thread
    # from app.src.email import send_emails
    # try:
    #     thread1 = Thread(target=send_emails, args=())
    #     thread2 = Thread(target=application.run(), args=())
    #     thread1.start()
    #     th
    # except Exception as e:
    #     print("Email error: ", e)
    from app import application
    application.run()