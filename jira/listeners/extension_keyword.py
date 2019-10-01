# -*- coding: utf-8 -*-
""" Created by Safa Arıman on 12.12.2018 """
""" Updated by David Hollinger on 08.21.2019 """
import base64
import json
import urllib
import ssl
import urllib.request as request
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

__author__ = 'dhollinger'


class ExtensionKeywordListener(EventListener):

    def __init__(self, icon_file):
        self.icon_file = icon_file

    def on_event(self, event, extension):
        query = event.get_argument()
        results = []

        workspace_url = extension.preferences.get('url')
        user = extension.preferences.get('username')
        password = extension.preferences.get('password')

        token = base64.b64encode(str('%s:%s' % (user, password)).encode()).decode()
        url = urllib.parse.urljoin(workspace_url, 'rest/api/2/issue/picker')
        get_url = "%s?%s" % (url, urllib.parse.urlencode({'query': query}))
        req = request.Request(get_url, headers={'Authorization': 'Basic %s' % token}, method="GET")

        result_types = {}

        try:
            response = urllib.request.urlopen(req, context=ssl._create_unverified_context())
            result_types = json.loads(response.read())
        except urllib.error.HTTPError as e:
            if e.code == 401:
                results.append(
                    ExtensionResultItem(
                        name='Authentication failed.',
                        description='Please check your username/e-mail and password.',
                        icon=self.icon_file,
                        on_enter=DoNothingAction()
                    )
                )
            return RenderResultListAction(results)
        except Exception as e:
            results.append(
                ExtensionResultItem(
                    name='Could not connect to Jira.',
                    description='{}'.format(e),
                    icon=self.icon_file,
                    on_enter=DoNothingAction()
                )
            )
            return RenderResultListAction(results)


        for section in result_types.get("sections", []):
            for issue in section.get("issues", []):
                key = issue.get('key')
                title = issue.get('summaryText')
                url = urllib.parse.urljoin(workspace_url, "browse/" + key)
                results.append(
                    ExtensionResultItem(
                        name=title if not key else '%s - %s' % (key, title),
                        description=key,
                        icon=self.icon_file, on_enter=OpenUrlAction(url=url)
                    )
                )

        if not results:
            results.append(
                ExtensionResultItem(
                    name="Search '%s'" % query,
                    description='No results. Try searching something else :)',
                    icon=self.icon_file,
                    on_enter=DoNothingAction()
                )
            )

        return RenderResultListAction(results)
