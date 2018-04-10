# Good-Bull-API
Good Bull API is a public-facing API for Texas A&M students who want to do development work with Howdy data. It scrapes the [course registrar](https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched), the [course catalog](http://catalog.tamu.edu/), the [building list](http://fcor.tamu.edu/webreporter/indexv6.asp?t=[Current_Inv_Bldgs]), and historical [grade distributions](http://web-as.tamu.edu/gradereport/) in order to provide students with data that is up-to-date (as of the last hour). 

## Motivation
Everybody who wants to work with Howdy data has to do the same thing: scrape the course registrar. It's a painful process, riddled with scraping poorly-written HTML, ECONNRESET errors, inconsistent data formatting, and more. In developing Good Bull Schedules, I found that the Howdy portal's inconsistencies caused more problems to my application than the code that I wrote myself. Thus, what I've decided to do is build this API, that does all of the scraping for students, so that all they have to do is simply query an API (which is much simpler than scraping the entire registrar over and over). Hopefully it will be of use to somebody besides myself!

## Objectives
Design a consistent and robust API that allows students to individually query for the following:
- [ ] Buildings, which includes addresses, zip codes, cities, names, and abbreviations.
- [ ] Courses, which includes course descriptions, semesters in which it was tradtionally offered, as well as credit hours and number of hours spent in lecture, laboratory, and recitation.
- [ ] Sections, which includes meeting times, instructors, and locations.
- [ ] Instructors, which includes their historical grade distributions, their historical GPA, as well as their cumulative grade distribution and cumulative GPA.

## Moving Forward
We'd like to include more and more information of the Howdy portal. It's a damn shame that not all of this information is easily accessible, but we're doing our best with what we have.

In the future, we'd like to include the following data in our API, and would __gladly__ welcome pull requests that contribute the following functionalities.
- [ ] A programmatic relationship between courses (co-requisites, pre-requisites, etc.)
