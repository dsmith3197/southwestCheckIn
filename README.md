# Southwest Check In Script
Script that automatically checks you into your Southwest flight 24 hours before by using Selenium and the Chrome driver.

## Example
```
caffeinate python check_in.py -f John -l Smith -c AABBCC -p 1234567890 -t 'Jan 1 2017 12:00AM'
```

## Flags

```
-f = first name
-l = last name
-c = confirmation number
-p = 10 digit phone number 
-t = date and time of flight in format shown above
```

## How it Works
When running this command, it schedules two events.  First it will open a Chrome web browser 20 seconds before 24 hours before your flight. Then, 24 hours before your flight, it will check you in and send your boarding pass to your phone via text.  We use the command caffeinate before python to ensure the computer does not go to sleep (this command only works on mac). 
