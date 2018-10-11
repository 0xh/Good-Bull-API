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
let Building = class Building extends typegoose_1.Typegoose {
};
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Building.prototype, "abbreviation", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Building.prototype, "address", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Building.prototype, "city", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", String)
], Building.prototype, "zip", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Number)
], Building.prototype, "yearBuilt", void 0);
__decorate([
    typegoose_1.prop(),
    __metadata("design:type", Number)
], Building.prototype, "numFloors", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Building.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Building.prototype, "searchableName", void 0);
Building = __decorate([
    typegoose_1.index({ searchableName: 'text' })
], Building);
exports.Building = Building;
//# sourceMappingURL=Building.js.map