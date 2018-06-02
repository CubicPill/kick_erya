import json
from auth import EryaAuth
from utils.parser import parse_params


def main():
    with open('config.json') as f:
        config = json.load(f)
    esession = EryaAuth(username=config['username'], password=config['password'])
    params = parse_params(config['init_url'])
    chapter_list = esession.get_course_chapter_list(params['courseId'], params['clazzid'], params['enc'])
    with open('chapters.json', 'w') as f:
        json.dump(chapter_list, f, indent=2, ensure_ascii=False)

    course_id, class_id, chapter_id, _, _ = chapter_list[10]
    chapter_data = esession.get_chapter_data(course_id, class_id, chapter_id)
    video_data = esession.get_video_data(class_id, course_id, chapter_id, num=chapter_data['video'])


if __name__ == '__main__':
    main()
