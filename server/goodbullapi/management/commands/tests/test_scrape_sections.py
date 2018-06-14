from django import test
from bs4 import BeautifulSoup
from goodbullapi.management.commands import scrape_sections as section_scraper


class ScrapeSectionsTestCase(test.TestCase):

    def test_request_term_codes(self):
        """Ensures that the term codes retrieved are correct."""
        expected = ''
        actual = section_scraper.request_term_codes()[0]
        self.assertEqual(expected, actual)

    def test_request_depts(self):
        """Ensures that the departments are being retrieved as intended."""
        expected = 'ACCT'
        actual = section_scraper.request_depts('201831')[0]
        self.assertEqual(expected, actual)

    def test_parse_ddtitle(self):
        """Ensures that relevant information is being extracted from a title."""
        html = """
                <th class="ddtitle" scope="colgroup">
                    <a href="/pls/PROD/bwckschd.p_disp_detail_sched?term_in=201831&amp;crn_in=10001">
                        SURVEY OF ACCT PRIN - 10001 - ACCT 209 - 501
                    </a>
                </th>
                """
        soup = BeautifulSoup(html, 'lxml')
        expected = ('SURVEY OF ACCT PRIN', 10001, '501')
        actual = section_scraper.parse_ddtitle(soup)
        self.assertTupleEqual(expected, actual)
