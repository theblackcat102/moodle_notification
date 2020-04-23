# NCTU new E3 Moddle bot 

## Background

For the record I am in no way a meticulous student at all, previously my university old online course platform has a lot of neat features that reminds me of due homework, robust mailing system (ensures I don't miss any annoucement), mail notify whenever I submit an assigment. These little details are the result of years and years of polishing our university in house platform which came into an end when the administration decided to move to [Moodle](https://en.wikipedia.org/wiki/Moodle). Which is a pretty looking platform that can't get things done.

Luckily, it has a REST like endpoint which the management team decided to enable it. Hence this is my effort to bring back useful functions that I missed about the old platform to Moodle. 

In theory Moodle platform (> v3? I am not sure which version my university was using ) should be able to use this with slight changes in E3_LOGIN_ENDPOINT and SERVER_API_ENDPOINT


## How it works


Currently, this service scans through each notifier function in a periodic time and sends notification when a match was found.

In the future this should be rewritten in a web service fashion for allowing user interaction of adding and removing notification rules.


# Setup

If your moodle domain is e3new.nctu.edu then start at step 1, otherwise start at step 0

0. Change the *e3new.nctu.edu.tw* inside const.py to your school moodle domain

You may need to check whether rest server endpoint is enabled.

1. Create a new telegram bot, through and obtain the bot token

You need to activate your bot and try to obtain your userid by chatting with your bot.

You can obtain userid by executing get_received_msg() inside telegram.py

2. Create environment files call .env inside this project with the following fields

```
TELEGRAM_API_KEY='telegram bot token'
TELEGRAM_USER_KEY='your user id'
E3_USERNAME='NCTU e3 username'
E3_PASSWORD='NCTU e3 password'
```

3. Setup your python environment by installing the required package inside requirements.txt and run the following script in sequence

```
python models.py
python moddle.py
```

This first script initialize sqlite database which cache all the notified message while the second make sure your moddle account (e3 login credentials) is usable.

## Moddle web service documentation: (the official moddle document sucks)

Getting started here: [https://stackoverflow.com/questions/44652206/getting-information-from-the-moodle-api-as-a-student](https://stackoverflow.com/questions/44652206/getting-information-from-the-moodle-api-as-a-student)

And checkout the full REST document, I am not sure which version NCTU newE3 is using, but at the time of writing this document seems to hold up?

[https://docs.moodle.org/dev/Web_service_API_functions](https://docs.moodle.org/dev/Web_service_API_functions)

Another good source of finding the parameters for each wfunction is this [repo](https://github.com/moodlehq/moodlemobile-scripts/tree/master/ws-samples) 

Try to search around this repo for your wsfunction name
```
{
    "moodlebasepath": "/Users/juanleyvadelgado/www/m/stable_master",
    "name": "mod_assign_view_submission_status",
    "description": "Trigger the submission status viewed event.",
    "type": "write",
    "parameters": {
        "assignid": {
            "external_value": {
                "type": "PARAM_INT",
                ...
            }
    ...
}
```

You have to experiment around on what parameters you need to provide otherwise you will get error.

