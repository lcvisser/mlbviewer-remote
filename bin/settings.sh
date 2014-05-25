#!/bin/bash

function load_settings() {
    local SETTINGS_FILE="$HOME/.mlbviewer_remote.settings"

    if [ ! -f $SETTINGS_FILE ]
    then
        # Settings not found; create it
        echo "# Created on $(date)" > $SETTINGS_FILE

        # Ask user for path to mlbviewer
        read -e -p "path to mlbviewer: " mlbviewer_path
        while [ ! -d "$mlbviewer_path/MLBviewer" ]
        do
            # Ask user for path to mlbviewer
            read -e -p "mlbviewer not found in $mlbviewer_path; path to mlbviewer: " mlbviewer_path
        done
        echo "$mlbviewer_path" >> $SETTINGS_FILE

        # Ask user for path to mplayer
        read -e -p "path to mplayer: " mplayer_path
        while [ ! -x "$mplayer_path/mplayer" ]
        do
            # Ask user for path to mplayer
            read -e -p "mplayer executable not found in $mplayer_path; path to mplayer: " mplayer_path
        done
        echo "$mplayer_path" >> $SETTINGS_FILE
    fi

    # Read settings from file
    unset $MLBVIEWER_REMOTE_SETTINGS
    while read setting
    do
        if [[ $setting != '#'* ]]
        then
            path=$(cd $setting; pwd)
            export MLBVIEWER_REMOTE_SETTINGS=$path:$MLBVIEWER_REMOTE_SETTINGS
        fi
    done < $SETTINGS_FILE
}

