import HowdyRowTitle from "./HowdyRowTitle";
import HowdyRowBody from "./HowdyRowBody";
import cheerio = require("cheerio");

export default class HowdyRow {
  private title: HowdyRowTitle;
  private body: HowdyRowBody;

  constructor(tr: CheerioElement) {
    const $ = cheerio.load(tr);
    const titleText = $(".ddtitle > a").text();
    this.title = new HowdyRowTitle(titleText);

    const dddefault = $(".dddefault");
    this.body = new HowdyRowBody(dddefault);
  }

  public get titleFields() {
    return this.title.fields;
  }

  public get bodyFields() {
    return this.body.fields;
  }

  public get asSection(): SectionFields {
    return {
      ...this.titleFields,
      ...this.bodyFields
    }
  }
}
