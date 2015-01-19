
import xmltodict

if __name__ == '__main__':
	f = open('D:\Work\scrpy1\ilovemid_bot.xml','r')
	c = f.read()
	items = xmltodict.parse(c)
	count = 0
	for item in items['items']['item']:
		if 'bo_table=house' in item['url']:
				count+=1
	print count