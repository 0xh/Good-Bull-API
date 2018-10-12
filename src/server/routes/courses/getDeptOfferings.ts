import { Request, Response, NextFunction } from "express";
import { courseModel } from '../../models/courses/Course';

export async function getDeptOfferings(req: Request, res: Response) {
    const { dept }: { dept: string } = req.params;
    try {
        const courses = await courseModel.find({ dept }, { _id: false, terms: false });
        res.json(courses);
    } catch (err) {
        console.error(req.url, err);
        res.sendStatus(400);
    }
}