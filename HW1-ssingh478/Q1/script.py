import sys
import http.client
import requests
import json
import csv
import time
#API_key=sys.argv[1]
#print ("Tha API Key is: {}".format(APIkey))
#APIkey=str(APIkey)
#print(APIkey)
#APIkey= "012945ec43875eb8fd0d1afdafc6a92e"
# conn=http.client.HTTPSConnection("api.themoviedb.org")
payload="{}"
# i=2
# conn.request("GET", "/3/discover/movie?page=1&api_key=012945ec43875eb8fd0d1afdafc6a92e&include_video=false&with_genre=Comedy&primary_release_date.gte>=2000&include_adult=false&sort_by=popularity.desc&language=en-US", payload)

# res = conn.getresponse()
# data = res.read()

# #print(data.decode("utf-8"))
# datafile=data.decode("utf-8")

# datafile=datafile.split(",")
# #print(datafile)
# dataset=[i for i in datafile if ("original_title") or ("id:") in i]
# print(dataset)
# print(len(dataset))
Api_key=sys.argv[1]
#i=1
ids=[]
titles=[]
for i in range(1,16):
    URL="http://api.themoviedb.org/3/discover/movie?api_key="+Api_key
    #print(URL)
    with_genre="35"
    Final_URL=URL+"&page="+str(i)+"&with_genres="+with_genre+"&sort_by=popularity.desc"+"&primary_release_date.gte=2000-01-01"
    #print(Final_URL)
#PARAMS={'api_key':Api_key,'with_genre':with_genre}
    r=requests.get(Final_URL)
    jdata=json.loads(r.text)
    for result in jdata['results']:
        ids.append(result['id'])
        titles.append(result['title'])
    #print(len(jdata))
#datafile=data.decode("utf-8")
#print(jdata)

with open('movie_ID_name.csv','w',newline='\n',encoding="utf-8") as f:
    thewriter=csv.writer(f)
    for i in range(len(ids)):
        thewriter.writerow([ids[i], titles[i]])
        print("\n")
idtupper=[]
tt=15
for id in ids:
    if tt==40:
        tt=0
        time.sleep(10) # after 30 seconds, "hello, world" will be printed
    URL="https://api.themoviedb.org/3/movie/"+str(id)+"/similar?api_key="+Api_key+"&page=1"
    #print(URL)
    r=requests.get(URL)
    jdata=json.loads(r.text)
    length=0
    #print(jdata)
    #print(type(idtupper))
    #print(len(idtupper))
    for result in jdata['results']:
        if length>=5:
            break
        #if result['id'] not in ids:
        idtupper.append((id,result['id']))
        length+=1
    tt+=1
#print(len(idtupper))

# temp = []
# for a,b in idtupper :
#     if (a,b) not in temp and (b,a) not in temp: #to check for the duplicate tuples
#         temp.append((a,b))
# idtupper = temp * 1 #copy temp to d

idtupper=[(a,b) for (a,b) in idtupper if (b,a) not in idtupper or a<b]

with open('movie_ID_sim_movie_ID.csv','w',newline='\n',encoding="utf-8") as f:
    thewriter=csv.writer(f)
    for ij in range(len(idtupper)):
        thewriter.writerow(idtupper[ij])
        print("\n")


