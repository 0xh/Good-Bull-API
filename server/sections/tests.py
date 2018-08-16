from bs4 import BeautifulSoup
from django import test

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
        expected = ('SURVEY OF ACCT PRIN', 10001, '209', '501')
        actual = section_scraper.parse_ddtitle(soup)
        self.assertTupleEqual(expected, actual)

    def test_parse_dddefault(self):
        """Extracts credits and meetings from dddefault."""
        html = """
                <td class="dddefault">
                WEB AUGMENTED COURSE. NON-BUSINESS, NON-AGRIBUSINESS MAJORS ONLY.
                <br>
                <span class="fieldlabeltext">Associated Term: </span>Fall 2018 - College Station 
                <br>
                <span class="fieldlabeltext">Registration Dates: </span>Mar 26, 2018 to Aug 31, 2018 
                <br>
                <span class="fieldlabeltext">Levels: </span>Graduate, Undergraduate 
                <br>
                <span class="fieldlabeltext">Attributes: </span>NonTraditional Format Approved 
                <br>
                <br>
                College Station Campus
                <br>
                Lecture Schedule Type
                <br>
                Traditional, Face-to-Face Instructional Method
                <br>
                3.000 Credits
                <br>
                <a href="/pls/PROD/bwckctlg.p_display_courses?term_in=201831&amp;one_subj=ACCT&amp;sel_crse_strt=209&amp;sel_crse_end=209&amp;sel_subj=&amp;sel_levl=&amp;sel_schd=&amp;sel_coll=&amp;sel_divs=&amp;sel_dept=&amp;sel_attr=">View Catalog Entry</a>
                <br>
                <br>
                <table class="datadisplaytable" summary="This table lists the scheduled meeting times and assigned instructors for this class..">
                    <caption class="captiontext">Scheduled Meeting Times</caption>
                    <tbody>
                        <tr>
                            <th class="ddheader" scope="col">Type</th>
                            <th class="ddheader" scope="col">Time</th>
                            <th class="ddheader" scope="col">Days</th>
                            <th class="ddheader" scope="col">Where</th>
                            <th class="ddheader" scope="col">Date Range</th>
                            <th class="ddheader" scope="col">Schedule Type</th>
                            <th class="ddheader" scope="col">Instructors</th>
                        </tr>
                        <tr>
                            <td class="dddefault">Lecture</td>
                            <td class="dddefault">8:00 am - 9:15 am</td>
                            <td class="dddefault">T</td>
                            <td class="dddefault">Wehner - College of Business 113</td>
                            <td class="dddefault">Aug 27, 2018 - Dec 12, 2018</td>
                            <td class="dddefault">Lecture</td>
                            <td class="dddefault">Mary Knetsar  Stasny (<abbr title="Primary">P</abbr>)</td>
                        </tr>
                        <tr>
                            <td class="dddefault">Examination</td>
                            <td class="dddefault">7:15 pm - 9:15 pm</td>
                            <td class="dddefault">R</td>
                            <td class="dddefault"><abbr title="To Be Announced">TBA</abbr></td>
                            <td class="dddefault">Sep 27, 2018 - Sep 27, 2018</td>
                            <td class="dddefault">Lecture</td>
                            <td class="dddefault">Mary Knetsar  Stasny (<abbr title="Primary">P</abbr>)</td>
                        </tr>
                        <tr>
                            <td class="dddefault">Examination</td>
                            <td class="dddefault">7:15 pm - 9:15 pm</td>
                            <td class="dddefault">R</td>
                            <td class="dddefault"><abbr title="To Be Announced">TBA</abbr></td>
                            <td class="dddefault">Oct 25, 2018 - Oct 25, 2018</td>
                            <td class="dddefault">Lecture</td>
                            <td class="dddefault">Mary Knetsar  Stasny (<abbr title="Primary">P</abbr>)</td>
                        </tr>
                        <tr>
                            <td class="dddefault">Examination</td>
                            <td class="dddefault">7:15 pm - 9:15 pm</td>
                            <td class="dddefault">R</td>
                            <td class="dddefault"><abbr title="To Be Announced">TBA</abbr></td>
                            <td class="dddefault">Nov 29, 2018 - Nov 29, 2018</td>
                            <td class="dddefault">Lecture</td>
                            <td class="dddefault">Mary Knetsar  Stasny (<abbr title="Primary">P</abbr>)</td>
                        </tr>
                    </tbody>
                </table>
                <br>
                <br>
                </td>
            """
        soup = BeautifulSoup(html, 'lxml')
        expected = (3.000, 3.000)
        actual = section_scraper.parse_dddefault(soup)
