import express = require('express');
import courseRouter from './courses';

const router = express.Router();
router.use('/courses', courseRouter);

export default router;