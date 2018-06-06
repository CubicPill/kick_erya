import json
from auth import EryaAuth, validate_cookies
from utils.parser import parse_params
import time
from threading import Timer
import os
from erya import EryaSession
import sys

def main():
    with open('config.json') as f:
        config = json.load(f)
    if os.path.isfile('cookies.json'):
        with open('cookies.json') as f:
            cookies = json.load(f)
        if validate_cookies(cookies):
            esession = EryaSession(cookies)
        else:
            print('Cookies invalid')
            esession = EryaAuth(username=config['username'], password=config['password'])
    else:
        esession = EryaAuth(username=config['username'], password=config['password'])
    with open('cookies.json', 'w') as f:
        json.dump(esession.cookies, f)
    params = parse_params(config['init_url'])
    time.sleep(1)
    chapter_list = esession.get_course_chapter_list(params['courseId'], params['clazzid'], params['enc'])
    with open('chapters.json', 'w') as f:
        json.dump(chapter_list, f, indent=2, ensure_ascii=False)
    for chapter in chapter_list:
        time.sleep(1)
        course_id, class_id, chapter_id, name, passed = chapter
        if passed == 1:
            continue
        print('Entering chapter {}: {}'.format(chapter_id, name))
        chapter_tab = esession.get_chapter_tabs(course_id, class_id, chapter_id)
        time.sleep(1)
        card_detail_video = esession.get_card_detail(class_id, course_id, chapter_id, num=chapter_tab['video'])
        attachment_data_video = card_detail_video['attachments'][0]
        if attachment_data_video.get('isPassed'):
            print('Video already passed')
        else:
            defaults = card_detail_video['defaults']
            user_id = defaults['userid']
            job_id = attachment_data_video['jobid']
            object_id = attachment_data_video['property']['objectid']
            interval = defaults['reportTimeInterval']
            school_id = defaults['fid']
            mid = attachment_data_video['property']['mid']
            ananas_data = esession.get_ananas_data(object_id, school_id)
            duration = ananas_data['duration']
            dtoken = ananas_data['dtoken']
            resource_id, checkpoint_time, answers = esession.get_checkpoint_data(mid)
            time.sleep(1)
            timer = Timer(checkpoint_time, lambda: print('Checkpoint answered'
                                                         if esession.answer_checkpoint(resource_id, answers)['isRight']
                                                         else 'Error handling checkpoint'))
            timer.start()
            current_time = 0
            print('Video length: {} seconds'.format(duration))

            while current_time < duration:
                retry = 3
                while retry:
                    try:
                        time.sleep(1)
                        esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time,
                                             chapter_id)
                    except Exception as e:
                        raise e
                        retry -= 1
                if not retry:
                    print('Critical error when requesting log')
                    sys.exit(1)
                print('Video at: {} seconds'.format(current_time))
                time.sleep(interval)
                current_time += interval
            esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
            print('Done playing video')
        # do quiz
        time.sleep(2)
        utenc = esession.get_utenc(chapter_id, course_id, class_id, params['enc'])
        time.sleep(1)
        card_detail_quiz = esession.get_card_detail(class_id, course_id, chapter_id, num=chapter_tab['quiz'])
        attachment_data_quiz = card_detail_quiz['attachments'][0]
        work_id = attachment_data_quiz['property']['workid']
        job_id = attachment_data_quiz['jobid']
        enc = attachment_data_quiz['enc']
        time.sleep(1)
        quiz_data = esession.get_quiz_data(work_id, job_id, chapter_id, class_id, enc, utenc, course_id)
        with open('test.txt', 'w', encoding='UTF-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        print('Quiz done')



if __name__ == '__main__':
    main()
