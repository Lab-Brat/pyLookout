from lookout import PyLookout


def main():
    threshold = 75
    notification_method = "sendgrid"
    lk = PyLookout(threshold, notification_method)
    lk.checker()


if __name__ == "__main__":
    main()
