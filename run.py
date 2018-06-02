import json
from auth import EryaAuth
from utils.parser import parse_params


def main():
    with open('config.json') as f:
        config = json.load(f)
    esession = EryaAuth(username=config['username'], password=config['password'])
    params = parse_params(config['init_url'])
    chapter_list = esession.get_course_chapter_list(params['courseId'], params['clazzid'], params['enc'])
    course_id, class_id, chapter_id,_,_ = chapter_list[0]
    video_data = esession.get_video_data(class_id, course_id, chapter_id)
    print(json.dumps(video_data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
