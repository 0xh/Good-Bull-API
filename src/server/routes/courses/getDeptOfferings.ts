import { Request, Response, NextFunction } from 'express';
import { CourseModel } from '../../models/courses/Course';
export default async function (req: Request, res: Response) {
    const { dept }: { dept: string } = req.params;
    const results = await CourseModel.find({ dept }, { terms: false, _id: false });
    res.json(results);
}