import requests
import time
from utils import get_enc, parse_course_id_list
from bs4 import BeautifulSoup


class EryaSession:
    def __init__(self, cookies: dict):
        self.session: requests.session = requests.session()
        for _k, _v in cookies.items():
            self.session.cookies.set(name=_k, value=_v)

    def get_course_chapter_id_list(self, course_id, class_id, enc):
        data = {
            'courseId': course_id,
            'clazzid': class_id,
            'enc': enc
        }
        response = self.session.get('https://mooc1-1.chaoxing.com/mycourse/studentcourse', params=data)
        chapter_id_list = parse_course_id_list(response)
        return chapter_id_list

    def get_video(self):
        pass

    def request_log(self, duration: int, user_id: int, job_id: int, object_id: str, class_id: int, playing_time: int):
        data = {
            'dtype': 'Video',
            'duration': duration,
            'userid': user_id,
            'rt': '0.9',
            'jobid': job_id,
            'objectId': object_id,
            'clipTime': '0_%d' % duration,
            'otherInfo': '',
            'clazzId': class_id,
            'view': 'pc',
            'playingTime': playing_time,
            'isdrag': '3',
            'enc': get_enc(class_id, user_id, job_id, object_id, playing_time, duration)
        }
        url = ''

        self.session.post(url, data=data)

    def request_checkpoint(self, mid):
        url = 'https://mooc1-1.chaoxing.com/richvideo/initdatawithviewer?&start=undefined&mid={mid}'.format(mid=mid)
        return self.session.get(url).json()

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
        self.session.get('https://passport2.chaoxing.com/api/monitor', data=data)
