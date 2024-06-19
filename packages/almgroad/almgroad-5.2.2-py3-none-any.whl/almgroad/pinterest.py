import requests
def Pinterest_Download(url):
	try:
		cookies = {
		    'cf_clearance': 'ppI6n83I9sWcr0OXVkB0efNyvNDoq73du_I2QrsYqCQ-1718719489-1.0.1.1-TnpeRzd3VFZbQkcSc1O8XAq_Ma7kQnRybXSGZBLPPQUBIuXEo1df2d0xKqaya41sSAG9q5NhzHkvY3KjBgu.nA',
		    '__gads': 'ID=079f036541417be9:T=1718719492:RT=1718719492:S=ALNI_MYk-OzBZv-vBfwTGbzx-GrWemOTwQ',
		    '__gpi': 'UID=00000e5e23a62ae3:T=1718719492:RT=1718719492:S=ALNI_MZsDICTnaqUFz2kbO9ffCo_PQuJCA',
		    '__eoi': 'ID=66c4303fc24f1c5d:T=1718719492:RT=1718719492:S=AA-Afjb7gfQWNlosV12_BiEQY6u1',
		    '_gid': 'GA1.2.5741638.1718719494',
		    '_gat_gtag_UA_159919929_1': '1',
		    '_ga_EQFV8CRHVZ': 'GS1.1.1718719489.1.1.1718719526.0.0.0',
		    '_ga': 'GA1.2.1743413195.1718719490',
		    'FCNEC': '%5B%5B%22AKsRol-aivGM3vGiEgHbOSk3BswtoWwrHKqcLKLpacsOQxc8IP1GiIr5wpj-UyFVR32HSeX9oCtuAI00HAeMwnjfF5OD-N_AfrTIJQ9q1SCWOBvtcISNUIG_RsWLhYxK4AH_9k4os_bGkKmMb_B7ul0P1ZrphQIyoQ%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C6%2C%5B1718719497%2C375585000%5D%5D%5D%22%5D%5D%5D',
		}
		
		headers = {
		    'authority': 'pinterestdownloader.com',
		    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		    'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		    'cache-control': 'max-age=0',
		    'content-type': 'application/x-www-form-urlencoded',
		    'origin': 'https://pinterestdownloader.com',
		    'referer': 'https://pinterestdownloader.com/',
		    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
		    'sec-ch-ua-mobile': '?1',
		    'sec-ch-ua-platform': '"Android"',
		    'sec-fetch-dest': 'document',
		    'sec-fetch-mode': 'navigate',
		    'sec-fetch-site': 'same-origin',
		    'sec-fetch-user': '?1',
		    'upgrade-insecure-requests': '1',
		    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
		}
		
		data = {
		    'url': url
		}
		
		r = requests.post('https://pinterestdownloader.com/', cookies=cookies, headers=headers, data=data).text.split('<div class="meta-video">')[1].split('<video controls src="')[1].split('"')[0]
		return {
		"is_photo":False ,
		"url":r
		}
	except:
		cookies = {
		    'cf_clearance': 'ppI6n83I9sWcr0OXVkB0efNyvNDoq73du_I2QrsYqCQ-1718719489-1.0.1.1-TnpeRzd3VFZbQkcSc1O8XAq_Ma7kQnRybXSGZBLPPQUBIuXEo1df2d0xKqaya41sSAG9q5NhzHkvY3KjBgu.nA',
		    '_gid': 'GA1.2.5741638.1718719494',
		    '_gat_gtag_UA_159919929_1': '1',
		    '__gads': 'ID=079f036541417be9:T=1718719492:RT=1718720062:S=ALNI_MYk-OzBZv-vBfwTGbzx-GrWemOTwQ',
		    '__gpi': 'UID=00000e5e23a62ae3:T=1718719492:RT=1718720062:S=ALNI_MZsDICTnaqUFz2kbO9ffCo_PQuJCA',
		    '__eoi': 'ID=66c4303fc24f1c5d:T=1718719492:RT=1718720062:S=AA-Afjb7gfQWNlosV12_BiEQY6u1',
		    '_ga_EQFV8CRHVZ': 'GS1.1.1718719489.1.1.1718720085.0.0.0',
		    '_ga': 'GA1.2.1743413195.1718719490',
		    'FCNEC': '%5B%5B%22AKsRol_3orWgSVvZRmZa70kIkhl6ktQGfpOTMuNsoUu39qwHMh2aLKINukqPAwq_Je3ibOwOmq1Kkf8jAktTOGRMHYXw-IymikGbkgwMwGH2EzYzO0pTQLubWO5ed5hKIELYPRQDCMOITfCjwuJ3M7iLh810uUvJDg%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C9%2C%5B1718719497%2C375585000%5D%5D%5D%22%5D%5D%5D',
		}
		
		headers = {
		    'authority': 'pinterestdownloader.com',
		    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		    'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		    'cache-control': 'max-age=0',
		    'content-type': 'application/x-www-form-urlencoded',
		    'origin': 'https://pinterestdownloader.com',
		    'referer': 'https://pinterestdownloader.com/',
		    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
		    'sec-ch-ua-mobile': '?1',
		    'sec-ch-ua-platform': '"Android"',
		    'sec-fetch-dest': 'document',
		    'sec-fetch-mode': 'navigate',
		    'sec-fetch-site': 'same-origin',
		    'sec-fetch-user': '?1',
		    'upgrade-insecure-requests': '1',
		    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
		}
		
		data = {
		    'url': url
		}
		
		re = requests.post('https://pinterestdownloader.com/', cookies=cookies, headers=headers, data=data).text.split('<div class="col-lg-6 col-md-12 col-sm-12">')[1].split('<img class="down_img img-fluid rounded d-block m-auto" src="')[1].split('"')[0]
		return {
		"is_photo":True ,
		"url":re
		}
