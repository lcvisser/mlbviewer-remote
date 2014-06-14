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
application will then be started and can be reached on http://<local-ip>:5000.

The remote control website will list all available games (corrected for your
timezone). Click on one to start watching it. Clicking on the game your watching
will stop it.

The remote uses mlbplay (part of mlbviewer). This means that your mlbviewer
settings will be honored (e.g. speed and nexdef options). If you have set
favorite or video-follow teams, these teams' broadcast will be shown. Otherwise,
the home team's broadcast is shown.

Execute 'start_mlbviewer' to launch mlbviewer. Use this to set up the mlbviewer
configuration and to test your mplayer executable.

Technical details
-----------------
The PATH environment variable is prepended with the path to mplayer that you
provided. This allows you to use alternative players, such as omxplayer that
comes with Raspbian on the Raspberry Pi (use the mplayer executable provided in
bin-omxplayer) or the "null-player" that pipes to /dev/null (use the mplayer
executable provided in bin-null).

Disclaimer
----------
This application is meant solely as a remote to mlbviewer, it does not provide
any functionality by itself. Its intention is to make watching games easy within
the comfort of your home. Please make sure that the application is only
accessible to your home network, and do not unintentionally expose it to the
outside world.

The team logos are shown in the game listing for your convencience, but they are
trademarked by MLBAM and are not part of this package; they are linked from the
MLBAM website. It is the author's belief that linking to these logos does not
violate the terms of use, as long as the application is used only within your
own home.

Access to game streams requires a mlb.tv account. 
