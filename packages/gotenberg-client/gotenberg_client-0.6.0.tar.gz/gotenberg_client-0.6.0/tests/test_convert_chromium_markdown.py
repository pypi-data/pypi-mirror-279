# SPDX-FileCopyrightText: 2023-present Trenton H <rda0128ou@mozmail.com>
#
# SPDX-License-Identifier: MPL-2.0
from httpx import codes

from gotenberg_client import GotenbergClient
from tests.conftest import SAMPLE_DIR


class TestConvertChromiumUrlRoute:
    def test_basic_convert(self, client: GotenbergClient):
        index = SAMPLE_DIR / "markdown_index.html"
        md_files = [SAMPLE_DIR / "markdown1.md", SAMPLE_DIR / "markdown2.md"]
        img = SAMPLE_DIR / "img.gif"
        font = SAMPLE_DIR / "font.woff"
        style = SAMPLE_DIR / "style.css"
        with client.chromium.markdown_to_pdf() as route:
            resp = route.index(index).markdown_files(md_files).resources([img, font]).resource(style).run_with_retry()

        assert resp.status_code == codes.OK
        assert "Content-Type" in resp.headers
        assert resp.headers["Content-Type"] == "application/pdf"
