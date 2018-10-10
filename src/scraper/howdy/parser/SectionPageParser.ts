import cheerio = require("cheerio");
import HowdyRow from "./HowdyRow";

export default class SectionPageParser implements IterableIterator<HowdyRow> {
  private i = 0;
  private rows: HowdyRow[];

  private mergeTRs(trs: Cheerio): HowdyRow[] {
    let merged: CheerioElement[] = [];
    trs.each(function(i, elem) {
      const $ = cheerio.load(elem);
      if ($(elem).find("th.ddtitle").length > 0) {
        merged.push(elem);
      } else if ($(elem).find("td.dddefault").length > 0) $(elem).appendTo($(merged[merged.length - 1]));
    });
    return merged.map(elem => new HowdyRow(elem));
  }

  constructor(html: string) {
    const $ = cheerio.load(html);
    const trs = $(".pagebodydiv > .datadisplaytable > tbody > tr");
    this.rows = this.mergeTRs(trs);
  }
  public next(): IteratorResult<HowdyRow> {
    if (this.i < this.rows.length) {
      return {
        done: false,
        value: this.rows[this.i++]
      };
    }
    return {
      done: true,
      value: this.rows[this.i++]
    };
  }
  [Symbol.iterator]() {
    return this;
  }
}
