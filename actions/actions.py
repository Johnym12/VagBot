from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector

class GetProfInfo(Action):
    def name(self) -> Text:
        return "action_get_professor_info"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mydb = mysql.connector.connect(user='vagbot', 
                                       password='Vagbot123',
                                       host='localhost',
                                       database='vagbot')
        mycursor = mydb.cursor()
        professor = next(tracker.get_latest_entity_values('professor'), None)
        print(professor)
        profName=str(professor)
        profNameCut=profName[:-1]
        profNameSqlReady=profNameCut.replace("ι","_").replace("η","_").replace("υ","_")
        print(profNameSqlReady)        
        query = "SELECT prof,mail FROM courseinfo where UPPER(prof) LIKE UPPER('%"+profNameSqlReady+"%')"
        print(query)
        mycursor.execute(query)
        myresult = mycursor.fetchone()
        print(myresult)
        if(myresult is not None):
            strg = 'Ο/Η κ.' +str(myresult[0])+' δέχεται email στο: ' +str(myresult[1])
        else:
            strg = 'Δεν βρεθηκε ο προφεσορασ'
        
        dispatcher.utter_message(strg)
        mydb.close()        
        return []

class ResolveIssue(Action):
    
    def name(self) -> Text:
        return "action_resolve_issue"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        service_type = next(tracker.get_latest_entity_values('yphresia'), None)

        if str(service_type) == 'apps':
            strg = 'Για προβλήματα σχετικά με το Apps επικοινωνήστε με το noc@it.teithe.gr'
        elif str(service_type) == 'webmail':
            strg = 'Για προβλήματα σχετικά με το Webmail επικοινωνήστε με το noc@it.teithe.gr ή στο https://helpdesk.the.ihu.gr'
        elif str(service_type) == 'thesis':
            strg = 'Για προβλήματα σχετικά με το Thesis επικοινωνήστε με τον Κυριάκο Τσιακμάκη στο ktsiak@physics.auth.gr'
        elif str(service_type) == 'pithia':
            strg = 'Για προβλήματα σχετικά με το Πυθία επικοινωνήστε με την γραμματεία του τμήματος info@iee.ihu.gr'
        elif str(service_type) == 'eudoxos':
            strg = 'Για πληροφορίες σχετικά με τον Εύδοξο: γραμματεία τμήματος info@iee.ihu.gr, /n για τεχνικά θέματα: https://helpdesk.the.ihu.gr/, noc@the.ihu.gr'
        elif str(service_type) == 'moodle':
            strg = 'Για προβλήματα πρόσβασης στα περιεχόμενα ενος μαθήματος στο Moodle επικοινωνήστε με τον εκάστοτε υπεύθυνο καθηγητή'                  
        else:
            strg = 'Συγγνώμη δεν κατάλαβα με ποιά υπηρεσία υπάρχει πρόβλημα. Μπορείτε να αναδιατυπώσετε την ερώτησή σας ή να επικοινωνήσετε με την γραμματεία του τμήματος info@iee.ihu.gr'
        dispatcher.utter_message(strg)     
        return []


class InChargeofService(Action):
    
    def name(self) -> Text:
        return "action_in_charge_of_service"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        service_type = next(tracker.get_latest_entity_values('yphresia'), None)

        if str(service_type) == 'apps':
            strg = 'Το apps.iee.ihu.gr και οι συνδεδεμένες εφαρμογές του, διαχειρίζονται από το τμήμα (καθηγητές και φοιτητές σε εθελοντική βάση).'
        elif str(service_type) == 'webmail' or str(service_type) == 'moodle' or str(service_type) == 'pithia':
            strg = 'Το ' +service_type+' και οι συνδεδεμένες εφαρμογές τους διαχειρίζονται από το Κέντρο Δικτύου της πανεπιστημιούπολης Σίνδου (http://www.noc.teithe.gr/). '        
        else:
            strg = 'Συγγνώμη δεν κατάλαβα ποιά υπηρεσία εννοείτε. Μπορείτε να αναδιατυπώσετε την ερώτησή σας ή να επικοινωνήσετε με την γραμματεία του τμήματος info@iee.ihu.gr'
        dispatcher.utter_message(strg)     
        return []


class PasswordRecovery(Action):
    
    def name(self) -> Text:
        return "action_password_recovery"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        service_type = next(tracker.get_latest_entity_values('yphresia'), None)

        if str(service_type) == 'vpn' or str(service_type) == 'webmail' or str(service_type) == 'moodle' or str(service_type) == 'pithia':
            strg = 'Για ανάκτηση του '+service_type+' μπορείτε να επικοινωνήσετε με γραμματεία τμήματος info@iee.ihu.gr'
        elif str(service_type) == 'apps':
            strg = 'Για ανάκτηση του κωδικού του '+service_type+' μπορείτε να το κάνετε αυτόματα από την πλατφορμα https://apps.iee.ihu.gr/user/reset'        
        elif str(service_type) == 'academicid' or str(service_type) == 'eudoxos' or str(service_type) == 'eduroam':
            strg = 'Για ανάκτηση του κωδικού του '+service_type+' μπορείτε να το κάνετε αυτόματα από https://mypassword.the.ihu.gr/ ή να επικοινωνήσετε https://helpdesk.the.ihu.gr/, noc@the.ihu.gr'                                  
        else:
            strg = 'Συγγνώμη δεν κατάλαβα ποιά υπηρεσία εννοείτε. Μπορείτε να αναδιατυπώσετε την ερώτησή σας ή να επικοινωνήσετε με την γραμματεία του τμήματος info@iee.ihu.gr'
        dispatcher.utter_message(strg)     
        return []