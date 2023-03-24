import os.path
import time
import requests


# 获取页面的json信息
def get_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }  # 伪装成浏览器
    '''
    构造一个向服务器请求资源的Request对象(Request),并且get方法返回一个包含服务器资源的Response对象
        requests.get() 返回值类型为 <class 'requests.models.Response'>
        r_j 返回值:<Response[200]>
        r_j.text 输出文本信息
        r_j.content 以二进制输出
    '''
    r_j = requests.get(url, headers=headers)  # 获取页面信息
    return r_j.json()  # 以json的形式返回


# 获取英雄的名称和原画的url,并存储在字典中
def get_hero_url_img_dist(json):
    hero_list = {}  # 定义一个空的字典用来保存数据
    for i in range(len(json['champions'])):  # 遍历json中'champions'对应的值
        name = json['champions'][i]['name']  # 获取对应的name
        uri = json['champions'][i]['image']['uri']  # 获取对应的uri
        # print(uri)    # 打印uri进行测试
        hero_list[name] = uri  # 将信息以键值对的方式存入字典中
    return hero_list    # 返回字典


# 创建文件夹并保存英雄原画到指定文件夹,文件命名为英雄名字，格式为jpg
def save_hero_img(dist):
    # 创建文件夹
    dir_name = "heroImg"    # 命名文件夹的名称
    if not os.path.exists(dir_name):  # os模块判断并创建
        os.mkdir(dir_name)  # 创建文件夹
    num = 0     # 设置一个计数变量
    for name, uri in dist.items():  # 遍历字典中的键值对分别用name、uri接收
        print(name)     # 打印name观察
        print(uri)  # 打印uri观察
        response = requests.get(uri)    # 从服务器返回uri对应的资源
        with open(f'./heroImg/{name}.jpg', 'wb') as f:  # 设置保存方式及文件名称
            f.write(response.content)   # 将http响应内容以二进制形式保存  视频、音频、图片皆用二进制保存
        num += 1    # 计数器加1
        print(f"已完成{num}/161")  # 打印完成情况
        time.sleep(4)  # 设置间隔时间，防止把网页爬崩


# 主程序
if __name__ == "__main__":
    # 1. 获取包含所有英雄信息的json
    url = "https://yz.lol.qq.com/v1/zh_cn/search/index.json"
    all_hero_json = get_json(url)
    # 2. 将所有英雄的名称及对应url添加在字典中，方便后续保存
    all_hero_img_dist = get_hero_url_img_dist(all_hero_json)
    print(all_hero_img_dist)
    # 3. 保存英雄原图
    save_hero_img(all_hero_img_dist)
