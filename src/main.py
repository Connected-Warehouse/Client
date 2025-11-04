from client.SocketClient import SocketClient
from client.listener.MyListener import MyListener


def main():
    host = "127.0.0.1"
    port = 8888

    listener = MyListener()
    client = SocketClient(host, port, listener)

    client.connect()
    client.send_message("Bonjour serveur !")

    # garder le programme actif pour recevoir les messages
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()


if __name__ == "__main__":
    main()