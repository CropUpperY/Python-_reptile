import os
import re
import time
import requests
from lxml import etree

# 规范化url
def url_standard(url):
    html_data = get_url_HTML(url)    # 通过get_url_HTML()函数获取html文档对象
    url_ = html_data.xpath('/html/head/meta[14]/@content')[0]    # 获取第14个mete中属性‘content’的内容
    # 处理后url格式为https://www.bilibili.com/video/ + BV号 + /
    return url_

# 返回B站目标页面的HTML文档对象
def get_url_HTML(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"  # 防盗链,用来标识这个请求是从哪个页面发过来的
    }
    response = requests.get(url, headers=headers)
    html_data = etree.HTML(response.text)   # 将传进去的字符串转变成_Element对象，方便使用getparent()、remove()、xpath()等方法
    return html_data

# 求出资源个数
def get_music_num(html_data):
    #1. 找到显示最后一P的位置，此时num_为字符串  num_ = 'part/total' total为我们需要的数据
    num_ = html_data.xpath('//*[@id="multi_page"]/div[1]/div[1]/span/text()')[0]    # // ———— 访问子孙节点
    #2. 使用正则表达式并将num_强转为int型
    num = int(re.findall('\(\d+/(.*?)\)', num_)[0])
    print(f"查询到共有{num}个资源")
    return num
# 将合集中的歌曲遍历并下载
def get_all_music(url, num):    # 传入经过url_standard()函数处理过的url 和 经过get_music_num()函数得到的num
    # dir_name = "周杰伦"
    dir_name = input('请输入歌手名字(作为文件夹名称):')   # 命名文件夹存放资源
    if not os.path.exists(dir_name):    # 判断文件夹是否存在
        os.mkdir(dir_name)  # 如果不存在则创建该文件夹
    for i in range(num):    # 遍历合集网站 i从0到num-1
        url_p = url+ '?p=' +str(i+1)    # 在传入的url后加上 ‘?p=’ 和 i+1 得到每一P完整的url，注意i为int，需要转为str
        html_data = get_url_HTML(url_p)     # 通过get_url_HTML()函数得到当前页面的HTML文档对象
        get_music(html_data, i, dir_name)   # 调用get_music()函数完成资源下载
        time.sleep(4)     # 设置间隔时间.防止被ban ip（不清楚B站会不会Ban）
    print('任务已完成，欢迎下次使用！')  # 循环结束说明主程序运行完毕

# 获取和下载资源
def get_music(html_data, num, dir_name):    # num 和 dir_name用来进行程序运行状态
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"  # 防盗链,用来标识这个请求是从哪个页面发过来的
    }
    title_ = html_data.xpath('/html/head/title/text()')[0]  # 获取此P的标题，（一般包括歌曲名称） text()的作用:获取文本内容
    print(title_)

    title = re.findall(r'\d+. (.*?)_哔哩哔哩', title_)[0]   # 使用正则得到歌曲名称 注意findall()得到的是列表，选取第一个元素得到str
    print(f'正在下载第{num + 1}首歌:{title}')  # 展示当前下载资源数目以及名称

    # 通过在网页原码中搜索Audio找到视频URL链接
    url_str = html_data.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    # 使用正则得到音频的url 正则注意细节————r、()中为匹配的内容，前面的负责定位！
    music_str = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]
    music_data = requests.get(music_str, headers=headers)   # 获取音频的HTML文档对象
    music = music_data.content      # .content方法将HTML文档对象转化为二进制  音频以二进制保存，
    with open(f'./{dir_name}/{title}--{dir_name}.mp3', 'wb') as f:  # 设置保存路径以及文件名称,
        f.write(music)      # 保存数据

# 主程序
if __name__ == "__main__":
    # url = 'https://www.bilibili.com/video/BV1UG4y1N7YK/?p=18&spm_id_from=pageDriver&vd_source=5c907d53d53b2f3ddc6b936af10ff60d'
    url_ori = input('请输入网址(仅限B站):')     # 输入网址
    url = url_standard(url_ori)     # 规范化url
    print(url)      # 打印查看
    html_data = get_url_HTML(url)   # 获取规范后url的HTML文档对象
    num = get_music_num(html_data)  # 统计资源数量
    get_all_music(url, num)         # 下载保存资源
