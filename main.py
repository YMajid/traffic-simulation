from src.validation import validation

if __name__ == "__main__":
    import time

    start = time.time()
    validation()
    end = time.time()

    print(end - start)
