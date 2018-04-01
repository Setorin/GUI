#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.clock import Clock
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
import numpy as np
import os

import json

class ListButton(ListItemButton):
    list = ListProperty()

class DomainButton(ListItemButton):
    list = ListProperty()

class UtilButton(ListItemButton):
    list = ListProperty()

class IssueButton(ListItemButton):
    list = ListProperty()

class ItemButton(ListItemButton):
    list = ListProperty()

class Graph():
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("X label")
        self.ax.set_ylabel("Y label")
        self.ax.grid(True)
        self.line = self.ax.plot([], [], 'r.')[0]
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

    def update(self, particle_num):
        x = np.random.rand(particle_num)
        y = np.random.rand(particle_num)
        self.line.set_data(x, y)
        plt.pause(0.01)

class Negotiation(Widget):
    text = StringProperty()
    list_item = ObjectProperty()
    result_text = StringProperty()
    strategy_list = []
    preference_list = []

    def __init__(self, **kwargs):
        super(Negotiation, self).__init__(**kwargs)
        self.dot_num = 0
        self.graph = Graph()
        self.i = 0
        self.init_strategy()
        self.init_preference()

    def init_strategy(self):
        self.strategy_list = []
        files = os.listdir('agents')
        for file in files:
            if file[-3:] == '.py':
                self.strategy_list.append(file[:-3])

    def init_preference(self):
        self.preference_list = []
        for pathname, dirnames, filenames in os.walk('domain'):
            for filename in filenames:
                if filename[-5:] == '.json' and filename.find('util') != -1:
                    self.preference_list.append(filename)
                    self.preference_list.sort()

    def buttonClicked(self):
        print('add party')
        item = [(self.ids["party"].text, self.ids["party_strategy"].text, self.ids["preference_profile"].text)]
        print(item)
        self.list_item.adapter.data.extend(item)
        self.list_item._trigger_reset_populate()

    def lists_args_converter(index, data_item):
        party, party_strategy, preference_profile = data_item
        return {'list': (party, party_strategy, preference_profile)}

    def buttonClicked1(self):
        self.text = self.ids["party"].text

    def list_clicked(self):
        print('ok')

    def start(self):
        self.i += 1
        if self.i % 2 != 0:
            # 1 / 10s毎に実行してくれるっぽい
            self.result_text = ""
            self.event = Clock.schedule_interval(self.fc2, 1.0 / 10.0)
        else:
            # unschedule using cancel
            self.dot_num = 0
            self.event.cancel()

    def fc2(self, dt):
        self.dot_num += 1
        self.ids.grade.remove_widget(self.graph.fig.canvas)
        self.graph.update(self.dot_num)
        self.ids.grade.add_widget(self.graph.fig.canvas)
        self.result_text = self.result_text+str(self.dot_num)+"\n"


class Scenarios(Widget):
    domain_name = StringProperty()
    file_name = StringProperty()
    text = StringProperty()
    label1 = StringProperty()
    label2 = StringProperty()
    label3 = StringProperty()
    label1_text = StringProperty()
    label2_text = StringProperty()
    label3_text = StringProperty()
    domain_list = ObjectProperty()
    util_list = ObjectProperty()
    issue_list = ObjectProperty()
    issue_item = ObjectProperty()
    data = ObjectProperty()
    string = StringProperty()
    string2 = StringProperty()
    state = StringProperty()
    popup1 = ObjectProperty()
    popup2 = ObjectProperty()
    dlist = []

    def __init__(self, **kwargs):
        super(Scenarios, self).__init__(**kwargs)
        self.state = "5"

    def initdomainlist(self):
        f = open("domainrepository.json",'r')
        domain = json.load(f)
        list = domain["domain_list"]
        for i in range(len(list)):
            item = [{list[i]}]
            self.domain_list.adapter.data.extend(item)
            self.dlist.append(str(list[i]))
        self.domain_list._trigger_reset_populate()

    def buttonClicked(self):
        self.domain_name = self.ids["domain_name"].text
        self.domain_load()

    def make_domain(self):
        issue = self.ids["pop1_text1"].text.split()
        item = self.ids["pop1_text2"].text.split()
        newdata = {"discount_factor":0.1,"issue_size":len(issue),"reservation":0.1}
        for i in range(len(issue)):
            have_item = item[i].split(",")
            new_issue = {"name":issue[i],"size":len(have_item),"type":"discrete","weight":1.0}
            for j in range(len(have_item)):
                new_item = {"evaluation":1,"index":int(j+1),"value":have_item[j]}
                string = "item"+str(j+1)
                new_issue[string] = new_item
            string = "issue"+str(i+1)
            newdata[string] = new_issue
        self.domain_name = self.ids["domain_name"].text
        self.file_name = self.domain_name+"_util1.json"
        os.makedirs("domain/"+self.domain_name)
        f = open("domain/"+self.domain_name+"/"+self.domain_name+".json", 'w')
        data = {"util_list": [self.file_name],"issue_size":len(issue),"item_size":len(item)}
        json.dump(data,f,indent=4,sort_keys=True)
        f = open("domain/"+self.domain_name+"/"+self.file_name, 'w')
        json.dump(newdata,f,indent=4,sort_keys=True)
        f = open("domainrepository.json", 'r')
        domainrepository = json.load(f)
        domainrepository["domain_list"] = domainrepository["domain_list"]+[str(self.domain_name)]
        f = open("domainrepository.json", 'w')
        json.dump(domainrepository,f,indent=4,sort_keys=True)
        item = [{self.domain_name}]
        self.domain_list.adapter.data.extend(item)
        self.domain_list._trigger_reset_populate()
        self.dlist.append(str(self.domain_name))
        self.domain_load()
        print(self.domain_name)

    def domain_load(self):
        self.state = "0"
        self.label1 = ""
        self.label2 = ""
        self.label3 = ""
        self.label1_text = ""
        self.label2_text = ""
        self.label3_text = ""
        self.issue_item.adapter.data.clear()
        self.issue_item.adapter.data.extend("")
        self.issue_item._trigger_reset_populate()
        self.issue_list.adapter.data.clear()
        self.issue_list.adapter.data.extend("")
        self.issue_list._trigger_reset_populate()
        f = open("domain/"+self.domain_name+"/"+self.domain_name+".json", 'r')
        data = json.load(f)
        self.data = data["util_list"]
        self.util_list.adapter.data.clear()
        for i in self.data:
            item = [{i}]
            self.util_list.adapter.data.extend(item)
        self.util_list._trigger_reset_populate()

    def domain_clicked(self, item):
        self.domain_name = str(item)[2:-2]
        self.domain_load()

    def domain_args_converter(index, data_item):
        return{'list': (data_item)}

    def util_clicked(self, item):
        self.state = "1"
        self.file_name = str(item)[2:-2]
        self.label1 = "discount_factor"
        self.label2 = "issue_size"
        self.label3 = "reservation"
        self.issue_item.adapter.data.clear()
        self.issue_item.adapter.data.extend("")
        self.issue_item._trigger_reset_populate()
        f = open("domain/"+self.domain_name+"/"+self.file_name, 'r')
        self.data = json.load(f)
        self.label1_text = str(self.data["discount_factor"])
        self.label2_text = str(self.data["issue_size"])
        self.label3_text = str(self.data["reservation"])
        Notlist = ["discount_factor","issue_size","reservation"]
        self.issue_list.adapter.data.clear()
        for key in self.data:
            if key not in Notlist:
                item = [{key: self.data[key]}]
                self.issue_list.adapter.data.extend(item)
        self.issue_list._trigger_reset_populate()

    def util_args_converter(index, data_item):
        return{'list': (data_item)}

    def issue_clicked(self, item):
        self.state = "2"
        self.label1 = "name"
        self.label2 = "size"
        self.label3 = "weight"
        self.string = str(item)[2:-2]
        list = self.data[self.string]
        self.label1_text = str(list['name'])
        self.label2_text = str(list['size'])
        self.label3_text = str(list['weight'])
        self.showissue(list)

    def showissue(self, list):
        Notlist = ["name","size","type","weight"]
        self.issue_item.adapter.data.clear()
        for key in list:
            if key not in Notlist:
                add_item = [{key: list[key]}]
                self.issue_item.adapter.data.extend(add_item)
        self.issue_item._trigger_reset_populate()

    def issue_args_converter(index, data_item):
        return{"list": (data_item)}

    def item_clicked(self, item):
        self.state = "3"
        self.label1 = "evaluation"
        self.label2 = "index"
        self.label3 = "value"
        self.string2 = str(item)[2:-2]
        list = self.data[self.string][self.string2]
        self.label1_text = str(list['evaluation'])
        self.label2_text = str(list['index'])
        self.label3_text = str(list['value'])

    def item_args_converter(index, data_item):
        return{'list': (data_item)}

    def add_clicked(self):
        if self.state != "5":
            issue = self.ids["pop2_text3"].text.split()
            item = self.ids["pop2_text4"].text.split()
            item_size = len(item[1].split(","))
            newdata = {"discount_factor":float(self.ids["pop2_text1"].text),"issue_size":len(issue),"reservation":float(self.ids["pop2_text2"].text)}
            for i in range(len(issue)):
                have_item = item[i].split(",")
                if(item_size != len(have_item)):
                    item_size = -1
                new_issue = {"name":issue[i],"size":len(have_item),"type":"discrete","weight":1.0}
                for j in range(len(have_item)):
                    new_item = {"evaluation":1,"index":int(j+1),"value":have_item[j]}
                    string = "item"+str(j+1)
                    new_issue[string] = new_item
                string = "issue"+str(i+1)
                newdata[string] = new_issue
            f = open("domain/"+self.domain_name+"/"+self.domain_name+".json", 'r')
            data = json.load(f)
            if(data["issue_size"] == len(issue) and data["item_size"] == item_size):
                string = self.domain_name+"_util"+str(len(self.util_list.adapter.data)+1)+".json"
                data["util_list"] = data["util_list"]+[string]
                f = open("domain/"+self.domain_name+"/"+self.domain_name+".json", "w")
                json.dump(data,f,indent=4,sort_keys=True)
                f = open("domain/"+self.domain_name+"/"+string, 'w')
                json.dump(newdata,f,indent=4,sort_keys=True)
                item = [{string}]
                self.util_list.adapter.data.extend(item)
                self.util_list._trigger_reset_populate()
                Notlist = ["discount_factor","issue_size","reservation"]
                self.issue_list.adapter.data.clear()
                self.data = newdata
                for key in self.data:
                    if key not in Notlist:
                        item = [{key: self.data[key]}]
                        self.issue_list.adapter.data.extend(item)
                self.issue_list._trigger_reset_populate()


    def save_clicked(self):
        newdata = self.data
        if self.state == "0":
            pass

        if self.state == "1":
            newdata["discount_factor"] = float(self.ids["textbox1"].text)
            newdata["reservation"] = float(self.ids["textbox3"].text)

        if self.state == "2":
            newdata[self.string]["name"] = self.ids["textbox1"].text
            newdata[self.string]["weight"] = float(self.ids["textbox3"].text)

        if self.state == "3":
            newdata[self.string][self.string2]["evaluation"] = int(self.ids["textbox1"].text)
            newdata[self.string][self.string2]["value"] = self.ids["textbox3"].text

        f = open("domain/"+self.domain_name+"/"+self.file_name, 'w')
        json.dump(newdata, f, indent=4,sort_keys=True)

class NegotiationRoot(Widget):
    def __init__(self, **kwargs):
        super(NegotiationRoot, self).__init__(**kwargs)
        self.scenarios.initdomainlist()

    def party_clicked(self):
        pass

    def domain_clicked(self, item):
        self.scenarios.domain_clicked(item)

    def util_clicked(self, item):
        self.scenarios.util_clicked(item)

    def issue_clicked(self, item):
        self.scenarios.issue_clicked(item)

    def item_clicked(self, item):
        self.scenarios.item_clicked(item)

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Jupiter'

if __name__ == '__main__':
    MainApp().run()
