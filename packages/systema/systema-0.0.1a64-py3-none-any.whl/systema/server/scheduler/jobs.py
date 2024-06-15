import schedule


def send_test_notification():
    from systema.utils import send_test_notification as send_

    send_()


def ping():
    print("Hello from Systema!")


def add_jobs():
    schedule.every(10).seconds.do(ping)
    schedule.every(30).minutes.do(send_test_notification)
