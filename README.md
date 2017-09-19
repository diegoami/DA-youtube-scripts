# YOUTUBE SCRIPTS COLLECTION

Collection of scripts used to perform various operations on Youtube.
Included are also collections of working youtube links.


## REQUIREMENTS

Required are **youtube credentials** (to be saved as **youtube-scripts/client_secrets_yt.json**).

Note that on the first execution you may also be required to login on youtube. An authentication json file will be saved locally and you will have to execute the script a second time.

For the Amara script, also an **amara Api-key** is required (See **amara_env_sample.py** )

An environment containing the libraries listed in **youtube-scripts.yml** is required (anaconda is preferred). Note that some libraries listed may be redundant.

## JSON FILE FORMAT

The format of the lists of the youtube videos you want to download, in the json format, is below. The key is the _youtube identifier_, the one which is at the end of the youtube URL. In the case of the first video below : https://www.youtube.com/watch?v=3lhzk9VTTUA

```

{"3lhzk9VTTUA": "Giulia Luzi - Paracadute (Official Video)", "7QEJDQlzGr0": "Bianca Atzei - Abbracciami perdonami gli sbagli", .... }

```

Note that that filename (withouth path) specified as *inputFile* should be in the directory specified as *workDir*.

## SCRIPTS DESCRIPTION

The scripts are under the directory **youtube-scripts** and should be executed from that directory.


### DOWNLOADING VIDEOS

**download_videos.py** is used to download the videos you listed in a json file, in the format specified above. For instance, in this case the files listed in *russian/liked.json* will be downloaded to *~/musicvideos/russian*

```
python download_videos.py --workDir=russian --inputFile liked.json --outDir ~/musicvideos/russian
```

--start and --end are optional to retrieve videos from *start* to *end* in the inputFile

### EXTRACTING SOUNDS FROM VIDEOS


**convert_to_audios.py** extracts the audio file from the videos in a specific directory (here *~/musicvideos/russian* ) and saves them as mp3 files only with sound to another directory (here *~/musicaudios/russian*)

```
python convert_to_audios.py ---inputDir ~/musicvideos/russian  --outputDir ~/musicaudios/russian
```


### DOWNLOAD SUBTITLES

**download_subtitles.py** is used to download subtitles from videos, if they are available on Amara. It tries to keep the names consistent with the video names, so programs like VLC find the subtitles automatically. This will download subtitles from *russian/subtitles.json* into *~/musicvideos/russian*

```
--workDir=russian --inputFile subtitles.json --outDir ~/musicvideos/russian --language ru
```

--start and --end are optional to retrieve videos from *start* to *end* in the inputFile

### SAVE LIKED VIDEOS


**save_liked_videos.py** is used to retrieve the list of videos you liked on youtube. For instance below you save them to *russian/liked.json* and limit the search only to the first page

```
python save_liked_videos.py --workDir=russian --maxCount=1
```

### RECOMMEND VIDEOS

**recommend_videos.py** is used to retrieve recommended videos based on the videos you liked on Youtbe. Here it saves recommended videos to *russian/recommended.json* taking into account the videos you liked in *russian/liked.json*.
Other parameters are accepted, such as *excludedFile*, *ignoredFile* and so on.
I wrote this script because I did not like the recommendation system on youtube, as it bases on your chronology and not on the videos you liked.
Later on I managed to make it work creating separate accounts for each "mood" - so I am not actually using this script any longer.

```
python recommend_videos.py --workDir=russian --maxCount=3 --inputFile=liked.json  --recommendedFile=recommended.json
```

