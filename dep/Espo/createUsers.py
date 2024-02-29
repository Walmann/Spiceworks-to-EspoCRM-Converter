
import json
from datetime import datetime

import dep.common as commonFunc

def createUsers():

    userList = json.load(open("./workingDir/ticketAndUsers", "r"))
    userList = userList["users"]

    # Is users being loaded corectly?
    SQLQuery = []
    SQLQuery.append("INSERT INTO `user` (`id`, `deleted`, `user_name`, `type`, `password`, `auth_method`, `api_key`, `salutation_name`, `first_name`, `last_name`, `is_active`, `title`, `gender`, `created_at`, `modified_at`, `delete_id`, `middle_name`, `default_team_id`, `contact_id`, `avatar_id`, `created_by_id`, `dashboard_template_id`, `working_time_calendar_id`, `layout_set_id`) VALUES")

    for user in userList:
        user = userList[user]

        # Get Username
        username = user["email"]#.split("@")[0]
        if username == 'spiceworks_builtin_account_do_not_alter':
            continue
        
        # Get Role of current user
        userRole = getCorrectUserRole(user["role"])

        # Get date, for creation time:
        time = datetime.now()
        formatedTime = time.strftime("%Y-%m-%d %H:%M:%S")
        # TODO Ask user for a default password for all users, and try to encrypt it
        # Default PW: 
        # clear: walmann 
        # Encrypted: 1X8bs.j.lTdLp6xKfXxRycUDlI9uDO/SznTucwOEyUUv79y1XRQPAj9/Ibgy6fAsOVt6BIjnx22SryKa7p9Kj0

        userQuery = f"('{user["id"]}', 0, '{username}', '{userRole}', '1X8bs.j.lTdLp6xKfXxRycUDlI9uDO/SznTucwOEyUUv79y1XRQPAj9/Ibgy6fAsOVt6BIjnx22SryKa7p9Kj0', NULL, NULL, NULL, '{user["first_name"]}', '{user["last_name"]}', 1, NULL, NULL, '{formatedTime}', '{formatedTime}', '0', NULL, NULL, NULL, NULL, 'importtool', NULL, NULL, NULL),"
        
        SQLQuery.append(userQuery)
    
    # Change the last query, replace "," with ";". SQL Syntax reasons
    SQLQuery = commonFunc.formatLastSQLQuery(SQLQuery)

    commonFunc.createSQLOutputFile(SQLQuery)
    # return SQLQuery


convertUserRoleToRegular = {} # For used with input from askUserRoleAction
def askUserRoleAction(userRole):
    global convertUserRoleToRegular

    
    if "repeatStep" in convertUserRoleToRegular:
        return convertUserRoleToRegular["repeatStep"]
  
    
    # If there is no section for this current userRole

    if userRole not in convertUserRoleToRegular:
        convertUserRoleToRegular[userRole] = {}
        validAnswers = False
        while True:
            convertUserRoleToRegular[userRole]["setRole"] = input(f"This users role is {userRole}, do you want to change {userRole} to 'regular', 'admin', or keep the current role? (R)egular/(a)dmin/(k)eep current: ")[0].lower()
            convertUserRoleToRegular[userRole]["RepeatForAll"] = input("Repeat this operation? (The user 'admin' is not affected by this): (a)ll roles/(T)his role only/(n)o repeat: ")[0].lower()
            
            for x in "rak":
                if x in convertUserRoleToRegular[userRole]["setRole"]:
                    validAnswers = True
                    break
            if validAnswers is False:
                print("Error in input. Try again:")
            else: 
                pass
            
            validAnswers = False
            for x in "yn":
                if x in convertUserRoleToRegular[userRole]["RepeatForAll"]:
                    validAnswers = True
                    break
            if validAnswers is False:
                print("Error in input. Try again:")
            else: 
                break
 

    # If user answered Yes on Repeat for all, replace the convertUserRoleToRegular variable, and insert the selected role.
    if convertUserRoleToRegular[userRole]["RepeatForAll"] == "y":
        repeatingRole = convertUserRoleToRegular[userRole]["setRole"]
        convertUserRoleToRegular["repeatStep"] = {repeatingRole}
        # return repeatingRole
        # convertUserRoleToRegular["repeatStep"] = convertUserRoleToRegular[userRole]["setRole"]
        # TODO Make this better. Repeating code.
        if repeatingRole == "a": 
            return "admin"
        elif repeatingRole == "r": 
            return "regular"
        elif repeatingRole == "k": 
            return userRole



    elif convertUserRoleToRegular[userRole]["setRole"] == "a": 
        return "admin"
    elif convertUserRoleToRegular[userRole]["setRole"] == "r": 
        return "regular"
    elif convertUserRoleToRegular[userRole]["setRole"] == "k": 
        return userRole

def getCorrectUserRole(userRole):
    # TODO Create questionare for what the user want to do with each userRole. 
    
    if userRole == "admin":
        return "admin"
    
    elif userRole == "end_user":
        return "regular"
    
    else:
        print("The user is not 'admin' or 'regular'. Setting role to 'regular'. (Work in progress)")
        return "regular"