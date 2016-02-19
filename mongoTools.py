from pymongo import *
import datetime

def insertUser(username, subreddits, client):
  user = {
          'username': username,
          'subreddits': subreddits,
          'updated': datetime.datetime.utcnow()
        }
  db = client.Reddit
  collection = db.users
  userID = collection.update({'username' : user['username']}, {'username': user['username'], 'subreddits': user['subreddits'], 'updated': user['updated']}, upsert = True)
  return userID
  
def insertSub(sub, client):
  sub = {
          'name': sub,
          'updated': datetime.datetime.utcnow()
        }
  db = client.Reddit
  collection = db.subreddits
  userID = collection.update({'name': sub['name']}, {'name': sub['name'], 'updated': sub['updated']}, upsert = True)

def queryUser(user, client):
  collection = client.Reddit.users
  user = collection.find_one({'username': username})
  return user
  
def update(username, subreddits, client):
  collection = client.Reddit.users
  collection.update({'username': username}, {"$set": {'subreddits': subreddits}})
  
def subreddits(client):
  return client.Reddit.subreddits.find()
  
def allUsersInArray(userArray, client):
  return client.Reddit.users.find({'username': {"$in": userArray}})
  
def allUsers(client):
  return client.Reddit.users.find()
  
def tempUserList(client):
  return client.Reddit.temp.find()
  
def tempBulkInsert(users, client):
  return client.Reddit.temp.insert(users)
