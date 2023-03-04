## pyLookout

A simple Python program to check Linux system's 
resource utilization and service availability.  

Currently it can:
* Check CPU, RAM and Disk space
* Send notifications via SendGrid and Simplepush

Planned functionality:
* Send notifications via Telegram, WhatsApp and IRC.
* Check container status.
* Report new active session.
* Monitor logs to find suspicious activity.
* Run continuously as a service. 

### Installation
To install the app, run:
```
python -m pip install pylookout
```

### Usage
To send notifications pyLookout reads API keys from 
the environment.  

SendGrid variables:
```
export SENDGRID_TO='<send-to-email>@<mail>.com'
export SENDGRID_FROM='<verified-sender>@<mail>.com'
export SENDGRID_API_KEY='.......'
```  

Simplepush
```
export SIMPLEPUSH='.......'
```  

To run the program, just run:
```
python main.py
```
It will gather server metrics and send a notificationa 
via preferred method.

It can be added to crontab to be ran on a schedule.
