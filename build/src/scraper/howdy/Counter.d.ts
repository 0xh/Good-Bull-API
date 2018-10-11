export declare class StringCounter {
    items: {
        [s: string]: number;
    };
    constructor(elems: string[]);
    mostCommon(n?: number): [string, number][];
    add(elem: string): void;
}
