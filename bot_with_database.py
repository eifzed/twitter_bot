import tweepy
import random
import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#import pprint

print('This is my twitter bot')

#twitter access
CONSUMER_KEY = '_____________________'
CONSUMER_SECRET = '____________________'
ACCESS_KEY = '_______________________'
ACCESS_SECRET = '___________________________'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

#spreadsheet access
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


sheet = client.open('casper_database').sheet1
FILE_NAME = 'last_id_row.txt'


def retrieve_last_id_row(file_name):
    f_read = open(file_name, 'r')
    last_id_row = str (f_read.read().strip())
    last_id_row = last_id_row.split(' ')
    last_id = int(last_id_row[0])
    last_row = int(last_id_row[1])
    f_read.close()
    return last_id, last_row

def store_last_id_row(last_id, last_row, file_name):
    a = str(last_id)
    b = str(last_row)
    last_id_row = a + ' ' + b
    print (last_id_row)
    f_write = open (file_name, 'w')
    f_write.write(str(last_id_row))
    f_write.close()
    return

def reply():
    with open('reply.txt') as f:
        lines = f.read().splitlines()
    a = random.randint(0, len(lines)-1)
    return lines[a]

def update_database(last_row_update, username_update, id_update, mention_update, reply_update,):
    print ("updating database...")
    num = (last_row_update)
    time = str(datetime.datetime.now())
    time = time.split(' ')
    row = [num, time[0], time[1], username_update, id_update, mention_update, reply_update]
    index = num+1
    sheet.insert_row(row, index)
    print ('database #'+ str(num) + ' updated')
    return index



#for testing, put 1088093617908928512 0 on the file
def reply_to_tweets():
    print ('Retrieving and Replying to tweets...')
    last_id, last_row = retrieve_last_id_row(FILE_NAME)
    mentions = api.mentions_timeline(last_id, tweet_mode = 'extended')
    for mention in reversed(mentions):
        print (str(mention.id)+' - '+mention.full_text)
        last_id = mention.id

        if '#casperbot' in mention.full_text.lower():
            print ('found #casperbot !')
            reply = insult()
            api.update_status('@'+ mention.user.screen_name + ' ' + reply, mention.id)
            print ('reply sent')
            name = mention.user.screen_name
            id = str(mention.id)
            print (last_row, name, id, mention.full_text, reply)
            last_row = update_database(last_row, name, id, mention.full_text, reply)
            store_last_id_row(last_id, last_row, FILE_NAME)

while True:
    reply_to_tweets()
    time.sleep(30)
