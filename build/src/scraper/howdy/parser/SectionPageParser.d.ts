import { HowdyRow } from './HowdyRow';
export declare class SectionPageParser implements IterableIterator<HowdyRow> {
    private i;
    private rows;
    private mergeTRs;
    constructor(html: string);
    next(): IteratorResult<HowdyRow>;
    [Symbol.iterator](): this;
}
