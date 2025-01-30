import socket
import threading
import json
from protocols import Protocols


class Client:
    def __init__(self, host="127.0.0.1", port=55555):
        self.nickname = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

        self.closed = False
        self.started = False
        self.questions = []
        self.current_question_index = 0
        self.opponent_question_index = 0
        self.opponent_name = None
        self.winner = None

    def start(self):
        recieve_thread = threading.Thread(target=self.recieve)
        recieve_thread.start()

    def send(self, request, message):
        data = {'type': request, 'data': message}
        self.server.send(json.dumps(data).encode('ascii'))

    def recieve(self):
        while not self.closed:
            try:
                data = self.server.recv(1024).decode("ascii")
                message = json.loads(data)
                self.handle_response(message)

            except:
                break
        self.close()

    def close(self):
        self.closed = True
        self.server.close()

    # def client_validate_answer(self, attempt):
    #     question = self.questions[self.current_question_index]

    
    def handle_response(self, response):

        r_type = response.get("r_type")
        data = response.get('data')

        if r_type == Protocols.Response.QUESTIONS:
            self.questions = data

        elif r_type == Protocols.Response.OPPONENT:
            self.opponent_name = data

        elif r_type == Protocols.Response.OPPONENT_ADVANCE:
            self.opponent_question_index +=1

        elif r_type == Protocols.Response.START:
            self.started = True

        elif r_type == Protocols.Response.WINNER:
            self.winner = data

        elif r_type == Protocols.Response.OPPONENT_LEFT:
            self.close()
        elif r_type == Protocols.Response.ANSWER_VALID:
            self.current_question_index+=1

    def get_current_question(self):
        return self.questions[self.current_question_index]