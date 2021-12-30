import os
import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, Filters
from telegram.ext.messagehandler import MessageHandler
from datetime import datetime
import yaml

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#config.yaml
config = yaml.load(open('./config.yaml').read(), Loader=yaml.FullLoader)
token = config['token']
trusted_users = config['trusted_users']

################
# bot commands # 
################

def start(update, context):
    print("start command used")
    update.message.reply_text("Hi, try the command /help to know more.")

def help(update, context):
    print("help command used")
    update.message.reply_text("""
    The following commands are available:

    /start      -> Welcome message.
    /help       -> This message.
    /contact    -> How to reach out to me.
    /list       -> List all the saved files.
    /print      -> Print a saved file.  Use -> /print <SNo of file in list>
    """)

def contact(update, context):
    print("contact command used")
    update.message.reply_text("@thesarthakjain")

def list(update, context):
    print("list command used")
    update.message.reply_text("Listing the available files\nSNo.     File Name")
    items_list = os.listdir('./saved')
    for item in items_list:
        update.message.reply_text(f'{items_list.index(item)}    {item}')

def print_file(update, context):
    inp=int(context.args[0])
    print("print command used")
    items_list = os.listdir('./saved')
    
    for item in items_list:
        if items_list.index(item)==inp:
            os.system(f'lp ./saved/{item}')
            break
    update.message.reply_text(f'printing {item}')
    print(f'printed {item}')

###################
# other functions # 
###################

def unknown(update, context):
    print("Unknown command used")
    update.message.reply_text("""
    I did not understand that.
    Try using /help
    """)

def no_perm_file(update, context):
    print("no_perm_file")
    update.message.reply_text("You do not have permission to upload a file.")

###################################
# download file handler functions #
###################################

def doc_handler (update, context):
    print("recieved doc")
    update.message.reply_text("recieved doc")
    #get file_path
    get_file_api_url = f'https://api.telegram.org/bot{token}/getFile'
    response = requests.post(url=get_file_api_url, params={'file_id':update.message.document.file_id})
    json_response = json.loads(response.content)
    file_name = update.message.document.file_name
    #get file_content
    get_file_content_api_url = f'https://api.telegram.org/file/bot{token}/' + '{file_path}'
    response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
    file_content = response.content
    with open(f"./saved/{file_name}", 'wb') as file:
        file.write(file_content)
    print("saved doc")
    update.message.reply_text("saved doc")

def photo_handler (update, context):
    print("recieved photo")
    update.message.reply_text("recieved photo")
    #get file_path
    get_file_api_url = f'https://api.telegram.org/bot{token}/getFile'
    response = requests.post(url=get_file_api_url, params={'file_id':update.message.photo[-1].file_id})
    json_response = json.loads(response.content) 
    #set name of the file as current datetime 
    file_name = str(datetime.now())
    file_name = "".join(file_name.split('-'))
    file_name = "-".join(file_name.split(' '))
    file_name = "".join(file_name.split(':'))
    file_name = file_name.split('.')[0]
    #get file_content
    get_file_content_api_url = f'https://api.telegram.org/file/bot{token}/' + '{file_path}'
    response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
    file_content = response.content
    with open(f"./saved/{file_name}.jpg", 'wb') as file:
        file.write(file_content)
    print("saved photo")
    update.message.reply_text("saved photo")

def video_handler (update, context):
    print("recieved video")
    update.message.reply_text("recieved video")
    #get file_path
    get_file_api_url = f'https://api.telegram.org/bot{token}/getFile'
    response = requests.post(url=get_file_api_url, params={'file_id':update.message.video.file_id})
    json_response = json.loads(response.content)
    file_name = update.message.video.file_name   
    #get file_content
    get_file_content_api_url = f'https://api.telegram.org/file/bot{token}/' + '{file_path}'
    response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
    file_content = response.content
    with open(f"./saved/{file_name}", 'wb') as file:
        file.write(file_content)
    print("saved video")
    update.message.reply_text("saved video")

def audio_handler (update, context):
    print("recieved audio")
    update.message.reply_text("recieved audio")
    #get file_path
    get_file_api_url = f'https://api.telegram.org/bot{token}/getFile'
    response = requests.post(url=get_file_api_url, params={'file_id':update.message.audio.file_id})
    json_response = json.loads(response.content)
    file_name = update.message.audio.file_name  
    #get file_content
    get_file_content_api_url = f'https://api.telegram.org/file/bot{token}/' + '{file_path}'
    response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
    file_content = response.content
    with open(f"./saved/{file_name}", 'wb') as file:
        file.write(file_content)
    print("saved audio")
    update.message.reply_text("saved audio")

######################################
# add command handlers to dispatcher # 
######################################

updater = Updater(token, use_context=True)
disp = updater.dispatcher
disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))
disp.add_handler(CommandHandler("contact", contact))
disp.add_handler(CommandHandler("list", list))
disp.add_handler(CommandHandler("print", print_file))

#add file handlers to dispatcher
disp.add_handler(MessageHandler(Filters.document & Filters.chat(username=trusted_users), doc_handler))
disp.add_handler(MessageHandler(Filters.photo & Filters.chat(username=trusted_users), photo_handler))
disp.add_handler(MessageHandler(Filters.video & Filters.chat(username=trusted_users), video_handler))
disp.add_handler(MessageHandler(Filters.audio & Filters.chat(username=trusted_users), audio_handler))
disp.add_handler(MessageHandler(Filters.document | Filters.photo | Filters.video | Filters.audio, no_perm_file))


#add message handlers to dispatcher
disp.add_handler(MessageHandler(Filters.text,unknown))


#run the bot
updater.start_polling()
print("Bot is online!")
updater.idle()