import { Request, Response } from 'express';
import { sectionModel } from '../../models/courses/Section';
export async function getSection(req: Request, res: Response) {
    const { dept, courseNum, sectionNum } = req.params;
    const { termCode }: { termCode: TermCode } = req.query;

    if (!termCode) {
        res.status(400).send({
            message: 'The "termCode" query parameter is required.'
        });
    } else {
        try {
            const section = await sectionModel.findOne({ dept, courseNum, sectionNum, termCode });
            res.json(section);
        } catch (err) {
            console.error(req.url);
            console.error(err);
        }
    }
}