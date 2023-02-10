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

from subenum.core.processors.file import FileOutput
from subenum.core.processors.screen import ScreenOutput
from subenum.core.providers import all_providers
from subenum.enumerator import Enumerator


class TestApp:
    def test_run_enumerator(
        self,
        capsys,
        tmp_path,
        mocker,
        target_domain_1,
        api_response_1,
        setup_virustotal_api_key,
    ):
        mocker.patch(
            "subenum.enumerator.Enumerator.query_provider", return_value=api_response_1
        )
        output_file = tmp_path / "test_file.txt"

        enumerator = Enumerator(
            targets=(target_domain_1,),
            providers=[provider() for provider in all_providers],
            max_threads=10,
        )
        screen = ScreenOutput(subject=enumerator)
        FileOutput(subject=enumerator, path=output_file)

        with enumerator:
            for _ in enumerator.execute():
                pass

        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Subdomain enumerator started with 10 threads for "
            f"{target_domain_1}\n\n"
            "[InstanceOfExternalService1] sub1.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub2.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub3.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub4.some-target-domain.com\n"
            "[InstanceOfExternalService1] sub5.some-target-domain.com\n"
            f"\n[+] Enumeration of 1 domain was completed in 0.00 seconds "
            f"and found {len(screen._known_domains)} subdomains\n"
            f"[+] Enumeration results successfully written to {output_file}\n"
        )
