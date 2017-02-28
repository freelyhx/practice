#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sqlite3

import json
import tornado.ioloop
import tornado.web
import tornado.httpserver

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        #self.write("This is new!")


class DealHandler(tornado.web.RequestHandler):
    def get(self):
        self.myName = self.get_argument('myName',default='vion')


        self.myId = self.get_argument('myId')

        if self.myId == 'undefined' or self.myId == '':
            self.myId = self.request.remote_ip


        conn = sqlite3.connect('click.db')
        cursor = conn.cursor()
        try:
            cursor.execute("create table counter(id varchar(60) PRIMARY KEY, count INTEGER)")
            cursor.close()
            conn.close()
        except sqlite3.OperationalError, x:
            print x.message
            if x.message == 'table counter already exists':
                print cursor.execute("select * from counter where id = '%s'" % self.myId).fetchall()
                if cursor.execute("select * from counter where id = '%s'" % self.myId).fetchall():
                    num = cursor.execute("select count from counter where id = '%s'" % self.myId).fetchall()[0][0]
                    num += 1
                    cursor.execute("update counter set count = %d where id = '%s'" % (num, self.myId))
                    num = cursor.execute("select count from counter where id = '%s'" % self.myId).fetchall()[0][0]
                    print num
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.write(json.dumps({
                        "success": True,
                        "result": {
                            "myId": self.myId,
                            "count": num
                        }
                    }))
                else:
                    print "insert into counter values ('%s', %d)" % (self.myId, 1)
                    print "select count from counter where id = '%s'" % self.myId
                    cursor.execute("insert into counter values ('%s', %d)" % (self.myId, 1))

                    num = cursor.execute("select count from counter where id = '%s'" % self.myId).fetchall()[0][0]
                    print num
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.write(json.dumps({
                        "success": True,
                        "result":{
                            "myId": self.myId,
                            "count": num
                        }
                    }))
            else:
                raise sqlite3.OperationalError(x.message)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/click', DealHandler)
    ],
        {"debug": True}
    )

    application.listen(8899)
    tornado.ioloop.IOLoop.instance().start()

