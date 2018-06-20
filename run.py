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
        if validate_cookies(cookies, config['init_url']):
            print('登录状态已加载')
            esession = EryaSession(cookies)
        else:
            print('Cookies 无效, 重新登陆')
            esession = EryaAuth(username=config['username'], password=config['password'], school_id=config['school_id'])
    else:
        esession = EryaAuth(username=config['username'], password=config['password'], school_id=config['school_id'])
    with open('cookies.json', 'w') as f:
        json.dump(esession.cookies, f)
    params = parse_params(config['init_url'])
    time.sleep(1)
    chapter_list = esession.get_course_chapter_list(params['courseId'], params['clazzid'], params['enc'])
    with open('chapters.json', 'w') as f:
        json.dump(chapter_list, f, indent=2, ensure_ascii=False)
    all_chapter_count = len(chapter_list)
    passed_chapter_count = len([0 for c in chapter_list if c[4]])
    print('共 {} 章, {} 已完成, 剩余 {}'.format(all_chapter_count, passed_chapter_count,
                                         all_chapter_count - passed_chapter_count))
    chapter_list = [c for c in chapter_list if not c[4]]
    for chapter in chapter_list:

        course_id, class_id, chapter_id, name, passed = chapter
        if passed == 1:
            continue
        time.sleep(1)
        print('进入章节 {}: {}'.format(chapter_id, name))
        chapter_tabs = esession.get_chapter_tabs(course_id, class_id, chapter_id)
        time.sleep(1)
        try:
            video_card_index = chapter_tabs.index('视频')
        except ValueError:
            print('未找到视频标签页, 跳过视频播放')
        else:

            card_detail_video = esession.get_card_detail(class_id, course_id, chapter_id, num=video_card_index)
            attachment_data_video = card_detail_video['attachments'][0]
            if attachment_data_video.get('isPassed'):
                print('视频任务点已完成')
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
                timer = Timer(checkpoint_time,
                              lambda: print('视频任务点已完成' if esession.answer_checkpoint(resource_id, answers)['isRight']
                                            else '视频任务点出错'))
                timer.start()
                current_time = 0
                print('视频长度: {} s'.format(duration))
                print('任务点位于 {} s'.format(checkpoint_time))
                while current_time < duration:
                    retry = 3
                    while retry > 0:
                        try:
                            time.sleep(1)
                            esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time,
                                                 chapter_id)

                            break
                        except Exception as e:
                            print(e)
                            retry -= 1
                    if not retry:
                        print('视频观看进度请求出错, 退出...')
                        sys.exit(1)
                    print('视频已播放: {} s'.format(current_time))
                    time.sleep(min(interval, duration - current_time))
                    current_time += interval
                esession.request_log(dtoken, duration, user_id, job_id, object_id, class_id, current_time, chapter_id)
                print('视频播放完成！')
        try:
            read_card_index = chapter_tabs.index('阅读')
        except ValueError:
            pass
        else:
            pass
        if config['do_quiz']:
            # do quiz
            try:
                quiz_card_index = chapter_tabs.index('章节测验')
            except ValueError:
                print('章节测验标签页未找到, 跳过')
            else:
                utenc = esession.get_utenc(chapter_id, course_id, class_id, params['enc'])
                time.sleep(1)
                card_detail_quiz = esession.get_card_detail(class_id, course_id, chapter_id, num=quiz_card_index)
                attachment_data_quiz = card_detail_quiz['attachments'][0]
                work_id = attachment_data_quiz['property']['workid']
                job_id = attachment_data_quiz['jobid']
                enc = attachment_data_quiz['enc']
                time.sleep(1)
                quiz_data, quiz_passed = esession.get_quiz_data(work_id, job_id, chapter_id, class_id, enc, utenc,
                                                                course_id)
                if quiz_passed:
                    print('测验已完成, 跳过')
                else:
                    print('手动完成章节测验并提交后, 按 Enter 以继续')
                    # TODO: parse page
                    input()
                print('章节测验完成')
        else:
            print('跳过章节测验, 请在稍后手动完成')
        time.sleep(2)

    print('全部任务点完成, 退出...')


if __name__ == '__main__':
    main()
