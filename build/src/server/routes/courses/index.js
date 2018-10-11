"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const getDeptOfferings_1 = require("./getDeptOfferings");
const getCourse_1 = require("./getCourse");
const router = express.Router();
router.get('/:dept', getDeptOfferings_1.default);
router.get('/:dept/:courseNum', getCourse_1.default);
exports.default = router;
//# sourceMappingURL=index.js.map