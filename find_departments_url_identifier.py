def locate_url_identifier(url):
	before = 'pastpapers/pdf/'
	after = '/sem'
	return url[(url.find(before) + len(before)) : url.rfind(after)]

if __name__ == '__main__':
	url = input("Enter the full URL for a single past paper: ")
	print() # print blank line
	print("Your URL Identifier is:")
	print(locate_url_identifier(url))