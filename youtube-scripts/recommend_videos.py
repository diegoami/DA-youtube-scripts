from youtube3 import YoutubeClient
from blogspotapi import BlogRepository
import json
from oauth2client.tools import argparser
import re
import os
from itertools import groupby
from operator import itemgetter
from pymongo import MongoClient

def process_videos( youtube_client , blog_repository, maxCount=5, maxValues=None):
    recommended_videos = set()
    recommendation_pairs = []
    all_video_ids = [blog_post.videoId for blog_post in blog_repository.posts_map.values()]
    max_index = 0
    for post_id, blog_post in blog_repository.posts_map.items():
        video_id = blog_post.videoId
        title = blog_post.title


        print("Now processing %s, %s" % (video_id, title))
        for relatedvideos in youtube_client.iterate_related_videos(video_id, maxCount):
            for item in relatedvideos['items']:
                rvideoId, rtitle = item['id']['videoId'], item['snippet']['title']
                if rvideoId not in all_video_ids :
                    recommended_videos.add((rvideoId, rtitle))
                    recommendation_pairs.append((rvideoId, video_id))
        if max_index > maxValues:
            break
        max_index += 1
    return recommended_videos, recommendation_pairs



def retrieve_recommended(youtube_client, blog_repository, **kwargs):
    recommended_videos, recommendation_pairs = process_videos(youtube_client, blog_repository, **kwargs)
    recommended_for_blog_video_groups = groupby(recommendation_pairs, itemgetter(1))
    recommended_for_blog_video = {k: [x[0] for x in vs ] for k, vs in recommended_for_blog_video_groups }
    return recommended_videos, recommendation_pairs, recommended_for_blog_video



if __name__ == "__main__":
    argparser.add_argument('--blogId')
    argparser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    args = argparser.parse_args()
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    blog_repository = BlogRepository(args.mongo_connection, args.blogId)
    client = MongoClient(args.mongo_connection)
    recommendations_database = client.recommendations
    rvs, rps, rfbvs = retrieve_recommended(youtube_client, blog_repository, maxCount=5, maxValues= 3)
    print(rv)
    print(rp)
    print(rfbv)

