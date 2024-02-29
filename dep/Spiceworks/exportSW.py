import sqlite3
import json
import os
import re
import shutil






def exportTickets(swCursor):
    """Exports tickets into a Dict format. Creates a sub category names tickets.

    Args:
        swCursor (sqlite3.Cursor): SQlite Cursor object

    Returns:
        Dict: Dict containing all exportet tickets
    """

    # Export Ticket data
    swCursor.execute("SELECT * FROM tickets")
    ticketData = swCursor.fetchall()
    ticketCategories = swCursor.description

    # Loop Through tickets
    dbDict = {}

    for ticketSingle in ticketData:
        ticketID = ticketSingle[0]

        # Create JSON structure
        dbDict[ticketID] = {}
        dbDict[ticketID]["info"] = {}


        for index, key in enumerate(ticketSingle):
            if isinstance(key, str):
                dbDict[ticketID]["info"][ticketCategories[index][0]] = key.replace("'","")

            else: 
                dbDict[ticketID]["info"][ticketCategories[index][0]] = key

        # if ticketID == 26:
        #     print()
        iZettleIndex = exportIZettleInfo(dbDict[ticketID]["info"]["description"])
        if iZettleIndex is not None:
            dbDict[ticketID]["iZettle"] = iZettleIndex
        
        # temp = dbDict[ticketID]
        # print("")

    # Export comments
    swCursor.execute("SELECT * FROM comments")
    commentData = swCursor.fetchall()
    commentsCategories = swCursor.description

    # dbDict[ticketID]["iZettle"] = None
    for commentSingle in commentData:
        ticketID = commentSingle[1]
        commentID = commentSingle[0]
        iZettleIndex = None


        # Create JSON structure
        if "comments" not in dbDict[ticketID]:
            dbDict[ticketID]["comments"] = {}
        if commentID not in dbDict[ticketID]["comments"]:
            dbDict[ticketID]["comments"][commentID] = {}

        for index, key in enumerate(commentSingle):
            dbDict[ticketID]["comments"][commentID][commentsCategories[index][0]] = key
        

        iZettleIndex = exportIZettleInfo(commentSingle[2])
        if iZettleIndex is not None:
            dbDict[ticketID]["iZettle"] = iZettleIndex    

    return dbDict


def exportUsers(swCursor):
    """Export User information from SW.

    Args:
        swCursor (SQL.curson): SQL cursor for current database.

    Returns:
        dict: dict with User information
    """
    # Export comments
    swCursor.execute("SELECT * FROM users")
    userData = swCursor.fetchall()
    userCategories = swCursor.description

    # currentSection = "users"

    curDict = {}
    # curDict[currentSection] = {}

    for user in userData:
        userID = user[0]

        # Create JSON structure
        # curDict[currentSection][userID] = {}
        curDict[userID] = {}

        for index, key in enumerate(user):
            # curDict[currentSection][userID][userCategories[index][0]] = key
            curDict[userID][userCategories[index][0]] = key

    return curDict



def exportIZettleInfo(ticketString):
    """Find iZettle information that is written in ticket comments. If it has a match for zettle but can't find the ID it will print an error and write that into Outputfolder/iZettleStrings.txt.

    Args:
        ticketString (str): string to search for iZettle information

    Returns:
        str: String containing the iZettle ID. Could be an int but isn't
    """
    iZettleIndex = None
    foundMatch = False


    regexString = re.compile(r"[iIzZ]ettle\D*(\d+)")

    x = re.findall(regexString, ticketString)



    if not len(x) == 0:
        foundMatch = True
        iZettleIndex = x[0]

    # if "iZettle: #" in ticketString:
    #     print("")

    if not foundMatch:
        if "Zettle" in ticketString or "zettle" in ticketString:
            #TODO Create this option:
            # input("Found the word Zettle in a string, but it did not match with the RegEx. Is this a valid iZettle number? y/N")
            # If no: Add to ingore list?
            print("Found String with iZettle match but no number. Writing string to 'iZettleStrings.txt' in root folder.")
            with open("./Outputfiles/iZettleStrings.txt", "a+") as file:
                file.write("#########\nNew ticket: \n"+ticketString+"\n\n\n\n")

    foundMatch = False
    return iZettleIndex


def exportTicketsAndUsers(SpiceworksDatabase):
    

    # Variables
    dbDict = {}

    swDb = sqlite3.connect(SpiceworksDatabase)
    swDbCursor = swDb.cursor()

    dbDict["tickets"] = exportTickets(swDbCursor)
    dbDict["users"] = exportUsers(swDbCursor)




    with open("workingDir/ticketAndUsers", "w+") as file:
        file.write(json.dumps(dbDict))

    print("")

def exportTicketUploads(SpiceWorksUploadLoc):
    workingDir = "./workingDir/Uploads"
    try:
        os.makedirs(os.path.dirname(workingDir), exist_ok=True)
        print(f"Copying Uploaded files to {workingDir}")
        shutil.copytree(SpiceWorksUploadLoc, workingDir)
    except Exception as e:
        print(f"Error copying Uploaded files: {e}")
   