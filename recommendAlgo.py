import math
from mongoTools import *
from pymongo import *
import redditstats
import operator 
import numpy as nump

def createVectorForUser(username):
    client = MongoClient()
    user = queryUser(username, client)
    unique = list(subreddits(client))
    vector = [0]*len(unique)
    for j in range(len(unique)):
      if unique[j]['name'] in user['subreddits']:
        vector[j] = 10
    return vector
    
def vectorDistance(firstUser, secondUser):
  firstVector = createVectorForUser(firstUser)
  secondVector = createVectorForUser(secondUser)
  #No idea if this will work. Very unfamiliar with Numpy module
  return nump.linalg.norm(nump.array(firstVector) - nump.array(secondVector))
  
def getNeighbors(username, arbitrary):
  """
  Gets the most similar users to username. The array can't be too long, hence I added an arbitrary value to check 
  the length of the array.
  """
  client = MongoClient()
  distances = []
  for user in allUsers(client):
    if len(distances) > arbitrary:
      break
    distance = vectorDistance(username, user['username'])
    distances.append((user['username'], distance))
  distances.sort(key=operator.itemgetter(1))
  return distances
  
def getRecommendation(username):
  client = MongoClient()
  neighbors = getNeighbors(username, 80)
  users = allUsersInArray([neighbor[0] for neighbor in neighbors], client)
  notApplicable = queryUser(username, client)['subreddits']
  frequency = {}
  total = [sub for user in users for sub in user['subreddits']]
  subredditFreq = {word: total.count(word) for word in set(total) if word not in notApplicable}
  return max(subredditFreq, key=subredditFreq.get)
  
def main(username):
  redditstats.getComments(username)
  return getRecommendation(username)
  
if __name__ == "__main__":
  myUser = raw_input()
  print(main(myUser))
