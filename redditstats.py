from multiprocessing import *
import praw
from praw.handlers import MultiprocessHandler
from mongoTools import *
from pymongo import *
import datetime 
import sys
import requests

def getSubredditUsers(subreddit):
  """
  Gets all of the commenters in a certain subreddit provided by the parameter.
  """
  client = MongoClient()
  reddit = praw.Reddit(user_agent="Subreddit Recommender", handler=MultiprocessHandler())
  subreddit = reddit.get_subreddit(subreddit)
  comments = subreddit.get_comments(limit=250)
  currentUsers = allUsers(client)
  if currentUsers:
    found = [user['username'] for user in currentUsers]
  else:
    found = []
  users = []
  for comment in comments:
    if comment.author.name not in found:
      users.append({'user': comment.author.name})
  return tempBulkInsert(users, client)
  
def getComments(username):
  """
  Return the subreddits a certain user, provided by the parameter, has commented in.
  """
  try:
        client = MongoClient()
        reddit = praw.Reddit(user_agent="Subreddit Recommender", handler = MultiprocessHandler())
        user = reddit.get_redditor(username)
        subs= []
        for comment in user.get_comments(limit=250):
          if comment.subreddit.display_name not in subs:
            subs.append(comment.subreddit.display_name)
          insertSub(comment.subreddit.display_name, client)
        return insertUser(username, subs, client)
  except requests.exceptions.HTTPError as exception:
    print(exception)
    pass
  
def getSubreddits():
  """
  Returns the 'all' subreddit to use as a test. Feel free to change this to any subreddit of your choice. 'All' is used here because 
  it is the most vague, and has users that are more likely to be similar to the general user.
  """
  return ['all']
  
def main():
  try:
    pool = Pool(processes=(cpu_count()*6))
    subs = getSubreddits()
    pool.map(getSubredditUsers, subs)
    users = [user['user'] for user in tempUserList(MongoClient())]
    pool.map(getComments, users)
    pool.close()
  except KeyboardInterrupt:
    pool.terminate()
    sys.exit()
    
if __name__ == "__main__":
  main()
