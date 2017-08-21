# RECOMMENDING AND RETRIEVING VIDEOS

Collection of scripts used to find out videos from youtube, download them with subtitles
Included are also collections of working youtube links. Required are youtube credentials (client_secrets_yt.json) and an amara Api-key (amara_env.py).
Scripts made for my specific use case and probably not reusable

* save_liked_videos.py is used to retrieve the list of videos liked on youtube. For instance

```
python save_liked_videos.py --workDir=russian --inputFile liked.json --outDir /home/diegoami/musicvideos/russian
```

* analyze_liked_videos.py is use to retrieve recommended videos based on the videos you liked. Other files are used, such as excluded and so on

```
python analyze_liked_videos.py --workDir=russian --maxCount=3 --inputFile=liked.json  --recommendedFile=recommended.json
```

* download_liked_videos.py is used to download the videos you liked

```
python download_liked_videos.py --workDir=russian --inputFile liked.json --outDir /home/diegoami/musicvideos/russian
```

* download_subtitles.py is used to download subtitles for your videos, if they are available on Amara. It tries to keep the names consistent with the video names, so programs like VLC find the subtitles automatically



