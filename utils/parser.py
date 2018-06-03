from bs4 import BeautifulSoup
import json
import re
from urllib.parse import unquote, parse_qsl, urlsplit

CHAPTER_PATTERN = re.compile(
    '/moocAnalysis/nodeStatisticByUser\?'
    'flag=1'
    '&courseId=(\d+)'
    '&classId=(\d+)'
    '&chapterId=(\d+)'
    '&chapterName=(.+)'
    '&totalStudent=0'
    '&compeletionNum=0'
)
VIDEO_DATA_PATTERN = re.compile('mArg = ({.+});')
__all__ = ['parse_chapter_tabs', 'parse_params', 'parse_chapter_detail', 'parse_chapter_list', 'parse_checkpoint_data']


def parse_params(url):
    return dict(parse_qsl(urlsplit(url).query))


def parse_chapter_list(response_text):
    matches = CHAPTER_PATTERN.findall(response_text)
    soup = BeautifulSoup(response_text, 'html5lib')
    status_list = [1 if em.get('class') and 'openlock' in em.get('class') else 0 for em in soup.find_all('em')]

    return [(course_id, class_id, chapter_id, unquote(chapter_name), status)
            for (course_id, class_id, chapter_id, chapter_name), status
            in zip(matches, status_list)]


def parse_chapter_tabs(response_text):
    soup = BeautifulSoup(response_text, 'html5lib')

    ret = {
        'video': -1,
        'quiz': -1
    }
    for i, span in enumerate(soup.find_all('span')):
        if span['title'] == '视频':
            ret['video'] = i
        elif span['title'] == '章节测验':
            ret['quiz'] = i
    return ret


def parse_chapter_detail(response_text):
    match = VIDEO_DATA_PATTERN.search(response_text)
    return json.loads(match.group(1))


def parse_checkpoint_data(data: dict):
    question_data = data[0]['datas'][0]
    answers = list()
    for option in question_data['options']:
        if option['isRight']:
            answers.append(option['name'])
    return question_data['resourceId'], question_data['startTime'], answers
