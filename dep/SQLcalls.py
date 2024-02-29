
import dep.common as commonFunc



def updateNote(columnValueId):
    currentValues = ""
    with open("./Outputfiles/notes.txt", "a+") as file:
        for x in columnValueId:
            column, value, id = x
            currentValues = currentValues+f"UPDATE note SET {column} = '{value}' WHERE id = {id};\n"
        file.write(currentValues)

def updateAttachment(columnValueId):
    currentValues = ""
    with open("./Outputfiles/attachments.txt", "a+") as file:
        for x in columnValueId:
            column, value, id = x
            currentValues = currentValues+f"UPDATE `attachment` SET `{column}` = '{value}' WHERE `attachment`.`id` = '{id}';\n"
        file.write(currentValues)
def createTickets():
    
    pass
