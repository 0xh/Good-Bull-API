"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const mongoose = require('mongoose');
const typegoose_1 = require("typegoose");
mongoose.connect('mongodb://localhost:27017/good-bull');
class GpaDistribution extends typegoose_1.Typegoose {
}
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Number)
], GpaDistribution.prototype, "gpa", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Array)
], GpaDistribution.prototype, "ABCDFISQUX", void 0);
class Section extends typegoose_1.Typegoose {
    get fullName() {
        return `${this.dept}-${this.courseNum}-${this.sectionNum}`;
    }
}
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Section.prototype, "dept", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Section.prototype, "courseNum", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Section.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ required: true, index: true }),
    __metadata("design:type", Number)
], Section.prototype, "crn", void 0);
__decorate([
    typegoose_1.prop({ required: true, index: true }),
    __metadata("design:type", String)
], Section.prototype, "sectionNum", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String),
    __metadata("design:paramtypes", [])
], Section.prototype, "fullName", null);
__decorate([
    typegoose_1.prop({ required: true, index: true }),
    __metadata("design:type", Number)
], Section.prototype, "termCode", void 0);
__decorate([
    typegoose_1.arrayProp({ items: Meeting, _id: false }),
    __metadata("design:type", Array)
], Section.prototype, "meetings", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Section.prototype, "gpaDistribution", void 0);
exports.Section = Section;
const sectionModel = new Section().getModelForClass(Section);
exports.sectionModel = sectionModel;
//# sourceMappingURL=Section.js.map