# PRBot

PRBot is a simple script that scrapes a GitHub repository for pull requests and
posts a message. It is particularly designed for the use case of projects which
use GitHub only for hosting or providing a read-only mirror, such as the Linux
kernel, where it's not uncommon for new contributors to attempt to contribute a
GitHub pull request rather than through mailing lists or other correct pathways.

PRBot works purely by scraping the GitHub API on a regular basis. While
[Webhooks](https://developer.github.com/webhooks/) are the "proper" method of
triggering a bot like this one, they also require setup by an organisation or
repository administrator, which isn't always possible.

# Installation

Install dependencies:

    pip3 install -r requirements.txt

Set up configuration in settings.py:

	GITHUB_TOKEN="<token here>"
	MESSAGE_PATH="/path/to/message.md"
	STATUS_FILE="/path/to/status.json"
	REPO_NAME="username/repo"
	AUTO_CLOSE=False

Add a job to your crontab, e.g.:

	*/5 * * * * /home/username/PRBot/kernelprbot.py 2>&1 | /usr/bin/logger

This example will run the script every 5 minutes and send all output
to syslog.

# Message Format

The message should be in Markdown format for display on the GitHub web
interface.

You can use the placeholder `{{ username }}` to dynamically insert the
GitHub username of the pull request originator:

	Hi @{{ username }},
	
	Thanks for your contribution...

# Contributions

PRBot is more-or-less feature-complete, but any fixes or other contributions are
welcome. Contributions by GitHub pull request are preferred, alternatively
patches may be sent by email to <andrew@donnellan.id.au>. Issues may be reported
on GitHub.

Contributions **must** include a `Signed-off-by:` line (use `git commit -s`),
under your real name, indicating that you have read and agree to the
[Developer Certificate of Origin v1.1](https://developercertificate.org/).

Please follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding
style wherever possible.

# Copyright

Copyright &copy; 2016-2017 Andrew Donnellan.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
