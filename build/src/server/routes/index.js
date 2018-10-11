"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const courses_1 = require("./courses");
const router = express.Router();
router.use('/courses', courses_1.default);
exports.default = router;
//# sourceMappingURL=index.js.map