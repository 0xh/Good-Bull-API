import unittest

import requests

from _functions.functions import split_into_reqs_and_desc


class TestParseSplitReqsDesc(unittest.TestCase):

    def test_no_reqs(self):
        EXAMPLE_TEXT = 'Computation to enhance problem solving abilities; understanding how people communicate with computers, and how computing affects society; computational thinking; software design principles, including algorithm design, data representation, abstraction, modularity, structured and object oriented programming, documentation, testing, portability, and maintenance; understanding programs’ abilities and limitations; development and execution programs.'
        EXPECTED = (EXAMPLE_TEXT, None, None)
        self.assertEqual(split_into_reqs_and_desc(EXAMPLE_TEXT), EXPECTED)

    def test_prereqs_only(self):
        EXAMPLE_TEXT = 'Computation to enhance problem solving abilities computational thinking understanding how people communicate with computers, how computing affects society design and implementation of algorithms data types, program control, iteration, functions, classes, and exceptions understanding abstraction, modularity, code reuse, debugging, maintenance, and other aspects of software development; development and execution of programs. Prerequisite: Programming course(high school or college).'
        DESCRIPTION = 'Computation to enhance problem solving abilities computational thinking understanding how people communicate with computers, how computing affects society design and implementation of algorithms data types, program control, iteration, functions, classes, and exceptions understanding abstraction, modularity, code reuse, debugging, maintenance, and other aspects of software development; development and execution of programs.'
        PREREQS = 'Programming course(high school or college).'
        EXPECTED = (DESCRIPTION, PREREQS, None)
        self.assertEqual(split_into_reqs_and_desc(EXAMPLE_TEXT), EXPECTED)

    def test_prereqs_cross_listed(self):
        EXAMPLE_TEXT = 'Provide mathematical foundations from discrete mathematics for analyzing computer algorithms, for both correctness and performance introduction to models of computation, including finite state machines and Turing machines. Prerequisite: MATH 151. Cross Listing: ECEN 222/CSCE 222.'
        DESCRIPTION = 'Provide mathematical foundations from discrete mathematics for analyzing computer algorithms, for both correctness and performance introduction to models of computation, including finite state machines and Turing machines.'
        PREREQS = 'MATH 151.'
        EXPECTED = (DESCRIPTION, PREREQS, None)
        self.assertEqual(split_into_reqs_and_desc(EXAMPLE_TEXT), EXPECTED)

    def test_prereqs_coreqs(self):
        EXAMPLE_TEXT = 'Intensive programming experience that integrates core concepts in Computer Science and familiarizes with a variety of programming/development tools and techniques students work on 2 or 3 month-long projects each emphasizing a different specialization within Computer Science focuses on programming techniques to ease code integration, reusability, and clarity. Prerequisites: CSCE 312 and CSCE 314 or CSCE 350/ECEN 350. Corequisite: CSCE 313.'
        DESCRIPTION = 'Intensive programming experience that integrates core concepts in Computer Science and familiarizes with a variety of programming/development tools and techniques students work on 2 or 3 month-long projects each emphasizing a different specialization within Computer Science focuses on programming techniques to ease code integration, reusability, and clarity.'
        PREREQS = 'CSCE 312 and CSCE 314 or CSCE 350/ECEN 350.'
        COREQS = 'CSCE 313.'
        EXPECTED = (DESCRIPTION, PREREQS, COREQS)
        self.assertEqual(split_into_reqs_and_desc(EXAMPLE_TEXT), EXPECTED)


if __name__ == '__main__':
    unittest.main()
