#!/usr/bin/env python3

# KernelPRBot - monitor a GitHub repository for new pull requests and post a comment
# Copyright (C) 2016 Andrew Donnellan <andrew@donnellan.id.au>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import traceback

import json
import github
import jinja2
from settings import GITHUB_TOKEN, MESSAGE_PATH, STATUS_FILE, REPO_NAME

def poll(repo, msg, status):
    pulls = repo.get_pulls(sort='created')
    threshold = status['pull_req_number']
    for pull in pulls.reversed:
        print("Pull request #{} by @{}: {}".format(pull.number, pull.user.login, pull.title))
        if pull.number <= threshold:
            print(" => Lower than threshold ({}), breaking".format(threshold))
            break
        comment = msg.render(username=pull.user.login)
        try:
            pull.create_issue_comment(comment)
            status['pull_req_number'] = max(status['pull_req_number'], pull.number)
            print(" => Comment posted successfully")
        except:
            print(" => Error occurred when posting comment")
            print("\n".join([" =>  " + line for line in traceback.format_exc().splitlines()]))

def main():
    try:
        status = json.load(open(STATUS_FILE))
    except FileNotFoundError:
        status = {'pull_req_number': 0}

    msg = jinja2.Template(open(MESSAGE_PATH).read())
    gh = github.MainClass.Github(GITHUB_TOKEN)
    repo = gh.get_repo(REPO_NAME)

    poll(repo, msg, status)
    json.dump(status, open(STATUS_FILE, 'w'))

if __name__ == '__main__':
    main()
