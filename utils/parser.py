from bs4 import BeautifulSoup
import json
import re

PET = re.compile(
    '/moocAnalysis/nodeStatisticByUser?flag=1&courseId=(\d+)&classId=(\d+)&chapterId=(\d+)&chapterName=(.+)&totalStudent=0&compeletionNum=0')


def parse_course_id_list(response_text):
    pass


def parse_checkpoint_info(data: dict):
    pass
