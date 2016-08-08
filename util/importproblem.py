# encoding:UTF-8
import requests
import re
import urllib.request


# 杭电oj编码方式为gb2312，需要用urllib读取后解码  需要用gbk解码 坑啊
def get_hdu_info(problem_id):
    base_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='
    url = base_url + str(problem_id)

    html = requests.get(url).text

    if 'No such problem' in html:
        return str(problem_id)+' : No such problem'
    if 'System Message' in html:
        return str(problem_id)+' : System error'

    response = urllib.request.urlopen(url)
    html = response.read().decode('gbk')

    reg_title = "<h1 style='color:#1A5CC8'>(.*?)</h1>"
    title = re.findall(reg_title, html, re.S)[0]

    reg_time_limit = "Time Limit:(.*?)&nbsp;"
    time_limit = re.findall(reg_time_limit, html, re.S)[0]

    reg_memory_limit = "Memory Limit:(.*?)<br>"
    memory_limit = re.findall(reg_memory_limit, html, re.S)[0]

    # 0 1 2 3 4分别是描述，输入，输出,样例输入，样例输出
    description = {}
    # if len(description) <= 4:# 因为某些题目缺少某些区域,所以只能一个个爬取判断
    # print(str(ProblemID)+" "+str(len(description)))
    reg = "Problem Description</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[0] = tmp[0] if tmp else "无"

    reg = "Input</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[1] = tmp[0] if tmp else "无"

    reg = "Output</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[2] = tmp[0] if tmp else "无"

    reg = "Sample Input</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[3] = tmp[0] if tmp else "无"

    reg = "Sample Output</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[4] = tmp[0] if tmp else "无"

    base_img_url = 'http://acm.hdu.edu.cn/'
    for i in range(0, 5):
        if 'src=' in description[i]:
            if "../../" in description[i]:
                description[i] = description[i].replace("../../data/images/", base_img_url + "data/images/")
            else:
                description[i] = description[i].replace("/data/images/", base_img_url + "data/images/")
    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description[0], 'input_description': description[1],
            'output_description': description[2], 'input': description[3], 'output': description[4]}


def get_poj_info(problem_id):
    base_url = 'http://poj.org/problem?id='
    url = base_url + str(problem_id)
    html = requests.get(url).text

    if 'Can not find problem' in html:
        return str(problem_id) + ' : Can not find problem'
    if 'Error Occurred' in html:
        return str(problem_id) + ' : Error Occurred'

    reg_title = '<div class="ptt" lang="en-US">(.*?)</div>'
    title = re.findall(reg_title, html, re.S)[0]

    reg_time_limit = "Time Limit:</b> (.*?)</td>"
    time_limit = re.findall(reg_time_limit, html, re.S)[0]

    reg_memory_limit = "Memory Limit:</b> (.*?)</td>"
    memory_limit = re.findall(reg_memory_limit, html, re.S)[0]

    # 0 1 2 分别是描述，输入描述，输出描述
    reg_description = '<div class="ptx" lang="en-US">(.*?)</div><p class="pst">'
    description = re.findall(reg_description, html, re.S)

    # 0 1 分别是输入，输出
    reg_in_out = '<pre class="sio">(.*?)</pre><p class="pst">'
    in_out = re.findall(reg_in_out, html, re.S)

    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description[0], 'input_description': description[1],
            'output_description': description[2], 'input': in_out[0], 'output': in_out[1]}