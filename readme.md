<p align="center">
	<h1 align="center"> Telegram Bot </h1>
</p>

## Description

This is a telegram Bot that can be used as a template for personal telegram bot.

## Telegram API Token Generation

1. First you will need to create a personal telegram account and then search for `@BotFather`. Then type the command - `/newbot`

1. After that enter the `username` for the bot.

1. The `@BotFather` will give you the API Token for the bot.

## Getting started with the Telegram-Bot

1. Make sure you are in the project directory: 

        $cd /path/to/telegram_bot
        
1. Install the requirements: 

        $pip3 install -r requirements.txt

1. Creating `config.yaml` file manually - This could be skipped as running the bot without this file will automatically generate it for you.

    	```yaml
            token: <put the bot token here>
            bot_admin: <bot admin username>
            trusted_users: <any trusted user>
        ```
	
1. The `bot.py` will also generate the `saved` folder inside the project directory.

    - Here all the files will be stored that the trusted_users and admins send to the bot via telegram.

1. Run the bot: 

        $python3 bot.py

1. To Stop the bot: 

        ctrl + c

## Bot Functions

#### There are 3 levels of privileges and has a bottom to top inclusive nature:
1. Admin - AU
1. Trusted User - TU
1. General User - U

|Function|Description|Privilege|
|:---|:---|:---:|
|   /start |   Welcome message |    U   |
|   /help  |   help message    |   U   |
|   /contact    |   Bot Admin Info  |   U   |
|   /ig_dp  |   Download Instagram DP   |   U   |
|   /list   |   List all the saved files    |   U   |
|   /print  |   Print a saved file  |    TU  |
| add_trusted `<username>` | Add new trusted user to list | AU|
| add_admin `<username>` | Add new bot admin to list | AU|
|   Upload a file | Downloads and saves the file locally | TU |

