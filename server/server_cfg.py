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
t_sleep = 3


###################################################################

def main(c=0):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    default_port = 13000
    try:
        serverSocket.bind((IP, default_port))
        serverSocket.listen()
        print(f"[LISTENING] Server is listening on {IP}:{default_port}")
        while True:
            conn, addr = serverSocket.accept()
            thread = threading.Thread(target=assign_socket, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except OSError:
        if c < 10:
            print(f"Port {default_port} in use... retry in {t_sleep} sec <--->  {c} secs passed")
        else:
            print(f"Port {default_port} in use... retry in {t_sleep} sec <---> {c} secs passed")
        time.sleep(t_sleep)
        c += t_sleep
        main(c)


def assign_socket(conn, addr):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = availablePorts[0]

    # TODO SEND TO CLIENT
    conn.send(("new_port" + SEP + f"{server_port}").encode(encoding=encoding))
    # TODO CLOSE OLD CONNECTION
    conn.close()

    availablePorts.remove(server_port)
    try:
        serverSocket.bind((IP, server_port))
        serverSocket.listen(1)
        print(f"[LISTENING] Server is listening on {IP}:{server_port} for {addr}")
        conn, addr = serverSocket.accept()

        tcp_socket(conn, addr, server_port)
    except OSError:
        release_socket(conn, server_port)
        assign_socket(conn, addr)


def release_socket(conn, port):
    conn.close()
    availablePorts.append(port)
    return port


def tcp_socket(conn, addr, server_port):
    print(f"[NEW CONNECTION] {addr} connected.")
    os.chdir(HOME)
    user = None

    done = False
    # LISTENER and HANDLING/RESOLVE REQUEST From client
    while not done:
        args = conn.recv(BUFFER_SIZE).decode(encoding=encoding)  # PROTOCOLLO - RICEVO COMANDO ED ARGS
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
        args = conn.recv(BUFFER_SIZE).decode(encoding=encoding)  # PROTOCOLLO - RICEVO COMANDO ED ARGS
        try:
            func_handled, arg1, arg2 = map(str, args.split(SEP))
            print(f"AFTER LOGIN: {args}")
        except ValueError:
            release_socket(conn, server_port)
            return

        if func_handled.lower() == "encode":
            # thread = threading.Thread(target=encode, args=(conn, addr, user))
            # thread.start()
            print(f"[ACTIVE THREADS ENCODING] {threading.activeCount() - 1}")
            encode(conn, addr, user=user)
            done = False
            release_socket(conn, server_port)

        elif func_handled.lower() == "list_dir":
            list_file = glob.glob(HOME + "encoded" + os.sep + f"{user}" + os.sep + "*")
            if len(list_file) == 0:
                conn.send(f"{len(list_file)}{SEP}{list_file}".encode(encoding=encoding))
            files = str()
            for i in range(len(list_file)):
                files += str(list_file[i][(list_file[i].rfind(os.sep) + 1):])
                if i < len(list_file) - 1:
                    files += SEP_ADG
            conn.send(f"{len(list_file)}{SEP}{files}".encode(encoding=encoding))

        elif func_handled.lower() == "streaming":
            # TODO parametri da leggere dal config file
            release_socket(conn, server_port)
            try:
                print(f"[ACTIVE THREADS] {threading.activeCount() - 1}")
                stream.streaming(user=f"{user}", filename=f"{arg1}")
                return
            except KeyError:
                print("Key not configured for user")
                # TODO ADVERTISE CLIENT OF MISSING KEY
                return

        elif func_handled.lower() == "delete_file":
            try:
                clear_shadows(str(arg1), str(user), f"{HOME}encoded")
                conn.send(str("delete_file" + SEP + "Correctly deleted").encode(encoding=encoding))
            except FileNotFoundError:
                conn.send(str("delete_file" + SEP + "FileNotFoundError").encode(encoding=encoding))
                pass

        elif func_handled.lower() == "download_my_file":
            filename = arg1
            filesize = calc_filesize(filename, user)

            time.sleep(0.5)
            conn.send((f"{filename}" + SEP + f"{filesize}").encode(encoding=encoding))
            os.chdir(f"{HOME}encoded" + os.sep + user)
            with open(f"{filename}", 'rb') as f:
                frames = f.read(BUFFER_SIZE)
                while frames:
                    conn.send(frames)
                    frames = f.read(BUFFER_SIZE)
            f.close()
            os.chdir(HOME)
            print(f"[DONE WITH] {user}")
            release_socket(conn, server_port)
            return

        elif func_handled.lower() == "alter_config":
            handle_cfg(conn, server_port, user)

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
        filename = conn.recv(BUFFER_SIZE).decode(encoding=encoding)
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
                "encoded" + os.sep + f"{user}"):
            os.mkdir("encoded" + os.sep + f"{user}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(compress_video, f"{filename}", str(user), conn)
            print("Future:", future)
        while not future.done():
            pass
        filesize = future.result()

        #print(f"\n\n\n\n{filesize}\n\n\n\n")

        conn.send((filename + SEP + str(filesize)).encode(encoding=encoding))

        # filesize = compress_video(filename, str(user), conn)

        path_file = f"{HOME}encoded{os.sep}{user}{os.sep}{filename}"
        with open(path_file, 'rb') as f:
            frames = f.read(BUFFER_SIZE)
            while frames:
                conn.send(frames)
                frames = f.read(BUFFER_SIZE)
            f.close()
            clear_shadows(filename, str(user))
            connected = False
    # conn.close()


def clear_shadows(filename, user, folder=f"{HOME}received"):
    folder = folder + os.sep + user
    os.chdir(folder)
    os.remove(os.path.join(folder, filename))
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
    os.chdir(HOME)
    return True


def calc_filesize(filename, user, folder=f"{HOME}encoded"):
    folder = folder + os.sep + user
    os.chdir(folder)
    filesize = os.path.getsize(os.path.join(folder, filename))
    os.chdir(HOME)
    return filesize


# TODO v_bitrate, preset, v_codec, a_bitrate, a_codec
def compress_video(filename: str, user: str, conn, bitrate: int = 1600, threads: int = 0, preset: int = 6):
    # cfg = read_cfg(user)
    # TODO Finire cfg parser

    presets = {9: "ultrafast", 8: "superfast", 7: "veryfast",
               6: "faster", 5: "fast", 4: "medium", 3: "slow",
               2: "slower", 1: "veryslow", 0: "placebo"}
    preset = presets[preset]
    path = (f'"{HOME}received{os.sep}{user}{os.sep}{filename}"')
    output = (f'"{HOME}encoded{os.sep}{user}{os.sep}{filename}"')
    cmd = f"ffmpeg -i {path} -b:v {bitrate}k -c:v libx264 -threads {threads} -preset {preset} {output} -y"
    result = subprocess.Popen(cmd, shell=True)
    while result.poll() is None:
        time.sleep(2)
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


# SAVE ALWAYS IN USER DIR
def save_cfg(config, user: str):
    with open(f"{HOME}received{os.sep}{user}{os.sep}config.ini", 'w') as configfile:
        config.write(configfile)
    configfile.close()
    return True


def read_cfg(user: str):
    cfg = configparser.ConfigParser()
    try:
        open(f"{HOME}received{os.sep}{user}{os.sep}config.ini", 'r')
    except FileNotFoundError:
        os.chdir(f'{HOME}')
        print("\tSostituito!<----------------------------------------------------------")
        fin = open("config.ini", 'rb')
        data = fin.read()
        fin.close()

        if not os.path.isdir("received"):
            os.mkdir("received")
        if not os.path.isdir(f"received{os.sep}{user}"):
            os.mkdir(f"received{os.sep}{user}")
        os.chdir(f"{HOME}received{os.sep}{user}{os.sep}")

        fout = open("config.ini", 'wb')
        fout.write(data)
        fout.close()
        os.chdir(HOME)

    cfg_path = ("{}received{}{}{}{}".format(HOME, os.sep, user, os.sep, "config.ini"))
    cfg.read(cfg_path, encoding="UTF-8")
    return cfg


def list_section(user, section=None):
    cfg = read_cfg(user)
    if section is None:
        list_back = list(cfg.keys())[1:]
    else:
        list_back = list(cfg[section].keys())
    print(f"{list_back}")
    l = str()
    for i in range(len(list_back)):
        l += str(list_back[i])
        if i < len(list_back) - 1:
            l += SEP_ADG
    return l


def handle_cfg(conn, server_port, user):
    args = conn.recv(BUFFER_SIZE).decode(encoding=encoding)  # PROTOCOLLO - RICEVO COMANDO ED ARGS
    print(f"\thandle_cfg: {args}")
    try:
        func_handled, arg1, arg2 = map(str, args.split(SEP))
        cfg = read_cfg(user)
    except ValueError:
        release_socket(conn, server_port)
        raise ValueError

    if func_handled == "insert_cfg":
        arg1 = arg1.strip()
        if arg1 != "DEFAULT":
            try:
                cfg.add_section(arg1)
                save_cfg(cfg, user)
                cfg = read_cfg(user)
                back_msg = f"{arg1} inserted correctly"
            except configparser.DuplicateSectionError:
                back_msg = "preset name already exists".capitalize()
            print(back_msg)
            conn.send(f"{func_handled}{SEP}{back_msg}".encode(encoding=encoding))

    elif func_handled == "edit_cfg":
        if arg1 == "None" and arg2 == "None":  # INVIARE LISTA PRESET
            print("SEZIONE 1")
            list_preset = list_section(user)
            conn.send(f"{list_preset}".encode(encoding=encoding))
        func_handled, arg1, arg2 = unpack_args(conn, server_port)
        if arg1 != "None" and arg2 == "None":
            print("SEZIONE 2")
            sections = list_section(user, arg1)
            conn.send(f"{sections}".encode(encoding=encoding))
        func_handled, arg1, arg2 = unpack_args(conn, server_port)
        if arg1 != "None" and arg2 != "None":
            print("ELSE")
            arg3 = None
            if len(arg2.split(SEP_ADG)) != 1:
                arg2, arg3 = arg2.split(SEP_ADG)
            if arg3 is None:
                print("SEZIONE 3")
                values = cfg[arg1][arg2].strip()
                conn.send(f"{values}".encode(encoding=encoding))
                time.sleep(1)
                func_handled, arg1, arg2 = unpack_args(conn, server_port)
                print("SEZIONE 4")
                cfg.set(arg1, arg2, arg3)
                save_cfg(cfg, user)
                conn.send(f"{func_handled}".encode(encoding=encoding))
                cfg = read_cfg(user)

    elif func_handled == "delete_cfg":
        if arg1 == "None" and arg2 == "None":
            list_preset = list_section(user)
            conn.send(f"{list_preset}".encode(encoding=encoding))
            func_handled, arg1, arg2 = unpack_args(conn, server_port)
        if arg1 != "None" and arg2 == "None":
            cfg.remove_section(arg1)
            save_cfg(cfg, user)
            cfg = read_cfg(user)
            conn.send((f"{func_handled}" + SEP + "preset_deleted").encode(encoding=encoding))

    elif func_handled == "delete_val":
        if arg1 == "None" and arg2 == "None":
            list_preset = list_section(user)
            conn.send(f"{list_preset}".encode(encoding=encoding))
            func_handled, arg1, arg2 = unpack_args(conn, server_port)
        if arg1 != "None" and arg2 == "None":
            sections = list_section(user, arg1)
            conn.send(f"{sections}".encode(encoding=encoding))
            func_handled, arg1, arg2 = unpack_args(conn, server_port)
            arg3 = None
            if len(arg2.split(SEP_ADG)) != 1:
                arg2, arg3 = arg2.split(SEP_ADG)
            if arg3 is None:
                values = cfg[arg1][arg2]
                conn.send(f"{values}".encode(encoding=encoding))
                func_handled, arg1, arg2 = unpack_args(conn, server_port)
                if len(arg2.split(SEP_ADG)) != 1:
                    arg2, arg3 = arg2.split(SEP_ADG)
                    cfg.remove_option(arg1, arg2)
                    save_cfg(cfg, user)
                    cfg = read_cfg(user)
                    conn.send((f"{func_handled}" + SEP + "Content successfully deleted").encode(encoding=encoding))

    elif func_handled == "restore_def_config":
        folder = f"{HOME}received{os.sep}{user}"
        os.chdir(folder)
        os.remove(os.path.join(folder, "config.ini"))
        os.chdir(HOME)
        conn.send((f"{func_handled}" + SEP + "File successfully deleted").encode(encoding=encoding))

    cfg = read_cfg(user)
    done = False


def unpack_args(conn, server_port):
    try:
        args = conn.recv(BUFFER_SIZE).decode(encoding=encoding)
        func_handled, arg1, arg2 = map(str, args.split(SEP))
        print(f"\t{args}")
    except ValueError:
        release_socket(conn, server_port)
        raise ValueError
    return (func_handled, arg1, arg2)


if __name__ == '__main__':
    main()
