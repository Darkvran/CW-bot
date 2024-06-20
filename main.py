from botdriver import botDriver

def main():
    session = botDriver(666, 'ffgwefew', 21424123)
    session.testMouse()
    session.safetyCheck()

if __name__ == "__main__":
    main()