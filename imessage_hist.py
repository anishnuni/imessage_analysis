#connection code
import os
from subprocess import call
import sqlite3
import pandas as pd
import numpy as np
import csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

conn = sqlite3.connect('/Users/anishnuni/Library/Messages/chat.db')
# connect to the database


messages = pd.read_sql_query("select * from message limit 5000000000", conn)




#export_csv = messages.to_csv('imessages.csv', index = None, header=True)

# get the handles to apple-id mapping table
handles = pd.read_sql_query("select * from handle", conn)
# and join to the messages, on handle_id

messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)
handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)
merge_leve_1 = temp = pd.merge(messages[['text', 'handle_id', 'date','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

message_list = list(merge_leve_1["text"])
number_list = list(merge_leve_1["phone_number"])

i = 0
while i < len(message_list):
    if not message_list[i] or type(number_list[i]) == float:
        del message_list[i]
        del number_list[i]
    else:
        i+=1



#
l = len(message_list)
#fix n maybe
contacts = {}
os.chdir(os.getcwd()+'/DeepMoji-master/')

for i in range(0,2):
    message = message_list[i]
    x = call(["python2",'examples/score_texts_emojis.py',message])
    #can be done more elegantly without having to read from an excel file-later
    with open('test_sentences.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            l = row
    indices = l[2:7]
    values = l[7:]
    n = 0 #max emoji index from excel file
    try:
        y = contacts[number_list[i]]
    except:
        y = np.zeros(64)
        #fix length of zeros array maybe
    for j in range(5):
        y[int(indices[j])] += float(values[j])
    contacts[number_list[i]] = y


#now we should have a dictionary contacts with each contact having a key which
#is bound to a value which is a numpy array of their weight on different emojis.
#the array has not been normalized yet. These values aren't perfect-just uses
#top 5 emojis describing each text.

for key,value in iter(contacts.items()):
    contacts[key] = value / sum(value)
#Values in contacts have been normalized

df = pd.DataFrame(contacts)
writer = ExcelWriter('Analysis.xlsx')
#overwrites file if it exists

df.to_excel(writer,'Sheet1',index=False)
writer.save()
exit()


"""
# get the chat to message mapping
chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)
# and join back to the merge_level_1 table
df_messages = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')
# convert 2001-01-01 epoch time into a timestamp
# Mac OS X versions before High Sierra
datetime(message.date + strftime("%s", "2001-01-01") ,"unixepoch","localtime")
# how to use that in the SQL query
messages = pd.read_sql_query("select *, datetime(message.date + strftime("%s", "2001-01-01") ,"unixepoch","localtime") as date_uct from message", conn)

# convert 2001-01-01 epoch time into a timestamp
# Mac OS X versions after High Sierra
datetime(message.date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")
# how to use that in the SQL query
messages = pd.read_sql_query("select *, datetime(message.date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime") as date_uct from message", conn)
print(messages)
"""
