"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const courses_1 = require("./courses");
const router = express.Router();
exports.router = router;
router.use('/courses', courses_1.courseRouter);
//# sourceMappingURL=index.js.map