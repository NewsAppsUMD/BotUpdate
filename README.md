Data I used for this project: 

https://data.princegeorgescountymd.gov/Public-Safety/Crime-Incidents-July-2023-to-Present/xjr

U-idbe/data_preview 



To start my project, it was originally just a crimebot that notifies me 10:00 am every Friday if there is a new crime. I decided to expand this project to include a site that talks about crime in PG county in general from July 2023 to April 2025. The dataset I used comes from the PG County official site. When you download the dataset you get a csv file called "Crime_Incidents_July_2023_to_Present_20250516.csv". For the bot part of this assignment, as it stopped working when I used it last time. I store the "Crime_Incidents_July_2023_to_Present_20250516.csv" data into my database called pg_county_crime.db, which was made with a code under database_pg.py. I originally had an issue with my APP not working due to the fact that the API only returns a maximum of 1,000 rows. Using an offset parameter instead of dates alone solved the issue. 



With this database of my project, I had a much easier time running my slack bot in the slackbot channel. As I realized, part of the reason I was having issues with my slack bot not running was due to the fact I originally only defined the secret in Actions. Then I needed to define it in both Actions and Codespaces under the secret and variables sections.  Now my bot runs automatically every Friday at 10:00. This bot will always be useful as long as PG County uses their current automatically updated API. If they decide to change the API, then the bot will no longer work. However, getting a summary over the past 3 weeks on crime in pg county will be useful for those who want to stay safe when there pg county. I will know my bot updates from my settings on GitHub. After I did this for the most part, it was smooth sailing when it came to the slack bot. However, I was flustered a few times when I ran my slack bot, and it wouldn’t work. I kept having to go to the Slack API and get a Bot User OAuth Token. Now, creating my site was even the harder part. Originally, I was using my database to create the site, but I had no idea what I was doing. 



There were a few days when my site was just a Google Maps page where pg county had some heat maps visuals. It was awful, and I decided not to use the database to create the site, but the original csv file itself. One thing that frustrated me with this CSV file was the fact that it had no city column. One idea I had for this project was to compare PG county crime to Montgomery County crime. Montgomery County website: https://data.montgomerycountymd.gov/Public-Safety/Crime/icn6-v9z3/data_preview



Data, while too large for GitHub, unfortunately, had a lot of interesting data for me to use. The equivalent of the city column in pg county was the street number and location column, which were just the latitude and longitude combined. I would like a city column in PG county, so I could compare the crimes of PG county and Montgomery County's most populated cities. Overall, if I had to start over this project. My final app would either be on Montgomery County crime or compare pg county crime to Montgomery County crime. As I mentioned earlier, the csv file for Montgomery County data was too large, and I was unable to push to GitHub. So I got frustrated and just kept my original idea with pg county. 

I originally had 5 graphs on my app. Four of them didn’t show the trend I was trying to go for. Having graphs that show if pg county crime is going down. As a result, to make it easier, I made 3 separate CSVs where I took the data from the original data. In order to make three charts. One about pg county total crime over the past few years. One chart where I take the 5 most common crimes in pg county and how they have trended over the past few years, and a stacked bar chart where I see which sectors in Maryland get the most crime. Since my CSV files display the data. That means it won’t update on its own when new crime data comes in. If I want the site to show the latest trends, I’ll have to update the CSV files myself. Because of this, the website might not last as long as the Slack bot, which runs automatically and stays up to date. Unless I change how the site works in the future, it could fall behind in showing the latest crime patterns. 



Overall, I’m a bit disappointed in my project. I procrastinated more than I should have, and I truly believe that I could have made a project deserving of being put on my resume if I put in more effort. 





