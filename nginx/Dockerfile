# CSCI 455 EMRKS Project - Optomet.me Optometry Clinic
# Copyright (C) 2024  Julia Dewhurst, Joseph Melancon, Anna Wille, Maya Wyganowska
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

FROM nginx:latest

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/site.key -out /etc/nginx/fullchain.cer -subj "/C=US/ST=Grand Forks/L=Grand Forks/O=UND CEM/OU=CSCI 455 JD JM AW MW/CN=optomet.me"

COPY nginx.conf /etc/nginx/nginx.conf