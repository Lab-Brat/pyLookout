## pyLookout

A simple Python program to check Linux system's 
resource utilization and service availability.  

Currently it can:
* Check CPU, RAM and Disk space
* Send notifications via SendGrid and Simplepush

Planned functionality:
* Send notifications via Telegram, WhatsApp and IRC.
* Check container status.
* Report new active SSH sessions.
* Monitor logs to find suspicious activity.
* Run continuously as a service in the background. 

### Installation
To install the app, clone the repository and install with pip:
```bash
git clone https://github.com/Lab-Brat/pyLookout.git
cd pyLookout
python -m pip install .
```

### Usage
To send notifications pyLookout reads API keys from 
the environment.  

SendGrid requires to specify sending and destination 
email addresses, and also an API key:
```
SENDGRID_TO
SENDGRID_FROM
SENDGRID_API_KEY
```  

Simplepush requires only the API key and sends notifications 
to the app"
```
SIMPLEPUSH
```  

To run the program, first install it with pip. 
It will create an executable in `/home/$USER/.local/bin/`, 
(which should be in $PATH), and launch it:
```bash
pylookout
```
It will gather server metrics and send a notificationa 
via preferred method if a certain total utilization percentage
is reached (75% by default).

Add it to crontab to run on a schedule.
