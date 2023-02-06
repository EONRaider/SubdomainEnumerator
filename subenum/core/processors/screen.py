"""
SubdomainEnumerator: Find subdomains belonging to given target hosts
using active and passive enumeration methods

Author: EONRaider
GitHub: https://github.com/EONRaider
Contact: https://www.twitter.com/eon_raider
    Copyright (C) 2023 EONRaider @ keybase.io/eonraider
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see
    <https://github.com/EONRaider/SubdomainEnumerator/blob/master/LICENSE>.
"""

from subenum.core.types import EnumerationSubscriber, EnumerationPublisher, EnumResult


class ScreenOutput(EnumerationSubscriber):
    def __init__(self, subject: EnumerationPublisher):
        super().__init__(subject)
        self._known_domains = set()

    def update(self, result: EnumResult) -> None:
        self._known_domains |= result.subdomains
        new_domains = self._known_domains - result.subdomains
        print(*(domain for domain in new_domains), sep="\n")

    def end_output(self) -> None:
        pass