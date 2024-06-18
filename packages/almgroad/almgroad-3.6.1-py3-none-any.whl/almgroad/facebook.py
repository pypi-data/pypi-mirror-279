import yt_dlp
def FaceBook_Download(urlt):
	dl = {
	'quiet':True ,
	'format':'bestaudio/best'
	}
	with yt_dlp.YoutubeDL(dl) as d:
		info = d.extract_info(urlt,download=False)
		url = info.get("url",None)
		photo = info.get("thumbnail ",None)
		title = info.get("title",None)
		performer = info.get("uploader",None)
		return {
		"url":url,
		"photo":photo,
		"title":title,
		"performer":performer
		}
