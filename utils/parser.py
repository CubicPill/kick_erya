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
CARD_DATA_PATTERN = re.compile('mArg = ({.+});')
UTENC_PATTERN = re.compile('var utEnc="([0-9a-z]+)";')
__all__ = ['parse_chapter_tabs', 'parse_params', 'parse_chapter_detail', 'parse_chapter_list', 'parse_checkpoint_data',
           'parse_quiz_data']


def parse_params(url):
    return dict(parse_qsl(urlsplit(url).query))


def parse_utenc(response_text):
    match = UTENC_PATTERN.search(response_text)
    return match.group(1)


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
    try:
        assert -1 not in list(ret.values())
    except AssertionError as e:
        print(response_text)
        raise e
    return ret


def parse_chapter_detail(response_text):
    match = CARD_DATA_PATTERN.search(response_text)
    if not match:
        print(response_text)
    return json.loads(match.group(1))


def parse_checkpoint_data(data: dict):
    question_data = data[0]['datas'][0]
    answers = list()
    for option in question_data['options']:
        if option['isRight']:
            answers.append(option['name'])
    return question_data['resourceId'], question_data['startTime'], answers


def parse_quiz_data(response_text):
    soup = BeautifulSoup(response_text, 'html5lib')
    all_questions = list()
    while True:
        div_timu = soup.find('div', {'class': 'TiMu'})
        if not div_timu:
            break

        all_questions.append(extract_question(div_timu))

        soup = div_timu

    return all_questions


def extract_question(div_TiMu):
    text_div, choices_div = div_TiMu.find_all('div', {'class': 'clearfix'})[1:3]
    question_text = text_div.text
    choices_item = choices_div.find_all('li')
    question_id = choices_item[0].input['name']
    choice_values = [c.input['value'] for c in choices_item]
    print(choice_values)
    try:
        choice_text = [c.a.text for c in choices_item]
    except AttributeError:
        choice_text = [''] * len(choice_values)
    return {
        'text': question_text,
        'id': question_id,
        'choices': list(zip(choice_values, choice_text))
    }
