# youtube.py
#
# Gary Chen
# 2018/04/14
#
# This file scrapes the search results and constructs a network based on 
# their similarity using Youtube Data API.
#
# Usage example:
# python youtube.py --videoid='<video_id>' --text='<text>'

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from graph_tool.all import *

ORDER = ["date", "rating", "relevance", "title", "viewCount"]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-discoverydocument.json", "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText",
    maxResults=100,
  ).execute()

  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("Comment by " + author + ": " + text)

  return results["items"]


# Call the API's comments.list method to list the existing comment replies.
def get_comments(youtube, parent_id):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText",
  ).execute()

  for item in results["items"]:
    author = item["snippet"]["authorDisplayName"]
    text = item["snippet"]["textDisplay"]
    print("Comment by " + author + ": " + text)

  return results["items"]

# Call the API to search with keyword.   
def search_list_by_keyword(youtube, keyword, nextpage, ordering):
  response = youtube.search().list(
    part="snippet",
    maxResults=50,
    q=keyword,
    type='',
    pageToken=nextpage,
    order=ordering
  ).execute()
  print response["pageInfo"]
  return response

# Call the API's video.list method to list the video's tags and id.
def video_tags_by_id(youtube, videoid):
  response = youtube.videos().list(
    part="snippet",
    id=videoid
  ).execute()
  
  return response["items"][0]["id"], response["items"][0]["snippet"]["tags"]

class VideoGraph:
  G = Graph(directed=False)
  # create property maps
  v_id = G.new_vertex_property('string') # record video id
  v_tag = G.new_vertex_property('vector<string>') # record tags of the video
  # make property maps internal
  G.vertex_properties["id"] = v_id
  G.vertex_properties["tag"] = v_tag
  id_dict = {}
  
  THRESHOLD = 3
  
  def __init__(self):
    pass
  
  def _similarity(self, a, b):
    return len(set(self.v_tag[a]).intersection(self.v_tag[b]))
    
  def _add_edge(self, index):
    for node in self.G.vertices():
      if node != index:
        if self._similarity(index, node) >= self.THRESHOLD:
          self.G.add_edge(index, node)
    
  def add_vertex_edge(self, id, tags):
    if id not in self.id_dict.keys():
      index = self.G.add_vertex()
      self.v_id[index] = id
      print "index: {0}\r".format(index)
      try:
        self.v_tag[index] = tags
        self.id_dict[id] = index
        self._add_edge(index)
      except:
        self.G.remove_vertex(index)
    
    
  def save(self, filename):
    self.G.save(filename)

  def inf(self):
    print("number of vertex: ", self.G.num_vertices())
    print("number of edge: ", self.G.num_edges())

if __name__ == "__main__":
  # The "query" option specifies the keyword that will be used to search.
  argparser.add_argument("--query",
    help="Required; keyword that will be used search.")
  # The "size" option specifies the number of search result and hence the
  # size of constructed network.
  argparser.add_argument("--size",
    help="Required; the number of search and hence the size of constructed network.")
  args = argparser.parse_args()

  if not args.query:
    exit("Please specify query using the --query= parameter.")
  if not args.size:
    exit("Please specify size using the --size= parameter.")

  youtube = get_authenticated_service(args)
  graph = VideoGraph()
  
  # All the available methods are used in sequence just for the sake of an example.
  try:
  #for a in range(1):
    print "for"
    for order in ORDER:
      nextpage = None
      for search in range(int(args.size) // 50):
        try:
          response = search_list_by_keyword(youtube, args.query, nextpage, order)
          nextpage = response["nextPageToken"]
          for i, video in enumerate(response["items"]):
            try:
              id, tags = video_tags_by_id(youtube, video["id"]["videoId"])
              graph.add_vertex_edge(id, tags)
            except:
              pass

        except:
          continue
  except (RuntimeError, TypeError, KeyError) as e:
    graph.inf()
    graph.save(args.query + "_" + args.size + "_temp.gt")
    print "Error:", e
  else:
    graph.inf()
    graph.save(args.query + "_" + args.size + ".gt")
    print "Done."
