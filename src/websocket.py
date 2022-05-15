from threading import Thread, Lock
import json
import time

class MatchManager:
    def __init__(self):
        self.pending = []
        self.pending_mutex = Lock()
        self.matches = {}

    def new_client(self, ws):
        self.pending_mutex.acquire()
        try:
            self.pending.append(ws)
        finally:
            self.pending_mutex.release()
        self.match_manager()
        while True:
            try:
                data = ws.receive()
            except:

                if ws in self.matches:
                    self.matches[ws].close()
                    del self.matches[self.matches[ws]]
                    del self.matches[ws]

                return

            data_json = json.loads(data)

            self.matches[ws].send(data)

            if data_json['status'] == 'win' or data_json['status'] == 'lose':
                ws.close()
                self.matches[ws].close()
                del self.matches[self.matches[ws]]
                del self.matches[ws]

    def match_players(self):
        self.pending_mutex.acquire()
        player1 = None
        player2 = None
        try:
            self.pending = list(filter(lambda x: x.connected, self.pending))
            if len(self.pending) < 2:
                return
            player1 = self.pending.pop()
            player2 = self.pending.pop()
        except IndexError:
            print("Index error")
            return
        finally:
            self.pending_mutex.release()

        self.matches[player1] = player2
        self.matches[player2] = player1
        self.start_match(player1, player2)


    def match_manager(self):
        self.match_players()

    @staticmethod
    def start_match(player1, player2):
        message = {
            "type": "start"
        }

        player1.send(message)
        player2.send(message)

    def __del__(self):
        pass#self.kill()