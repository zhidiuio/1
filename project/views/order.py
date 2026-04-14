from flask import Blueprint, request, redirect, render_template, session
from ublit import db

od=Blueprint('od',__name__)
@od.route('/s/<string:short_url>')
def order(short_url):
    short_url = 'http://127.0.0.1:5000/s/'+short_url
    url=db.fetch_one('SELECT true_url FROM ma WHERE short_url = %s',[short_url])
    print('url',url)
    if url:
        return redirect(url['true_url'])
    else:
        return '短码不存在'