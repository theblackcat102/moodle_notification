from moddle import ModdleAPI
from models import send_notification
from datetime import datetime
import humanize
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

moddle = ModdleAPI(os.getenv("E3_USERNAME", ""), os.getenv("E3_PASSWORD", ""))
moddle.get_valid_courses()

def notify_new_assignment():
    assignments = moddle.get_undue_assignment()
    for assignment in assignments:
        assignment_id = 'new_{}_{}'.format(assignment['course'], assignment['id'])
        duedate = datetime.fromtimestamp(int(assignment['duedate']))
        countdown = humanize.naturaltime( datetime.now() - duedate)
        duedate = duedate.strftime("%Y-%m-%d %H:%M:%S")
        assignment_name = assignment['name']
        intro = assignment['intro']
        course = assignment['course']
        content = f'*[ 新作業! ] {assignment_name}*\n*截止時間：{countdown}\n {duedate}*\n 課程: {course}\n {intro}'

        success = send_notification({
            'id': assignment_id,
            'content': content
        }, parse_mode='Markdown')

def notify_assignment_due1day():
    assignments = moddle.get_undue_assignment()
    for assignment in assignments:
        duedate = datetime.fromtimestamp(int(assignment['duedate']))
        countdown = datetime.now() - duedate
        if countdown.days == -1 or ( countdown.seconds <= (3600*24)  and countdown.days == 0):
            assignment_id = 'due1day_{}_{}'.format(assignment['course'], assignment['id'])

            countdown = humanize.naturaltime( datetime.now() - duedate)
            duedate = duedate.strftime("%Y-%m-%d %H:%M:%S")
            assignment_name = assignment['name']
            intro = assignment['intro']
            course = assignment['course']
            content = f'*[ 作業倒數1天 ] {assignment_name}*\n*截止時間：{countdown}\n {duedate}*\n 課程: {course}\n {intro}'

            success = send_notification({
                'id': assignment_id,
                'content': content
            }, parse_mode='Markdown')


def notify_assignment_due2day():
    assignments = moddle.get_undue_assignment()
    for assignment in assignments:
        duedate = datetime.fromtimestamp(int(assignment['duedate']))
        countdown = datetime.now() - duedate
        if countdown.days == -2:
            assignment_id = 'due1day_{}_{}'.format(assignment['course'], assignment['id'])

            countdown = humanize.naturaltime( datetime.now() - duedate)
            duedate = duedate.strftime("%Y-%m-%d %H:%M:%S")
            assignment_name = assignment['name']
            intro = assignment['intro']
            course = assignment['course']
            content = f'*[ 作業倒數2天 ] {assignment_name}*\n*截止時間：{countdown}\n {duedate}*\n 課程: {course}\n {intro}'

            success = send_notification({
                'id': assignment_id,
                'content': content
            }, parse_mode='Markdown')


def notify_announcment():
    valid_courses = moddle.get_valid_courses()
    for c in valid_courses:
        announcements = moddle.get_course_announcement(c)
        for announcement in announcements:
            announcement_id = 'announce_{}_{}'.format(c['id'], announcement['id'])
            content = '[通知] {} \n {} [link]({})'.format(c['fullname'], announcement['name'], announcement['url'])
            # print(content)
            success = send_notification({
                'id': announcement_id,
                'content': content
            }, parse_mode='Markdown')


if __name__ == "__main__":
    import inspect, sys
    fset = [ (name, obj) for name,obj in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(obj) ]
    for fname, f in fset:
        if 'notify_' in fname:
            f()
