
import json

import dep.common as commonFunc

def createComments():
    
    ticketList = json.load(open("./workingDir/ticketAndUsers", "r"))
    ticketList = ticketList["tickets"]

   
    SQLQuery = []
    SQLQuery.append("INSERT INTO `note` (`id`, `deleted`, `post`, `data`, `type`, `target_type`, `number`, `is_global`, `is_internal`, `created_at`, `modified_at`, `parent_id`, `parent_type`, `related_id`, `related_type`, `created_by_id`, `modified_by_id`, `super_parent_id`, `super_parent_type`) VALUES")
    
    
    for ticket in ticketList:

        for comment in ticketList[ticket]["comments"]:
            comment = ticketList[ticket]["comments"][comment]

            ticketQuery = f"({comment["id"]}, 0, '{commonFunc.formatStringForSQL(comment["body"])}', '{{}}', 'Post', NULL, {comment["id"]}, 0, 0, '{comment["created_at"]}', '{comment["updated_at"]}', '{comment["ticket_id"]}', 'Case', NULL, NULL, '{comment["created_by"]}', NULL, NULL, NULL),"
            

            SQLQuery.append(ticketQuery)
        
    # Change the last query, replace "," with ";". SQL Syntax reasons
    SQLQuery = commonFunc.formatLastSQLQuery(SQLQuery)


    commonFunc.createSQLOutputFile(SQLQuery)
