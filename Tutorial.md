# What is this? 
After Spiceworks stopped supporting local hosting of their ticket system we needed another solution. 
This solution became EspoCRM. 
EspoCRM does not give much control over the import process, so in need of a converter tool i went searching.
I could not find any, and being a lover of challenges i startet creating this script.

This script is created by me for me, so there are some "me specific" things in here. But you are welcome to Fork this Repo and make it work with your own systems.
In other words, this script is not meant for widespread use. But if people are actually going to use it, open an issue and i will make it less me-specific.

If you are looking to use this script, files of interest would be: 
dep/Espo/createComments.py
dep/Espo/createTickets.py
dep/Espo/createUsers.py
dep/Spiceworks/exportSW.py


# TODO
- Script
    - Create save/load system for settings 🕰️
    - Create in-script tutorial ❓
    - Create "Export / Transport SW database" section. 
        - Coding Script ✔️
    - Create "Import to EspoCRM" section. 
        - Coding Script ✔️ 
            - Import users (SQL) ✔️ 
            - Import Tickets (SQL) ✔️ 
                - Import Attachments (API) ✔️
                - Update Attachments info (SQL) ✔️
            - Update creator of notes via SQL. ✔️
                - API Only allows for API user as Creator of notes. Sure this is a thing with Tickets too.
            - Create system for creating files and folders for this tool automatically ✔️
            - Change all Y/N questions to use commonfunc.questionYN
        - BugFix
            - Search for iZettle is giving Error about false positives.
    - Clean up leftover code
- Write tutorial
    - Export Spiceworks ✔️
    - Import to EspoCRM
    
- Other notes: 
    - Legg til "Fjernhjelp, hos oss, hos kunde" felt. ?

# Requirements
- Access to your current Spiceworks data
- EspoCRM installed and setup.
- mySQL (Is usually installed by EspoCRM)
- phpmyadmin (For importing Spiceworks Data)

# How to

# Run in Devmode: 
- Create a file with theh name "DEVFILE" and put in the root folder. The script is programmed to only look for that file to enable Devmode.

## Setup EspoCRM
1. Setup EspoCRM (This guide will use the included Docker Compose file)
    - Edit the Docker Compose file to not use default values for usernames and PW.
    - Create a API user for this tool
        - Give API user full access
        - Copy the API key and paste it in "APIkey" in userSettings.txt
    - Enter IP of EspoCRM in "EspoIP". 
        - Only IP or localhost, no "http" or such.


2. Copy Spiceworks SQL database to Userdata/SpiceworksSQLData
    - Default location: ``C:\Program Files (x86)\Spiceworks\db``
    - Place the content of the db folder directly into SpiceworksSQLData
3. Copy Spiceworks Uploads/Ticket folder to Userdata/SpiceworksSQLData
    - Default location: ``C:\Program Files (x86)\Spiceworks\data\uploads\Ticket``
    - Place the content of the Ticket folder directly into SpiceworksUploads

3. Start app.py and follow the instructions.

4. Enter phpMyAdmin and import these files:
    - users_x.txt | Import into the user table
    - case_x.txt  | Import into the case table
    - note_x.txt  | Import into the note table
    - attachments.txt | Copy the content of the file and run them as a SQL Querie

5. All users have the PW set to "walmann". Change this manually. ( I may make this automatic in the future.)

Default PW for all new users is "walmann"