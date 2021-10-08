from apiclient.discovery import build
import csv, json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def build_service(filename):
    with open(filename) as f:
        key = f.readline()

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 developerKey=key)

def get_response(service,videoID):
    return service.commentThreads().list(
        part='snippet',
        maxResults=100,
        textFormat='plainText',
        order='relevance',
        videoId=videoID
    ).execute()

def filter_json(response):
    top_level_comments = []

    for item in response["items"]:
        top_level_comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"].replace("\n",""))

    return top_level_comments

def iterate_process_videos(video_ids_csv,service):
    all_info_dict = {}

    for video_id, title in video_ids_csv:
        response = get_response(service,video_id)
        top_level_comments = filter_json(response)

        all_info_dict[video_id] = {
            "title": title,
            "top_level_comments": top_level_comments
        }

    return all_info_dict

def main(video_list_title):

    service = build_service('./resources/api_cred.json')

    with open("./resources/video_ids_"+video_list_title+".csv") as csv_file:
        video_ids_csv = csv.reader(csv_file)
        all_video_dict = iterate_process_videos(video_ids_csv,service)

    with open("./resources/collected_comments_"+video_list_title+".json", 'w') as file:
        json.dump(all_video_dict , file)

#main("corey_israel")
#main("corey_palestinian")
main("corey_whole")


