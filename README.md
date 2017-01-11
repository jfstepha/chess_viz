Requirements:
 - X11:
    - linux: you probably already have it
    - windows: wait... do you really need this? 
 - python 3:
    - linux: sudo apt-get install python3
    - windows: 
 - python-chess:   
    - linux: sudo pip install python-chess
    - windows: in a cmd 
 - tkinter:   
    - sudo apt-get install tkinter
    - I installed for cywin, but for standalone???
Known bugs:
- some .pgn files fail with something like "UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 405: character maps to <undefined>".
    workaround:  open the file in vim and type: :%s/\%x81//g  , then save
 