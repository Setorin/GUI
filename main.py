#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.clock import Clock
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
import numpy as np


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

class AddDomain(Widget):
    popup = ObjectProperty()

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

    def __init__(self, **kwargs):
        super(Negotiation, self).__init__(**kwargs)
        self.dot_num = 0
        self.graph = Graph()
        self.i = 0

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

    def __init__(self, **kwargs):
        super(Scenarios, self).__init__(**kwargs)
        self.state = "0"
        self.text = "add domain"

    def initdomainlist(self):
        f = open("domainrepository.json",'r')
        domain = json.load(f)
        list = domain["domain_list"]
        for i in range(len(list)):
            item = [{list[i]}]
            self.domain_list.adapter.data.extend(item)
        self.domain_list._trigger_reset_populate()

    def buttonClicked(self):
        self.domain_name = self.ids["domain_name"].text
        if {self.domain_name} in self.domain_list.adapter.data:
            self.domain_load()
#        else:
#            f = open(self.file_name, 'w')
#            newdata = {"discount_factor":0.1,"issue_size":1,"reservation":0.1}
#            newdata["issue1"]["item1"] = {"evaluation":1,"index":1,"value":""}
#            json.dump(newdata,f,indent=4,sort_keys=True)
#            f = open("domainrepository.json", 'r')
#            domainrepository = json.load(f)
#            domainrepository["domain_list"] = domainrepository["domain_list"]+[str(self.file_name)]
#            f = open("domainrepository.json", 'w')
#            json.dump(domainrepository,f,indent=4,sort_keys=True)
#            item = [{self.file_name}]
#            self.domain_list.adapter.data.extend(item)
#            self.domain_list._trigger_reset_populate()
#            self.domain_load()


    def domain_load(self):
        self.state = "0"
        self.text = "add domain"
        self.label1 = "discount_factor"
        self.label2 = "issue_size"
        self.label3 = "reservation"
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
        self.text = "add util"
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
        self.text = "add issue"
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
        self.text = "add item"
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
        if self.state == "0":
            pass
        if self.state == "1":
            pass
        if self.state == "2":
            add_issue = {}
            self.data["issue_size"] = self.data["issue_size"]+1
            self.string = "issue"+str(self.data["issue_size"])
            for i in range(int(self.ids["textbox2"].text)):
                add_item = {}
                add_item["evaluation"] = 1
                add_item["index"] = i+1
                add_item["value"] = ""
                item = "item"+str(i+1)
                add_issue[item] = add_item
            add_issue["name"] = self.ids["textbox1"].text
            add_issue["size"] = int(self.ids["textbox2"].text)
            add_issue["type"] = "discrete"
            add_issue["weight"] = float(self.ids["textbox3"].text)
            self.data[self.string] = add_issue
            item = [{self.string: add_issue}]
            self.issue_list.adapter.data.extend(item)
            self.issue_list._trigger_reset_populate()
            self.showissue(self.data[self.string])

        if self.state == "3":
            add_item = {}
            self.data[self.string]["size"] = self.data[self.string]["size"]+1
            add_item["evaluation"] = int(self.ids["textbox1"].text)
            add_item["index"] = self.data[self.string]["size"]
            add_item["value"] = self.ids["textbox3"].text
            string = "item"+str(self.data[self.string]["size"])
            self.data[self.string][string] = add_item
            item = [{string: add_item}]
            self.issue_item.adapter.data.extend(item)
            self.issue_item._trigger_reset_populate()

    def save_clicked(self):
        newdata = self.data
        if self.state == "0":
            newdata["discount_factor"] = float(self.ids["textbox1"].text)
#            newdata["issue_size"] = int(self.ids["textbox2"].text)
            newdata["reservation"] = float(self.ids["textbox3"].text)

        if self.state == "1":
            pass

        if self.state == "2":
            newdata[self.string]["name"] = self.ids["textbox1"].text
#            newdata[self.string]["size"] = int(self.ids["textbox2"].text)
            newdata[self.string]["weight"] = float(self.ids["textbox3"].text)

        if self.state == "3":
            newdata[self.string][self.string2]["evaluation"] = int(self.ids["textbox1"].text)
#            newdata[self.string][self.string2]["index"] = int(self.ids["textbox2"].text)
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
