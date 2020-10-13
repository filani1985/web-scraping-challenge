#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import modules
from bs4 import BeautifulSoup 
from splinter import Browser


# In[13]:

def scrape():
	MarsData = {}
	#start the bowser 
	browser = Browser('firefox',executable_path = 'C:\\Python_test\\geckodriver-v0.27.0-win64\\geckodriver.exe')
	newsURL = "https://mars.nasa.gov/news/"
	#visit URL
	browser.visit(newsURL)
	newsHtml = browser.html


	# In[14]:



	soup = BeautifulSoup(newsHtml, 'html5lib')
	newsTitle = soup.find("div", class_="content_title").get_text()
	newsParagraph = soup.find("div", class_="article_teaser_body").get_text()
	MarsData['news_title'] = newsTitle
	MarsData['news_paragraph'] = newsParagraph
	# In[16]:


	### JPL Mars Space Images - Featured Image
	marsImageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	#open the site
	browser.visit(marsImageURL)
	imgHtmlinfo = browser.html
	imgBS = BeautifulSoup(imgHtmlinfo,'html.parser')

	featureImgInfo = imgBS.find('article',attrs={'class':'carousel_item'})
	


	# In[21]:


	#Get the Full url 
	import re
	featureImgUrlStyle = featureImgInfo['style']
	featuredImageLink = re.findall(r"'(.*?)'",featureImgUrlStyle)
	print (featuredImageLink)
	featuredImageUrl = 'https://www.jpl.nasa.gov'+ featuredImageLink[0]
	MarsData['featured_img_link'] = featuredImageUrl


	# In[23]:


	### Mars Weather
	marsWeatherUrl='https://twitter.com/marswxreport?lang=en'
	browser.visit(marsWeatherUrl)


	# In[24]:


	hemiHTML = browser.html
	weatherBS = BeautifulSoup(hemiHTML,'html5lib')


	# In[26]:


	marsWeather=weatherBS.find('div', attrs={'class':'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})
	MarsData['weather'] = marsWeather.text


	# In[27]:


	### Mars Facts
	import pandas as pd
	MarsFactsurl = "https://space-facts.com/mars/"

	marsFactsDF = pd.read_html(MarsFactsurl)
	marsFactsDF[0]


	# In[28]:


	factsDF = marsFactsDF[0]
	factsDF.columns = ['Paramter','Value']
	factsDF.set_index('Paramter',inplace=True)
	factsDF
	MarsData['facts'] = factsDF.to_html()



	# In[29]:


	#Mars Hemispheres
	#browser = Browser('firefox',executable_path = 'C:\\Users\\Sagar.Yadav1\\Desktop\\Teacher\\Assignment\\Fill_Pandas\\webscrping\\12-Web-Scraping-and-Document-Databases\\geckodriver-v0.27.0-win64\\geckodriver.exe')
	USGSurl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(USGSurl)
	hemiHTML = browser.html
	hemiBS = BeautifulSoup(hemiHTML,'html5lib')


	# In[31]:


	hemisphereImageurls = []
	marsImgLinks = hemiBS.find_all('img',attrs={'class':'thumb'})


	marsImgLinks
	for each_img in marsImgLinks:
		title = each_img.attrs['alt']
		url = each_img.attrs['src']
		full_url = 'https://astrogeology.usgs.gov/' + url
		hemisphereImageurls.append({'title':title,'img_url':full_url})
		

	MarsData['hemi_img'] = hemisphereImageurls
	browser.quit()
	return MarsData 



# In[ ]: