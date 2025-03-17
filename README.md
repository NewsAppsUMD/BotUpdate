# BotUpdate


I have a new plan for my bot update. I want to create a bot that would update me every time a crime is recorded in pg county. This both would preferebly tell me the details of the crime, but ultimately the most improtant part is knowing the crime that happened.

So the output of this bot is that it would first notify me whether or not a violent or nonviolent crime took place. It would then tell me the type of crime that happened such as murder , or unarmed robbery. Finally it will tell me the location of where the crime took place.

My code as of right now currently produces crimes from July 1st, even though I want it to produce a list of the crimes from the most recent day. I have to figure out away for this to be replicated.

As of now my current data will be collected from the pg county open data portal. The link is currently found here: https://data.princegeorgescountymd.gov/resource/xjru-idbe.json. The data is returned in JSON format, containing crime details such as the incident type, crime category, street address, and more.
As I stated earlier my bot should first be able to determine if the recorded crime is violent or non-violent.  However as of right now my code is only working for violent crimes, because when I attempted to create a variable to store non violent crimes for the dataset my code wasn’t working. When I run my code currently it produces: 
🚨 Non-Violent - ACCIDENT
📍 2116 INGRAHAM ST
🕒 2023-07-01 00:00:00
 So right now my code does extract the location of the crime, now I just need to figure out how to get it up to date. I need to figure out away to have some sort of date variable in my data where the data stored can change automatically without manually changing the code myself. 

I want my data either to store the data temporarily in memory or store it in a JSON or SQLite database for quick retrieval. Then figure out a bot system to send me notifications automatically without having to run the code.
The first step in implementing this is to set up a script that will fetch the crime data from the Dataset. Using the library request to get the data  and pandas, json  to process and store it. Once the data is fetched, I should be able to completely categorize the crimes and format the output for the bot.

Once all  this setup is complete, My bot will be able to notify details about each new crime as soon as it’s recorded, helping me stay updated in real time.

