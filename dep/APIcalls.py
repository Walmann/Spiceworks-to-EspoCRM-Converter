# import requests

from dep.common import getUserSettings
from dep.espocrm_api_client import EspoAPI


userSettings = getUserSettings()
api_url = f"http://{userSettings["EspoIP"]}"

EspoApiClient = EspoAPI(url=f"http://{userSettings['EspoIP']}",api_key=userSettings['APIkey'])

def createComment(commentParentId, commentBody,createdAt, modifiedAt, createdBy, commentType = "Post", commentParentType = "Case" ):
    
    commentData = {
        "type": commentType,
        "parentId": commentParentId,
        "parentType": commentParentType,
        "post": commentBody,
        "createdAt": createdAt,
        "modifiedAt": modifiedAt, 
        "createdBy": createdBy
    }

    response = EspoApiClient.request('POST', 'Note', commentData)
    return response