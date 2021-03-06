# -*- coding: utf-8 -*-

import json
import re

from module.network.RequestFactory import getURL
from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class OpenloadIo(SimpleHoster):
    __name__    = "OpenloadIo"
    __type__    = "hoster"
    __version__ = "0.10"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?openload\.(co|io)/(f|embed)/(?P<ID>[\w\-]+)'
    __config__  = [("activated", "bool", "Activated", True)]

    __description__ = """Openload.co hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [(None, None)]


    # The API reference, that this implementation uses is available at https://openload.co/api
    API_URL = 'https://api.openload.co/1'

    _DOWNLOAD_TICKET_URI_PATTERN = '/file/dlticket?file={0}'
    _DOWNLOAD_FILE_URI_PATTERN   = '/file/dl?file={0}&ticket={1}'
    _FILE_INFO_URI_PATTERN       = '/file/info?file={0}'

    OFFLINE_PATTERN = r'>We are sorry'


    @classmethod
    def _load_json(cls, uri):
        return json.loads(getURL(cls.API_URL + uri))


    @classmethod
    def api_info(cls, url):
        file_id   = cls.info['pattern']['ID']
        info_json = cls._load_json(cls._FILE_INFO_URI_PATTERN.format(file_id))
        file_info = info_json['result'][file_id]

        return {'name'  : file_info['name'],
                'size'  : file_info['size']}


    def setup(self):
        self.multiDL     = True
        self.chunk_limit = 1


    def handle_free(self, pyfile):
        # If the link is being handled here, then it matches the file_id_pattern,
        # therefore, we can call [0] safely.
        file_id     = self.info['pattern']['ID']
        ticket_json = self._load_json(self._DOWNLOAD_TICKET_URI_PATTERN.format(file_id))

        self.wait(ticket_json['result']['wait_time'])

        ticket = ticket_json['result']['ticket']

        download_json = self._load_json(self._DOWNLOAD_FILE_URI_PATTERN.format(file_id, ticket))
        self.link = download_json['result']['url']


getInfo = create_getInfo(OpenloadIo)
