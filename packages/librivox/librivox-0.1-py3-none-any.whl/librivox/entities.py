# SPDX-FileCopyrightText: © 2024 Frederik “Freso” S. Olesen
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""""""

from typing import Optional

from .typing import (
    Seconds,
    Date,
    LibriVoxID,
    AuthorList,
    ReaderList,
    GenreList,
    SectionList,
)


class Person:
    """Abstract class for LibriVox authors and volunteers"""

    def __init__(self, lv_id: Optional[LibriVoxID] = None) -> None:
        self.id: Optional[LibriVoxID] = lv_id

    @property
    def name(self) -> str:
        """Name of the person"""
        return ""


class Author(Person):
    """Class representing a LibriVox author"""

    def __init__(
        self,
        author_id: Optional[LibriVoxID] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        date_of_death: Optional[str] = None,
    ) -> None:
        super().__init__(lv_id=author_id)
        self.first_name: Optional[str] = first_name
        self.last_name: Optional[str] = last_name
        self.date_of_birth: Optional[Date] = date_of_birth
        self.date_of_death: Optional[Date] = date_of_death

    @property
    def name(self) -> str:
        """Name of the author"""
        return " ".join([self.first_name or "", self.last_name or ""]).strip()


class Reader(Person):
    """Class representing a LibriVox volunteer"""

    def __init__(self, reader_id: Optional[LibriVoxID] = None):
        super().__init__(lv_id=reader_id)
        self.display_name: str = ""

    @property
    def name(self) -> str:
        """Name of the reader"""
        return self.display_name.strip()


class Genre:
    """Class representing a LibriVox genre"""

    def __init__(self, lv_genre_id: LibriVoxID, name: str) -> None:
        self.id: LibriVoxID = lv_genre_id
        self.name: str = name


class Section:
    """Class representing a section of a LibriVox book"""

    def __init__(self) -> None:
        self.id: Optional[LibriVoxID] = None
        self.section_number: Optional[int] = None
        self.title: Optional[str] = None
        self.listen_url: Optional[str] = None
        self.language: Optional[str] = None
        self.playtime: Optional[Seconds] = None
        self.file_name: Optional[str] = None
        self.readers: Optional[ReaderList] = None


class Book:
    """Class representing a LibriVox books (i.e., an audiobook)"""

    def __init__(self, lv_book_id: Optional[LibriVoxID] = None):
        self.id: Optional[LibriVoxID] = lv_book_id
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.url_text_source: Optional[str] = None
        self.language: Optional[str] = None
        self.copyright_year: Optional[Date] = None
        # self.num_sections: Optional[int] = None
        # self.url_rss: Optional[str] = None
        self.url_zip_file: Optional[str] = None
        self.url_project: Optional[str] = None
        self.url_librivox: Optional[str] = None
        self.url_iarchive: Optional[str] = None
        self.url_other: Optional[str] = None
        self.totaltime: Optional[str] = (
            None  # TODO: Replace with property method based on self.totaltimesecs
        )
        self.totaltimesecs: Optional[Seconds] = None
        self.authors: Optional[AuthorList] = None
        self.sections: Optional[SectionList] = None
        self.genres: Optional[GenreList] = None
        self.translators: Optional[list] = None

    @property
    def num_sections(self) -> Optional[int]:
        """Number of sections of the given book"""
        if self.sections is None:
            return None
        return len(self.sections)

    @property
    def url_rss(self) -> str:
        """URL to the RSS"""
        return "https://librivox.org/rss/{}".format(self.id)

    def populate(self) -> None:
        """Get data from LibriVox"""
        # All options:
        # - url_text_source,language,copyright_year,num_sections,url_rss,url_zip_file,url_project,url_librivox,url_iarchive,url_other,totaltime,totaltimesecs,authors,sections,genres,translators
        # https://librivox.org/api/feed/audiobooks?format=json&offset=50&extended=1&fields={id,title,description,url_text_source,language,copyright_year,url_zip_file,url_project,url_librivox,url_iarchive,url_other,totaltimesecs,authors,sections,genres,translators}
        pass
