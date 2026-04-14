from flask import Blueprint, request, redirect, render_template, session
import requests
from ublit import db
wo = Blueprint('wo', __name__)

# 62进制字符表
code = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z']


def encode_base62(num):
    """将数字转为62进制短码"""
    if num == 0:
        return code[0]
    result = []
    while num > 0:
        result.append(code[num % 62])
        num = num // 62
    return ''.join(reversed(result))


@wo.route('/worker', methods=['GET', 'POST'])
def worker():
    # GET请求：显示表单页面
    if request.method == 'GET':
        return render_template('worker.html')

    # POST请求：处理短链接生成
    if request.method == 'POST':
        url = request.form.get('url')

        # 1. 验证URL
        if not url or not url.strip():
            return "请输入URL"

        url = url.strip()

        # 2. 补全协议
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 3. 验证URL是否可访问
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
            }

            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code >= 400:
                return f'生成失败，网址返回错误码：{resp.status_code}'
        except requests.exceptions.Timeout:
            return '连接超时，请稍后重试'
        except requests.exceptions.ConnectionError:
            return '无法连接到该网址'
        except Exception as e:
            return f'检测失败：{str(e)}'

        # 4. 获取当前登录用户
        cookie = session.get('cookie')
        if not cookie:
            return "请先登录"
        username = cookie.get('user') if isinstance(cookie, dict) else cookie

        # 5. 先检查是否已存在相同URL的短链接
        existing = db.fetch_one('SELECT id, short_url FROM ma WHERE true_url = %s', [url])
        if existing:
            # 已存在，直接返回已有的短链接
            return f'该链接已有短链接：{existing["short_url"]}'

        # 6. 插入原始URL，获取自增ID
        db.mysql_caozuo(
            'INSERT INTO ma (true_url, usrname) VALUES (%s, %s)',
            [url, username]
        )

        # 7. 获取刚插入的记录ID
        result = db.fetch_one('SELECT id FROM ma WHERE true_url = %s', [url])
        if not result:
            return "生成失败，请重试"

        record_id = result['id']

        # 8. 生成短码
        short_code = encode_base62(record_id)
        short_url = f'http://127.0.0.1:5000/s/{short_code}'

        # 9. 更新记录的short_url字段
        db.mysql_caozuo(
            'UPDATE ma SET short_url = %s WHERE id = %s',
            [short_url, record_id]
        )

        return f'生成成功！短链接：{short_url}'

