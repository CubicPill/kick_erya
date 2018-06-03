import requests
import time
from utils import get_enc, HEADERS
from utils.parser import *
from bs4 import BeautifulSoup

ERYA_V = '20160407'


class EryaSession:
    def __init__(self, cookies: dict):
        self.session = requests.session()
        for _k, _v in cookies.items():
            self.session.cookies.set(name=_k, value=_v)
        self.session.headers.update(HEADERS)

    def get_course_chapter_list(self, course_id, class_id, enc):
        """
        You need a valid combination of course_id, class_id, enc to get chapter list

        :param course_id:
        :param class_id:
        :param enc:
        :return:list[course_id, class_id, chapter_id, chapter_name]
        """
        data = {
            'courseId': course_id,
            'clazzid': class_id,
            'enc': enc
        }
        response = self.session.get('http://mooc1-1.chaoxing.com/mycourse/studentcourse', params=data, headers=HEADERS)
        chapter_list = parse_chapter_list(response.text)
        return chapter_list

    def get_chapter_tabs(self, course_id, class_id, chapter_id):
        data = {
            'courseId': course_id,
            'clazzid': class_id,
            'chapterId': chapter_id
        }
        response = self.session.post('http://mooc1-1.chaoxing.com/mycourse/studentstudyAjax', data=data,
                                     headers=HEADERS)
        return parse_chapter_tabs(response.text)

    def get_chapter_detail(self, class_id, course_id, chapter_id, num=0, v=ERYA_V):
        url = 'http://mooc1-1.chaoxing.com/knowledge/cards'
        params = {
            'clazzid': class_id,
            'courseid': course_id,
            'knowledgeid': chapter_id,
            'num': num,
            'v': ERYA_V + '-1'  # currently is '20160407-1'
        }
        response = self.session.get(url, params=params, headers=HEADERS)
        return parse_chapter_detail(response.text)

    def get_ananas_data(self, object_id, school_id):
        url = 'http://mooc1-1.chaoxing.com/ananas/status/{}'.format(object_id)
        params = {
            'k': school_id,
            '_dc': int(time.time() * 1000)
        }
        return self.session.get(url, params=params, headers=HEADERS).json()

    def get_checkpoint_data(self, mid):
        url = 'http://mooc1-1.chaoxing.com/richvideo/initdatawithviewer?&start=undefined&mid={mid}'.format(
            mid=mid)
        return parse_checkpoint_data(self.session.get(url, headers=HEADERS).json())

    def request_log(self, dtoken, duration, user_id, job_id, object_id, class_id, playing_time, chapter_id):
        duration, user_id, job_id, class_id, playing_time, chapter_id = \
            list(map(int, [duration, user_id, job_id, class_id, playing_time, chapter_id]))
        params = {
            'dtype': 'Video',
            'duration': duration,
            'userid': user_id,
            'rt': '0.9',
            'jobid': job_id,
            'objectId': object_id,
            'clipTime': '0_%d' % duration,
            'otherInfo': 'nodeId_{}'.format(chapter_id),
            'clazzId': class_id,
            'view': 'pc',
            'playingTime': playing_time,
            'isdrag': '3',
            'enc': get_enc(class_id, user_id, job_id, object_id, playing_time, duration)
        }
        url = 'http://mooc1-1.chaoxing.com/multimedia/log/{}'.format(dtoken)

        return self.session.get(url, params=params, headers=HEADERS).json()

    def answer_checkpoint(self, resource_id, answers: list):
        resource_id = int(resource_id)
        url = 'https://mooc1-1.chaoxing.com/richvideo/qv'
        params = {
            'resourceid': resource_id,
            'answer': "'" + ''.join(answers) + "'"
        }
        # {"resourceId":655244,"isRight":true,"answer":"A"}
        return self.session.get(url, params=params, headers=HEADERS).json()

    def request_monitor(self, version: str, jsoncallback: str, referer='http://i.mooc.chaoxing.com',
                        t: int = int(time.time())):
        """
        the periodic request to detect multi client login

        :param version:
        :param jsoncallback:
        :param referer:
        :param t:
        :return:
        """

        data = {
            'version': version,
            'jsoncallback': jsoncallback,
            'referer': referer,
            't': t
        }
        self.session.get('http://passport2.chaoxing.com/api/monitor', data=data)
