import spotipy
import json
import argparse
import pkg_resources
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

# colours for terminal output
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# spotify auth
spotify_creds = json.load(open(pkg_resources.resource_filename('spot2mp3.data', 'spotify_creds.json')))
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds["client_id"], client_secret=spotify_creds["client_secret"])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def printLog(*args, **kwargs):
	open('log.txt', 'a').close()
	print(*args, **kwargs)
	with open('log.txt', 'a') as f:
		print(*args, **kwargs, file=f)

def youtube_search(query, max_results=3):
	yt = YTMusic(pkg_resources.resource_filename('spot2mp3.data', 'oauth.json'))
	try:
		search_results = yt.search(query, limit=max_results)
	except Exception as e:
		printLog(f'Error: {e}')
		return []
	video_ids = []
	for result in search_results:
		try:
			video_ids.append("www.music.youtube.com/watch?v=" + result["videoId"])
		except:
			continue
	return video_ids

def yt_download(links, title, output_dir):
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
	
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	audio = AudioSegment.from_file(downloaded)
	audio.export(f'{os.getcwd()}/{output_dir}/{title}.mp3', format="mp3")
	os.remove(downloaded)

	printLog("Converted to mp3 - saved as \"{}.mp3\"".format(title))

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

def main():
	parser = argparse.ArgumentParser(description='Download Spotify playlist/album tracks as mp3 files.')
	parser.add_argument('playlist', type=str, help='Spotify playlist/album link')
	parser.add_argument('-o', '--output', type=str, default='downloads', help='Output directory for mp3 files')
	args = parser.parse_args()

	playlist = args.playlist

	# extracting tracks from a playlist
	#playlist_link = input("Enter Spotify playlist/album link: ")
	try:
		list_type = playlist.split("/")[3]
		if list_type == "playlist":
			playlist_uri = playlist.split("/")[-1].split("?")[0]
			tracklist = sp.playlist_tracks(playlist_uri)["items"]
			print(f'Extracted tracks from playlist "{sp.playlist(playlist_uri)["name"]}"...')
		else:
			album_uri = playlist.split("/")[-1].split("?")[0]
			tracklist = sp.album_tracks(album_uri)["items"]
			print(f'Extracted tracks from album "{sp.album(album_uri)["name"]}"...')
	except Exception as e:
		print(f'Error: {e} - please enter a valid Spotify playlist/album link.')
		exit()

	songcount = 0;
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
		
		print(f'{color.UNDERLINE}{color.BOLD}Song {songcount}:{color.END}')
		print(f'Searching with query \"{sanitized_title} by {artist_name}\"...')
		yt_download(youtube_search(f'{sanitized_title} by {artist_name}'), sanitized_title, args.output)
		print("Editing metadata...")
		try:
			update_mp3_metadata(f'{args.output}/{sanitized_title}.mp3', metadata, album_cover)
		except Exception as e:
			print(f'{color.RED}Error editing metadata: {e}{color.END}')
			continue
		print(f"{color.GREEN}Done!{color.END}\n")
		songcount += 1

if __name__ == "__main__":
	main()