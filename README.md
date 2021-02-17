# VideoPoliceBot
This discord bot started simple, but I kept adding features, at the moment they are the following:

# 1. Video Surveillance

This is the bot's original functionaly, hence I thought that it should give the bot its name.
After using the command '!surveillance on', the bot finds all the voice channels on a server, and looks at the users connected in each of them.

If the ratio of camera_users/no_camera_users in a channel is greater or equal than a certain value, then it sends a message to all the users without video turned on, telling them they have 15 seconds to turn it on, or they will be disconnected.

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/firstmessage.png)

After that time passes, the bot checks if any of the users without a webcamera have turned it on. Lastly, it disconnects the ones who haven't turned their cameras on

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/disconnectmessage.png)

This feature can be turned on or off as follows:

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/surveillance.png)

# 2. Ciocoflenderposting

After every message send by a user, be it text, or an embedded media, the bot has a chance of 5% to post the following image:

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/ciocoflender.jpg)

# 3. Emoji Counter

The emoji counter provides a top of 5 to 15 of the most used emojis for any user on the server. It does this by making use of a simple SQL database to keep track of all the users on the server, the emojis, be it custom or default, and how many times each user has used each emoji.

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/topemoji.png)

As it can be seen from the image abose the default structure of the topemoji command is the following:

!topemoji user_name emoji_number

However, the bot can handle cases that stray from the default format:

 - if user_name is missing, the bot will just provide the top emoji_number emojis for the user who entered the command;

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/nouserbutnumber.png)

 - if emoji_number is missing, the bot will provide the top 5 emojis for the requested user;

 - if both of them are missing, the top 5 emojis will be provided for the user who entered the command;
 
 - if any of the parameters is wrong, the bot will give an appropriate message.

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/nouser.png)

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/nocount.png)

# 4. Tic Tac Toe

VideoPoliceBot can allow two users to play a game of tic tac toe. This is done by using the command !tictactoe @user1 @user2, which prompts the bot to create a secret text channel and give the two tagged users a role, enabling them to see and write messages in said channel.

Afterwards, the bot posts the board in the channel and calls the first player to make a move:

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/tictactoecommand.png)

Afterwhich, players alternate by using the command '!place line column', until one of them wins, or until the match finishes with a draw.

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/pictures/placecommand.png)

When match is finished, the players can choose to go for another one, in which case the bot resets the board, or they can stop, which prompts the bot to delete the channel and remove the tic tac toe role from the two users.

