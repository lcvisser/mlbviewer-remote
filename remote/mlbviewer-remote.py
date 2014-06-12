# -*- coding: utf-8 -*-

# Copyright (c) 2014 Ludo Visser
#
# mlbtv-control is distributed under the terms and conditions of the MIT
# license. The full license can be found in the LICENSE file.


import datetime
import flask
import os
import signal
import subprocess
import sys
import time

from MLBviewer import MLBConfig, MLBGameTime, MLBSchedule, MLBSession
from MLBviewer import AUTHDIR, AUTHFILE, TEAMCODES

## Set up mlbviewer
# Bare minimum defaults for mlbviewer
MLBVIEWER_DEFAULTS = {'video_follow': [],
                      'audio_follow': [],
                      'blackout': [],
                      'favorite': []}

# Load config
config_dir = os.path.join(os.environ['HOME'], AUTHDIR)
config_file = os.path.join(config_dir, AUTHFILE)
config = MLBConfig(MLBVIEWER_DEFAULTS)
config.loads(config_file)

# Session placeholder
session = None

# Current game
watching = None
player = None


## Application
# Application instance
app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    global session
    global watching
    
    # Check if a game is being watched
    if watching is not None:
        return flask.render_template('watching.html', game=watching)
    
    # Get "today", correct for local timezone and eastern timezone
    now = datetime.datetime.now()
    gametime = MLBGameTime(now)
    t = time.localtime()
    local_zone = (time.timezone, time.altzone)[t.tm_isdst]
    local_offset = datetime.timedelta(0, local_zone)
    eastern_offset = gametime.utcoffset()
    
    # Get requested offset
    request_offset = flask.request.args.get('offset')
    if request_offset is not None:
        try:
            request_offset = int(request_offset)
        except ValueError:
            request_offset = 0
    else:
        request_offset= 0
    view_offset = datetime.timedelta(days=request_offset)
    
    # Determine request
    view_day = now + local_offset - eastern_offset + view_offset
    schedule_date = (view_day.year, view_day.month, view_day.day)
    
    # Start MLB.TV session
    if session is None:
        session = MLBSession(user=config.data['user'], passwd=config.data['pass'])
        session.getSessionData()

    # Get game listing for requested day
    schedule = MLBSchedule(ymd_tuple=schedule_date)
    listing = schedule.getListings(config.data['speed'], config.data['blackout'])
    
    # Parse game data
    games = []
    for index, gamedata in enumerate(listing):
        if gamedata[5] in ('I', 'CG'):  #TODO: can pre-game be added?
            # Game in progress or condensed game available
            away = gamedata[0]['away']
            home = gamedata[0]['home']
            game = {}
            game['away_code'] = away
            game['away_name'] = TEAMCODES[away][1]
            game['home_code'] = home
            game['home_name'] = TEAMCODES[home][1]
            games.append(game)
    
    # Set navigation parameters
    nav = {}
    nav['prev'] = request_offset - 1
    nav['next'] = request_offset + 1
    
    # Render template
    context = {}
    context['nav'] = nav
    context['date'] = view_day
    context['games'] = games
    return flask.render_template('games.html', **context)


@app.route('/watch/<year>/<month>/<day>/<home>/<away>/')
def watch(year, month, day, home, away):
    global session
    global watching
    global player
    
    # Select video stream
    fav = config.get('favorite')
    if fav:
        fav = fav[0]  # TODO: handle multiple favorites
        if fav in (home, away):
            # Favorite team is playing
            team = fav
        else:
            # Use stream of home team
            team = home
    else:
        # Use stream of home team
        team = home
    
    # End session
    session = None
    
    # Start mlbplay
    mm = '%02i' % int(month)
    dd = '%02i' % int(day)
    yy = str(year)[-2:]
    cmd = 'python2.7 mlbplay.py v=%s j=%s/%s/%s i=t1' % (team, mm, dd, yy)
    player = subprocess.Popen(cmd.split(), cwd=sys.argv[1])
    
    # Render template
    game = {}
    game['away_code'] = away
    game['away_name'] = TEAMCODES[away][1]
    game['home_code'] = home
    game['home_name'] = TEAMCODES[home][1]
    watching = game
    return flask.render_template('watching.html', game=game)


@app.route('/stop/')
def stop():
    global watching
    global player
    
    # Stop mlbplay
    if watching is not None:
        watching = None
    if player is not None:
        player.send_signal(signal.SIGINT)
        player.communicate()
        player = None
    
    # Redirect to gameday index
    return flask.redirect('/index')


## Start application
if os.path.isdir(sys.argv[1]):
    app.run(host='0.0.0.0')
else:
    print 'not a valid directory: ' + sys.argv[1]
    sys.exit(-1)
