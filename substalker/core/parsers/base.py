"""
SubStalker: Find subdomains belonging to given target hosts
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
    <https://github.com/EONRaider/SubStalker/blob/master/LICENSE>.
"""

from abc import ABC, abstractmethod

from reconlib.core.base import ExternalService


class Parser(ABC):
    def __init__(self, parser):
        """
        Base class for all parsers responsible for processing
        configuration settings and/or options
        """
        self.parser = parser

    @property
    @abstractmethod
    def providers(self) -> set[ExternalService]:
        """
        Get a set of properly initialized instances of ExternalService
        """
        ...

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        Parse configuration settings and/or options
        """
        ...