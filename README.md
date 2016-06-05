# KernelPRBot

# Installation

Install dependencies:

    pip3 install -r requirements.txt

Set up configuration in settings.py:

	GITHUB_TOKEN="<token here>"
	MESSAGE_PATH="/path/to/message.md"
	STATUS_FILE="/path/to/status.json"
	REPO_NAME="username/repo"

Add a job to your crontab, e.g.:

	*/5 * * * * /home/username/KernelPRBot/kernelprbot.py 2>&1 | /usr/bin/logger

This example will run the script every 5 minutes and send all output
to syslog.

# Copyright

Copyright &copy; 2016 Andrew Donnellan.

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
