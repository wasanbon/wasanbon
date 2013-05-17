# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques vincent@vincent-jacques.net
# Copyright 2012 Zearin zearin@gonk.net
# Copyright 2013 Vincent Jacques vincent@vincent-jacques.net

# This file is part of PyGithub. http://jacquev6.github.com/PyGithub/

# PyGithub is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with PyGithub.  If not, see <http://www.gnu.org/licenses/>.

import github
import sys

import Framework

atLeastPython26 = sys.hexversion >= 0x02060000
atMostPython2 = sys.hexversion < 0x03000000


class Exceptions(Framework.TestCase):  # To stay compatible with Python 2.6, we do not use self.assertRaises with only one argument
    def testInvalidInput(self):
        raised = False
        try:
            self.g.get_user().create_key("Bad key", "xxx")
        except github.GithubException, exception:
            raised = True
            self.assertEqual(exception.status, 422)
            self.assertEqual(
                exception.data,
                {
                    "errors": [
                        {
                            "code": "custom",
                            "field": "key",
                            "message": "key is invalid. It must begin with 'ssh-rsa' or 'ssh-dss'. Check that you're copying the public half of the key",
                            "resource": "PublicKey"
                        }
                    ],
                    "message": "Validation Failed"
                }
            )
        self.assertTrue(raised)

    def testUnknownObject(self):
        raised = False
        try:
            self.g.get_user().get_repo("Xxx")
        except github.GithubException, exception:
            raised = True
            self.assertEqual(exception.status, 404)
            self.assertEqual(exception.data, {"message": "Not Found"})
            if atLeastPython26 and atMostPython2:
                self.assertEqual(str(exception), "404 {u'message': u'Not Found'}")
            else:
                self.assertEqual(str(exception), "404 {'message': 'Not Found'}")  # pragma no cover (Covered with Python 3)
        self.assertTrue(raised)

    def testUnknownUser(self):
        raised = False
        try:
            self.g.get_user("ThisUserShouldReallyNotExist")
        except github.GithubException, exception:
            raised = True
            self.assertEqual(exception.status, 404)
            self.assertEqual(exception.data, {"message": "Not Found"})
            if atLeastPython26 and atMostPython2:
                self.assertEqual(str(exception), "404 {u'message': u'Not Found'}")
            else:
                self.assertEqual(str(exception), "404 {'message': 'Not Found'}")  # pragma no cover (Covered with Python 3)
        self.assertTrue(raised)

    def testBadAuthentication(self):
        raised = False
        try:
            github.Github("BadUser", "BadPassword").get_user().login
        except github.GithubException, exception:
            raised = True
            self.assertEqual(exception.status, 401)
            self.assertEqual(exception.data, {"message": "Bad credentials"})
            if atLeastPython26 and atMostPython2:
                self.assertEqual(str(exception), "401 {u'message': u'Bad credentials'}")
            else:
                self.assertEqual(str(exception), "401 {'message': 'Bad credentials'}")  # pragma no cover (Covered with Python 3)
        self.assertTrue(raised)


class SpecificExceptions(Framework.TestCase):
    def testBadCredentials(self):
        self.assertRaises(github.BadCredentialsException, lambda: github.Github("BadUser", "BadPassword").get_user().login)

    def testUnknownObject(self):
        self.assertRaises(github.UnknownObjectException, lambda: self.g.get_user().get_repo("Xxx"))
