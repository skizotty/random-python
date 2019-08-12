from bs4 import BeautifulSoup
fileInformation = [
	['file1',[
		'1','2','3'
	]],
	['file2',[
		'1','3'
	]],
	['file3',[
		'2','3']
	]]
for specificFile in fileInformation: 
	baseSoup = BeautifulSoup(open("./html/basefile.html"), 'html.parser')
	for element in specificFile[1]: 
		soup2 = BeautifulSoup(open("./html/"+ element+".html"), 'html.parser')
		baseSoup.body.append(soup2)
	with open("./output/"+specificFile[0]+".html", "w") as file:
	    file.write(unicode(baseSoup))
