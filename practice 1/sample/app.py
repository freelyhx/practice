# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:07:19

import sqlite3
import json
import time
import os

import tornado.web
import tornado.httpserver
import tornado.ioloop


def create_conn():

    conn = sqlite3.connect(os.path.dirname(__file__) + '\\count.db')
    cur = conn.cursor()
    try:
        cur.execute('create table user_id(uid PRIMARY KEY, ip_addr VARCHAR(60),count INTEGER)')
        conn.commit()
        return conn, cur
    except sqlite3.OperationalError, x:
        if x.message == 'table user_id already exists':
            return conn, cur
        else:
            raise sqlite3.OperationalError(x.message)


def query_user_id(uid):
    conn, cur = create_conn()
    print uid
    res = cur.execute("select * from user_id where uid='{uid}'".format(uid=uid)).fetchall()
    cur.close()
    conn.close()
    if res:
        return True
    else:
        return False


def edit_user_count(uid):
    conn, cur = create_conn()
    res = cur.execute("select count from user_id where uid='{uid}'".format(uid=uid)).fetchall()
    print res
    cur.execute("update user_id set count={count} where uid='{uid}'".format(uid=uid, count=res[0][0] + 1))
    conn.commit()
    cur.close()
    conn.close()


def create_user_count(uid, ip):
    conn, cur = create_conn()
    cur.execute("insert into user_id VALUES ('{uid}', '{ip}', {count})".format(uid=uid, ip=ip, count=1))
    conn.commit()
    cur.close()
    conn.close()

def find_all():
    conn, cur = create_conn()
    res = cur.execute("select uid, ip_addr, count from user_id").fetchall()
    res_dict = {}
    for i in res:
        res_dict[i[0]] = [i[1], i[2]]
    cur.close()
    conn.close()
    return res_dict


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class CountHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            self.user_id = self.get_argument('user_id')
            if self.user_id == 'undefined' or self.user_id == '':
                self.user_id = None
            elif not query_user_id(self.user_id):
                self.write(json.dumps({'success':False, 'result':''}))
        except tornado.web.MissingArgumentError:
            self.user_id = None


        if self.user_id is None or self.user_id =='':
            new_user_id = 'test' + str(time.time()).replace('.', '')
            ip = self.request.remote_ip
            create_user_count(new_user_id, ip)
            self.write(json.dumps({'success': True, 'result': new_user_id}))
        else:
            edit_user_count(self.user_id)
            self.write(json.dumps({'success':True, 'result':''}))

class DataGridHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(json.dumps(
            {
                'success': True,
                'result': find_all()
            }
        ))

if __name__ == '__main__':
    app = tornado.web.Application(
        handlers=[
            (r'/',IndexHandler ),
            (r'/count', CountHandler),
            (r'/datagrid', DataGridHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    tornado.ioloop.IOLoop.instance().start()

