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
    console.log(results);
    for (let result of results){
        const instructor: string = result["_id"].instructor;
        if (!(instructor in instructorSummary)){
            instructorSummary[instructor] = {
                ABCDFISUQX: [0,0,0,0,0,0,0,0,0,0],
                GPA: 0
            }
        }
        instructorSummary[instructor].ABCDFISUQX[result._id.index] = result.grades;
    }
    for (let key of Object.keys(instructorSummary)){
        instructorSummary[key].GPA = getGPA(instructorSummary[key].ABCDFISUQX);
    }
    res.json(instructorSummary);
}

function getGPA(grades: number[]){
    const sum: number = grades.slice(0, 5).reduce((a: number, b: number) => a + b, 0);
    return (grades[0] * 4.0 + grades[1] * 3.0 + grades[2] * 2.0 + grades[3] * 1.0)/(sum);
}