import express = require('express');
import { getCourse } from './getCourse';
import { getDeptOfferings } from './getDeptOfferings';
import { Router } from 'express';

export class CourseRouter {
    routes: Router

    constructor()   {
        this.routes = Router({mergeParams: true});
        this.init();
    }

    init()  {
        this.routes.get('/', getDeptOfferings);
        this.routes.get('/:courseNum', getCourse);
    }
}