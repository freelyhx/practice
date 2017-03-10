### practice 2 --python

目标： 读取本地json文件, 并展示或输出为格式化后的多叉树

样例：

	{
		"a":{
			"b": 1,
			"c": 2
		},
		"d":{
			"e": 3
		},
		"f": 4
	}

转化为：

			   root			      
			 /   |   \
			a    d    f(4)
		  /  \   |   
       b(1) c(2) e(3)

提交方式：使用github, pull new request 至 branch ( commit )，存放至commit 文件夹下，以人名全拼建立子文件夹。


### practice 2 --javascript

目标： 页面结构如下：
		
	...
	<div>
		<input id='input' placeholder='input new node'>
		<input type='button' id='confirm' value='confirm'>	
	</div>
	<div id='div'></div>
	...

现需求如下：

1. 用户可以在 input 中输入数据, 当点击 "confirm" 按钮时, 触发事件( 假设事件名为 A ).
2. 事件A触发时, 检查用户输入, 若为非正整数, 丢弃并提示. 若为正整数, 作为参数提交给 callback function.
3. 在 callback 中, 根据输入数值的大小, 按递增顺序排列将其插入 #div 元素中.

提交方式：使用github, pull new request 至 branch ( commit )，存放至commit 文件夹下，以人名全拼建立子文件夹。
