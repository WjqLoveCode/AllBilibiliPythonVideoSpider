import requests
import re
from requests.exceptions import RequestException
import json
import time


def get_one_page(url):
    try:
        headers = {
            "Cookie": "bsource=search_baidu; _uuid=CB4DBC52-ED1A-C11B-D930-9C7D5D5F0B5221210infoc; buvid3=6CFCDF81-E680-4DEB-AEA7-9853EE7B127B167643infoc; b_nut=1627799022; fingerprint=7c6d601e79096fba9244aca00c7e4b4a; buvid_fp=6CFCDF81-E680-4DEB-AEA7-9853EE7B127B167643infoc; buvid_fp_plain=6CFCDF81-E680-4DEB-AEA7-9853EE7B127B167643infoc; sid=ae7m9xlv; fingerprint=15d4ecbb6b8f9714ca92d013bf7456fa; buvid_fp=6CFCDF81-E680-4DEB-AEA7-9853EE7B127B167643infoc; buvid_fp_plain=6CFCDF81-E680-4DEB-AEA7-9853EE7B127B167643infoc; SESSDATA=db53ed39%2C1643351052%2C97b07%2A81; bili_jct=8189de7846f459b0b56db0a7686f493d; DedeUserID=1677337799; DedeUserID__ckMd5=b006526b6425309b",
            "Host": "search.bilibili.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        }
        response = requests.get(
            url=url,
            headers=headers,
        )
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<li class="video-item matrix">.*?href="(.*?)".*?title="(.*?)".*?img-anchor.*?lazy-img"><img.*?src="(.*?)"></div><span.*?so-imgTag_rb">(.*?)</span>.*?icon-playtime"></i>(.*?)</span>.*?icon-date"></i>(.*?)</span>.*?up-name.*?>(.*?)</a>.*?</li>',
        re.S,
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "videa": item[0],
            "name": item[1],
            "img": item[2],
            "time": item[3],
            "watch_num": item[4].strip(),
            "data": item[5].strip(),
            "up_name": item[6],
        }


def write_to_file(content):
    with open("pyvideo", "a", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def main(offset):
    url = (
        "https://search.bilibili.com/all?keyword=python&from_source=webtop_search&spm_id_from=333.851"
        + offset
    )
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == "__main__":
    for i in range(1, 10):
        if i == 1:
            main("")
            time.sleep(1)
        else:
            main("&page=" + str(i))
            time.sleep(1)
