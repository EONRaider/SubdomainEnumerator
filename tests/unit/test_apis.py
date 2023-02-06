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

import pytest
from reconlib.core.exceptions import APIKeyError
from reconlib.crtsh.api import CRTShAPI
from reconlib.hackertarget.api import HackerTargetAPI
from reconlib.virustotal.api import VirusTotalAPI

from subenum.core.apis import crtsh, hackertarget, virustotal


class TestAPIs:
    def test_crtsh(self):
        assert isinstance(crtsh(), CRTShAPI)

    def test_hackertarget(self):
        assert isinstance(hackertarget(), HackerTargetAPI)

    def test_virustotal_env_key(self, api_key, setup_virustotal_api_key):
        assert isinstance((api := virustotal()), VirusTotalAPI)
        assert api.api_key == api_key

    def test_virustotal_init_key(self, api_key):
        assert isinstance(
            (api := virustotal(virustotal_api_key=api_key)), VirusTotalAPI
        )
        assert api.api_key == api_key

    def test_virustotal_invalid_key(self):
        with pytest.raises(APIKeyError):
            virustotal()
