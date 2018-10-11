"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class StringCounter {
    constructor(elems) {
        this.items = {};
        for (const elem of elems) {
            if (!(elem in this.items)) {
                this.items[elem] = 1;
            }
            else {
                this.items[elem]++;
            }
        }
    }
    mostCommon(n = this.items.length) {
        return Object.keys(this.items)
            .map(value => {
            const x = [value, this.items[value]];
            return x;
        })
            .sort((a, b) => {
            return b[1] - a[1];
        })
            .slice(0, n);
    }
    add(elem) {
        if (!(elem in this.items)) {
            this.items[elem] = 1;
        }
        else {
            this.items[elem]++;
        }
    }
}
exports.StringCounter = StringCounter;
//# sourceMappingURL=Counter.js.map