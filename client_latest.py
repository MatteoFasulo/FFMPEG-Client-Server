"""
    Client App edited
                        """
import argparse
import os
from socket import *
import tqdm
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

serverName = "51.91.254.112"
BUFFER_SIZE = 1024 * 4
encoding = 'utf-8'


def tcp_echo_server(filename, verbose):
    print(verbose)
    serverPort = 13000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    path, filename = os.path.split(filename)
    if path != '':
        os.chdir(path)
    clientSocket.send(f"{filename}".encode(encoding=encoding))
    filesize = os.path.getsize(filename)

    print("test", f"{path}", filename, sep="\t")

    if verbose:
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as video:
        l = video.read(BUFFER_SIZE)
        while l:
            clientSocket.send(l)
            l = video.read(BUFFER_SIZE)
            if verbose:
                progress.update(len(l))
        video.close()
        clientSocket.shutdown(SHUT_WR)

    filename, filesize = clientSocket.recv(BUFFER_SIZE).decode().split("SEPARATOR")
    if not os.path.isdir("Download"):
        os.mkdir("Download")
    with open("." + os.sep + "Download" + os.sep + filename, 'wb') as f:
        if verbose:
            print("\n\n\n")
            progress.reset(total=None)
            progress = tqdm.tqdm(range(int(filesize)), f"Receiving {filename}", unit="B", unit_scale=True,
                                 unit_divisor=1024)
        while True:

            data = clientSocket.recv(BUFFER_SIZE)
            if verbose:
                progress.update(len(data))

            if not data:
                break
            f.write(data)
        f.close()
        print('Successfully get the file')
        print('connection closed')
        clientSocket.shutdown(SHUT_RDWR)


def parse_args():
    arg_error = False
    parser = argparse.ArgumentParser(description='Description of your program', exit_on_error=False)
    try:
        parser.add_argument('-f', '--target_file', help='specify file to be compressed', type=str, required=False)
    except argparse.ArgumentError:
        arg_error = True
    parser.add_argument('-v', '--verbose', help='show verbose data', action="store_true")
    args = parser.parse_args()
    if arg_error:
        args.target_file = None
    return [args.target_file, args.verbose]


def main():
    filename, verbose = parse_args()
    verbose = True
    print(filename, verbose, sep="\t")
    if filename is None:
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        print(filename, verbose, sep="\t")
        if verbose is None:
            verbose = True
    tcp_echo_server(filename, verbose=verbose)


if __name__ == '__main__':
    main()
