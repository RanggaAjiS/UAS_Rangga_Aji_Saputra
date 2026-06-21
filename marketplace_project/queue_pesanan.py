from collections import deque

antrian = deque()

def tambah_pesanan(data):
    antrian.append(data)

def proses_pesanan():
    if antrian:
        return antrian.popleft()
    return None

def lihat_antrian():
    return list(antrian)