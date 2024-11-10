import requests
import json

def scrape_data(url, data):
    """
    发送POST请求以抓取指定URL的页面数据。

    参数:
    url (str): 目标URL。
    xiaoqu (str): 小区名称，用作请求的关键字。
    page (int): 页码，用于请求的分页。

    返回:
    str: 如果请求成功，返回响应的文本内容。
    None: 如果请求失败，返回None。
    """
    # data = {
    #     "keywords": xiaoqu,
    #     "page": page,
    #     "xqid": 0
    # }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # 检查请求是否成功
        ret = response.json().get("list")
        return json.dumps(ret, ensure_ascii=False, indent=4)
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

if __name__ == '__main__':

    # 示例POST请求
    post_url = 'https://zwfw.fgj.hangzhou.gov.cn/jjhygl/webty/WebFyAction_getGpxxSelectList.jspx'  # 替换为你要访问的API链接
    data = {
        "keywords": "万家星城",
        "page": 1,
        "xqid": 0
    }
    response_data = scrape_data(post_url, data)
    print(response_data) 