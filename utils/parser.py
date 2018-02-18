from bs4 import BeautifulSoup


def parse_course_id_list(response):
    soup = BeautifulSoup(response.content, 'html5lib')
    chapter_urls = soup.select('div.leveltwo > h3 > span > a')
    chapter_id_list = list()
    for a in chapter_urls:
        chapter_id_list.append(a.href)
    return chapter_id_list
