from viewer import show

def main():
    try:
        while True:
            viewer.show()

    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        print("Cleaning up...")

if __name__ == "__main__":
    main()