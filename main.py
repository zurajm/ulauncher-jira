# -*- coding: utf-8 -*-
""" Created by Safa Arıman on 10.12.2018 """
""" Updated by David Hollinger on 08.21.2019 """
import gi
gi.require_version('Gdk', '3.0')
from jira.extension import JiraExtension

__author__ = 'dhollinger'


if __name__ == '__main__':
    JiraExtension().run()
