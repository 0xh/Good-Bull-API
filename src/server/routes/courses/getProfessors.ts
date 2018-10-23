import {Request, Response} from 'express';
import {sectionModel} from '../../models/courses/Section';
import { Aggregate } from 'mongoose';

type InstructorAggregation = {
    _id: {
        instructor: string,
        index: number
    },
    grades: number
}

interface InstructorSummary{
    [key: string]: {
        ABCDFISUQX: number[],
        GPA: number
    }
}

export async function getProfessors(req: Request, res: Response){
    const {dept, courseNum}: {dept: string, courseNum: string} = req.params;
    let instructorSummary: InstructorSummary = {}
    let aggregationOperation: Object[] = [
        {$match:
            {$and: [
                {dept: dept},
                {courseNum: courseNum}
            ]}
        },
        {$unwind: {
            path: "$gradeDistribution.grades",
            includeArrayIndex: "index"
        }},
        {$group: {
            _id: {instructor: "$instructor", index: "$index"},
            grades: {$sum : "$gradeDistribution.grades"}
        }}
    ];
    const results: InstructorAggregation[] = await sectionModel.aggregate(aggregationOperation);
    for (let result of results){
        const instructor: string = result["_id"].instructor;
        if (instructor in instructorSummary){
            
        }
        else{
            instructorSummary[instructor] = 
        }
    }
    console.log(results);
}