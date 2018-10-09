import { Request, Response, NextFunction } from 'express';
import { CourseModel } from '../../models/courses/Course';
export default async function (req: Request, res: Response) {
    const { dept, courseNum }: { dept: string, courseNum: string } = req.params;
    const result = await CourseModel.findOne({ dept, courseNum }, { _id: false });
    res.json(result);
}