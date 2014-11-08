##bookwalker
下载轻小说封面 输入系列轻小说ID即可

##pixivDatabase
抓取pixiv数据

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

使用时在setting中填写PHPSESSID