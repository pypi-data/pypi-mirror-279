# SPDX-FileCopyrightText: © 2024 Frederik “Freso” S. Olesen
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""""""

# https://librivox.org/api/info

import json

from typing import Optional
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen
from urllib.response import addinfourl

from .typing import LibriVoxID, AuthorList, SectionList, BookList


class LibriVox:
    """"""

    def __init__(self, api_base_url: str = "https://librivox.org/api/feed/") -> None:
        self.api_base_url = api_base_url
        self.known_endpoints = frozenset({"audiobooks", "audiotracks", "authors"})

    def _request(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        experimental: bool = False,
    ) -> addinfourl:
        """Send a HTTP API request."""
        if params is None:
            # Ensure that dict methods will work for parameters
            params = dict()
        if not experimental:
            # The default mode of operation!
            if endpoint not in self.known_endpoints:
                # TODO: Raise exception for using unknown endpoint
                pass
            if "format" not in params:
                # Always set “format”
                params["format"] = "json"
            if "format" in params and params["format"] != "json":
                # TODO: Raise exception for using non-JSON format
                pass
        request_url = f"{urljoin(self.api_base_url, endpoint)}?{urlencode(params)}"
        response = urlopen(request_url)
        return response

    def audiobooks(
        self,
        audiobook_id: Optional[LibriVoxID] = None,
        since: Optional[int] = None,
        author_last_name: Optional[str] = None,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        extended: Optional[bool] = None, # Upstream default: False
        limit: Optional[int] = None,  # Upstream default: 50
        offset: Optional[int] = None,  # Upstream default: 0
    ) -> BookList:
        """Get a list of audiobooks."""
        search_variables = [since, author_last_name, title, genre]
        if not audiobook_id and search_variables.count(None) == 0:
            # TODO: Raise error: no parameters provided
            pass
        elif audiobook_id and search_variables.count(None) > 0:
            # TODO: Raise error: only one of id or search query can be given
            pass
        query = dict()
        if audiobook_id is not None:
            query["id"] = audiobook_id
        if since is not None:
            query["since"] = since
        if author_last_name is not None:
            query["author_last_name"] = author_last_name
        if title is not None:
            query["title"] = title
        if genre is not None:
            query["genre"] = genre
        if extended is not None:
            query["extended"] = extended
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        response = self._request("audiobooks", params=query)
        return json.load(response)["books"]

    def audiotracks(
        self,
        audiotrack_id: Optional[LibriVoxID] = None,
        project_id: Optional[LibriVoxID] = None,
    ) -> SectionList:
        """Get a list of audio tracks (sections)."""
        if audiotrack_id is None and project_id is None:
            # TODO: Raise error: no parameters provided
            pass
        elif audiotrack_id is not None and project_id is not None:
            # TODO: Raise error: only one of audio track id or project id can be given
            pass
        query = dict()
        if audiotrack_id is not None:
            query["id"] = audiotrack_id
        if project_id is not None:
            query["project_id"] = project_id
        results = self._request("audiotracks", params=query)
        data = json.load(results)["sections"]
        if type(data) is not list:
            data = [data]
        return data

    def authors(
        self,
        author_id: Optional[LibriVoxID] = None,
        last_name: Optional[str] = None,
    ) -> AuthorList:
        """Get a list of authors."""
        if author_id is None and last_name is None:
            # TODO: Raise error: no parameters provided
            pass
        elif author_id is not None and last_name is not None:
            # TODO: Raise error: only one of id or search query can be given
            pass
        query = dict()
        if author_id is not None:
            query["id"] = author_id
        if last_name is not None:
            query["last_name"] = last_name
        results = self._request("authors", params=query)
        return json.load(results)["authors"]
