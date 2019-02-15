import pandas as pd
import numpy as np
import csv
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def import_chats(filenames):
	filenames
	# Import and combine all chats
	group_names = [(n.split('/')[-1]).split('.')[0] for n in filenames]
	messages_raw = pd.DataFrame()
	for i,name in enumerate(filenames):
		txt = pd.read_table(name,header=None,names=["contents"])
		txt = txt.assign(chatName=group_names[i])
		messages_raw = messages_raw.append(txt)
	return messages_raw

def parse_messages(messages_raw,name_map={}):
		# Process chats
	date_re = '(\[[0-9]{2}\/[0-9]{2}\/[0-9]{4})'
	time_re = '([0-9]{2}:[0-9]{2}:[0-9]{2}\])'
	author_re = '(\] [A-Za-z ]+:)'
	header_re = '(\[[0-9]{2}\/[0-9]{2}\/[0-9]{4}, [0-9]{2}:[0-9]{2}:[0-9]{2}\] [A-Za-z0-9 ]+:)'

	# Parse date, time, author and messages
	# chat
	messages = pd.DataFrame(messages_raw.chatName)
	# date
	messages = messages.assign(dateTxt=messages_raw.contents.str.extract(date_re))
	messages['dateTxt'] = messages['dateTxt'].str[1:]
	# time
	messages = messages.assign(timeTxt=messages_raw.contents.str.extract(time_re))
	messages['timeTxt'] = messages['timeTxt'].str[0:-1]
	# author
	messages = messages.assign(author=messages_raw.contents.str.extract(author_re))
	messages['author'] = messages['author'].str[1:-1]
	messages['author'] = messages['author'].str.replace(" ","")
	# message
	messages = messages.assign(message=messages_raw.contents.str.split(header_re,expand=True).iloc[:,2])

	# Remove nonsense/attachments etc.
	messages = messages.dropna()
	group_names = messages.chatName.unique()
	for n in group_names:
		messages = messages.loc[messages.author.str.lower()!=n.lower()]
		
	# Process names, date and time
	if bool(name_map):
		messages.author = messages.author.map(name_map)

	# Add date/time number columns and then a time since first message column
	messages = pd.concat([messages,
						  messages.dateTxt.str.split('/',expand=True).set_axis(['day','month','year'],axis='columns',inplace=False).astype(int),
						  messages.timeTxt.str.split(':',expand=True).set_axis(['hour','minute','second'],axis='columns',inplace=False).astype(int)],
						  axis=1,sort=False)

	t = pd.to_datetime(messages[['year','month','day','hour','minute','second']])
	t_min = t.min()
	messages = messages.assign(timeStamp=t.apply(lambda x: (x-t_min).total_seconds()))

	# Flag attachments
	messages = messages.assign(attachment=messages['message'].str.contains('<attached: '))

	# Reset index
	messages = messages.reset_index(drop=True)
	return messages

def chats2pandas(filenames,name_map={}):
	messages_raw = import_chats(filenames)
	messages = parse_messages(messages_raw,name_map)
	return messages


