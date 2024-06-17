import requests 
import json

def Info_Insta(user_name):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}"
    headers = {
        "X-Ig-App-Id": "1217981644879628",
    }
    try:
        req = requests.get(url ,headers=headers).json()
        bio = req["data"]["user"]["biography"]
        followers = req["data"]["user"]["edge_followed_by"]["count"]
        following = req["data"]["user"]["edge_follow"]["count"]
        fullname = req["data"]["user"]["full_name"]
        idd =  req["data"]["user"]["id"]
        username = req["data"]["user"]["username"]
        is_private = req["data"]["user"]["is_private"]
        profile_pic_url = req["data"]["user"]["profile_pic_url_hd"]
        infoo = {
                "username": username,
                "full_name": fullname,
                "followers": followers,
                "following": following,
                "bio": bio,
                "id": idd,
                "is_private":is_private,
                "profile_pic_url" : profile_pic_url,
                "programmer": "ibrahim : telegram @B_xxBx"
            }
        return infoo
                
    except Exception as e:
        return f"حدث خطأ :{e}"


