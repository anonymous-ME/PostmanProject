# Postman Project 2

## Problem Statement:

### Monitor a MySQL Database For Tables That Are About To Run Out Of Autoincrement IDs

send an alert to Slack.
https://dev.mysql.com/doc/refman/8.0/en/example-auto-increment.html
MySQL allows auto increment ids as a way of uniquely identifying each row in a database.
However, each attribute in a MySQL table has a fixed maximum size, which limits the total
possible number of rows that can be accommodated with auto increment. Your script should
check for all tables in a database that have auto increment ids and are about to run out of those
IDs. All identified tables should be sent as an alert to Slack.

## Expected solution format:
A GitHub repository (under your own account) that contains a script to check a local MySQL
database for the conditions described above.
