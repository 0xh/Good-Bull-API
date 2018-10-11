import { CourseBlock } from '../CourseBlock';
export declare function requestCatalogDepts(url: string): Promise<string[]>;
export declare function requestCourses(url: string, dept: string): Promise<CourseBlock[]>;
