import pytz
from datetime import datetime, timedelta
from jira.commons.constants import Constants
from jira.model.issue_base import IssueBase

tz = pytz.timezone('America/Lima')


class Story(IssueBase):
    def __init__(self):
        super().__init__()
        self.feature_key = ''
        self.pi_result = ''
        self.comments = []
        self.jira_tasks = []
        self.label_folio_id = ''
        self.label_source_id = ''
        self.label_process_id = ''
        self.desc_folio_id = ''
        self.desc_source_id = ''
        self.desc_tds_id = ''
        self.desc_bui_local_id = ''
        self.desc_pgyc_id = ''
        self.created_team_backlog_id = ''
        self.created_team_backlog_name = ''
        self.current_team_backlog_id = ''
        self.current_team_backlog_name = ''

    def __add_attr_dictamen(self):
        data_text = self.description
        # Extraemos el Folio, Id Fuente y TDS
        start_index = data_text.find(Constants.CRITERIA_TO_FIND_TABLE) + len(Constants.CRITERIA_TO_FIND_TABLE)
        data_dictamen = data_text[start_index:len(data_text) - 1]
        arr_row = data_dictamen.split(Constants.CRITERIA_TO_FIND_TABLE)
        if len(arr_row) >= 1:
            row_first = arr_row[0]
            arr_cell = row_first.split(Constants.PIPE_ID)

            if len(arr_cell) >= 3:
                self.desc_folio_id = arr_cell[0]
                self.desc_source_id = arr_cell[1]
                self.desc_tds_id = arr_cell[2]
        # Extraemos la BUI Local y el PGyC
        bui_start_index = data_text.find(Constants.CRITERIA_TO_FIND_GS) + len(Constants.CRITERIA_TO_FIND_GS)
        data_bui = data_text[bui_start_index: len(data_text) - 1]
        bui_end_index = data_bui.find(Constants.SLASH_ID)
        self.desc_bui_local_id = data_bui[0:bui_end_index]
        # Extraemos el PGyC
        pgyc_start_index = data_bui.find(Constants.CRITERIA_TO_FIND_GS) + len(Constants.CRITERIA_TO_FIND_GS)
        data_pgyc = data_bui[pgyc_start_index:len(data_bui) - 1]
        pgyc_end_index = data_pgyc.find(Constants.SLASH_ID)
        self.desc_pgyc_id = data_pgyc[0:pgyc_end_index]
    def __add_team_backlog(self, json_histories):

        # minor_team_backlog_date = datetime.max.astimezone(tz)
        today = datetime.today().astimezone(tz)
        minor_team_backlog_date = today + timedelta(days=1)
        self.current_team_backlog_name=''
        for story in json_histories:
            items = story.get('items')
            for item in items:
                if item.get('field') == 'Team Backlog':
                    finish = datetime.strptime(story.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
                    finish = finish.astimezone(tz)
                    # finish = finish.strftime("%Y-%m-%d %H:%M:%S")
                    if finish < minor_team_backlog_date:
                        self.created_team_backlog_id = item.get('from')
                        from_string = item.get('fromString')
                        start_index = from_string.find(Constants.CRITERIA_TO_FIND_START_TEAM_BACKLOG)
                        end_index = from_string.find(Constants.CRITERIA_TO_FIND_END_TEAM_BACKLOG)
                        self.created_team_backlog_name = from_string[start_index:end_index]
                        minor_team_backlog_date = finish
                    if self.current_team_backlog_id == item.get('to') and self.current_team_backlog_name == '':
                        to_string = item.get('toString')
                        start_index = to_string.find(Constants.CRITERIA_TO_FIND_START_TEAM_BACKLOG)
                        end_index = to_string.find(Constants.CRITERIA_TO_FIND_END_TEAM_BACKLOG)
                        self.current_team_backlog_name = to_string[start_index:end_index]

    def convert_json_story(self, json_jira):
        self.id = json_jira["id"]
        self.key = json_jira["key"]
        fields = json_jira["fields"]
        changelog = json_jira["changelog"]
        histories = changelog.get('histories')
        self.title = fields.get("summary")
        self.description = fields.get("description")
        self.status_id = fields.get("status").get("id")
        self.status_name = fields.get("status").get("name")
        self.feature_key = fields.get("customfield_10004")
        self.issue_type_id = fields.get('issuetype').get('id')
        self.issue_type_name = fields.get('issuetype').get('name')
        self.labels = fields["labels"]
        for label in self.labels:
            if label[0:2] == 'F-':
                self.label_folio_id = label[2:len(label)]
            if label[0:3] == 'ID-':
                self.label_source_id = label[3:len(label)]
            if label[0:2] == 'P-':
                self.label_process_id = label[2:len(label)]

        self.assignee_name = fields.get("assignee").get("name")
        self.assignee_email = fields.get("assignee").get("emailAddress")
        self.creator_name = fields.get("creator").get("name")
        self.creator_email = fields.get("creator").get("emailAddress")
        self.current_team_backlog_id = fields.get('customfield_13300').pop(0)
        self._convert_histories_to_status(histories)
        self.__add_team_backlog(histories)
        self.__add_attr_dictamen()
