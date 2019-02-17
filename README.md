# YOUTUBE SCRIPTS COLLECTION

Collection of scripts used to perform various operations on Youtube.
Included are also collections of working youtube links.
Note that Ctrl+C interrupts only the current conversion but not the whole process in those scripts - use CTRL+Z or kill from another terminal.


## REQUIREMENTS

Required are **youtube credentials** (to be saved as **youtube-scripts/client_secretst.json**). See here to find out how to get credentials : https://developers.google.com/youtube/analytics/registering_an_application#Create_OAuth2_Tokens

Note that on the first execution you may also be required to login on youtube. An authentication json file will be saved locally and you will have to execute the script a second time.


## SCRIPTS DESCRIPTION

The scripts are under the directory **youtube-scripts** and should be executed from that directory.


### DOWNLOADING VIDEOS

**download_videos.py** is used to download the videos from a mongo repository created in the repository musicblogs https://github.com/diegoami/musicblogs-scripts-PY

Obviously, it is required to install the related codecs.

```
python download_videos.py --blogId 556901760723185848  --outDir ~/musicvideos/southslavic
```

### EXTRACTING SOUNDS FROM VIDEOS


**convert_to_audios.py** extracts the audio file from the videos in a specific directory (here *~/musicvideos/russian* ) and saves them as mp3 files only with sound to another directory (here *~/musicaudios/russian*)

Requires FFMMPEG. On Ubuntu :  *sudo apt-get install ffmpeg*

```
python convert_to_audios.py --inputDir ~/musicvideos/russian  --outDir ~/musicaudios/russian
```

### DOWNLOAD SUBTITLES

**download_subtitles.py** is used to download subtitles from videos, if they are available on Amara. It tries to keep the names consistent with the video names, so programs like VLC find the subtitles automatically. This will download subtitles from *russian/subtitles.json* into *~/musicvideos/russian*

```
python download_subtitles.py --workDir=russian --inputFile subtitles.json --outDir ~/musicvideos/russian --language ru
```

--start and --end are optional to retrieve videos from *start* to *end* in the inputFile

### SAVE LIKED VIDEOS


**save_liked_videos.py** is used to retrieve the list of videos you liked on youtube. For instance below you save them to *russian/liked.json* and limit the search only to the first page

```
python save_liked_videos.py --workDir=russian --maxCount=1
```

### RECOMMEND VIDEOS

**recommend_videos.py** is used to retrieve recommended videos based on the videos you liked on Youtube. Here it saves recommended videos to *russian/recommended.json* taking into account the videos you liked in *russian/liked.json*.
Other parameters are accepted, such as *excludedFile*, *ignoredFile* and so on.
I wrote this script because I did not like the recommendation system on youtube, as it bases on your chronology and not on the videos you liked.
Later on I managed to make it work creating separate accounts for each "mood" - so I am not actually using this script any longer.

```
python recommend_videos.py --workDir=russian --maxCount=3 --inputFile=liked.json  --recommendedFile=recommended.json
```

