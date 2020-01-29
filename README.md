# Project

SMTP Email Client project built to be able to control all of the SMTP information myself, rather than relying on the unflexible nature of the web-based email writing providers.

Project completed in early 2018, around February ~ March, but since I didn't have the practice of using Git/GitHub at the time, I just uploaded it now (2020).

# Technology

Technologies used: Python, SMTP, TCP, SSL, Web Servers

# Usage

This creates an alternative to using the web browser to send emails. It is flexible because you can set all SMTP information required for an email yourself, e.g. "FROM", "TO", "SUBJECT", etc. (There is no need for the "FROM" field to match your email username/login, for example)

# How-To

1.  Download source code
2.  Make sure Python is installed. Type in a terminal:
    ```python --version```
3.  If output shows a version of Python installed, procceed to step 5. Otherwise, go to step 4:
4.  [Download](https://www.python.org/downloads/) and install Python. Check the steps in their website and come back after you've installed it.
5.  Navigate in a terminal, from root to project folder, with ```cd <folder>``` **until you reach the folder which the project is in!**
6.  Type the command ```python SMTP_PA.py``` to run the email client
7.  Type all requested information in **string** format, i.e. between " "
8.  Enjoy!

## Important Observation

The default email provider is set to Outlook, but if you use another provider, e.g. Gmail, Yahoo, etc., it can be easily changed in the source code. Find the ```mailserver``` variable and set it to the URL of your preferred provider, e.g. 'gmail.com'.

## Open Source

Feel free to contribute! I haven't worked much on it for a while, but I plan on doing so in the future. Also, **please create an "Issue" to let me know of anything that isn't working as expected.** Thanks!

### Disclaimer

This project is not to be used for unethical purposes. The flexibe nature of the SMTP headers and information can be leveraged in many different ways, so please limit it to normal usage or ethical pranks. I don't intend to promote nor encourage unethical behavior in any way.
