import json
from auth import EryaAuth
from utils.parser import parse_params
import time
from threading import Timer


def main():
    with open('config.json') as f:
        config = json.load(f)
    esession = EryaAuth(username=config['username'], password=config['password'])
    params = parse_params(config['init_url'])
    chapter_list = esession.get_course_chapter_list(params['courseId'], params['clazzid'], params['enc'])
    with open('chapters.json', 'w') as f:
        json.dump(chapter_list, f, indent=2, ensure_ascii=False)
    for chapter in chapter_list:
        course_id, class_id, chapter_id, name, passed = chapter

        if passed == 1:
            continue
        print('Entering chapter {}: {}'.format(chapter_id, name))
        chapter_tab = esession.get_chapter_tabs(course_id, class_id, chapter_id)
        chapter_detail = esession.get_chapter_detail(class_id, course_id, chapter_id, num=chapter_tab['video'])
        attachment_data = chapter_detail['attachments'][0]
        print(attachment_data)
        if attachment_data['isPassed']:
            print('Video already passed')
        else:
            defaults = chapter_detail['defaults']
            user_id = defaults['userid']
            job_id = attachment_data['jobid']
            object_id = attachment_data['property']['objectid']
            interval = defaults['reportTimeInterval']
            school_id = defaults['fid']
            mid = attachment_data['property']['mid']
            ananas_data = esession.get_ananas_data(object_id, school_id)
            duration = ananas_data['duration']
            dtoken = ananas_data['dtoken']
            checkpoint_data = esession.get_checkpoint_data(mid)

            current_time = 0

            while current_time < duration:
                esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
                print('Video at: {} seconds'.format(current_time))
                time.sleep(interval)
                current_time += interval
            esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
            print('Done playing video')
            # def request_log(self, duration: int, user_id: int, job_id: int, object_id: str, class_id: int,
            #               playing_time: int,                        chapter_id: int):


if __name__ == '__main__':
    main()
