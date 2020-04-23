import requests
import os, json
from const import *
from utils import call

from datetime import datetime, timedelta
os.makedirs(CACHE_PATH, exist_ok=True)




class ModdleAPI():


    def __init__(self, username, password):
        self.enrolled_courses = []
        self.valid_courses = []
        cache_path = os.path.join(CACHE_PATH, 'user.json')
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                self.user_details = json.load(f)
        else:
            token = ModdleAPI.login(username, password)
            user_details = call(token, 'core_webservice_get_site_info')
            user_details['token'] = token
            with open(cache_path, 'w') as f:
                json.dump(user_details, f)
                self.user_details = user_details

    def get_all_courses(self):
        enrolled_courses = call(self.user_details['token'], 'core_enrol_get_users_courses', userid=self.user_details['userid'])
        self.enrolled_courses = enrolled_courses
        return self.enrolled_courses

    def get_valid_courses(self):
        timestamp_now = datetime.timestamp(datetime.now())
        if len(self.enrolled_courses) == 0:
            self.get_all_courses()
        valid_courses = []
        for course in self.enrolled_courses:
            if course['enddate'] > timestamp_now:
                valid_courses.append(course)
        self.valid_courses = valid_courses
        return valid_courses

    def get_course_announcement(self, course):
        # returns a list
        course_annoncements = call(self.user_details['token'], 'core_course_get_contents', courseid=course['id'])
        course_annoncement_modules = []
        for course_a in course_annoncements:
            course_annoncement_modules += course_a['modules']
        
        course_annoncement_modules.sort(key=lambda x: x['id'])
        return course_annoncement_modules

    def get_assignment_submission_status(self, assignment):
        '''
        params: assignment: assignment dictionary, must contain id attributes
        returns: 
            results: {
                "lastattempt": {
                    "submission": {
                        "id": ,
                        "userid": ,
                        "attemptnumber": 0,
                        "timecreated": ,
                        "timemodified": ,
                        "status": "new",
                    ...
                }
        '''
        
        results = call(self.user_details['token'], 'mod_assign_get_submission_status', 
            assignid=assignment['id'], userid=self.user_details['id'])
        
        return results

    def get_undue_assignment(self):
        results = call(self.user_details['token'], 'mod_assign_get_assignments')
        valid_course_ids = [ course['id'] for course in self.valid_courses ]

        timestamp_now = datetime.timestamp(datetime.now())

        assignments = []
        for course in results['courses']:
            if course['id'] in valid_course_ids:
                for assign in course['assignments']:
                    # print(assign['duedate'], timestamp_now)
                    if assign['duedate'] > timestamp_now:
                        assign['courseid'] = course['id']
                        assign['course'] =course['fullname']
                        assignments.append(assign)
        return assignments
    
    def get_course_group(self, course):
        results = call(self.user_details['token'], 'core_group_get_course_user_groups', courseid=course['id'])
        return results


    @staticmethod
    def login(username, passsword):
        payload = {'username': username,
            'password': passsword,
            'rememberusername': '0',
            'service': 'moodle_mobile_app'
        }
        res = requests.post(E3_LOGIN_ENDPOINT,  data = payload)
        if res.status_code != requests.codes.ok:
            raise Exception('Login failed please check username or password')
    
        
        credentials = res.json()
        # we only  need this shit, privatetoken usage is still unknown
        token = credentials['token']
        return token
    



if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv(verbose=True)
    moddle = ModdleAPI(os.getenv("E3_USERNAME", ""), os.getenv("E3_PASSWORD", ""))
    print(len(moddle.get_valid_courses()))
    print(moddle.get_course_announcement(moddle.get_valid_courses()[1]))
    # print(moddle.get_undue_assignment())