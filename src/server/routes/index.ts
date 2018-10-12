import { CourseRouter } from './courses';
import { Router } from 'express';

export class IndexRouter {
    routes: Router;

    constructor()   {
        this.routes = Router({mergeParams: true});
        this.init();
    }

    init()  {
        this.routes.use('/courses/:dept', new CourseRouter().routes);
    }
}