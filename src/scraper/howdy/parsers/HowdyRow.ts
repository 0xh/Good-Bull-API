import {HowdyRowBody} from './HowdyRowBody';
import {HowdyRowTitle} from './HowdyRowTitle';

import cheerio = require('cheerio');

export class HowdyRow {
  private title: HowdyRowTitle;
  private body: HowdyRowBody;

  constructor(tr: CheerioElement) {
    const $ = cheerio.load(tr);
    const titleText = $('.ddtitle > a').text();
    this.title = new HowdyRowTitle(titleText);

    const dddefault = $('.dddefault');
    this.body = new HowdyRowBody(dddefault);
  }

  get fields(): SectionFields {
    return {...this.title.fields, ...this.body.fields};
  }
}
