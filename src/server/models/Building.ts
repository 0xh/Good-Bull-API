import mongoose = require('mongoose');
import {Typegoose, index, prop} from 'typegoose';
import {Model, Document} from 'mongoose';
mongoose.connect('mongodb://localhost:27017/good-bull');

@index({searchableName: 'text'})
class Building extends Typegoose {
  @prop({required: true}) abbreviation!: string;

  @prop() address!: string;

  @prop() city!: string;

  @prop() zip!: string;

  @prop() yearBuilt!: number|null;

  @prop() numFloors!: number|null;

  @prop({required: true}) name!: string;

  @prop({required: true}) searchableName!: string;
}

const buildingModel: Model<Document> =
    new Building().getModelForClass(Building);

export {Building, buildingModel};