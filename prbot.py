#!/usr/bin/env python3

# PRBot - monitor a GitHub repository for new pull requests and post a comment
# Copyright (C) 2016-2017 Andrew Donnellan <andrew@donnellan.id.au>
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

try:
    from settings import AUTO_CLOSE
except ImportError:
    AUTO_CLOSE = False

def poll(repo, msg, status, username):
    pulls = repo.get_pulls(sort='created')
    threshold = status['pull_req_number']
    for pull in pulls.reversed:
        print("Pull request #{} by @{}: {}".format(pull.number, pull.user.login, pull.title))
        if pull.number <= threshold:
            print(" => Lower than threshold ({}), breaking".format(threshold))
            break
        comment = msg.render(username=pull.user.login)
        try:
            if pull.closed_at:
                print(" => Pull request closed. Skipping...")
                continue

            # Double check that we haven't posted on this before...
            existing_comments = pull.get_issue_comments()
            if any([comment.user.login == username for comment in existing_comments]):
                print(" => Existing comment detected. Skipping...")
                continue

            pull.create_issue_comment(comment)
            if AUTO_CLOSE:
                pull.edit(state="closed")
                print(" => Comment posted and Pull Request closed successfully")
            else:
                print(" => Comment posted successfully")
            status['pull_req_number'] = max(status['pull_req_number'], pull.number)
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
    username = gh.get_user().login
    print("Bot is posting as user: {}".format(username))

    poll(repo, msg, status, username)
    json.dump(status, open(STATUS_FILE, 'w'))

if __name__ == '__main__':
    main()
