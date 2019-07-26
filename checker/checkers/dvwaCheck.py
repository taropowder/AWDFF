from checker.checker import CheckerTemplate, ProblemTemplate


class dvwaCheck(CheckerTemplate):
    checker_problem_template = ProblemTemplate.objects.get(image_id='b843afe11c5f')

    def _login(self):
        print(123)
        # self.session.get(self.url)

    def _check1(self):
        print('check1')