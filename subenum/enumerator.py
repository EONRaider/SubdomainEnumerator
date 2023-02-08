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

import time
from collections import defaultdict
from collections.abc import Collection, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from pathlib import Path

from reconlib.core.base import ExternalService

from subenum.core.types import EnumResult, EnumerationPublisher, EnumerationSubscriber


class Enumerator(EnumerationPublisher):
    def __init__(
        self,
        targets: Collection[str],
        *,
        providers: Collection[ExternalService],
        max_threads: int,
        output_file: [str, Path] = None,
    ):
        """
        Enumerate subdomains of given targets by using available data
        providers

        :param targets: A collection of strings defining target domains
        :param providers: A collection of instances of ExternalServices
            to be queried during the enumeration of subdomains of
            selected targets
        :param max_threads: Maximum number of threads to use when
            enumerating subdomains. A new thread will be spawned for
            each combination of data provider and target domain
        :param output_file: Absolute path to a file to which enumeration
            results will be written
        """
        super().__init__()
        self.targets: Collection[str] = targets
        self.providers: Collection[ExternalService] = providers
        self.output_file: [str, Path] = output_file
        self.max_threads: int = max_threads
        self.found_domains = defaultdict(set)

    def __enter__(self) -> None:
        self.start_time = time.perf_counter()
        [observer.startup(subject=self) for observer in self._observers]

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.total_time = time.perf_counter() - self.start_time
        [observer.cleanup(subject=self) for observer in self._observers]

    def register(self, observer: EnumerationSubscriber) -> None:
        """
        Attach an observer to the enumerator for further processing
        and/or output of results.

        :param observer: An object implementing the interface of
            EnumerationSubscriber
        """
        self._observers.append(observer)

    def unregister(self, observer: EnumerationSubscriber) -> None:
        """
        Remove an observer previously attached to the enumerator.

        :param observer: An object implementing the interface of
            EnumerationSubscriber
        """
        with suppress(ValueError):
            # Supress exceptions raised by an attempt to unregister a
            # non-existent observer
            self._observers.remove(observer)

    def _notify_all(self, result: EnumResult) -> None:
        """
        Notify all registered observers of an enumeration result for
        further processing and/or output.

        :param result: An instance of type EnumResult
        """
        [observer.update(result) for observer in self._observers]

    @staticmethod
    def query_provider(provider: ExternalService, target: str) -> EnumResult:
        """
        Query a data provider about known subdomains of a given target domain

        :param provider: An instance of type ExternalService to query
        :param target: A string defining a target domain
        :return: An instance of type EnumResult containing enumeration
            results as its attributes
        """
        return EnumResult(
            provider=provider.__class__.__name__,
            domain=target,
            subdomains=provider.fetch_subdomains(target),
        )

    def execute(self) -> None:
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Generate tuples containing combinations of available
            # providers and targets to pass as tasks to spawned threads
            tasks: Iterator[tuple[ExternalService, str]] = (
                (provider, target)
                for target in self.targets
                for provider in self.providers
            )
            # Spawn a new thread for each combination of provider and target
            for result in executor.map(lambda task: self.query_provider(*task), tasks):
                # Add results to known subdomains of a given target and
                # notify all observers, if any, of new results
                self.found_domains[result.domain] |= result.subdomains
                self._notify_all(result)
