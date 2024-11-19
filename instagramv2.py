import os
import sys
import json
from time import sleep
from datetime import datetime
import requests

def Logo():
    print('''\033[1;36m
==============================================
██╗  ██╗ ██████╗ ███████╗     ██████╗ ███████╗██╗     ██████╗ ██╗███╗   ██╗
██║  ██║██╔═══██╗██╔════╝    ██╔════╝ ██╔════╝██║     ██╔══██╗██║████╗  ██║
███████║██║   ██║███████╗    ██║  ███╗█████╗  ██║     ██║  ██║██║██╔██╗ ██║
██╔══██║██║   ██║╚════██║    ██║   ██║██╔══╝  ██║     ██║  ██║██║██║╚██╗██║
██║  ██║╚██████╔╝███████║    ╚██████╔╝███████╗███████╗██████╔╝██║██║ ╚████║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚══════╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝
 ----------------------------------------------\033[0m
           \033[1;32mSiber güvenlik & Yazılım Geliştiricisi\033[0m
            \033[1;33mBy Gokhan Yakut\033[0m
==============================================\033[0m''')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def request_token():
    valid_token = "gokhanyakut04"  # Burada geçerli token'ı belirleyin
    input_token = input("\033[1;37mLütfen güvenlik token'ını girin => \033[0m")
    return input_token == valid_token

def attempt_login(session, username, password, csrf_token):
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    timestamp = int(datetime.now().timestamp())
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf_token
    }
    return session.post(login_url, data=payload, headers=headers)

def get_csrf_token(session):
    link = 'https://www.instagram.com/accounts/login/'
    req = session.get(link)
    return req.cookies.get('csrftoken', None)

def get_followers(session, user_id, csrf_token, max_count=50):
    followers_url = f'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{max_count}%7D'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "x-csrftoken": csrf_token
    }
    response = session.get(followers_url, headers=headers)
    followers = []
    if response.status_code == 200:
        data = response.json()
        for edge in data['data']['user']['edge_followed_by']['edges']:
            followers.append(edge['node']['username'])
    return followers

def get_following(session, user_id, csrf_token, max_count=50):
    following_url = f'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{max_count}%7D'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "x-csrftoken": csrf_token
    }
    response = session.get(following_url, headers=headers)
    following = []
    if response.status_code == 200:
        data = response.json()
        for edge in data['data']['user']['edge_follow']['edges']:
            following.append(edge['node']['username'])
    return following

def print_social_media_icons():
    print('''\n\033[1;34m  Beni Sosyal Medyada Takip Edin:\033[0m
\033[1;32m  [📸] Instagram: \033[0mGokhan_yakut_04
\033[1;33m  [💬] WhatsApp: \033[0m+44 7833 319922
\033[1;35m  [🔗] GitHub: \033[0mhttps://github.com/bygokhanyakut
\033[1;36m  [🐦] Twitter: \033[0m@bygokhanYakut
''')

def main():
    clear_console()
    print('')
    Logo()
    print_social_media_icons()
    
    # Sürüm numarasını büyük ve kanlı bir şekilde ekle
    print("\033[1;31m==============================================")
    print("                  SÜRÜM 2.3.4 V                ")
    print("==============================================\033[0m")
    
    if not request_token():
        print("\033[1;31mGeçersiz güvenlik token'ı!\033[0m")
        return

    username = input("\033[1;37mKullanıcı adı => \033[0m")
    password = input("\033[1;37mŞifre => \033[0m")
    
    with requests.Session() as session:
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            print("\033[1;31mCSRFTOKEN not found in cookies\033[0m")
            return
        
        login_response = attempt_login(session, username, password, csrf_token)
        if 'checkpoint_url' in login_response.text or 'userId' in login_response.text:
            print("\033[1;32mGiriş başarılı!\033[0m")
        else:
            print("\033[1;31mGiriş başarısız!\033[0m")
            return
        
        user_id = login_response.json().get('userId')
        if not user_id:
            print("\033[1;31mKullanıcı ID'si alınamadı!\033[0m")
            return
        
        max_count = 100  # Daha fazla sayıda takipçi ve takip edilenler almak için
        followers = get_followers(session, user_id, csrf_token, max_count)
        following = get_following(session, user_id, csrf_token, max_count)
        
        unfollowers = set(following) - set(followers)
        
        print("\033[1;36mTakipçiler:\033[0m")
        for follower in followers:
            print(f"\033[1;33m - {follower}\033[0m")
        
        print("\033[1;36mTakip Edilenler:\033[0m")
        for follow in following:
            print(f"\033[1;33m - {follow}\033[0m")
        
        print("\033[1;36mTakipten Çıkanlar:\033[0m")
        for unfollower in unfollowers:
            print(f"\033[1;33m - {unfollower}\033[0m")
        
        # Sayıları renkli bir şekilde göster
        print(f"\n\033[1;32mToplam Takipçi Sayısı: \033[1;33m{len(followers)}\033[0m")
        print(f"\033[1;32mToplam Takip Edilen Sayısı: \033[1;33m{len(following)}\033[0m")
        print(f"\033[1;32mTakipten Çıkan Sayısı: \033[1;33m{len(unfollowers)}\033[0m")

if __name__ == "__main__":
    main()
