let mongoose = require('mongoose');
import { arrayProp, prop, Ref, Typegoose } from 'typegoose';
import { Meeting } from './Meeting';
mongoose.connect('mongodb://localhost:27017/good-bull')

class GpaDistribution extends Typegoose {
    @prop()
    gpa!: number;

    @prop()
    ABCDFISQUX!: number[];
}


class Section extends Typegoose {
    @prop()
    dept!: string;

    @prop()
    courseNum!: string;

    @prop()
    name!: string;

    @prop({ required: true, index: true })
    crn!: number;

    @prop({ required: true, index: true })
    sectionNum!: string;

    @prop()
    get fullName(): string {
        return `${this.dept}-${this.courseNum}-${this.sectionNum}`
    }

    @prop({ required: true, index: true })
    termCode!: number;

    @arrayProp({ items: Meeting, default: [] })
    meetings?: Ref<Meeting>[];

    @prop()
    gpaDistribution?: Ref<GpaDistribution>;
}

const SectionModel = new Section().getModelForClass(Section);

export { Section, SectionModel };
