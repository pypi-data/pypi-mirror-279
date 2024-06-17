# SPDX-FileCopyrightText: © 2024 Frederik “Freso” S. Olesen
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Collection of typing utilities for LibriVox for Python"""

from typing import Annotated, Union, Sequence, TypeAlias, NewType

# General purpose value type aliases
Seconds: TypeAlias = Annotated[int, "seconds"]
Date: TypeAlias = Annotated[
    Union[str, int],
    "date, typically given as a 4-digit year but can sometimes be a string",
]

# LibriVox specific type aliases
LibriVoxID = NewType(
    "LibriVoxID", Annotated[int, "LibriVox numeric identifier (positive integer)"]
)

# List value type aliases
AuthorList: TypeAlias = Annotated[Sequence["Author"], "list of LibriVox authors"]
ReaderList: TypeAlias = Annotated[Sequence["Reader"], "list of LibriVox readers"]
GenreList: TypeAlias = Annotated[Sequence["Genre"], "list of LibriVox genres"]
SectionList: TypeAlias = Annotated[Sequence["Section"], "list of LibriVox book sections"]
BookList: TypeAlias = Annotated[Sequence["Book"], "list of LibriVox (audio)books"]
