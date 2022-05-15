from threading import Thread, Lock
import json
import time
# pending = []
# pending_mutex = Lock()
#
# matches = {}
#
#
#
# def start_match(player1, player2):
#     message = {
#         "type": "start"
#     }
#
#     player1.send(message)
#     player2.send(message)
#
#
# def match_players():
#     time.sleep(1)
#     pending_mutex.acquire()
#     player1 = None
#     player2 = None
#     try:
#         global pending
#         pending = list(filter(lambda x: x.connected, pending))
#         if len(pending) < 2:
#             return
#         player1 = pending.pop()
#         player2 = pending.pop()
#     except IndexError:
#         print("Index error")
#         return
#     finally:
#         pending_mutex.release()
#
#     matches[player1] = player2
#     matches[player2] = player1
#
#     start_match(player1, player2)
#
#
# end_thread = False
# def kill():
#     global end_thread
#     end_thread = True
#
# def match_manager():
#     while not end_thread:
#         match_players()
#
# match_manager_thread = None
# def create_match_manager():
#     match_manager_thread = Thread(target=match_manager)
#     match_manager_thread.start()
#     return kill
#
#
#
#
#
#
# def new_client(ws):
#     pending_mutex.acquire()
#     try:
#         pending.append(ws)
#     finally:
#         pending_mutex.release()
#
#     while True:
#         try:
#             data = ws.receive()
#         except:
#
#             if ws in matches:
#                 matches[ws].close()
#                 del matches[matches[ws]]
#                 del matches[ws]
#
#             return
#
#         data_json = json.loads(data)
#
#         matches[ws].send(data)
#
#         if data_json['status'] == 'win' or data_json['status'] == 'lose':
#             ws.close()
#             matches[ws].close()
#             del matches[matches[ws]]
#             del matches[ws]
#
import sys
def log(*args):
    print( args[0] % (len(args) > 1 and args[1:] or []))
    sys.stdout.flush()

class MatchManager:
    def __init__(self):
        self.pending = []
        self.pending_mutex = Lock()
        self.matches = {}
        self.end_thread = False
        self.match_manager_thread = None
        #self.create_match_manager()

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
        #time.sleep(1)
        self.pending_mutex.acquire()
        player1 = None
        player2 = None
        try:
            log("pending:")
            for pend in self.pending:
                log("    {}".format(pend))
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

    def create_match_manager(self):
        self.match_manager_thread = Thread(target=self.match_manager)
        self.match_manager_thread.start()

    def kill(self):
        self.end_thread = True

    def match_manager(self):
        #while not self.end_thread:
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