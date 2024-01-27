import threading

battle_status = {'in_battle': None}
status_lock = threading.Lock()
