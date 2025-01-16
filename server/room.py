class Room:

    def __init__(self, client1, client2):

        self.questions, self.answers = self.generate_questions()
        self.index = {client1: 0, client2: 0}
        self.finished = False

    def generate_questions(self):
        return ["What is the capital of France?", "What is the capital of Germany?", "What is the capital of Italy?", "What is the capital of Spain?", "What is the capital of Portugal?", "What is the capital of Greece?", "What is the capital of Poland?", "What is the capital of Russia?", "What is the capital of Turkey?", "What is the capital of Egypt?"], ["Paris", "Berlin", "Rome", "Madrid", "Lisbon", "Athens", "Warsaw", "Moscow", "Ankara", "Cairo"]
    
    def verify_answer(self, client, attempt):
        if self.finished:
            return False
        index = self.index[client]
        answer = self.answers[index]
        correct = attempt == answer
        if correct:
            self.index[client] += 1
        
        return correct