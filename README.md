# Calcolatori
### *Features*
Il nostro applicativo è un compressore ffmpeg.....




# *Reti_Di_Calcolatori.md*

---

**Table of Contents**

[TOCM]

[TOC]

#*Libraries*

---

###*Referal Links*

`<link>` :<https://github.com/MatteoFasulo/Calcolatori/blob/main/server_lastest.py>

| Name | Description |
| ------------- | ------------------------------ |
| [OS] | Used for miscellaneous operating system operations
| [Time] | Time is a package that implements time in python script
| [Tqdm]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable)
| [Socket] | This module provides access to the BSD socket interface
| [Subprocess] | The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
| [Threading] | This module constructs higher-level threading interfaces on top of the lower level _thread module
| [Json] | Json exposes an API familiar to users of the standard library marshal and pickle modules
| [Tkinter] | The tkinter package (“Tk interface”) is the standard Python interface to the Tk GUI toolkit
| [Configparser] | Use this to write Python programs which can be customized by end users easily

---
#*Dependencies*

---

[Python 3.9.X]
- OS
| import os  |

- Time
| import time  |

- Tdqm
| import tqdm |

- Socket
| import socket |

- Subprocess
| import subprocess |

- Threading
| import threading |

- Json
| import json  |

- Argparse
| import argparse  |

- Tkinter
| import TK from tkinter  |

- Tkinter.filedialog
| import askopenfilename from tkinter.filedialog  |

- Configparser
| import configparser  |

- Client_latest
| import client_latest  |

----
                    
###*Tables*
- Principal Function:
                    

| Function name | Description                    |
| ------------- | ------------------------------ |
| `def main()`      | **funzione cardine che esegue il programma **|
| `def main()`   | **mette in ascolto il server sulla porta di defeault; attiva la connessione**|
| `def assign_socket()`      | **richiesta al client di una nuova porta; mette in ascolto il server con l'IP e chiude l'assign**|
| `def release_socket()`   | **chiude la connessione e restituisce la porta**|
| `def tcp_socket()`      | **instaura una connessione tcp; fa un controllo sullo status della registrazione; scarica il file e chiude la connessione**|
| `def encode()`   | **crea una cartella dove mettere tutti i file inviati da un IP e li aggiorna per utente non per user previa registrazione client; crea una cartella dove mettere i file elaborati di un IP e li aggiorna per utente non per IP**|
| `def clear_shadow()`      | **stampa la cartella con il nome del file**|
| `def calc_filesize()`   | **preso in input il filename e la cartella, restituisce la grandezza del file**|
| `def compress_video()`      | **presa in input la stringa del filename, la comprime e restituisce il filesize**|
| `def register_user()`   | **fase di registrazione**|
| `def login()`      | **login dell'utente tramite user e password**|
| `def fetch_port()`   | **è l'equivalente di assign però lato server**|
| `def connect_to_server()`      | **comunica con assign al fine di connettersi al server**|
| `def send_file()`   | **ricezione filename, lo scarica e printa un messaggio di avvenuta ricezione del file**|
| `def list_files()`      | **prende in input la conn. , invia una lista di file e restituisce quest'ultimo**|
| `def stream_specific()`   | **preso uno dei file caricati dall'utente, grazie a questa funzione viene streammato a video**|
| `def delete_my_file()`      | **preso un file da quelli scaricati, elimina il mio file**|
| `def download_my_file()`   | **il file dopo essere stato inviato e ricevuto, viene scaricato**|
| `def edit_cfg()`   | **permette di modificare il file di configurazione dell'utente**|
| `def print_welcome()`   | **printa welcome + im menù inziale**|
| `def print_menu()`   | **printa il menù nel quale l'utente sceglie quale azione esguire**|
| `def print_submenu_1()`   | **sottomenù relativo al menù precedente nel quale vengono illustrate le azioni**|
| `def print_submenu_2()`   | **scegliere cosa comprimere e in che modo comprimere un file audio o video("ultrafast",...,"placebo")**|
| `def print_submenu_streaming()`   | **streamma il sottomenù**|
| `def center_title()`   | **restituisce il titolo**|
| `def handle_choice_menu()`   | **restituisce la scelta fatta dall'utente**|

----

###*End*


[Python 3.9.X]: <https://www.python.org/downloads/release/python-390/>
[OS]: <https://docs.python.org/3/library/os.html>
[Time]: <https://docs.python.org/3/library/time.html> 
[Tqdm]: <https://pypi.org/project/tqdm/>
[Socket]: <https://docs.python.org/3/library/socket.html> 
[Subprocess]: <https://docs.python.org/3/library/subprocess.html>
[Threading]: <https://docs.python.org/3/library/threading.html>
[Json]: <https://docs.python.org/3/library/json.html>
[Tkinter]: <https://docs.python.org/3/library/tkinter.html> 
[Configparser]: <https://docs.python.org/3/library/configparser.html>
