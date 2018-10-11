"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const routes_1 = require("./routes");
const app = express();
app.use('/', routes_1.router);
app.listen(3000, () => {
    console.log('Listening on port 3000!');
});
//# sourceMappingURL=app.js.map