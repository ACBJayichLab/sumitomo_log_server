"# sumitomo_log_server" 
Uses this library:
https://pypi.org/project/sumitomo-f70/#files

# To set up:
* Verify your compressor has a recent enough firmware for serial communication 
* Make a DB-9 cable that connects **ONLY** pin 2 -> pin 3 & pin 3 -> pin 2
* Attach compressor via DB-9 cable and rs232-usb adapter
* At the top folder of the repo run:
  
```
python3 -m venv venv
.\venv\Scripts\activate    <-This will need to be run any time you launch the server
python -m pip install loguru dash plotly pandas sumitomo-f70
```

* Configure the parameters in the sumitomoF70_log_server.py file for your specifc computer
* Within the virtual environment, run python sumitomoF70_log_server.py
* The server should now be available at local host port 8050.
* If you want the server to be available outside of local, you will need to go to windows firewall -> advanced -> new rule -> open port 8050
