from bs4 import BeautifulSoup

from checker.checker import CheckerTemplate, ProblemTemplate


class dvwaCheck(CheckerTemplate):
    checker_problem_template = ProblemTemplate.objects.get(image_id='b843afe11c5f')

    def _prepare(self):
        url = self.url + '/login.php'
        res = self.session.get(self.url)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        soup = BeautifulSoup(res.text, 'html.parser')
        user_token = soup.select('input[name=user_token]')
        data = {'username': 'admin', 'password': 'password', 'user_token': user_token[0]['value'], 'Login': 'Login'}
        res = self.session.post(url, data=data, headers=headers)
        self.session.cookies['security'] = 'low'
        return True

    def _check1(self):
        # print('check1')
        url = self.url + '/vulnerabilities/sqli/?id=1&Submit=Submit#'
        res = self.session.get(url)
        if 'Surname: admin' in res.text:
            return True, 'ok'
        else:
            return False, 'sqli is down'
