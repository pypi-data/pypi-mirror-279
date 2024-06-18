from .client import RshipExecClient

def main():
    client = RshipExecClient("10.147.20.13", 5155)
    client.connect()
    while not client.is_connected:
        pass
    print("Connected to Rship")

if __name__ == "__main__":
    main()