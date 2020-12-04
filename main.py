import tkinter
from tkinter import messagebox
import datetime as dt
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


def get_top_100_and_create_playlist(timestamp):

    date = timestamp.strftime("%Y-%m-%d")
    class_ = "chart-element__information__song text--truncate color--primary"

    url = f"https://www.billboard.com/charts/hot-100/{date}"


    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Error")


    soup = BeautifulSoup(response.content,"html.parser")

    tags = soup.find_all("span",class_=class_)


    titles = [tag.getText() for tag in tags]

    scope = "playlist-modify-private"
    sp_oauth =SpotifyOAuth(scope=scope,show_dialog=True,cache_path="token.txt")


    sp = spotipy.Spotify(auth_manager=sp_oauth)

    user_id = sp.current_user()["id"]
    uris = []
    for title in titles:
        result = sp.search(q=f"track:{title} year:{timestamp.year}",limit=1)
        try:
            uri = result['tracks']['items'][0]['uri']
        except IndexError:
            print(f"Track {title} could not be found on Spotify")
        else:
            uris.append(uri)

    description = f"Top 100 Billboard songs week of {timestamp.strftime('%b %d %Y')}"
    playlist_name = f"Hot 100 {date}"


    playlist_id = sp.user_playlist_create(user=user_id,name=playlist_name,public=False,description=description)["id"]

    sp.user_playlist_add_tracks(user_id,playlist_id,uris)



def create_playlist():
    date = entry.get()
    if not date:
        messagebox.showerror(title="Error",message="Please enter a data")
        return
    try:
        timestamp =pd.to_datetime(date)
    except ValueError:
        messagebox.showerror(title="Error",message="Could not recognize date. Please enter a valid date!")
    else:
        get_top_100_and_create_playlist(timestamp)
    finally:
        entry.delete(0,tkinter.END)



font = ("Arial",40,"bold")

green = "#1DB954"
window = tkinter.Tk()
window.title("Hot 100 Playlist Creator")
window.configure(padx=50,pady=50,bg=green)


label = tkinter.Label(text="SPOTIFY HOT 100 PLAYLIST CREATOR",font=font,bg=green)
label.pack()


frame = tkinter.Frame()
date_label = tkinter.Label(frame,text="Date: ",font=font,bg=green)
date_label.grid(row=0,column=0)
entry = tkinter.Entry(frame,font=font)
entry.focus_set()
entry.grid(row=0,column=1)
frame.pack(pady=20)



generate = tkinter.Button(text="Generate",command=create_playlist,font=font)
generate.pack(pady=20)


window.mainloop()


#date = input("Which day in the past do you want to travel to?(May 29 1994)" )

