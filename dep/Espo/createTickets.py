
import re
import json

import dep.common as commonFunc

def createTickets():
    """Takes in a list of tickets exported from Spiceworks.
    The returned list can be assembled to a query to mySQL

    Args:
        ticketList (List): List of tickets exported from Spiceworks

    Returns:
        Dict: Dict that can be converted to a string, for importing tickets into mySQL, via phpMyadmin
    """    
    
    ticketList = json.load(open("./workingDir/ticketAndUsers", "r"))
    ticketList = ticketList["tickets"]
    
    SQLQuery = []

    SQLQuery.append("INSERT INTO `case` (`id`, `name`, `deleted`, `number`, `status`, `priority`, `type`, `description`, `created_at`, `modified_at`, `account_id`, `lead_id`, `contact_id`, `inbound_email_id`, `created_by_id`, `modified_by_id`, `assigned_user_id`, `i_zettle_i_d`, `faktura_nummer`, `statusvente`) VALUES")
    
    for ticket in ticketList:
        ticket = ticketList[ticket]
        ticketinfo = ticket["info"]

        fakturaNumber = findFakturaNumber(ticket["comments"])

        ticketStatus, statusvente = handleFakturerbar(ticketStatus=ticketinfo["c_fakturerbar"], ticket=ticket, fakturaNumber=fakturaNumber)

        ticketLocation = ticketinfo["category"]


        if "iZettle" in ticket:
            ticketiZettle = ticket["iZettle"]
            ticketStatus = "Closed"
        else: 
            ticketiZettle = 0


        # If ticket is marked as closed in SW, just mark it as closed in Espo too.
        if ticketinfo["status"] == "closed":
            ticketStatus = "Closed"

        
        ticketQuery = f"('{ticketinfo["id"]}', '{commonFunc.formatStringForSQL(ticketinfo["summary"])}', 0, {ticketinfo["id"]}, '{ticketStatus}', 'Normal', {ticketLocation}, '{commonFunc.formatStringForSQL(ticketinfo["description"])}', '{commonFunc.formatStringForSQL(ticketinfo["created_at"])}', '{commonFunc.formatStringForSQL(ticketinfo["updated_at"])}', NULL, NULL, NULL, NULL, {ticketinfo["created_by"]}, NULL, {ticketinfo["assigned_to"]}, {ticketiZettle}, {fakturaNumber if isinstance(fakturaNumber, int) else 'NULL'}, {f'\'{statusvente}\'' if isinstance(statusvente, str) else 'NULL'}),"
        

        SQLQuery.append(ticketQuery)


    SQLQuery = commonFunc.formatLastSQLQuery(SQLQuery)

    commonFunc.createSQLOutputFile(SQLQuery)


def handleFakturerbar(ticketStatus, ticket, fakturaNumber):
    """Convert ticketStatus from SW to EspoCRM names.

    Args:
        ticketStatus (string): ticketStatus from Spiceworks
        ticket (dict): The current ticket in whole
        fakturaNumber (int): FakturaNumber for current ticket

    Raises:
        UserWarning: Raised if unknow ticetStatus is found.

    Returns:
        tuple: (newStatus, statusvente). newStatus is the new status used in EspoCRM. statusvente is a subStatus, used for newStatus = Pending
    """    
    ticketStatus = ticketStatus.lower()

    newStatus = ""
    statusvente = None

    # TODO Change this:
    #   - If ticketStatus is New:
    #       What should new status be?
    #       Save answer into variable/textfile for lookup later
              

    if ticketStatus == "avtalt":
        # Create check for ticket Close status from SW
        newStatus = "Closed"
    
    elif ticketStatus == "ja":
        newStatus = "Closed"
    
    elif ticketStatus == "klar til levering":
        # newStatus = Pending, statusvente = Klar for levering
        newStatus = "Pending"
        statusvente = "Klar for levering"
    
    elif ticketStatus == "ja på e-post":
        newStatus = "Closed"
    
    elif ticketStatus == "laget utkast":
        # Check for ticket Closed status in SW.
        newStatus = "Closed"
    
    elif ticketStatus == "ferdig":
        # Check for Fakturanummer, if no number is found set newStatus to "Klar til fakturering"
        newStatus = "Closed"
    
    elif ticketStatus == "nei":
        newStatus = "New"

    elif ticketStatus == "goodwill":
        newStatus = "Closed"
    
    elif ticketStatus == "betalt izettle":
        newStatus = "Closed"
    
    elif ticketStatus == "venter på kunde":
        # newStatus = Pending, statusvente = Klar for levering
        newStatus = "Pending"
        statusvente = "Venter på kunde"
    
    elif ticketStatus == "venter på levering":
        # newStatus = Pending, statusvente = Klar for levering
        newStatus = "Pending"
        statusvente = "Klar for levering"
    
    elif ticketStatus == "venter på tredjepart":
        # newStatus = Pending, statusvente = Klar for levering
        newStatus = "Pending"
        statusvente = "Venter på tredjepart"
    
    elif ticketStatus == "venter på varer":
        # newStatus = Pending, statusvente = Klar for levering
        newStatus = "Pending"
        statusvente = "Venter på varer"
    
    else: 
        raise UserWarning(f"Unknown ticketStatus: {ticketStatus}")
        # return ("Fakturert", fakturaNummerTicket)
    
    return (newStatus, statusvente)



def handleInvalidFakturaNumber(fakturaNumber, ticketID):

    if commonFunc.checkForDev():
        # If Dev, just pass "No fakturanumber".
        userInput = 3
    elif isinstance(fakturaNumber, list):
        userInput = int(input(f"Multiple fakturaNumbers detected\nfakturanumber: {str(fakturaNumber)}\nTicketID: {ticketID}\n\nChoose an option:\n1. Everything is fine (Currently this script can't handle multiple FakturaNumbers, use only if there is only 1 number in fakturanumber.\n2. Manualy input fakturanumber\n3. No Faktura number for ticket\nSelect 1, 2, 3: "))
    else:
        userInput = int(input(f"Invalid fakturanumber detected. \nfakturanumber: {fakturaNumber}\nTicketID: {ticketID}\n\nChoose an option: \n1. Everything is fine, use this number\n2. Manually type Faktura number\n3. No Faktura number for ticket\nSelect 1, 2, 3: "))
    
    if not isinstance(userInput, int):
        print("Error in input. Try again.")
        handleInvalidFakturaNumber(fakturaNumber=fakturaNumber)

    if userInput == 1:
        # print(f"Returning {fakturaNumber}")
        return fakturaNumber
    elif userInput == 2:
        manualInput = input("Manually input faktura number: (numbers only): ")
        try:
            # print(f"returning {manualInput}")
            return int(manualInput)
        except TypeError:
            print("Error in input. Try again.")
            handleInvalidFakturaNumber(fakturaNumber=fakturaNumber)
    elif userInput == 3:
        # print("Returning 0")
        return 0
        
def findFakturaNumber(ticketComments):
    # TODO Cleanup this function
    regex_pattern = re.compile(r'\b(?:fakt(?:ura)?\.?|Ticket closed:)\s*(\d+)\b')
    
    
    forSureFakturaNummer = 0
    for ticket in ticketComments:
        fakturaString = []
        ticketBody = ticketComments[ticket]["body"]
        resultater = regex_pattern.findall(ticketBody)

        if len(resultater) >= 1:

                for x in resultater:
                    if len(str(x)) == 4:
                        forSureFakturaNummer = x
                    if len(str(x)) == 1 or len(str(x)) == 8:
                        fakturaString.append(handleInvalidFakturaNumber(fakturaNumber=x, ticketID=ticketComments[ticket]["ticket_id"]))
                        break
                        # allreadyFiledFakuraNumber = True
                    if int(x) and len(resultater) > 1:
                        fakturaString.append(handleInvalidFakturaNumber(fakturaNumber=resultater, ticketID=ticketComments[ticket]["ticket_id"]))
                        break
                    elif int(x) and len(resultater) == 1:
                        fakturaString.append(x)
                        break
                        
                # file.write(str(fakturaString)+"\n")
    # if not forSureFakturaNummer == 0 and fakturaString[0] == 0:
    #     print(f"Pretty sure we found Fakturanummer, please double check: \nTicketID: {ticketComments[ticket]["ticket_id"]}\nFakturanummer: {forSureFakturaNummer}\nPossible Fakturanummer: {str(fakturaString) if len(fakturaString) == 0 else "None"}")
    #     correctFakturaNummer = input("Is this correct? y/ or correct FakturaNummer: ")
    #     if correctFakturaNummer.lower()[0] == "y":
    #         fakturaString = forSureFakturaNummer
    #     elif isinstance(correctFakturaNummer, int): 
    #         fakturaString = correctFakturaNummer
    try: 
        if fakturaString[0] == 0:
            return None
    except IndexError:
        return None

    if len(fakturaString[0]) == 3:
        pass
    try:
        fakturaString = int(fakturaString[0])
    except Exception as e:
        raise Exception(f"Error!: {e}")
        

    return fakturaString