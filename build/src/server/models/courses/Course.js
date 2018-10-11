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
const mongoose = require("mongoose");
const typegoose_1 = require("typegoose");
mongoose.connect('mongodb://localhost:27017/good-bull');
let Course = class Course extends typegoose_1.Typegoose {
};
__decorate([
    typegoose_1.prop({ required: true, index: true }),
    __metadata("design:type", String)
], Course.prototype, "dept", void 0);
__decorate([
    typegoose_1.prop({ required: true, index: true }),
    __metadata("design:type", String)
], Course.prototype, "courseNum", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "distributionOfHours", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "description", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "prereqs", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "coreqs", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "minCredits", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "maxCredits", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "name", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Course.prototype, "searchableName", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Object)
], Course.prototype, "terms", void 0);
Course = __decorate([
    typegoose_1.index({ searchableName: 'text' })
], Course);
exports.Course = Course;
exports.courseModel = new Course().getModelForClass(Course, { existingMongoose: mongoose });
//# sourceMappingURL=Course.js.map