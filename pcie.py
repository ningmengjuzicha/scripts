#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os,re
import pdfkit
from bs4 import BeautifulSoup

categories = {'.html': 2,'Eye.png': 0, 'TransitionEye.png': 1}

rules = {
    'Gen1': [2.5, 0.2],
    'Gen2': [5, 0.2],
    'Gen3': [8, 0.2],
    'Gen4': [16, 0.2]
}


def prepare(filepaths):
    mydic = {}
    for rowname in os.listdir(filepaths):
        if os.path.isdir(rowname):
            mydic[rowname] = {}
            for file in os.listdir(os.path.join(filepaths,rowname)):
                pos = file.rindex('_')
                group = file[0:pos]

                matched = re.search('Gen\d', file)
                if not matched:
                    print('{0} is invalid file'.format(file))
                gen = matched.group(0)
                print(gen)
                #category = file[pos + 1:]

                category = file[pos + 1:][5:]
                print(category)
                if group not in mydic[rowname]:
                    mydic[rowname][group] = [None] * 4
                if category not in categories:
                    print('Error: {0}'.format(category))
                if (category.endswith(".html")):
                    paths = os.path.join(filepaths,rowname)
                    result = parsehtml(os.path.join(paths,file),rules[gen])
                    print('.html..................',result)
                    mydic[rowname][group][3] = result
                    pdfname = save_pdf(os.path.join(paths,file))
                    category = file.replace(file, pdfname)
                    mydic[rowname][group][2] = 'attach:'+category


                elif (category.endswith("TransitionEye.png")):
                    
                    paths2 = os.path.join(paths, file)

                    mydic[rowname][group][1] = 'attach:'+paths2
                    #mydic[rowname][group][categories[category]] = paths2

                    #mydic[rowname][group][categories[category]] = rowname
                #mydic[rowname][group] = file
                #mydic.update(rowname)
                elif (category.endswith("Eye.png")):
                    pathss = os.path.join(paths, file)
                    print("---------------\n\n\n\n\n", pathss, "\n\n\n\n\n--------------")
                    mydic[rowname][group][0] = 'attach:'+pathss
                    # mydic[rowname][group][categories[category]] = pathss

                    print('ttttt:', pathss)

            fhdata = open('data.csv','w+')

            csv.register_dialect('myDialect',
                                 quoting=csv.QUOTE_ALL,
                                 skipinitialspace=True)
            writer = csv.writer(fhdata, dialect='myDialect')
            for rowname in sorted(mydic.keys()):
                ## need to know how to sort the column
                print(mydic.keys())
                line = []
                for group in sorted(mydic[rowname].keys()):
                    line.extend([mydic[rowname][group][itemindex] for itemindex in range(4) if str(itemindex).strip() != "" and itemindex is not None])
                line.insert(0, rowname)
                line.insert(1, "")

                #fhdata.write(','.join(line) + '\n')
                
                writer.writerow(line)
            
            fhdata.seek(0)
            lines = fhdata.readlines()
            fhdata.close()
           
            fhdata = open('data.csv','w+')
            for line in lines:
                line = str(line).strip("\n")

                if line.replace(" ", "") != "":
                    fhdata.write(line+"\n")
            
            fhdata.close()
            fhinstall = open('instruction.csv', 'w+')
            fhinstall.write("'TestPlanTemplate','PCIe Gen1&2&3','data.csv','A5'")
            fhinstall.close()


def parsehtml(file, rule):
    print('***parse html***')
    term = 'Data Rate \(Gb\/s\):\s*(\d[^\s]+)'
    try:
        standard = rule[0]
        difference = rule[1]

        fhhtml = open(file)
        content = ' '.join(fhhtml.readlines())
        fhhtml.close()

        matched = re.search(term, content)
        if matched:
            thevalue = float(matched.group(1))
            if standard - difference < thevalue < standard + difference:
                result = getresult(file)
                print('rrrrrrrrrr:',result)
            else:
                result = updateresult(file)
                print('update&&&&&&&&&&&&&&:', result)

    except Exception as ex:
        pass
    print(result,'haaaaaaaaaaaaaaaaaaaa')
    return result


def getresult(htmlfile):

    print('***get Overall Sigtest Result result***')
    with open(htmlfile, 'rb') as htmlfile:
        htmlfile = htmlfile.read()
    soup = BeautifulSoup(htmlfile, "html.parser")
    soup.li.font.string
    result = "Pass"
    
    print('get result',result)
    return result


def updateresult(htmlfile):

    print('***update Overall Sigtest Result result***')
    with open(htmlfile, 'rb') as htmlfiles:
        html = htmlfiles.read()
    soup = BeautifulSoup(html, "html.parser")
    
    soup.li.font.string.string.replace_with('Fail!')
    result = "Fail"
    soup.prettify()

    htmlfiles.close()
    save(htmlfile,soup.prettify())
    return result


def save(htmlfile,result):
    print('***Save Overall Sigtest Result result***')
    with open(htmlfile, 'w+') as newfile:
        newfile.write(result)
        newfile.close()
def save_pdf(htmlfile):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    """
    print('***save pdf***')
    print("*******************",htmlfile)
    pdfname = '_'.join(os.path.splitext(htmlfile)[0].split('_')[:-1]) + '.pdf'
    print('pdfname:', pdfname)
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],

    }
    pdfkit.from_file(htmlfile, pdfname, options=options)
    return pdfname

if __name__ == '__main__':
    prepare('D:\\shishi')
