 Copyright 2017 Jon Stephan

    This file is part of ChessViz.

    ChessViz is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ChessViz is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ChessViz.  If not, see <http://www.gnu.org/licenses/>.

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
 - python3-imaging
 - python3-imaging-tk
 - python3-setuptools
 
Known bugs:
- some .pgn files fail with something like "UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 405: character maps to <undefined>".
    workaround:  open the file in vim and type: :%s/\%x81//g  , then save

Windows install might work with python download, you probably have to install python3-imaging
cygwin install:
- Select python3, python3-tkinter, python3-setuptools, git, python3-imaging, python3-imaging-tk, xinit
- $ easy_install-3.4 python-chess
- $ git clone <URL>
- $ cd chess_viz
- $ startxwin &
- $ export $DISPLAY=:0
- $ python3 chess_viz.py

- click on "ReadData"
- click "Down" to display the 2nd move.
- click a square to descend down to that move.
- click "top" to return to the first move
- click "SaveImage" to save a jpg image of the grid
- click "ConvertPGN" to read in a .pgn file of chess games and save in the ChessViz database format
 