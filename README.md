# whatsapptools

Written by Henry Dalgleish 20190215

Tools for importing whatsapp chat files into pandas dataframe and parsing basic message information.

Chats should be exported from whatsapp:
- swipe right on the chat, select "more" and "export chat"
- unzip the resulting folder and rename the .txt file with the name of the chat

Pass the full filepath of the chats you want to import as a list to the high level function chats2pandas to return the corresponding data frame.

Optionally you can pass a dictionary containing aliases for each author in the group chat ('author_name':'alias').
