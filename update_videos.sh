#!/bin/bash

update_videos () {
    echo $1
    rm youtube-scripts/update_videos_in_dir.py-oauth2.json
    python youtube-scripts/update_videos_in_dir.py --workDir youtube-scripts/$1 --outDir /media/diego/Data/musicvideos/$1
}

update_videos 'italian'
update_videos 'russian'
update_videos 'polish'
update_videos 'southslavic'
update_videos 'romanian'
update_videos 'french'
update_videos 'easteurope'
