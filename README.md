# VideoPoliceBot
The bot works as follows:

-It finds all the voice channels on a server, then it starts iterating through all the members of each channel;

-It looks if a user has their webcamera on, if yes it adds it to a counter, if no it adds it to a separate counter (it also differentiates between bots and real users);

-If the ratio of camera_users/no_camera_users is greater than or equal to a certain value, then it sends a message to all the users without video turned on, telling them they have a minute to turn it on, or they will be disconnected.

-After a minute passes, the bot checks if any of the users without a webcamera have turned it on and sends them a message and it also disconnects the ones who haven't turned their cameras on;

-Lastly, the bot moves on to the next voice channel and when it's done it waits for 5 minutes, then it goes through each channel again.
