# Howdy!
Good Bull API is an open-data API written in [TypeScript](https://www.typescriptlang.org/) for Texas A&M University student developers looking to use course data from [Howdy](https://howdy.tamu.edu/uPortal/normal/render.uP).

# Objective
Provide an open, public, read-only API for students to retrieve rich data for Texas A&M University.

Currently, the following data is scraped and served:
- [X] Courses from [catalog.tamu.edu](http://catalog.tamu.edu/undergraduate/course-descriptions/)
- [X] Sections from [Compass](https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched)
- [X] Building data from [fcor.tamu.edu](http://fcor.tamu.edu/webreporter/indexv6.asp?t=[Current_Inv_Bldgs]).

Future data to scrape includes:
- [ ] Grade data from [the registrar](http://web-as.tamu.edu/gradereport/).

# Background
This section has very little pertinence to the tech stack or project implementation, but describes my motivations for this project.

## Why Build This?
Texas A&M provides no way of programmatically retrieving historical (or present) course data to students. Students who _want_ to use that data are required to write a webscraper that is, in itself, a Herculean task, depending on how much information you want to retrieve.

Examples of completed scrapers that I've seen over the years:
- [Jake Leland](http://jakeleland.com/)'s [CourseScraper](https://github.com/jake-leland/CourseScraper) written in Java. This (I suspect) is the scraper used to power [Aggie Scheduler](http://www.aggiescheduler.com/).
- [Juliang](https://github.com/Juliang0705/)'s [CoursePicker](https://github.com/Juliang0705/CoursePicker), an awesome self-contained Java application that runs on your local machine.
- [Xiaoyu Li](https://github.com/xiaoyu-tamu/)'s [tamu-course](https://github.com/xiaoyu-tamu/tamu-course) scraper, written in JS.  This scraper requires students to provide important TAMU credentials, which __I do not recommend__.
- [yaoyuan0553](https://github.com/yaoyuan0553/)'s [Howdy Schedule Crawler](https://github.com/yaoyuan0553/HowdyScheduleCrawler), written in Python.
- [Tao Wang](https://github.com/taobupt/)'s [scraper](https://github.com/taobupt/tamu) written in Python, used to select courses.

And of course, [my scraper](https://github.com/SaltyQuetzals/GoodBullSchedules/tree/master/server/scraper) for [Good Bull Schedules](https://goodbullschedules.com).

Each one of these scrapers has their own individual pros and cons, but one thing that unites them is the fact that none of them address the problem that required the scraper in the first place: 

__Somebody else will have to write another scraper if these don't address their needs__.

# Implementation

Finally, the good stuff! If you read the [background](#background) above, thanks for bearing with me. If not, that's fine.

This API has undergone a number of iterations, from JavaScript (in the [original scraper](https://github.com/SaltyQuetzals/GoodBullSchedules/tree/master/server/scraper)), to [Django and GraphQL](https://github.com/SaltyQuetzals/Good-Bull-API/tree/5fa008f2225d6ded9f4aa9f86788dccc1427b65a), to finally TypeScript. I don't intend to change the language from now on, so TypeScript is what I'll be discussing here.

## Backend
The application server is implemented with JavaScript through [NodeJS](https://nodejs.org/en/), using [Express](https://github.com/expressjs/express) for handling incoming requests. Data is stored using [MongoDB](https://www.mongodb.com/). To interface with MongoDB, I use [mongoose](https://mongoosejs.com/) and [typegoose](https://github.com/szokodiakos/typegoose) to keep the representations strongly-typed and simplify my code.

### Scraper
The scraper can be broken down into multiple different sections. Requested data is retrieved using [request-promise](https://github.com/request/request-promise).

### Courses and Sections
This aspect of the scraper is written using [cheeriojs](https://cheerio.js.org/), an awesome implementation of JQuery designed specifically for servers. I use cheerio to efficiently select the HTML elements on pages, and then use various string splitting techniques to extract the data I want.

### Buildings
I stream a CSV that includes the fields I'm looking for, and parse the CSV into individual buildings.

### Grades
In progress...

# Contributing
I'm excited that you want to contribute to this project! After all, this API is for everybody! 

## New Features
If you have a new feature you'd like to see happen, open a [feature request issue](https://github.com/SaltyQuetzals/Good-Bull-API/issues/new?template=feature_request.md). These issues let me know what you hope to see added, and why you think it's important.

__PLEASE NOTE__: This API is intended to be a data source and __READ ONLY__. The only way that data should be changing is if the output of the scrapers changes.

## Missing/Incorrect Data
Something missing from the scraped data? Is an instructor listed incorrectly? Is a section not listed as honors or special topics when it should be? Please open a [missing/incorrect data issue](https://github.com/SaltyQuetzals/Good-Bull-API/issues/new?template=missing-incorrect-data.md)! This kind of scraping is difficult and I'm bound to make mistakes.

## Bugs
Is there a bug in the API? Please open a [bug issue](https://github.com/SaltyQuetzals/Good-Bull-API/issues/new?template=bug_report.md), and be descriptive as to what sequence of events you performed that caused the bug. If I can't reproduce your bug, I can't fix it!
