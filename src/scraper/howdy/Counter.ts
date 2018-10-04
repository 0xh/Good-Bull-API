export class StringCounter {
    items: { [s: string]: number };

    constructor(elems: any[]) {
        this.items = {};
        for (let elem of elems) {
            if (!(elem in this.items)) {
                this.items[elem] = 1;
            } else {
                this.items[elem]++;
            }
        }
    }

    mostCommon(n: number = this.items.length) {
        return Object.keys(this.items).map(value => {
            let x: [string, number] = [value, this.items[value]]
            return x
        }).sort((a, b) => {
            return b[1] - a[1]
        }).slice(0, n)
    }

    add(elem: string) {
        if (!(elem in this.items)) {
            this.items[elem] = 1;
        } else {
            this.items[elem]++;
        }
    }
}