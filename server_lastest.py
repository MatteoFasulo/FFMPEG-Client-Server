"""
    Server App edited
                        """

"""
    /home/smoxy/PycharmProjects/TCP_UDP/Server/
    /home/smoxy/FFmpeg_proj/
    /home/ubuntu/RC/
                                                """

import os
import time, tqdm
from socket import *
import subprocess
import threading
import json

serverSocket = socket(AF_INET, SOCK_STREAM)
server_port = 13000
serverSocket.bind(('0.0.0.0', server_port))
HOME = "/home/ubuntu/RC/"   # /home/smoxy/PycharmProjects/TCP_UDP/Server/
                            # /home/smoxy/FFmpeg_proj/
                            # /home/ubuntu/RC/
BUFFER_SIZE = 1024 * 4
encoding = 'utf-8'



def main():
    serverSocket.listen()
    print("[LISTENING] Server is listening")
    while True:
        conn, addr = serverSocket.accept()
        conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        thread = threading.Thread(target=tcp_socket, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



def tcp_socket(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    os.chdir(HOME)
    if not os.path.isdir("received"):
        os.mkdir("received")
    if not os.path.isdir("received" + os.sep + f"{addr[0]}"):  # Creazione di una cartella dove mettere tutti i file inviati da un IP
        os.mkdir("received" + os.sep + f"{addr[0]}")  # TODO: aggiornarlo per user e non per IP, chiedendo il login al client

    connected = True
    while connected:
        filename = conn.recv(BUFFER_SIZE).decode()
        data = conn.recv(BUFFER_SIZE)
        f = open("." + os.sep + "received" + os.sep + f"{addr[0]}" + os.sep + '%s'.replace(" ", "\\") % str(filename), 'wb')
        i = 0
        while data:
            f.write(data)
            # print("data {0}".format(i))
            i += 1
            data = conn.recv(BUFFER_SIZE)
        f.close()
        if not os.path.isdir("encoded"):
            os.mkdir("encoded")
        if not os.path.isdir(
                "encoded" + os.sep + f"{addr[0]}"):  # Creazione di una cartella dove mettere i file elaborati di un IP
            os.mkdir("encoded" + os.sep + f"{addr[0]}")  # TODO: aggiornarlo per user e non per IP
        file = compress_video(filename, str(addr[0]), conn)
        #conn.send((f"{filename}" + "SEPARATOR" + f"{filesize}").encode(encoding=encoding))

        f = open("." + os.sep + "encoded" + os.sep + f"{addr[0]}" + os.sep + '%s'.replace(" ", "\\") % str(filename), 'rb')
        l = f.read(BUFFER_SIZE)
        while l:
            conn.send(l)
            l = f.read(BUFFER_SIZE)
        f.close()
        print(f"[DONE WITH] {addr}")
        clear_shadows(filename, str(addr[0]))
        connected = False
    conn.close()



def udp_socket():
    server_port = 15000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', server_port))
    print("Listening UDP")
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.upper()
        serverSocket.sendto(modifiedMessage, clientAddress)



def clear_shadows(filename, user, folder=f"{HOME}received"):
    folder = folder + os.sep + user
    os.chdir(folder)
    os.remove(os.path.join(folder, filename))
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
    os.chdir(HOME)
    return



def compress_video(filename: str, user: str, conn, bitrate: int = 1400, threads: int = 4, preset: int = 9):
    presets = {9: "ultrafast", 8: "superfast", 7: "veryfast",
               6: "faster", 5: "fast", 4: "medium", 3: "slow",
               2: "slower", 1: "veryslow", 0: "placebo"}
    preset = presets[preset]
    path = ('"{}received/{}/{}"'.format(HOME, user, filename))
    output = ('"{}encoded/{}/{}"'.format(HOME, user, filename))  # if u rush u gay
    cmd = f"ffmpeg -i {path} -b:v {bitrate}k -c:v libx264 -threads {threads} -preset {preset} {output}"
    result = subprocess.Popen(cmd, shell=True)
    #print("\n\n\n\n",result.poll(),"\n\n\n\n")
    while result.poll()==None:
        #print("Processing:", f"{result.poll()}")
        time.sleep(10)
        conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    return output



def receive_file(conn, addr="Downloads", verbose: bool=False):
    """
    riceve filename e size e mostra la barra di caricamento (verbose). Alla fine salva il file e
    ritorna la path e il nome del file
    """
    args = conn.recv(BUFFER_SIZE).decode().split("SEPARATOR")
    if len(args)==2:
        filename, filesize = args
    else:
        filename = args[0].strip()
        filesize = None
    data = conn.recv(BUFFER_SIZE)
    f = open("." + os.sep + "received" + os.sep + f"{addr[0]}" + os.sep + '%s'.replace(" ", "\\") % str(filename), 'wb')
    if verbose:
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    while data:
        if verbose:
            progress.update(len(data))
        f.write(data)
        data = conn.recv(BUFFER_SIZE)
    f.close()
    return filename



def send_file(conn, filename, verbose=False):
    """
    Instaura connessione, innanzitutto manda filename e size e fino a che il file non è terminato lui lo invia e mostra la barra di caricamento
    ritorna True se tutto è andato bene, altrimenti False
    """
    conn.send(f"{filename}".encode(encoding=encoding))
    filesize = os.path.getsize(os.path.join('%sencoded/%s', '%s'.replace(" ", "\\")) % (HOME, str(user), str(filename)))
    conn.send((f"{filename}" + "SEPARATOR" + f"{filesize}").encode(encoding=encoding))
    filesize = os.path.getsize(filename)
    if verbose:
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as video:
        l = video.read(BUFFER_SIZE)
        while l:
            if verbose:
                progress.update(len(l))
            conn.send(l)
            l = video.read(BUFFER_SIZE)
        video.close()
    return



main()