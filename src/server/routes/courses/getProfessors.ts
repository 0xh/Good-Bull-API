import {Request, Response} from 'express';

import {sectionModel} from '../../models/courses/Section';

type SummaryAggregation = {
  _id: {instructor: string, termCode: number, index: number},
  grades: number
};

interface InstructorSummary {
  [instructorName: string]: {
    ABCDFISUQX: number[],
    GPA: number,
    history: {[termCode: number]: {ABCDFISUQX: number[], GPA: number}}
  };
}

export async function getProfessors(req: Request, res: Response) {
  try {
    const {dept, courseNum}: {dept: string, courseNum: string} = req.params;
    const result = await getSummaryInfo(dept, courseNum);
    res.json(result);
  } catch (err) {
    console.error(req.url, err);
    res.sendStatus(400);
  }
}

async function getSummaryInfo(dept: string, courseNum: string) {
  try {
    const instructorSummary: InstructorSummary = {};
    const summaryAggregationOperation: Array<{}> = [
      {$match: {$and: [{dept}, {courseNum}]}}, {
        $unwind:
            {path: '$gradeDistribution.grades', includeArrayIndex: 'index'}
      },
      {
        $group: {
          _id: {
            instructor: '$instructor',
            index: '$index',
            termCode: '$termCode'
          },
          grades: {$sum: '$gradeDistribution.grades'}
        }
      }
    ];
    const summaryResults: SummaryAggregation[] =
        await sectionModel.aggregate(summaryAggregationOperation);
    for (const result of summaryResults) {
      const instructor: string = result['_id'].instructor;
      if (!(instructor in instructorSummary)) {
        instructorSummary[instructor] = {
          ABCDFISUQX: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          GPA: 0,
          history: {}
        };
      }
      instructorSummary[instructor].ABCDFISUQX[result._id.index] +=
          result.grades;

      const termCode: number = result['_id'].termCode;
      if (!(termCode in instructorSummary[instructor].history)) {
        instructorSummary[instructor].history[termCode] = {
          ABCDFISUQX: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          GPA: 0
        };
      }
      instructorSummary[instructor]
          .history[termCode]
          .ABCDFISUQX[result._id.index] = result.grades;
    }
    for (const summaryKey of Object.keys(instructorSummary)) {
      instructorSummary[summaryKey].GPA =
          calculateGPA(instructorSummary[summaryKey].ABCDFISUQX);
      for (const historyKey of Object.keys(
               instructorSummary[summaryKey].history)) {
        const termCode = Number(historyKey);
        instructorSummary[summaryKey].history[termCode].GPA = calculateGPA(
            instructorSummary[summaryKey].history[termCode].ABCDFISUQX);
      }
    }
    return instructorSummary;
  } catch (err) {
    console.log(err);
    return {};
  }
}

function calculateGPA(grades: number[]): number {
  const sum: number =
      grades.slice(0, 5).reduce((a: number, b: number) => a + b, 0);
  return (grades[0] * 4.0 + grades[1] * 3.0 + grades[2] * 2.0 +
          grades[3] * 1.0) /
      (sum);
}