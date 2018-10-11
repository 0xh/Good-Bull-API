"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const getDeptOfferings_1 = require("./getDeptOfferings");
const getCourse_1 = require("./getCourse");
const courseRouter = express.Router();
exports.courseRouter = courseRouter;
courseRouter.get('/:dept', getDeptOfferings_1.getDeptOfferings);
courseRouter.get('/:dept/:courseNum', getCourse_1.getCourse);
//# sourceMappingURL=index.js.map