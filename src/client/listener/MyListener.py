class MyListener:
    def on_connected(self):
        print("Connecté au serveur !")

    def on_disconnected(self):
        print("Déconnecté du serveur !")

    def on_received(self, message: str):
        message = message.strip()
        self.last_response = message
        print(f"Message reçu : {message}")

    def on_error(self, exception):
        print(f"Erreur : {exception}")