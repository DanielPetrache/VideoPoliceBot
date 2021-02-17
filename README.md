# VideoPoliceBot
The bot works as follows:

-It finds all the voice channels on a server, then it starts iterating through all the members of each channel;

-It looks if a user has their webcamera on, if yes it adds it to a counter, if no it adds it to a separate counter (it also differentiates between bots and real users);

-If the ratio of camera_users/no_camera_users is greater or equal than a certain value, then it sends a message to all the users without video turned on, telling them they have a minute to turn it on, or they will be disconnected.

-After a minute passes, the bot checks if any of the users without a webcamera have turned it on and sends them a message and it also disconnects the ones who haven't turned their cameras on;

After receiving this message, the user has 15 seconds to turn their camera on, if not they will be disconnected from the channel and also receive another message from the bot.

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/disconnectmessage.png)

The bot does all this by getting a list of all the voice channels of the server, then iterating through every channel' users, if there are any, and keeping track if there are any with webcams on and how many. Also, after those 15 seconds have passed the bot checks the status of the users who didn't have their webcams on to see if any have changed.

This feature can be turned on or off as follows:

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/surveillance.png)

# 2. Ciocoflenderposting

After every message send by a user, be it text, or an embedded media, the bot has a chance of 5% to post the following image:

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/ciocoflender.jpg)

# 3. Emoji Counter

The emoji counter provides a top of 5, up to 15 of the most used emojis for any user on the serve. It does this by making use of a simple SQL database to keep track of all the users on the server, the emojis, be it custom or default, and how many times each user has used each emoji.

![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/topemoji.png)

As it can be seen from the image abose the default structure of the topemoji command is the following:

!topemoji user_name emoji_number

However, the bot can handle cases that stray from the default format:

 - if user_name is missing, the bot will just provide the top emoji_number emojis for the user who entered the command;

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/nouserbutnumber.png)

 - if emoji_number is missing, the bot will provide the top 5 emojis for the requested user;

 - if both of them are missing, the top 5 emojis will be provided for the user who entered the command;
 
 - if any of the parameters is wrong, the bot will give an appropriate message.

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/nouser.png)

 ![alt text](https://github.com/DanielPetrache/VideoPoliceBot/blob/main/nocount.png)
