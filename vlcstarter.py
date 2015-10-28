import sys, re, json, urllib.request

# for local usage
import subprocess

# TODO
# handle both playlist urls AND single videos
# provide nice json output as final result
# videos should be in dict/array/list (store videoid and length)

# WARNING
# currently only tested on Windows (shame on me, I know)


def main(args):
	
	#basics
	apikey = "YOUR YOUTUBE API KEY"
	vlcpath = "YOUR PATH TO VLC PLAYER"
	snippetlength = 30
	
	#take first argument as url
	url = args[1:][0]
	
	#youtube: playlists
	youtube=re.compile(r"https?:\/\/w{0,3}.?youtube.com\/playlist\?list=(.+)")
	
	yt_playlist=youtube.match(url)
	if(yt_playlist):
		
		print("Awesome, got a YouTube playlist.")
		
		videos=[]
		playlist_id=yt_playlist.group(1)
		videolist=""

		url=("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={0}&fields=items%2FcontentDetails%2CnextPageToken%2CpageInfo%2CprevPageToken&key={1}&maxResults=50").format(playlist_id, apikey)
		
		response = urllib.request.urlopen(url)
		data = json.loads(response.read().decode('utf-8'))
		
		print("Found the following videos (HA, GOTEM!):")
		for items in data["items"]:
					
					
			url=("https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={0}&fields=items(contentDetails)&key={1}").format(items["contentDetails"]["videoId"], apikey)
			
			response = urllib.request.urlopen(url)
			data = json.loads(response.read().decode('utf-8'))
			
			# needs some polishing
			# youtube API only provides shitty weird sting we have to encrypt
			
			# better regex: PT(\d*).?(\d*).?(\d*).?
			# - if last group is empty: no hour
			# - if 2 last groups empty: no hour and minute
			# good: we won't need to extract integer and type casting can leave the room
			
			
			length_raw=re.compile(r"PT(?P<h>\d*H)*(?P<m>\d*M)*(?P<s>\d*S)*")
			length=length_raw.match(data["items"][0]["contentDetails"]["duration"])
			
			
			if length.group("h") is not None:
				hours=length.group("h").replace("H", "")
			else:
				hours=0
				
			if length.group("m") is not None:
				minutes=length.group("m").replace("M", "")
	
			seconds=length.group("s").replace("S", "")

			
			length_in_sec=int(hours)*60*60+int(minutes)*60+int(seconds)
			middletime=length_in_sec/2
			
			print(items["contentDetails"]["videoId"])
			print(length_in_sec)
			print(middletime)
			
			videolist+=("https://www.youtube.com/watch?v={0} :start-time={1} :stop-time={2} ").format(items["contentDetails"]["videoId"], middletime, middletime+snippetlength)

			
		# --no-video
		print("Sending these videos to VLC. Cause.. I can.")
		subprocess.Popen(args=("{0} {1}").format(vlcpath, videolist))
		
		
	else:
		print("Sorry, but your URL can't be regognized by me.")


if __name__ == '__main__':
	import sys
	main(sys.argv)