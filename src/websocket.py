from threading import Thread, Lock
import json
import time
pending = []
pending_mutex = Lock()

matches = {}



def start_match(player1, player2):
    message = {
        "type": "start"
    }

    player1.send(message)
    player2.send(message)


def match_players():
    time.sleep(1)
    pending_mutex.acquire()
    player1 = None
    player2 = None
    try:
        global pending
        pending = list(filter(lambda x: x.connected, pending))
        if len(pending) < 2:
            return
        player1 = pending.pop()
        player2 = pending.pop()
    except IndexError:
        print("Index error")
        return
    finally:
        pending_mutex.release()

    matches[player1] = player2
    matches[player2] = player1

    start_match(player1, player2)


end_thread = False
def kill():
    global end_thread
    end_thread = True

def match_manager():
    while not end_thread:
        match_players()

match_manager_thread = None
def create_match_manager():
    match_manager_thread = Thread(target=match_manager)
    match_manager_thread.start()
    return kill






def new_client(ws):
    pending_mutex.acquire()
    try:
        pending.append(ws)
    finally:
        pending_mutex.release()

    while True:
        try:
            data = ws.receive()
        except:
            
            if ws in matches:
                matches[ws].close()
                del matches[matches[ws]]
                del matches[ws]

            return

        data_json = json.load(data)

        matches[ws].send(data)

        if data_json['status'] == 'win' or data_json['status'] == 'lose':
            ws.close();
            matches[ws].close()
            del matches[matches[ws]]
            del matches[ws]


