# Good-Bull-API
A flexible GraphQL API that enables Texas A&M University students to retrieve as much data as they need regarding Texas A&M
University course data.

This API is built off of scraping multiple different sources of data from around the tamu.edu domain, converting the results into
SQL tables, and providing that data through GraphQL.

Pieces of information being tracked:
- Buildings
- Courses
- Grade distributions
- Instructors
- Sections

Things not being tracked (yet):
- Open seats in each section.

# Why?

**TL;DR: I'm tired of re-inventing the wheel to do the same thing. Course data should be open. [This](https://api.goodbullschedules.com/graphql) is my solution.**

Say you're interested in doing some analysis on a certain section of a course. Maybe you want to answer some questions like:
- Who's teaching it? 
- Overall, what percentage of students have made As, Bs, Cs, etc. when this instructor has taught the course?
- Where's it taking place?
- What's the course supposed to be about?

If you want to answer **any** of the above questions, or do any kind of analysis, you have to do one of two things:
1. Go in by hand and manually gather data by clicking through some horribly-designed website that takes upwards of 5 seconds to load some pages.
2. Write a webscraper that retrieves this information, from scratch. Deal with random server errors, poorly-structured HTML, inconsistencies, **hard-coded whitespace** (my favorite), and all of the other issues involved with webscraping.

You [wouldn't](https://github.com/jake-leland/CourseScraper) [be](https://github.com/xiaoyu-tamu/aggie-scraper) [the](https://github.com/SaltyQuetzals/GoodBullSchedules/tree/master/server/scraper) first person to build your scraper from scratch.

Everybody has to do the same thing, over and over, across different projects, in order to achieve the same goal. All because there's not a public API available.

I had to write my own scraper for my website [Good Bull Schedules](https://goodbullschedules.com) (shameless plug) that helped students plan their schedules out for upcoming semesters.  But even then, I *still* didn't have enough to provide the experience I wanted.

So a year later, here it is. An open-source API for providing students with course information.

All of my sources are available to the public, if you'd like to use them.
- [Buildings](http://fcor.tamu.edu/webreporter/indexv6.asp?t=[Current_Inv_Bldgs])
- [Sections and Instructors](https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched)
- [Courses](http://catalog.tamu.edu/undergraduate/)
- [Grade Distributions](http://web-as.tamu.edu/gradereport/)

# Contributing

Firstly, thank you for your interest in contributing! This has so far been a one-man show, and I'd love to get some help on things.  I need help more-thoroughly testing this application, so if you're looking to learn a little bit of TDD, ***please*** don't hesitate to send me a pull request with some unit tests you've made. Also, obviously, documentation is never good enough, so that's also up for grabs.

If you want to implement more features, I'm currently looking to do the following:
- [ ] Programmatically relate prerequisites and corequisites
- [ ] Monitor open seats
- [ ] [Scrape more detailed information about instructors](http://catalog.tamu.edu/undergraduate/faculty/)

If you've got a new feature that's not listed above, please open a feature request issue before you go on and build it. I may not want to include that functionality in the application.
