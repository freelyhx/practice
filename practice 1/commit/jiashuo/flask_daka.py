from flask import Flask, render_template, request
import sqlite3
import time, json, os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('1.html')


@app.route('/sb')
def mystring():
    id_daka = request.args.get("id_daka")
    conn = sqlite3.connect(os.path.dirname(__file__) + '/sign-in.db')
    cu = conn.cursor()
    print id_daka
    try:
        cu.execute("create table MESS_ALL(user_id VARCHAR2(32), user_ip VARCHAR2(32), count INTEGER)")
        conn.commit()
    except:
        pass

    if id_daka == '' or id_daka == 'undefined':
        nowtime = time.time()
        cu.execute("insert into MESS_ALL values('%s', '%s', '%d')" % (str(nowtime).split(".")[0], "1.1.1.1", 1))
        conn.commit()
        return json.dumps({"success": True, "result": str(nowtime).split(".")[0]})

    else:
        print id_daka
        if cu.execute("select * from MESS_ALL where user_id ='%s'" % id_daka).fetchall():
            print "user_id exist"
            i = cu.execute("select count from MESS_ALL where user_id='%s'" % id_daka).fetchall()[0][0]
            i += 1
            cu.execute("update MESS_ALL set count=%d where user_id='%s'" % (i, id_daka))
            conn.commit()
            return json.dumps({"success": False, "result": ''})
        else:
            nowtime = time.time()
            cu.execute("insert into MESS_ALL values('%s', '%s', '%d')" % (str(nowtime).split(".")[0], "1.1.1.1", 1))
            print "not exist +++"
            conn.commit()
            return json.dumps({"success": True, "result": str(nowtime).split(".")[0]})

    cu.close() 
    conn.close()


if __name__ == '__main__':
    app.run(host='192.168.9.18', port=9090)
