if __name__ == '__main__':
    from app import application, scheduler
    scheduler.init_app(application)
    scheduler.start()
    application.run()