import { Typegoose } from 'typegoose';
export declare class Building extends Typegoose {
    abbreviation: string;
    address: string;
    city: string;
    zip: string;
    yearBuilt: number;
    numFloors: number;
    name: string;
    searchableName: string;
}
