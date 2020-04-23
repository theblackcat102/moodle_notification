from const import *
from requests import get, post
import requests
'''
Function copied from https://github.com/mrcinv/moodle_api.py/blob/master/moodle_api.py
Give @mrcinv a huge shout out
'''

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(token, fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": token, 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = requests.post(SERVER_API_ENDPOINT, parameters)
    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response


if __name__ == "__main__":
    print(rest_api_parameters({
        'userid': 000
    }))