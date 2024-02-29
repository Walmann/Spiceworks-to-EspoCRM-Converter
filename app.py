# Information
# - spiceworks_prod.db -> Ticket DB
# - SWUploadDir -> Ticket Attachments, Foldername corresponds to ticket number

# Defaults
# - TicketDB ->  C:\Program Files (x86)\Spiceworks\db
# - UploadDir -> C:\Program Files (x86)\Spiceworks\data\uploads\Ticket
#
# - Docker Container location -> \\wsl$\docker-desktop-data\mnt\wsl\docker-desktop-data\data\docker\image


import os
import dep.Spiceworks.exportSW as exportSW

from dep.Espo import createComments, createTickets, createUsers, uploadAttachments

def main():
    # Defaults
    swDbLoc = "./Userdata/SpiceworksSQLData/spiceworks_prod.db"
    swUploadLoc = "./Userdata/SpiceworksUploads/"

    CheckUserdataIsOK((swDbLoc, swUploadLoc))

    # Create needed files and folders:
    neededFolders = [
        "./workingDir",
        "./Outputfiles"
    ]

    for folder in neededFolders:
        os.makedirs(folder, exist_ok=True)

    # Export EspoCRM Information
    print("#### EspoCRM: Exporting Tickets and Users ####")
    exportSW.exportTicketsAndUsers(SpiceworksDatabase=swDbLoc)
    print("\n#### EspoCRM: Exporting Attachments from tickets. ####")
    exportSW.exportTicketUploads(SpiceWorksUploadLoc=swUploadLoc)


    # Import into EspoCRM
    print("\n#### Creating SQL file for Users ####")
    createUsers.createUsers() # This has to be SQL. So no need to change
    print("\n#### Creating SQL file for Tickets ####")
    createTickets.createTickets()
    print("\n#### Creating SQL file for Comments. ####")
    createComments.createComments() # TODO Recreate this to use API. Attachments need to be uploaded with the comment.
    print("\n#### Starting upload of Attachments ####")
    uploadAttachments.uploadAttachments()
    
    print("Finnished!")
    
    pass




def CheckUserdataIsOK(neededFiles):
    """Check if all the files needed for export is available in the right places.

    Args:
        neededFiles (Tuple)): Tuple containing string(s) needed files

    Returns:
        Bool: Returns true if all files are available.
    """
    errorLog = []

    try:
        for entry in neededFiles:
            # temp = os.path.isfile(entry)
            if os.path.isdir(entry):
                x = os.listdir(entry)
                if len(x) == 0:
                    errorLog.append("Can't find %s", entry)
            elif not os.path.isfile(entry):
                errorLog.append("Can't find %s", entry)
                pass
            else:
                break
    except Exception as e:
        print("Error: " + str(e))
        exit()

    return True


if __name__ == "__main__":
    main()
    pass
