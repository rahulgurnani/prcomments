import os
import pickle

dir_path = os.path.join(os.path.expanduser('~'), '.prcomments')

"""
Storage : We should store todos and archives. 

"""

def file_for_pr(prid):
	return os.path.join(dir_path, prid + '.pickle')

def get_data(prid):
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)
	if not os.path.exists(file_for_pr(prid)):
		return None
	file = open(file_for_pr(prid), "rb")
	
	return pickle.load(file)

def add_comment(prid, comment, comment_type):
	prid = str(prid)
	data = get_data(prid)
	if data is None:
		data = {}
	if comment_type in data:
		data[comment_type].append(comment)
	else:
		data[comment_type] = [comment]
	file_w = open(file_for_pr(prid), "wb")
	pickle.dump(data, file_w)
	file_w.close()

def get_comments(prid, comment_type):
	data = get_data(str(prid))

	if data is None:
		return []
	if comment_type in data:
		return data[comment_type]
	return []
