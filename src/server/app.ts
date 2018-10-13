import express = require('express');
import {IndexRouter} from './routes';
const app = express();

app.use('/', new IndexRouter().routes);
app.listen(3000, () => {
  console.log('Listening on port 3000!');
});