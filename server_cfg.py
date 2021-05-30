"""
    Server App edited
                        """

"""
    /home/smoxy/PycharmProjects/TCP_UDP/Server/
    /home/smoxy/FFmpeg_proj/
    /home/ubuntu/RC/
                                                """

import os
import time
import tqdm
from socket import *
import subprocess
import threading
import configparser

serverSocket = socket(AF_INET, SOCK_STREAM)
server_port = 13000
serverSocket.bind(('0.0.0.0', server_port))
HOME = "/home/ubuntu/RC/"  # /home/smoxy/PycharmProjects/TCP_UDP/Server/
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
    if not os.path.isdir(
            "received" + os.sep + f"{addr[0]}"):  # Creazione di una cartella dove mettere tutti i file inviati da un IP
        os.mkdir(
            "received" + os.sep + f"{addr[0]}")  # TODO: aggiornarlo per user e non per IP, chiedendo il login al client

    connected = True
    while connected:
        filename = conn.recv(BUFFER_SIZE).decode()  # Ricevo filename
        while filename[-4:].lower() == ".cfg":  # Se è il file di config
            cfg = conn.recv(BUFFER_SIZE)
            f_cfg = open(
                "." + os.sep + "received" + os.sep + f"{addr[0]}" + os.sep + 'user_config.cfg'.replace(" ", "\\"), 'wb')
            while cfg:
                f.write(cfg)
                i += 1
                cfg = conn.recv(BUFFER_SIZE)
            f_cfg.close()
            filename = conn.recv(BUFFER_SIZE).decode()

        data = conn.recv(BUFFER_SIZE)
        f = open("." + os.sep + "received" + os.sep + f"{addr[0]}" + os.sep + '%s'.replace(" ", "\\") % str(filename),
                 'wb')
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
        # conn.send((f"{filename}" + "SEPARATOR" + f"{filesize}").encode(encoding=encoding))

        f = open("." + os.sep + "encoded" + os.sep + f"{addr[0]}" + os.sep + '%s'.replace(" ", "\\") % str(filename),
                 'rb')
        l = f.read(BUFFER_SIZE)
        while l:
            conn.send(l)
            l = f.read(BUFFER_SIZE)
        f.close()
        print(f"[DONE WITH] {addr}")
        clear_shadows(filename, str(addr[0]))
        connected = False
    conn.close()


def clear_shadows(filename, user, folder=f"{HOME}received"):
    folder = folder + os.sep + user
    os.chdir(folder)
    os.remove(os.path.join(folder, filename))
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
    os.chdir(HOME)
    return


def compress_video(filename: str, user: str, conn, bitrate: int = 1400, threads: int = 0, preset: int = 9):
    cfg = configparser.ConfigParser()  ### Setting parser for language selection
    cfg_path = ('"{}received/{}/{}"'.format(HOME, user, "user_config.cfg"))
    cfg.read(cfg_path, encoding="UTF-8")
    # TODO Finire cfg parser

    presets = {9: "ultrafast", 8: "superfast", 7: "veryfast",
               6: "faster", 5: "fast", 4: "medium", 3: "slow",
               2: "slower", 1: "veryslow", 0: "placebo"}
    preset = presets[preset]
    path = ('"{}received/{}/{}"'.format(HOME, user, filename))
    output = ('"{}encoded/{}/{}"'.format(HOME, user, filename))
    cmd = f"ffmpeg -i {path} -b:v {bitrate}k -c:v libx264 -threads {threads} -preset {preset} {output}"
    result = subprocess.Popen(cmd, shell=True)
    # print("\n\n\n\n",result.poll(),"\n\n\n\n")
    while result.poll() is None:
        # print("Processing:", f"{result.poll()}")
        time.sleep(10)
        conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # TODO Keep alive non funziona
    return output
