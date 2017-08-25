#! _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
'''
通过BeautifulSoup定位html，将定位出的结果转化成xpath

'''

soup = BeautifulSoup(open("D:\\Code\\python\\paths.html"), "html.parser")

class path_store:
    """
    存储路径
    """
    def __init__(self):
        self.divs = []
        self.path_nums = []
        self.cont_nums = []
    
    def push(self, div, path_num=0, cont_num=0):
        self.divs.insert(0, div)
        self.path_nums.insert(0, path_num)
        self.cont_nums.insert(0, cont_num)
        return True
    
    def mid_path(self):
        mid = []
        for index in range(len(self.divs)):
            if self.path_nums[index]:
                mid.append('contents[{}]'.format(self.cont_nums[index]))
            else:
                mid.append(self.divs[index])
        return '.'.join(mid)

    def all_path(self):
        path = []
        for index in range(len(self.divs)):
            if self.path_nums[index]:
                path.append(self.divs[index] + '[{}]'.format(self.path_nums[index]))
            else:
                path.append(self.divs[index])
        return '.'.join(path)

store = path_store()

def number(elements, attr):
    """
    将传入的元素和要定位的属性进行处理，得出该元素在这一层的位置
    path_num 表示xpath里的位置，cont_num 表示BS里的位置
    """
    same_name = []
    content = elements.parent.contents
    for raw in content:
        if raw.name == elements.name:
            same_name.append(raw)

    if len(same_name) == 1:
        return 0, 0
    else:
        for same in same_name:
            try:
                string = "same.%s" %store.mid_path()
                com =  eval(string)
                if com.attrs == attr:
                    path_num = same_name.index(same) + 1
                    cont_num = content.index(same)
                    return path_num, cont_num
            except Exception:
                pass


def xpath(element):
    """
    返回xpath路径
    """
    path = []
    attrs = element.attrs
    if element.name:
        store.push(element.name)
    for elen in element.parents:
        if elen.name == "[document]":
            break
        else:
            path_num, cont_num = number(elen, attrs)
            if path_num >= 1:
                store.push(elen.name, path_num, cont_num)
            else:
                store.push(elen.name)
    return store.all_path()

        
text = soup.find(attrs={"placeholder": u"\u8bf7\u8f93\u5165\u5bc6\u7801"})
print xpath(text)
