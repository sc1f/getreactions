import requests, json, time, sys

client_id = input("enter your fb client id")
client_secret = input("enter your client secret")
page_id = input("enter the page id you would like to scrape")

access_token = client_id + "|" + client_secret

def get_memes(url):
	req = requests.get(url)
	res = req.json()

	try:
		nxt = res['paging']['next']
		prev = res['paging']['previous']
	except:
		print("DONE!")
		return 1

	data = res['data']

	for post in data:
		post_id = post['id']
		post_ids.append(post_id)
		print(post_id, 'has been appended!')

	return get_memes(nxt)

def parse_memes(ids):

	out = [] # each item is {id: likes}
	
	for post_id in ids:
		token = requests.get('https://graph.facebook.com' + '/oauth/access_token?client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=client_credentials&redirect_uri="facebook.com"').json()['access_token']
		url = 'https://graph.facebook.com/' + post_id + '/reactions?access_token=' + token + '&summary=total_count'
		req = requests.get(url).json()
		try:
			count = req['summary']['total_count']
		except:
			continue

		output = {
			'id': post_id,
			'total_count': count
		}

		out.append(output)
		print("Post", post_id, "got", count, "reactions.")
	return out

def order_memes(memes):
	# sort
	sorted_list = sorted(memes, key=lambda k: k['total_count'], reverse=True)
	print(sorted_list) 

if __name__ == '__main__':
	start = time.time()
	post_ids = []
	get_memes('https://graph.facebook.com/' + page_id + '/feed?access_token=' + access_token)
	'''
	# READS IDs from file. Uncomment to do that.
	with open('meme_ids.txt', 'r') as ids:
		ids = [i.strip() for i in ids.readlines()]

		for post_id in ids:
			post_ids.append(post_id)
	'''
	# writes IDs to new file for future use
	with open('post_ids.txt', 'w') as post_ids_file:
		post_ids_file.write('\n'.join(lines))
		print("post_ids file written!")

	parsed = parse_memes(post_ids)

	with open('parsed_posts.py', 'w') as parsed_posts_file:
		parsed_posts_file.write(parsed)
		print('parsed posts written!')

	sorted_memes = order_memes(parsed)

	with open('sorted_output.py', 'w') as sorted_output_file:
		sorted_output_file.write(sorted_memes)
		print('final output written!')

	end = time.time()
	print("this took", time.strftime('%H:%M:%S', time.localtime(end - start)))
	sys.exit(0)
