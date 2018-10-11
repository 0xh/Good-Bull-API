"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
//courseblock
class CourseBlock {
    constructor(courseBlock) {
        this.courseBlock = courseBlock;
    }
    get titleFields() {
        const titleText = this.courseBlock.find('.courseblocktitle').text();
        const [dept, courseNum, ...name] = titleText.split(' ');
        return [dept, courseNum, name.join(' ')];
    }
}
exports.CourseBlock = CourseBlock;
//# sourceMappingURL=CourseBlock.js.map