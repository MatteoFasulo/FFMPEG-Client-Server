import json
import os
import time
from socket import *
import subprocess
import threading
import concurrent.futures
import configparser
import glob
import stream

########################## STATIC INT #############################
IP = '0.0.0.0'
HOME = "/home/ubuntu/RC/"
BUFFER_SIZE = 1024 * 4
encoding = 'utf-8'
SEP = "<SEPARATOR>"
SEP_ADG = "><SEP><"
availablePorts = list(range(13001, 13021))


###################################################################

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    default_port = 13000
    serverSocket.bind((IP, default_port))
    serverSocket.listen()
    print(f"[LISTENING] Server is listening on {IP}:{default_port}")
    while True:
        conn, addr = serverSocket.accept()
        thread = threading.Thread(target=assign_socket, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def assign_socket(conn, addr):
    print("\t\t open assign_socket")
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = availablePorts[0]

    # TODO SEND TO CLIENT
    conn.send(("new_port" + SEP + f"{server_port}").encode(encoding=encoding))
    # TODO CLOSE OLD CONNECTION
    conn.close()

    availablePorts.remove(server_port)

    serverSocket.bind((IP, server_port))
    serverSocket.listen(1)
    print(f"[LISTENING] Server is listening on {IP}:{server_port} for {addr}")
    conn, addr = serverSocket.accept()

    tcp_socket(conn, addr, server_port)
    print("\t\t close assign_socket")
    # conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)


def release_socket(conn, port):
    conn.close()
    availablePorts.append(port)
    print("\t\t close assign_socket")
    return port


def tcp_socket(conn, addr, server_port):
    print(f"[NEW CONNECTION] {addr} connected.")
    print("\t\t open tcp_socket")
    os.chdir(HOME)
    user = None

    done = False
    # LISTENER and HANDLING/RESOLVE REQUEST From client
    while not done:
        args = conn.recv(BUFFER_SIZE).decode()  # PROTOCOLLO - RICEVO COMANDO ED ARGS
        print(f"\t{args}")
        # user, pwd = args.split("SEPARATOR")
        try:
            func_handled, arg1, arg2 = map(str, args.split(SEP))
        except ValueError:
            release_socket(conn, server_port)
            return
        if func_handled.lower() == "login":
            login_status = login(user=arg1, pwd=arg2)
            conn.send(f"{login_status}".encode(encoding=encoding))
            if login_status == 0:
                user = arg1
                done = True

        elif func_handled.lower() == "register":
            register_status = register_user(user=arg1, pwd=arg2)
            conn.send(f"{register_status}".encode(encoding=encoding))

    while done:
        print("SUCCESSFULLY LOGGED IN: {}".format(user))
        args = conn.recv(BUFFER_SIZE).decode()  # PROTOCOLLO - RICEVO COMANDO ED ARGS
        try:
            func_handled, arg1, arg2 = map(str, args.split(SEP))
            print(f"AFTER LOGIN: {args}")
        except ValueError:
            release_socket(conn, server_port)
            return

        if func_handled.lower() == "get_cfg":
            ...

        elif func_handled.lower() == "encode":
            # thread = threading.Thread(target=encode, args=(conn, addr, user))
            # thread.start()
            print(f"[ACTIVE THREADS ENCODING] {threading.activeCount() - 1}")
            encode(conn, addr, user=user)
            done = False
            release_socket(conn, server_port)

        elif func_handled.lower() == "list_dir":
            list_file = glob.glob(HOME + "encoded" + os.sep + f"{user}" + os.sep + "*")
            files = str()
            for i in range(len(list_file)):
                files += str(list_file[i][(list_file[i].rfind(os.sep) + 1):])
                if i < len(list_file) - 1:
                    files += SEP_ADG

            conn.send(f"{files}".encode(encoding=encoding))
            print("Lista inviata")

        elif func_handled.lower() == "streaming":
            # TODO parametri da leggere dal config file
            release_socket(conn, server_port)
            try:
                print("\t\tENTER TRY STREAMING")
                """streamingSocket = socket(AF_INET, SOCK_STREAM)
                streaming_port = streamingPorts[0]
                streamingPorts.remove(streaming_port)
                streamingSocket.bind((IP, streaming_port))
                streamingSocket.listen(2)
                print(f"[LISTENING] Server is listening for streaming on {server_port}")
                stream_conn, addr = streamingSocket.accept()"""
                # thread = threading.Thread(target=stream.streaming, args=(f"{user}", f"{arg1}"))
                # thread.start()
                # print(f"[ACTIVE THREADS] {threading.activeCount() - 1}")
                finished = stream.streaming(user=f"{user}", filename=f"{arg1}")
                return
            except KeyError:
                print("Chiave non trovata")
                # TODO ADVERTISE CLIENT OF MISSING KEY
                return

        elif func_handled.lower() == "delete_file":
            try:
                clear_shadows(str(arg1), str(user), f"{HOME}encoded")
                conn.send(str("delete_file" + SEP + "Correctly deleted").encode(encoding=encoding))
            except FileNotFoundError:
                conn.send(str("delete_file" + SEP + "FileNotFoundError").encode(encoding=encoding))
                # TODO invia messaggio al client FileNotFoundError
                pass

        elif func_handled.lower() == "download_my_file":
            filename = arg1
            filesize = calc_filesize(filename, user)
            print(f"\t\t{filename} {filesize}")
            time.sleep(0.5)
            conn.send((f"{filename}" + SEP + f"{filesize}").encode(encoding=encoding))
            os.chdir(f"{HOME}encoded" + os.sep + user)
            with open(f"{filename}",'rb') as f:
                frames = f.read(BUFFER_SIZE)
                while frames:
                    conn.send(frames)
                    frames = f.read(BUFFER_SIZE)
            f.close()
            os.chdir(HOME)
            print(f"[DONE WITH] {user}")
            release_socket(conn, server_port)
            return

        elif func_handled.lower() == "close":
            loop = False
            release_socket(conn, server_port)


def encode(conn, addr, user):
    if not os.path.isdir("received"):
        os.mkdir("received")
    if not os.path.isdir(
            "received" + os.sep + f"{user}"):  # Creazione di una cartella dove mettere tutti i file inviati da un IP
        os.mkdir(
            "received" + os.sep + f"{user}")  # TODO: aggiornarlo per user e non per IP, chiedendo il login al client

    connected = True
    while connected:
        filename = conn.recv(BUFFER_SIZE).decode()
        print(f"\tJUST ARRIVED {filename}")
        path_file = f"{HOME}received{os.sep}{user}{os.sep}{filename}"
        with open(path_file, "wb") as f:
            data = conn.recv(BUFFER_SIZE)
            while data:
                f.write(data)
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
        f.close()
        if not os.path.isdir("encoded"):
            os.mkdir("encoded")
        if not os.path.isdir(
                "encoded" + os.sep + f"{user}"):  # Creazione di una cartella dove mettere i file elaborati di un IP
            os.mkdir("encoded" + os.sep + f"{user}")  # TODO: aggiornarlo per user e non per IP

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(compress_video, f"{filename}", str(user), conn)
            filesize = future.result()
        # filesize = compress_video(filename, str(user), conn)
        conn.send((f"{filename}" + SEP + f"{filesize}").encode(encoding=encoding))
        path_file = f"{HOME}encoded{os.sep}{user}{os.sep}{filename}"
        with open(path_file, 'rb') as f:
            frames = f.read(BUFFER_SIZE)
            while frames:
                conn.send(frames)
                frames = f.read(BUFFER_SIZE)
            f.close()
            print(f"[DONE WITH] {addr}")
            clear_shadows(filename, str(user))
            connected = False
    # conn.close()


def clear_shadows(filename, user, folder=f"{HOME}received"):
    folder = folder + os.sep + user
    print(f"\t\t{folder}\t {filename}")
    os.chdir(folder)
    os.remove(os.path.join(folder, filename))
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
    os.chdir(HOME)
    return True


def calc_filesize(filename, user, folder=f"{HOME}encoded"):
    folder = folder + os.sep + user
    print(f"\t\t{folder}\t {filename}")
    os.chdir(folder)
    filesize = os.path.getsize(os.path.join(folder, filename))
    os.chdir(HOME)
    return filesize

# TODO v_bitrate, preset, v_codec, a_bitrate, a_codec
def compress_video(filename: str, user: str, conn, bitrate: int = 1800, threads: int = 0, preset: int = 9):
    print(f"\tTo compress: {filename}")
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
    print(f"\n\t{path}\n\t{filename}")
    cmd = f"ffmpeg -i {path} -b:v {bitrate}k -c:v libx264 -threads {threads} -preset {preset} {output}"
    print(f"{cmd}")
    result = subprocess.Popen(cmd, shell=True)
    # print("\n\n\n\n",result.poll(),"\n\n\n\n")
    while result.poll() is None:
        # print("Processing:", f"{result.poll()}")
        time.sleep(10)
        conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # TODO Keep alive non funziona
    filesize = os.path.getsize(os.path.join('%sencoded/%s', '%s'.replace(" ", "\\")) % (HOME, str(user), str(filename)))
    return filesize


########################## L O G I N   F U N C T I O N S #############################
def register_user(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding=encoding)
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        users = dict()

    if user == '' or pwd == '':
        # "EMPTY FIELD" ERROR CODE -2
        return -2

    if user not in users.keys():
        users[user] = dict()
        users[user]['pwd'] = pwd
    else:
        # "ALREADY IN USE" ERROR CODE -1
        # UTENTE GIÀ ESISTENTE
        return -1

    js_file = open("auth.json", 'w', encoding=encoding)
    json.dump(obj=users, fp=js_file, indent=2)
    js_file.close()
    return 0


def login(user, pwd):
    try:
        js_file = open("auth.json", 'r', encoding=encoding)
        users = json.load(js_file)
        js_file.close()
    except FileNotFoundError:
        # "PLEASE FIRST REGISTER YOUR USER" ERROR CODE -1
        return -1

    if user not in users.keys():
        # "WRONG USER" ERROR CODE -2
        return -2
    elif users[user]['pwd'] == pwd:
        return 0
    else:
        # "WRONG PASSWORD" ERROR CODE -3
        return -3


if __name__ == '__main__':
    main()
