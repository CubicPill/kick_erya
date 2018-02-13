import requests
import time


class EryaSession:
    def __init__(self, cookies: dict):
        self.session: requests.session = requests.session()
        for _k, _v in cookies.items():
            self.session.cookies.set(name=_k, value=_v)

    def get_course_list(self):
        pass

    def get_course_checkpoint_list(self):
        pass

    def request_log(self, duration: int, user_id: int, job_id: int, object_id: str):
        data = {
            'dtype': 'Video',
            'duration': duration,
            'userid': user_id,
            'rt': '0.9',
            'jobid': job_id,
            'objectId': object_id
        }

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
