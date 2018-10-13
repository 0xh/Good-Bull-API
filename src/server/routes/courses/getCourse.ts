import {NextFunction, Request, Response} from 'express';

import {Course, courseModel} from '../../models/courses/Course';

export async function getCourse(req: Request, res: Response) {
  const {dept, courseNum}: {dept: string, courseNum: string} = req.params;
  try {
    const course = await courseModel.findOne({dept, courseNum}, {_id: false});
    res.json(course);
  } catch (err) {
    console.log(req.url, err);
    res.sendStatus(400);
  }
}