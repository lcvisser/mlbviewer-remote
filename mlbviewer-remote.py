# -*- coding: utf-8 -*-

# Copyright (c) 2014 Ludo Visser
#
# mlbtv-control is distributed under the terms and conditions of the MIT
# license. The full license can be found in the LICENSE file.


import datetime
import flask

from MLBviewer import MLBConfig, MLBSchedule, MLBSession
from MLBviewer import MediaStream
from MLBviewer import TEAMCODES

## Set up mlbviewer
#TODO: this needs to be loaded from user input
MLB_CONFIG_FILE = '/Users/ludo/.mlb/config'
MLB_DEFAULTS = {'video_follow': [],
                'audio_follow': [],
                'blackout': [],
                'favorite': 'DET'}
TZ_OFFSET = 1

# Load config
#TODO: this should probably be done on a per-session basis
config = MLBConfig(MLB_DEFAULTS)
config.loads(MLB_CONFIG_FILE)

# Start MLB.TV session
session = MLBSession(
    user=config.data['user'],
    passwd=config.data['pass'],
    debug=config.data['debug'])
session.getSessionData()

## Helper functions
def get_schedule(ymd, config):
    schedule = MLBSchedule(ymd_tuple=ymd)
    listing = schedule.getListings(config.data['speed'], config.data['blackout'])
    return listing

## Application
# Instantiate application
app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # Determine requested day
    schedule_date = datetime.date.today()
    offset = flask.request.args.get('offset')
    if offset is not None:
        try:
            offset = int(offset)
        except ValueError:
            offset = 0
    else:
        offset= 0
    delta = datetime.timedelta(days=offset)
    schedule_date += delta
    
    # Determine if a game is being watched
    watching = flask.request.args.get('game')
    if watching is not None:
        watching = int(watching)
    else:
        watching = -1
    
    # Set navigation parameters
    nav = {}
    nav['prev'] = offset - 1
    nav['next'] = offset + 1
    
    # Get game listing for requested day
    ymd = (schedule_date.year, schedule_date.month, schedule_date.day)
    schedule = get_schedule(ymd, config)
    
    # Parse game data
    games = []
    for index, gamedata in enumerate(schedule):
        away = gamedata[0]['away']
        home = gamedata[0]['home']
        game = {}
        game['index'] = index
        game['away_code'] = away
        game['away_name'] = TEAMCODES[away][1]
        game['home_code'] = home
        game['home_name'] = TEAMCODES[home][1]
        game['watching'] = 1 if index == watching else 0
        games.append(game)
    
    # Render template
    context = {}
    context['nav'] = nav
    context['date'] = schedule_date
    context['games'] = games
    return flask.render_template('games.html', **context)


@app.route('/watch/<year>/<month>/<day>/<index>/')
def watch(year, month, day, index):
    # Get game listing for requested day
    ymd = (int(year), int(month), int(day))
    schedule = get_schedule(ymd, config)
    
    # Get stream
#     stream = MediaStream(
#         schedule[int(index)][2][0],
#         session=session,
#         cfg=config,
#         start_time=None)
#     
    
    # Redirect to gameday index
    today = datetime.datetime.today()
    gameday = datetime.datetime(year=int(year), month=int(month), day=int(day))
    delta = gameday - today
    return flask.redirect('/index?offset=%i&game=%i' % (delta.days+TZ_OFFSET, int(index)))


@app.route('/stop/<year>/<month>/<day>/')
def stop(year, month, day):
    # Redirect to gameday index
    today = datetime.datetime.today()
    gameday = datetime.datetime(year=int(year), month=int(month), day=int(day))
    delta = gameday - today
    return flask.redirect('/index?offset=%i' % (delta.days+TZ_OFFSET))


## Start application
app.run(debug=True)