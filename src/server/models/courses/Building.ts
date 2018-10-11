import mongoose = require('mongoose');
import { Typegoose, index, prop } from 'typegoose';
mongoose.connect('mongodb://localhost:27017/good-bull');

@index({ searchableName: 'text' })
export class Building extends Typegoose {
    @prop({ required: true })
    abbreviation!: string;

    @prop()
    address!: string;

    @prop()
    city!: string;

    @prop()
    zip!: string;

    @prop()
    yearBuilt!: number;

    @prop()
    numFloors!: number;

    @prop({ required: true })
    name!: string;

    @prop({ required: true })
    searchableName!: string;

}