### practice 1

目标： 写出 browser <--> server <--> database 一整套系统组成的简易打卡功能。

描述： 前端页面仅有一个 button， 点击后触发事件，向后端提交数据。 后端记录下该台电脑信息，并写入数据库，记录其打卡次数。

建议： 

1. 前端js 使用 jquery ajax 向后台提交。
2. 后台需要能够区分出不同的前端终端。
3. 数据库可以使用sqlite3，最为简便。
4. 后端python web 框架建议使用 web.py, flask 或者 tornado 等。

提交方式：

使用github, pull new request 至 branch ( commit )

PS： 可以查看 sample 文件夹内的样例，以作参考。