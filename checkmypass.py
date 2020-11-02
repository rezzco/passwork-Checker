import sys
import requests
import hashlib


# password_list = sys.argv[1:]

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)

	if res.status_code !=200:
		raise RuntimeError(f" Error fetching: {res.status_code}, check the api adress and try again")
	
	return res

def check_password_in_response(res, hash_to_check ):
	matched_hash_passwords_list = [tuple(item.split(":")) for (item) in res.text.split("\r\n") ] 
	for hsh,count in matched_hash_passwords_list:
		if hsh == hash_to_check:
			return count
	return 0
		

def pwned_api_check (password):
	hashed_password=hashlib.sha1(password.encode('utf-8'))
	hashed_password = hashed_password.hexdigest().upper()
	first_5_char, tail =hashed_password[:5], hashed_password[5:]
	response = request_api_data(first_5_char)
	count = check_password_in_response(response, tail)
	return count
	
	
def main(args):
	for password in args:
	pwned_count = pwned_api_check(password)
	if pwned_count:
		print (f"{password} has been breached: total {pwned_count} unauthorized usage found!")
	else:
		print(f"luckily, {password} has not been hacked yet :)")

	return "done!"
if __name__ = "__main__":
	sys.exit(main(sys.argv[1:]))