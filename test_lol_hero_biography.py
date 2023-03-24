import re  # 正则表达式
import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
    定义一个获取json数据的方法
"""


def get_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }
    r_j = requests.get(url, headers=headers)
    return r_j.json()


"""
    获取所有英雄链接的方法
    观察可知 英雄背景故事的url格式为 ’https://yz.lol.qq.com/v1/zh_cn/champions/‘ + 英雄英文名称 +‘/index.json’
        json中数据存储的方式为 字典， 英雄的英文名称均存储在key为"champions"的value中，其value为列表
        英雄英文名称获取方式为 json['champions'][i]['slug']  i为变量，每次+1 负责遍历“champions”的value
    hero_list为列表,保存所有英雄背景故事存放的url
"""


def get_hero_url_list(json):
    hero_list = []
    for i in range(len(json['champions'])):
        hero_list.append("https://yz.lol.qq.com/v1/zh_cn/champions/{}/index.json".format(json['champions'][i]['slug']))
    return hero_list


def get_hero_info(json):
    ## 英雄的名字 -- 辛德拉
    name = json['champion']['name']
    ## 英雄的别称 -- 暗黑元首
    other_name = json['champion']['title']
    ## 上线时间
    release_date = json['champion']['release-date']
    ## 英雄背景故事
    hero_biography = re.sub('<p>|<\\/p>', '\n    ', re.sub('<em>|<\\/em>', '', json['champion']['biography']['full']))
    ## 英雄定位
    roles = []
    for r in range(len(json['champion']['roles'])):
        roles.append(json['champion']['roles'][r]['name'])
    roles = '/'.join(roles)
    data = {
        'name': name,
        'other_name': other_name,
        'release_date': release_date,
        'roles': roles,
        'hero_biography': hero_biography
    }
    return data


def save_hero_info(lis):
    num = 1
    hero_url_lis = lis
    for i in range(len(hero_url_lis)):
        hero_biography_json = get_json(hero_url_lis[i])
        hero_data = get_hero_info(hero_biography_json)
        # print(hero_url_list[i][41:-11])
        hero_name = hero_data['name']
        hero_other_name = hero_data['other_name']
        hero_release_date = hero_data['release_date']
        hero_roles = hero_data['roles']
        hero_biography = hero_data['hero_biography']

        with open(f'./hero/{hero_name}.txt', 'w', encoding='utf-8') as f:
            f.write("\t\t\t\t\t\t\t\t" + hero_name + '\t' + hero_other_name + '\n' +
                    '\t\t\t\t\t\t\t\t\t\t上线时间:' + hero_release_date[:-14] + '\t' +
                    '定位:' + hero_roles)

        with open(f'./hero/{hero_name}.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + hero_biography)
        print(f'已完成{num}/161')
        num += 1


if __name__ == '__main__':
    ## 1. 获得存放英雄名称的json
    url = 'https://yz.lol.qq.com/v1/zh_cn/search/index.json'
    all_hero_json = get_json(url)
    # print(all_hero_json)

    ## 2. 获得英雄背景故事的url
    hero_url_list = get_hero_url_list(all_hero_json)
    # print(hero_url_list)

    # 3. 保存heros` data
    save_hero_info(hero_url_list)
    print('程序运行完毕')

    # num = 1
    # data = pd.DataFrame(columns=['name', 'other_name', 'release_date', 'roles', 'hero_biography'])
    # for i in range(len(hero_url_list)):
    #     hero_json = get_json(hero_url_list[i])
    #     hero_data = get_hero_info(hero_json)
    #     data = pd.concat([data, hero_data])
    #     print(f'已完成{num}/161')
    #     num +=1
    #
    # data.to_json('./LOL.json', orient='records', forcle_ascii=False)
