from threading import Thread, Lock
import json
import time
import sys
pending = []
pending_mutex = Lock()

matches = {}

# logging helper
def log(*args):
    print (args[0] % (len(args) > 1 and args[1:] or []))
    sys.stdout.flush()

def start_match(player1, player2):
    message = {
        "type": "start"
    }
    log("Sending messages")
    player1.send(message)
    player2.send(message)


def match_players():
    #time.sleep(1)
    log("Acquiring mutex")
    pending_mutex.acquire()
    player1 = None
    player2 = None
    log("Starting try")
    try:
        global pending
        
        log("pending:")
        for pend in pending:
            log("    {}".format(pend))
        log("Clearing pending")
        pending = list(filter(lambda x: x.connected, pending))
        log("Cleared pending")
        log("pending:")
        for pend in pending:
            log("    {}".format(pend))
        if len(pending) < 2:
            return
        player1 = pending.pop()
        player2 = pending.pop()
        log("Players: {} {}".format(player1, player2))
    except IndexError:
        log("Index error")
        return
    finally:
        log("releasing mutex")
        pending_mutex.release()

    matches[player1] = player2
    matches[player2] = player1

    log("Starting match")
    start_match(player1, player2)
    log("Started match")


end_thread = False
def kill():
    global end_thread
    end_thread = True

def match_manager():
    match_players()

match_manager_thread = None
def create_match_manager():
    match_manager_thread = Thread(target=match_manager)
    match_manager_thread.start()
    return kill






def new_client(ws):
    ws.send("SIEMA IEMA SIEMA")
    log("[{}] New client".format(ws))
    pending_mutex.acquire()
    try:
        pending.append(ws)
        log("[{}] Added ws to pending".format(ws))
    finally:
        pending_mutex.release()
    log("[{}] Calling match manager".format(ws))
    match_manager()
    log("[{}] Match manager called".format(ws))
    while True:
        try:
            log("[{}] Waiting for messsage".format(ws))
            data = ws.receive()
            log("[{}] Got message".format(ws))
        except:
            log("[{}] closed ws".format(ws))
            if ws in matches:
                matches[ws].close()
                del matches[matches[ws]]
                del matches[ws]

            return

        data_json = json.loads(data)

        log("[{}] sends message".format(ws))
        matches[ws].send(data)

        if data_json['status'] == 'win' or data_json['status'] == 'lose':
            ws.close()
            matches[ws].close()
            del matches[matches[ws]]
            del matches[ws]


