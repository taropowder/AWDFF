from checker.checker import CheckerTemplate, ProblemTemplate


class dvwaCheck(CheckerTemplate):
    checker_problem_template = ProblemTemplate.objects.get(image_id='b843afe11c5f')

    def _prepare(self):
        return True

    def _check1(self):
        # print('check1')
        return False, 'reason'
