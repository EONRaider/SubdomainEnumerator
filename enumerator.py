#!/usr/bin/python3

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

from subenum.core.parsers.cli import CLIParser
from subenum.core.parsers.configuration import ConfigurationParser
from subenum.core.processors.file import FileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.enumerator import Enumerator


class App:
    def __init__(self):
        self.cli_args = (cli_parser := CLIParser()).parse()
        (config_parser := ConfigurationParser()).parse(
            file_path=self.cli_args.config_file
        )
        self.enumerator = Enumerator(
            targets=self.cli_args.targets,
            enumerators=cli_parser.enumerators | config_parser.enumerators,
            output_file=self.cli_args.output,
            max_threads=self.cli_args.max_threads,
        )

    def run(self) -> None:
        ScreenOutput(self.enumerator)
        if self.cli_args.output is not None:
            FileOutput(self.enumerator)
        try:
            with self.enumerator:
                self.enumerator.execute()
        except KeyboardInterrupt:
            raise SystemExit("[!] Subdomain enumeration aborted by user. Exiting...")


if __name__ == "__main__":
    App().run()