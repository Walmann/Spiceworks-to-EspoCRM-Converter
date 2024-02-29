import os.path
import re
import mimetypes
import base64
import requests
# import magic
import dep.common as commonFunc
from dep.common import getUserSettings
from dep.espocrm_api_client import EspoAPI
import dep.SQLcalls as SQLcalls
uploadFolder = "./Userdata/SpiceworksUploads"
userSettings = getUserSettings()

def checkFilepath(PathString):
    """Function to check if the Attachment actually exists.

    Args:
        PathString (str): Path string for the file you want to check

    Raises:
        ValueError: Raised if the file does not exists

    Returns:
        str: Return Pathstring if the file exists.
    """
    if os.path.isfile(PathString):
        return PathString
    else:
        raise ValueError(f"Could not find file: {PathString}")



def findCommentID(fileName):
    """Find the Comment ID from the filename. \n The Comment ID can be found at the start of the filename.

    Args:
        fileName (str): Filename for the file you wish to find the Comment ID of.

    Returns:
        str: The Comment ID
    """
    matches = re.search(r"^\d+", fileName)

    commentID = matches.group()
    return commentID


def findCorrectFile(folderPath, ticketID):
    """There are two files with almost the same name. One is the original the other is the thumbnail version.

    Args:
        folderPath (str): Path to the Uploads folder.
        ticketID (str): The Ticket ID from the ticket the file is uploaded to.

    Raises:
        ValueError: Raised if it could not find the non-thumbnail version of the file.

    Returns:
        str: The filename of the non-thumbnail version
    """

    regExPattern = re.compile(r"^\d{1,6}-thumb-")

    # TODO Tickets can include multiple attachments. Make sure this works.

    fileList = os.listdir(folderPath)
    for attachmentFilename in fileList:
        if len(fileList) == 1:
            return attachmentFilename
        elif regExPattern.match(attachmentFilename):
            pass
        else:
            return attachmentFilename

    raise ValueError("Could not find attachment!")
    pass

def getMimeType(filePath):
    """Return the filetype in a way that can be used in a API call.

    Args:
        filePath (str): Full path to the file

    Returns:
        str: The found mimeType.
    """
    mimeType = mimetypes.guess_type(filePath)
    return mimeType


def createFileDict():
    """Scans the Spiceworks Uploads folder and create a dict with information about attachments that needs to be uploaded to Espo.

    Returns:
        dict: File Dict
    """
    fileDict = []
    folderList = os.listdir(uploadFolder)
    for x in folderList:
        currentAttachmentFolder = os.path.realpath(uploadFolder + "/" + x)

        tempDict = {}
        tempDict["ticketID"] = x  # x is the foldername, wich also is the ticket ID
        tempDict["filename"] = findCorrectFile(folderPath=currentAttachmentFolder, ticketID=x)
        tempDict["filePath"] = checkFilepath(currentAttachmentFolder + "/" + tempDict["filename"])
        tempDict["CommentID"] = findCommentID(tempDict["filename"])  # Get the Comment ID from the filename
        tempDict["mimeType"] = getMimeType(tempDict["filePath"])

        fileDict.append(tempDict)

    return fileDict

def convertFileToBase64(filePath):
    """Convert file to base64 string

    Args:
        filePath (str): Full path to the file you want to encode.

    Returns:
        str: Base64 String
    """
    binary_file = open(filePath, 'rb')
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data).decode("utf-8")
    return base64_encoded_data


def uploadToEspo(currentTicket):
    """Upload file to EspoCRM. Includes uploading the file via API and creating entry in attachments.txt file wich are used to edit "parent_id" and such.

    Args:
        currentTicket (dict): Current ticket.
    """
    
    api_url = f"http://{userSettings["EspoIP"]}"
    EspoApiClient = EspoAPI(url=f"http://{userSettings['EspoIP']}",api_key=userSettings['APIkey'])

    ApiRequestData = {
        "field": "attachments",
        "file": f"data:{currentTicket["mimeType"][0]};base64,{convertFileToBase64(currentTicket["filePath"])}",
        "name": currentTicket["filename"],
        "parentType": "Note",
        "role": "Attachment",
        "type": currentTicket["mimeType"][0]
    }

    response = EspoApiClient.request('POST', 'Attachment', ApiRequestData)

    SQLcalls.updateAttachment((
        ("parent_id", currentTicket["CommentID"], response['id']),
    ))

    pass


def uploadAttachments():
    """Start process of uploading attachments. Remember to run the SQL queries in "attachments.txt" file in "OutputFiles"

    Returns:
        bool: Returns True if everything is OK.
    """
    # Make sure the user has importer Users, Tickets, and Comments into EspoCRM
    if not commonFunc.checkForDev():
        inputReadyToStart = commonFunc.questionYN(
            "Starting job of importing Attachments. Are Users, Tickets, and Comments already imported into EspoCRM? Y/n : "
        )
    else:
        inputReadyToStart = True

    if inputReadyToStart:
        # Create dict of uploads
        attachmentsDict = createFileDict()

        print("Uploading Attachments, and creating attachments.txt")
        attachLen = len(attachmentsDict)
        for index, entry in enumerate(attachmentsDict):
            uploadToEspo(entry)
            print(f"Attachments: {index} / {attachLen}")
            pass

    else:
        input(
            "Go import Users, Tickets, and Comments before continuing. Press Enter to try again: "
        )
        uploadAttachments()

    return True
