import urllib
import BeautifulSoup

html = '<div><span><a href=http://naver.com>naver.com</a></span></div>'
soup = BeautifulSoup.BeautifulSoup(html)
print soup.prettify()

data = urllib.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=fri')
soup = BeautifulSoup.BeautifulSoup(data)
cartoons = soup.findAll('td', attrs={'class':'title'})

title = cartoons[0].find('a').text
link = cartoons[0].find('a')['href']


print soup.prettify()
print title, link

'''
print cartoons[1].find('a').text
print cartoons[0]
'''
