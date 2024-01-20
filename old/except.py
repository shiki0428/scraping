for i in range(10):
    try:
        print(1)
        raise Exception
    except Exception:
        pass