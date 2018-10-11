const URL =
  "http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[YearBuilt],%20[NumFloors],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^^~";
import csv = require("csv-parse");
import request = require("request");
import fs = require("fs");

request.get(URL).on('response', function(response)  {
    console.log(JSON.stringify(response, null, 3));
})
