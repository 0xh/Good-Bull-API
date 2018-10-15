import request = require('request');
import parse = require('csv-parse');
const CSV_URL =
  'http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[YearBuilt],%20[NumFloors],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^~';

import { buildingModel } from '../../server/models/Building';

type UpdateOperation = {
  updateOne: {
    filter: { abbr: string },
    update: {
      abbreviation: string,
      name: string,
      yearBuilt: number | null,
      numFloors: number | null,
      address: string,
      city: string,
      zip: string,
      searchableName: string
    },
    upsert: true
  }
};

export function downloadCSV() {
  const updateOps: UpdateOperation[] = [];
  request.get(CSV_URL, (err, response, body) => {
    if (!err && response.statusCode === 200) {
      parse(body, {relax_column_count: true}, (err: Error, output: string[][]) => {
        if (err) {
          throw err;
        }
        for (const row of output) {
          const [abbr, name, yearStr, floorStr, address, city, zip, ...rest] = row;
          let yearBuilt: number | null = null;
          let numFloors: number | null = null;
          if (yearStr !== '') {
            yearBuilt = Number(yearStr);
          }
          if (floorStr !== '') {
            numFloors = Number(floorStr);
          }
          const searchableName = abbr + ' ' + name;

          updateOps.push({
            updateOne: {
              filter: { abbr },
              update: {
                abbreviation: abbr,
                name,
                yearBuilt,
                numFloors,
                address,
                city,
                zip,
                searchableName
              },
              upsert: true
            }
          });
        }
        buildingModel.bulkWrite(updateOps).then(() => {
          console.log('Buildings scraped successfully.');
          process.exit();
        });
      });

    }
  });
}

downloadCSV();
