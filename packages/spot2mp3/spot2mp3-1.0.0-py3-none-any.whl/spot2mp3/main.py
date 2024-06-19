import spotipy
import json
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from pydub import AudioSegment
from ytmusicapi import YTMusic
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK
import requests
import os
import re

def printLog(*args, **kwargs):
	open('log.txt', 'a').close()
	print(*args, **kwargs)
	with open('log.txt', 'a') as f:
		print(*args, **kwargs, file=f)

def youtube_search(query, max_results=3):
	yt = YTMusic('oauth.json')
	search_results = yt.search(query, limit=max_results)
	#search_response = VideosSearch(query, limit=max_results)
	#results = "https://www.youtube.com/watch?v=" + search_response.result()["result"][0]["id"]
	video_ids = []
	for result in search_results:
		try:
			video_ids.append("www.music.youtube.com/watch?v=" + result["videoId"])
		except:
			continue
	return video_ids

def yt_download(links, title):
	index = 0
	success = False
	while (success == False and index < len(links)):
		try:
			yt_vid = YouTube(links[index])
			stream = yt_vid.streams.filter(only_audio=True).first()
			downloaded = stream.download()
			success = True
		except Exception as e:
			printLog(f'Error: {e}')
			index += 1
			continue

	if not success:
		printLog("Error: Could not download video.")
		return

	printLog(f'Downloaded mp4 file from {links[index]}, converting to mp3...')

	if not os.path.exists("spot2mp3_downloads"):
		os.makedirs("spot2mp3_downloads")

	audio = AudioSegment.from_file(downloaded)
	audio.export(f'downloads/{title}.mp3', format="mp3")

	os.remove(downloaded) # clean up
	printLog("Converted to mp3 - saved as \"{}.mp3\"".format(sanitized_title))

def update_mp3_metadata(file_path, metadata, cover_url):
	cover = requests.get(cover_url, stream=True)
	with open('cover.jpg', 'wb') as f:
		for chunk in cover.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)

	audio = MP3(file_path, ID3=ID3)

	audio.tags["TIT2"] = TIT2(encoding=3, text=metadata["title"])
	audio.tags["TPE1"] = TPE1(encoding=3, text=metadata["artist"])
	audio.tags["TALB"] = TALB(encoding=3, text=metadata["album"])
	audio.tags["TDRC"] = TDRC(encoding=3, text=metadata["date"])
	audio.tags["TRCK"] = TRCK(encoding=3, text=str(metadata["track_number"]))
	audio.tags["APIC"] = APIC(
		encoding=3,
		mime='image/jpeg',
		type=3, desc='Cover',
		data=open('cover.jpg', 'rb').read()
	)
	audio.save()
	os.remove('cover.jpg')

# spotify auth
spotify_creds = json.load(open('spotify_creds.json'))
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds["client_id"], client_secret=spotify_creds["client_secret"])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# extracting tracks from a playlist
playlist_link = input("Enter Spotify playlist/album link: ")
try:
	list_type = playlist_link.split("/")[3]
	if list_type == "playlist":
		playlist_uri = playlist_link.split("/")[-1].split("?")[0]
		tracklist = sp.playlist_tracks(playlist_uri)["items"]
	else:
		album_uri = playlist_link.split("/")[-1].split("?")[0]
		tracklist = sp.album_tracks(album_uri)["items"]
except Exception as e:
	printLog(f'Error: {e} - please enter a valid Spotify playlist/album link.')
	exit()

for track in tracklist:
	# track_link = track["track"]["external_urls"]["spotify"]
	# track_uri = track["track"]["uri"]
	if list_type == "playlist":
		album_uri = track["track"]["album"]["uri"]
	# artist_uri = track["track"]["artists"][0]["uri"]

	album_info = sp.album(album_uri)

	# mp3 metadata variables
	if list_type == "playlist":
		track_name = track["track"]["name"]
		artist_name = track["track"]["artists"][0]["name"]
		album = track["track"]["album"]["name"]
		album_release_date = album_info["release_date"].split("-")[0]
		track_number = track["track"]["track_number"]
		album_cover = album_info["images"][0]["url"]
	else:
		track_name = track["name"]
		artist_name = track["artists"][0]["name"]
		album = album_info["name"]
		album_release_date = album_info["release_date"].split("-")[0]
		track_number = track["track_number"]
		album_cover = album_info["images"][0]["url"]

	metadata = {
		"title": track_name,
		"artist": artist_name,
		"album": album,
		"date": album_release_date,
		"track_number": track_number,
	}

	sanitized_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', track_name)

	printLog(f'Searching with query \"{sanitized_title} by {artist_name}\"...')
	yt_download(youtube_search(f'{sanitized_title} by {artist_name}'), sanitized_title)
	printLog("Editing metadata...")
	update_mp3_metadata(f'downloads/{sanitized_title}.mp3', metadata, album_cover)
	printLog("Done!")
