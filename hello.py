from requests import get,post
from re import findall
import json
import time

def getInfoHashtag(hashtags):
    media_counter=[]
    for hashtag in hashtags:
        res=get("https://www.instagram.com/web/search/topsearch/",headers={
            "User-Agent":user_agent,
            "X-Requested-With":"XMLHttpRequest"
        },params={
            "context":"blended",
            "query":hashtag,
            "rank_token":"0.8042610760106192",
            "include_reel":"true"
        })
        js=json.loads(res.text)
        media_counter.append(js["hashtags"][0]["hashtag"]["media_count"])
    return media_counter


#--------------------------------------------------------------------------------------
#                             ESSENTIAL VARIABLE YOU SHOULD CHANGE THEM B
full_counter = 0
user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
username="********"
password="*******"
keyword="*******"
query_hash="***************"
MIN_LIKES=100
MIN_COMMENTS=0
min_hashtag=100
#---------------------------------------------------------------------------

array_hash_tag=[]
response =get("https://www.instagram.com/explore/tags/"+keyword+"/",headers={
    "User-Agent":user_agent,
    "X-Requested-With":"XMLHttpRequest"
})
csrf_token=findall("csrf_token\":\"([a-zA-Z0-9]+)",response.text)[0]


cookie = response.cookies.get_dict()



data={
    "username":username,
    "password":password,
    "enc_password":"",
    "queryParams":'{"next":"/explore/tags/'+keyword+'/","source":"desktop_nav"}',
    "optIntoOneTap":"false"
}
header={
    "User-Agent":user_agent,
    "X-Requested-With":"XMLHttpRequest",
    "X-CSRFToken":csrf_token,
    "X-IG-App-ID":"************"
}
response=post("https://www.instagram.com/accounts/login/ajax/",headers=header,cookies=cookie,data=data)
cookie = response.cookies.get_dict()
header["X-CSRFToken"]=cookie["csrftoken"]
response=get("https://www.instagram.com/explore/tags/"+keyword+"/",headers=header,cookies=cookie)
end_cursor=findall("end_cursor\":\"([a-zA-Z0-9\-_:=\.]+)",response.text)[0]
"""response=get("https://www.instagram.com/static/bundles/ProfilePageContainer.js/031ac4860b53.js",headers=header,cookies=cookie)
query_hash=findall("queryId:\"([a-zA-Z0-9]+)",response.text)[0]"""
response=get("https://www.instagram.com/graphql/query",headers=header,cookies=cookie,params={
    "query_hash":query_hash,
    "variables":'{"tag_name":"bracelets","first":3,"after":"'+end_cursor+'"}'
})

js = json.loads(response.text)
has_next=True

has_next=js["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]
end_cursor=js["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
edges =js["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]
while has_next:
    
    for data in edges:
        if data["node"]["edge_liked_by"]["count"] > MIN_LIKES:
            text=""
            try:
                text=data["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            except IndexError:
                text=""
            hashs=findall("#[a-zA-Z0-9\-_\:=\.]+",text)
            url_to_post="https://www.instagram.com/p/"+data["node"]["shortcode"]
            if len(hashs) > 0:
                arraymediacounter=getInfoHashtag(hashs)
            print("-------------------------------------------------------")
            print("[X] "+url_to_post+"\t [OWNER_ID]"+str(data["node"]["owner"]["id"])+"\t[LIKES] ["+str(data["node"]["edge_liked_by"]["count"])+"]")
            for (i,j) in zip(arraymediacounter,hashs):
                if (i<min_hashtag and i> 10 ) and array_hash_tag.count<=25:
                    array_hash_tag.append(j)
                    print("[+] "+j+"[GOOD HASHTAG !]")
                else:
                    print("[+] "+j+" ["+str(i)+"]\t (number of competitive is high or under 5)")
            print("[+] sleep for 10..")
            time.sleep(3)
        else:
            url_to_post="https://www.instagram.com/p/"+data["node"]["shortcode"]
            print("[+] "+url_to_post)
            time.sleep(5)    
        response=get("https://www.instagram.com/graphql/query",headers=header,cookies=cookie,params={
        "query_hash":query_hash,
        "variables":'{"tag_name":"'+keyword+'","first":3,"after":"'+end_cursor+'"}'})
        js = json.loads(response.text)
        has_next=js["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]
        if has_next == True:
            end_cursor=js["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
            edges =js["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        #print("[+] sleep for 30..")
        #time.sleep(30)
        if full_counter == 100:
            print("[+] sleep for 2min..")
            time.sleep(1200)
            full_counter=0
        else:
            full_counter = full_counter + 1

        
   
            

