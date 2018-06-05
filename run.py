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
        card_detail_video = esession.get_card_detail(class_id, course_id, chapter_id, num=chapter_tab['video'])
        attachment_data_video = card_detail_video['attachments'][0]
        if attachment_data_video['isPassed']:
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
            resource_id, start_time, answers = esession.get_checkpoint_data(mid)
            # timer = Timer(start_time, esession.answer_checkpoint, [resource_id, answers])
            # timer.start()
            # current_time = 0
            #
            # while current_time < duration:
            #     esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
            #     print('Video at: {} seconds'.format(current_time))
            #     time.sleep(interval)
            #     current_time += interval
            # esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
            # print('Done playing video')
        # do quiz
        utenc = esession.get_utenc(chapter_id, course_id, class_id, params['enc'])
        card_detail_quiz = esession.get_card_detail(class_id, course_id, chapter_id, num=chapter_tab['quiz'])
        attachment_data_quiz = card_detail_quiz['attachments'][0]
        work_id = attachment_data_quiz['property']['workid']
        job_id = attachment_data_quiz['jobid']
        enc = attachment_data_quiz['enc']
        quiz_data = esession.get_quiz_data(work_id, job_id, chapter_id, class_id, enc, utenc, course_id)
        with open('test.html', 'w', encoding='UTF-8') as f:
            f.write(quiz_data)
        exit(0)

if __name__ == '__main__':
    main()
