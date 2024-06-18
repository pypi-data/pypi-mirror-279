from typing import List

from jira.api_client.jira_api import JiraApi
from jira.model.feature import Feature
from jira.model.story import Story


class JiraProducer:
    def __init__(self, username=None, token=None, proxy=False):
        self._jira_api = JiraApi(username=username, token=token, proxy=proxy)

    def get_feature_by_pi(self, pi_key) -> List[Feature]:
        json_jira = self._jira_api.get_feature_by_pi(pi_id=pi_key)
        arr_feature = []
        for feature in json_jira:
            current_feature = Feature()
            current_feature.convert_json_to_feature(feature)
            arr_feature.append(current_feature)
        return arr_feature

    def get_feature_by_key(self, feature_key) -> Feature:
        json_jira = self._jira_api.get_feature_by_key(feature_id=feature_key)
        current_feature = Feature()
        if len(json_jira) > 0:
            current_feature.convert_json_to_feature(json_jira[0])
        return current_feature

    def get_story_by_feature(self, feature_key) -> List[Story]:
        json_jira = self._jira_api.get_story_by_feature(feature_id=feature_key)
        arr_story = []
        for story in json_jira:
            current_story = Story()
            current_story.convert_json_story(story)
            arr_story.append(current_story)
        return arr_story

    def get_story_by_key(self, story_key) -> Story:
        json_jira = self._jira_api.get_story_by_key(story_id=story_key)
        current_story = Story()
        if len(json_jira) > 0:
            current_story.convert_json_story(json_jira[0])

        return current_story
