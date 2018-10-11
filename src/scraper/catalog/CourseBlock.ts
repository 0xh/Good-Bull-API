import cheerio = require('cheerio');
import {Course} from '../../server/models/courses/Course';

type DescriptionFields = {
  description: string|null; prereqs: string | null; coreqs: string | null;
  crossListings: string | null;
};

export class CourseBlock {
  courseBlock: Cheerio;

  constructor(courseBlock: Cheerio) {
    this.courseBlock = courseBlock;
  }

  get titleFields(): {dept: string; courseNum: string; name: string | null} {
    const titleText = this.courseBlock.find('.courseblocktitle').text();
    const [dept, courseNum, ...name] = titleText.split(/\s+/g);
    return {dept, courseNum, name: name.join(' ')};
  }

  get hoursFields(): {
    minCredits: number|null; maxCredits: number | null;
    distributionOfHours: string;
  } {
    const hourText =
        this.courseBlock.find('.courseblock > .hours').text().trim();
    const [credits, distributionOfHours]: string[] = hourText.split(/\s{2,}/g);
    let minCredits: number|null = null;
    let maxCredits: number|null = null;
    const matches = credits.match(/[0-9\.]+/g);
    if (!matches) {
    } else {
      minCredits = Number(matches[0]);
      if (matches.length === 1) {
        maxCredits = Number(matches[0]);
      } else if (matches.length === 2) {
        maxCredits = Number(matches[1]);
      }
    }
    return {minCredits, maxCredits, distributionOfHours};
  }

  get descriptionFields(): DescriptionFields {
    const descriptionText =
        this.courseBlock.find('.courseblockdesc').text().trim();
    const DESCRIPTION_PATTERN =
        /(.+?(?= Prerequisites?: | Corequisites?: | Cross Listings?: |$))/g;

    const matches = descriptionText.match(DESCRIPTION_PATTERN);
    const output: DescriptionFields =
        {description: null, prereqs: null, coreqs: null, crossListings: null};
    if (!matches) {
      return output;
    }
    output.description = matches[0].trim();

    for (let match of matches.slice(1)) {
      match = match.trim();
      const colonIndex = match.indexOf(':');
      const info = match.slice(colonIndex + 2).trim();
      if (match.startsWith('Prereq')) {
        output.prereqs = info;
      } else if (match.startsWith('Coreq')) {
        output.coreqs = info;
      } else if (match.startsWith('Cross')) {
        output.crossListings = info;
      }
    }
    return output;
  }

  get fields(): CourseFields {
    const {dept, courseNum, name} = this.titleFields;
    const searchableName = `${dept} ${courseNum}: ${name}`;
    return {
      ...this.titleFields,
      ...this.hoursFields,
      ...this.descriptionFields,
      searchableName
    };
  }
}
