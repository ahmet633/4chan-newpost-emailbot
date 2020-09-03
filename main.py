import requests
import json
import refinepost
import myemail

response = requests.get("https://a.4cdn.org/biz/catalog.json")

#every thread number on /biz/
thread_no_list = []

#key: threadNo ,  value: lastPost'sID
lastPostDict = {}

#keywords to look for
keywords = []
keywords = open("keywords.txt","r").read().split()

#email list
emaillist = []
emaillist = open("emails.txt","r").read().split()

for i in range(0,11):
  for j in range(0,len(response.json()[i]['threads'])):
    thread_no_list.append(response.json()[i]['threads'][j]['no'])

#prints every post on /biz/
def printEveryPost(thread_list):
  for thread in thread_list:
    response = requests.get("https://a.4cdn.org/biz/thread/" + str(thread) + ".json")
    postCount = len(response.json()['posts'])
  for i in range(0,postCount):
    if 'com' in response.json()['posts'][i]:
      print(response.json()['posts'][i]['com'])
      print("\n-----------------------------------")

#associates threads with their last posts
def associateLastPostId(thread_list):
  for thread in thread_list:
    response = requests.get("https://a.4cdn.org/biz/thread/" + str(thread) + ".json")
    lastPost = len(response.json()['posts']) - 1
    if 'com' in response.json()['posts'][lastPost]:
      if thread in lastPostDict:
      #this means that thread was already associated
        if lastPostDict[thread] == response.json()['posts'][lastPost]['id']:
        #this means nothing changed
          continue
        else:
        #this means a new post is added!
        #IMPORTANT
          rawpost = response.json()['posts'][lastPost]['com']
          refinedpost = refinepost.refinepost(rawpost)
          if len(keywords) == 0:
            print("NEW POST!\n") 
            print(refinedpost)
            print("\nhttps://boards.4channel.org/biz/thread/" + str(thread))
            print("|-------------------------------------------------------|\n")
          else:
            for keyword in keywords:
              found = refinedpost.lower().find(keyword)
              if found != -1:
                print("New post with keyword \"",keyword,"\"!\n")
                print(refinedpost)
                print("\nhttps://boards.4channel.org/biz/thread/" + str(thread))
                print("|-------------------------------------------------------|\n")
                myemail.sendEmailToEveryone(emaillist, myemail.prepareContent(keyword, thread))
          lastPostDict[thread] = response.json()['posts'][lastPost]['id']
          
      else:
      #this means its probably first time running the loop
      #or this thread is just created
        if 'id' in response.json()['posts'][lastPost]:
          lastPostDict[thread] = response.json()['posts'][lastPost]['id']
        
print("Starting...")
print("This may take a while...")
while True:
  try:
    associateLastPostId(thread_no_list)
    print("Reloading...")
  except Exception:
    continue

