mlbviewer-remote
================

A web-based remote for mlbviewer. Useful to control mlbviewer from your phone or
tablet with mlbviewer running on a computer connected to your tv.

Requirements
------------
 - python2.7
 - flask

Requires mlbviewer: http://sourceforge.net/projects/mlbviewer/ and its
dependencies.

Usage
-----
Execute 'start_remote' from the command line to start the application. On the
first run, you will be asked to provide the path to mlbviewer and mplayer. The
application will then be started and can be reached on http://<your-ip>:5000.
The remote control website will list all available games (corrected for your
timezone). Click on one to start watching it. Clicking on the game your watching
will stop it.

The PATH environment variable is prepended with the path to mplayer that you
provided. This allows you to use alternative players, such as omxplayer that
comes with Raspbian on the Raspberry Pi (use the mplayer executable provided in
bin-omxplayer) or the "null-player" that pipes to /dev/null (use the mplayer
executable provided in bin-null).

Execute 'start_mlbviewer' to launch mlbviewer. Use this to set up the mlbviewer
configuration and to test your mplayer executable.
