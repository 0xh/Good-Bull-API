import express = require('express');
import getDeptOfferings from './getDeptOfferings';
import getCourse from './getCourse';
const router = express.Router();

router.get('/:dept', getDeptOfferings);
router.get('/:dept/:courseNum', getCourse);

export default router;