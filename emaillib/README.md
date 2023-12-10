# Email Application
## Updates: SMTP-Implementation (10.12.2023)
1. Create a new project based on Python
1. In debug mode, your program can be tested but no emails will be sent.
2. The program will output a list of email addresses to a file, to which emails are allowed to be sent.
2. To start the bulk-send app, several files should be provided:
    - A file to store the configuration of your email.
    - A file to store the email addresses to which email will be sent.
    - A file to store the email addresses whose owner has unsubscribed the ad
    - A file to achieve email addresses to avoid duplicated email sending.
    - A log file to suspect the status of the program.
    - A EML file that contains your email content. It can also be seen as a email template.


Run the program with the following command:
```bash
python3 app.py -c config.yaml -s list_send.txt -u unsubs.txt -a achieve.txt -l info.log -e sample.eml --debug false
```