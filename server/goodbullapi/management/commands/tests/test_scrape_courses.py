from django import test
from bs4 import BeautifulSoup
from goodbullapi.management.commands import scrape_courses as course_scraper


class ScrapeCoursesTestCase(test.TestCase):

    def test_collect_departments(self):
        """Selects elems matching CSS selector."""

        html = """
                <!DOCTYPE html>
                <html>
                    <body>
                        <div id="atozindex">
                            <ul>
                                <li>
                                    <a href="first">DEPT - Longer department name (DEPT)</a>
                                </li>
                                <li>
                                    <a href="second">EXAM - Example department name (EXAM)</a>
                                </li>
                            </ul>
                        </div>
                    </body>
                </html>
                """
        soup = BeautifulSoup(html, 'lxml')
        expected = [("first", "DEPT"), ("second", "EXAM")]
        actual = course_scraper.collect_departments(soup)
        self.assertEqual(expected, actual)

    def test_parse_courseblocktitle(self):
        """Extracts course number and course name from .courseblocktitle elem."""
        html = """
                <p class="courseblocktitle noindent">
                    <strong>AALO&nbsp;285 Directed Studies</strong>
                </p>
               """
        soup = BeautifulSoup(html, 'lxml')
        expected = ("285", "Directed Studies")
        actual = course_scraper.parse_courseblocktitle(soup)
        self.assertEqual(expected, actual)

    def test_parse_courseblock(self):
        """Extracts important information from courseblock."""

        html = """
                    <div class="courseblock">
                        <p class="courseblocktitle noindent">
                            <strong>AALO&nbsp;285 Directed Studies</strong>
                        </p>
                        <p class="hours noindent">
                            <strong>Credits 1 to 4. 1 to 4 Other Hours.</strong>
                        </p>
                        <p class="courseblockdesc">
                            Individual supervision of readings or assigned projects in an Asian Language, selected for each student individually; written or oral reports. <br><strong>Prerequisite:</strong> Approval of Arabic and Asian Language Office Director.<br>
                        </p>
                    </div>
                """
        soup = BeautifulSoup(html, 'lxml')
        expected = ("285",                  # Course number
                    "Directed Studies",     # Course name
                    1,                      # Min credits
                    4,                      # Max credits
                    "1 to 4 Other Hours",   # Hours Distribution
                    "Individual supervision of readings or assigned projects in an Asian Language, selected for each student individually; written or oral reports.",   # Description
                    "Approval of Arabic and Asian Language Office Director."    # Prereqs
                    )
        actual = course_scraper.parse_courseblock(soup)
