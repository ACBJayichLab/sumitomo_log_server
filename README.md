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

Activation each time (you could put this in a .bat for speed)
```
.\venv\Scripts\activate
python sumitomoF70_log_server.py
```

* Configure the parameters in the sumitomoF70_log_server.py file for your specifc computer
* Within the virtual environment, run python sumitomoF70_log_server.py
* The server should now be available at local host port 8050.
* If you want the server to be available outside of local, you will need to go to windows firewall -> advanced -> new rule -> open port 8050


This is making use of this module for serial communication:
https://pypi.org/project/sumitomo-f70/#files

If the DB9 cable connects more than pin 2/3, then the compressor will fail to boot after a power cycle (presumably due to a ground loop). This can be worked around either by modifying the cable or by attaching the cable after the compressor is already powered on.

Sometimes (exactly once in my experience) Dash can fail to close while the rest of the python closes. When this happens, on subsequent runs the program will still succeed in polling the equipment, but the front-end will fail to update/crash. This can be fixed by manually killing the Python process (or a restart).
