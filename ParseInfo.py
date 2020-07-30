import pymongo
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from xml.dom.minidom import parseString
from xml.dom.minidom import parse
from lxml import etree

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import pandas as pd

import os


def parseInfo(list):
    print(len(list))
    key = str(list[0])
    print("key",key)
    value = list[1]
    print("value",value)
    # host = '10.10.11.1'
    # client = MongoClient(host, 27017)
    try:
        client = MongoClient("mongodb://readonly:readonly@10.10.11.1:27017")
        table = client.crawlerPdf.text
        query = {"_id": value}
        data = table.find_one(query, {"grobid": 1})["grobid"]
        # print(type(data))
    except pymongo.errors.ConnectionFailure:
        with open('parseFailed.txt', 'w') as f:
            f.write(key+':'+value)
            f.write('\n')
        print("mogoDB AutoReconnect exception")
    else:
        if (data):
            xml_dom = parseString(data)
            fxmlName = 'data/' + key + '.xml'
            ftxtName = 'data/' + key + '.txt'

            try:
                with open(fxmlName, 'w', encoding='UTF-8') as fh:
                    xml_dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
                    print('写入xml OK!')
            except Exception as err:
                print('错误信息：{0}'.format(err))

            tree = ET.parse(fxmlName)
            root = tree.getroot()

            for rchild in root:
                if "text" in rchild.tag:
                    for rchildren in rchild:
                        if "body" in rchildren.tag:
                            body = rchildren
                            break

            print(body)
            with open(ftxtName, 'w') as f:
                for child in body:
                    if "div" in child.tag:
                        for children in child:
                            # if ("head" in children.tag):
                            #     if (children.text):
                            #         f.write(children.text)
                            #         f.write('\n')
                            #         print(children.text)
                            if ("head" in children.tag or "p" in children.tag):
                                if (children.text):
                                    f.write(children.text)
                                    f.write('\n')
                                    print(children.text)
                    if "figure" in child.tag:
                        for children in child:
                            if ("figDesc" in children.tag or "table" in children.tag):
                                if (children.text):
                                    f.write(children.text)
                                    f.write('\n')
                                    print(children.text)
                            # if ("table" in children.tag):
                            #     if (children.text):
                            #         f.write(children.text)
                            #         f.write('\n')
                            #         print(children.text)

        # if os.path.exists(fxmlName):
        #     os.remove(fxmlName)

# parseInfo([369567474,'/home/raw_data/pdfs/Wiley/a4/a4fd823ba9da0a49c74ad6a8dd62a28ba11a6f3c'])

