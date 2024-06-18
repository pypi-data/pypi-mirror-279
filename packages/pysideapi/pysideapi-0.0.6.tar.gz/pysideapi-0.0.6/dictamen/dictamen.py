import datetime
from datetime import datetime
from datetime import date
from time import gmtime, strftime
import pytz
tz = pytz.timezone('America/Lima')



class Dictamen:
    def __init__(self, url_pgyc: str):
        self.url_pgyc = url_pgyc

    def validate_dictamen(self, incident_jira: str):
        arr_rule_hut = []

        rule_1_1 = (self, '', '', '')
        arr_rule_hut.append(rule_1_1)

        return arr_rule_hut

    def validate_bui(self, url_bui: str, sheet_name: str) ->[]:
        arr_rule_bui = []

        rule_1_1 = (self, '', '', '')
        arr_rule_bui.append(rule_1_1)

        return arr_rule_bui

    def validate_buc(self, url_buc: str, sheet_name: str) ->[]:
        arr_rule_buc = []

        rule_1_1 = (self, '', '', '')
        arr_rule_buc.append(rule_1_1)

        return arr_rule_buc

    def validate_dictamen(self, incident_jira: str) -> []:
        arr_rule = []

        rule_1_1 = (self, '', '', '')
        arr_rule.append(rule_1_1)

        return []

    def get_date_servicedesk_by_key(arr, criteria, lastdate=''):
        date1 = []
        for element in arr:
            subject_change = element.get("items")[0].get("toString")
            if criteria in subject_change:
                finish = datetime.strptime(element.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
                finish = finish.astimezone(tz)
                finish = finish.strftime("%Y-%m-%d %H:%M:%S")
                if lastdate != '':
                    if finish > lastdate:
                        date1.append(finish)
                else:
                    date1.append(finish)
        return date1.pop(0)
