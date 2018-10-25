import express = require('express');
import {getCourse} from './getCourse';
import {getDeptOfferings} from './getDeptOfferings';
import {Router} from 'express';
import {getSection} from './getSection';
import {getProfessors} from './getProfessors';

export class CourseRouter {
  routes: Router;

  constructor() {
    this.routes = Router({mergeParams: true});
    this.init();
  }

  init() {
    this.routes.get('/', getDeptOfferings);
    this.routes.get('/:courseNum', getCourse);
    this.routes.get('/:courseNum/professors', getProfessors);
    this.routes.get('/:courseNum/:sectionNum', getSection);
  }
}