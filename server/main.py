import socket
import threading
import json
from protocols import Protocols
import time
from room import Room


class Server:

    def __init__(self, host="127.0.0.0", port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.clients_names  = {}
        self.opponents = {}
        self.rooms = {}
        self.waiting_for_pair = None

    def handle_connect(self, client):
        while True:
            self.send(Protocols.Response.NICKNAME, None, client)
            message = json.loads(client.recv(1024).decode('ascii'))
            r_type = message.get("type")
            data = message.get("data")

            if r_type == Protocols.Request.NICKNAME:
                self.clients_names[client] = data
            else:
                continue

            if not self.waiting_for_pair:
                self.waiting_for_pair = client
                print('waiting for pair')
            else:
                self.create_room(client)
            break

    
    def create_room(self, client):
        
        print("creating room")
        room = Room(client, self.waiting_for_pair)
        self.opponents[client] = self.waiting_for_pair
        self.opponents[self.waiting_for_pair] = client

        self.send(Protocols.Response.OPPONENT, self.clients_names[self.waiting_for_pair], client)
        self.send(Protocols.Response.OPPONENT, self.clients_names[client], self.waiting_for_pair)

        self.rooms[client] = room
        self.rooms[self.waiting_for_pair] = room
        self.waiting_for_pair = None

    def wait_for_room(self, client):
        while True:
            room = self.rooms.get(client)
            opponent = self.opponents.get(client)

            if(room and opponent):
                self.send(Protocols.Response.QUESTIONS, room.questions, client)
                time.sleep(1)
                self.send(Protocols.Response.START, None, client)
                break

    def handle_client(self, client):
        self.handle_connect(client)
        self.wait_for_room(client)

        while True:
            try:
                data = client.recv(1024).decode("ascii")
                if not data:
                    break
                message = json.load(data)
                self.handle_receive(message, client)
            except:
                break
        self.send_to_opponent(Protocols.Response.OPPONENT_LEFT, None, client)
        self.disconnect(client)



    def disconnect(self, client):

        opponent = self.opponents.get(client)
        if opponent in self.opponents:
            del self.opponents[opponent]

        if client in self.clients_names:
            del self.clients_names[client]

        if opponent in self.clients_names:
            del self.clients_names[opponent]

        if client in self.opponents:
            del self.opponents[client]
        
        if client in self.rooms:
            del self.rooms[client]

        if opponent in self.rooms:
            del self.rooms[opponent]
        
        client.close()

    def handle_receive(self, client, message):
        r_type = message.get("type")
        data = message.get('data')
        room = self.rooms[client]

        if r_type != Protocols.Request.ANSWER:
            return
        
        correct = room.verify_answer(client, data)

        if not correct:
            self.send(Protocols.Response.ANSWER_INVALID, None, client)
            return

        if room.index[client] >= len(room.questions):

            if not room.finished:
                room.finished = True

            self.send_to_opponent(Protocols.Response.WINNER, self.clients_names[client], client)
            self.send(Protocols.Response.WINNER, self.clients_names[client], client)
        
        else:
            self.send_to_opponent(Protocols.Response.OPPONENT_ADVANCE, None, client)
            self.send(Protocols.Response.ANSWER_VALID, None, client)

    def send(self, r_type, data, client):

        message = {'type': r_type, 'data': data}
        message = json.dumps(message).encode("ascii")
        client.send(message)

    def send_to_opponent(self, r_type, data, client):

        opponent = self.opponents.get(client)
        if(not opponent): 
            return
        self.send(r_type, data, opponent)
    
    def receive(self, client):
        while True:
            client, adress = self.server.accept()
            print(f"Connected with {str(adress)}")
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.receive()