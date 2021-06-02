# Calcolatori
### Features
Il nostro applicativo è un compressore ffmpeg client-server con possibilità di scelta del preset di compressione. Supporta multithreading per encoding concorrenti e permette di eseguire uno streaming su piattaforme RTMP (YouTube e Twitch) previa configurazione di indirizzo e chiave. E' stato creato un sistema di registrazione utente in chiaro per poter indicizzare i file compressi nel server ed eseguire download e/o streaming dei file personali in base al preset scelto nel proprio file di configurazione utente.




# Reti_Di_Calcolatori.md

###*Referal Links*

`<link>` :<https://github.com/MatteoFasulo/Calcolatori/blob/main/server_lastest.py>

# Libraries

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
# Dependencies

[Python 3.9.X]
---
# PyPi

```sh
$ pip install tqdm
```

----
# Functions:                

- Server:
         
| Function                   | Description                    |
| -------------------------- | ------------------------------ |
| `def main()`                        | **rappresenta la socket TCP principale su cui ogni client si connette prima di essere instradato sulla sua socket personale**|
| `def assign_socket()`               | **crea una nuova socket prendendo una porta disponibile nel nostro sistema a coda, notifica il client e chiude la vecchia connessione**|
| `def release_socket()`              | **chiude la connessione attuale e restituisce la porta al sistema a coda per un nuovo utente**|
| `def tcp_socket()`                  | **instaura una connessione tcp e gestisce tutto il mapping degli argument per eseguire ogni specifica funzione richiesta**|
| `def encode()`                      | **gestisce la compressione video per utenti concorrenti**|
| `def clear_shadow()`                | **rimuove i file nativi dopo che essi sono stati compressi risparmiando spazio sul server**|
| `def compress_video()`              | **comprime il video tramite ffmpeg in un sottoprocesso shell**|

----

- Client:
- 
| Function      | Description                    |
| ------------- | ------------------------------ |
| `def register_user()`   | **fase di registrazione per l'utente**|
| `def login()`      | **login dell'utente tramite user e password**|
| `def fetch_port()`   | **permette il corretto funzionamento del sistema di assegnazione di socket-porta sul client**|
| `def send_file()`   | **ricezione del file inviato dal client e stampa un messaggio di avvenuta ricezione del file**|
| `def stream_specific()`   | **preso uno dei file caricati dall'utente, grazie a questa funzione viene streammato a video**|
| `def alter_config()`   | **permette di modificare il file di configurazione dell'utente**|

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
