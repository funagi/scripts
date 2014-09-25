##bookwalker
下载轻小说封面 输入系列轻小说ID即可

##pixivDatabase
抓取pixiv数据

##9gal
9gal刷在线时间 点盒子 抽卡片

使用说明:

修改9gal.py中`login.add_account('user','password')`为真实账户密码
去掉`#`的注释 可添加多个账户

##move
减少文件目录层数

before:

	test1
	|  test2
	|  |  test3
	|  |  |  test4
	|  |  |  kk.txt

after:

	test1
	|  test4
	|  kk.txt

## PixivCrawler
aiohttp抓取pixiv插画信息