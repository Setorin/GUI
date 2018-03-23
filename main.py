#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT

import json

class ListButton(ListItemButton):
    list = ListProperty()

class DomainButton(ListItemButton):
    list = ListProperty()

class IssueButton(ListItemButton):
    list = ListProperty()

class ItemButton(ListItemButton):
    list = ListProperty()

class Negotiation(Widget):
    text = StringProperty()
    list_item = ObjectProperty()

    def __init__(self, **kwargs):
        super(Negotiation, self).__init__(**kwargs)

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


class Senarios(Widget):
    file_name = StringProperty()
    text = StringProperty()
    label1 = StringProperty()
    label2 = StringProperty()
    label3 = StringProperty()
    label1_text = StringProperty()
    label2_text = StringProperty()
    label3_text = StringProperty()
    domain_list = ObjectProperty()
    domain_item = ObjectProperty()
    issue_item = ObjectProperty()
    data = ObjectProperty()
    string = StringProperty()
    string2 = StringProperty()
    state = StringProperty()

    def __init__(self, **kwargs):
        super(Senarios, self).__init__(**kwargs)

    def initdomainlist(self):
        f = open("domainrepository.json",'r')
        domain = json.load(f)
        list = domain["domain_list"]
        for i in range(len(list)):
            item = [{list[i]}]
            self.domain_list.adapter.data.extend(item)
        self.domain_list._trigger_reset_populate()

    def buttonClicked(self):
        self.file_name = self.ids["file_name"].text
        self.fileLoading()

    def fileLoading(self):
        self.state = "1"
        self.label1 = "discount_factor"
        self.label2 = "issue_size"
        self.label3 = "reservation"
        f = open(self.file_name, 'r')
        self.data = json.load(f)
        self.label1_text = str(self.data["discount_factor"])
        self.label2_text = str(self.data["issue_size"])
        self.label3_text = str(self.data["reservation"])
        self.showdomain()

    def showdomain(self):
        self.issue_item.adapter.data.clear()
        self.issue_item.adapter.data.extend("")
        self.issue_item._trigger_reset_populate()
        Notlist = ["discount_factor","issue_size","reservation"]
        self.domain_item.adapter.data.clear()
        for key in self.data:
            if key not in Notlist:
                item = [{key: self.data[key]}]
                self.domain_item.adapter.data.extend(item)
        self.domain_item._trigger_reset_populate()
        self.text = json.dumps(self.data,indent=4)

    def domain_clicked(self, item):
        self.file_name = str(item)[2:-2]
        print(self.file_name)
        self.fileLoading()


    def domain_args_converter(index, data_item):
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

        self.text = json.dumps(list,indent=4)

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
        self.text = json.dumps(list,indent=4)

    def item_args_converter(index, data_item):
        return{'list': (data_item)}

    def add_clicked(self):
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
            self.domain_item.adapter.data.extend(item)
            self.domain_item._trigger_reset_populate()
            self.showissue(self.data[self.string])
            self.text = json.dumps(self.data,indent=4)

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
            self.text = json.dumps(self.data,indent=4)

    def save_clicked(self):
        newdata = self.data
        if self.state == "1":
            newdata["discount_factor"] = float(self.ids["textbox1"].text)
#            newdata["issue_size"] = int(self.ids["textbox2"].text)
            newdata["reservation"] = float(self.ids["textbox3"].text)

        if self.state == "2":
            newdata[self.string]["name"] = self.ids["textbox1"].text
#            newdata[self.string]["size"] = int(self.ids["textbox2"].text)
            newdata[self.string]["weight"] = float(self.ids["textbox3"].text)

        if self.state == "3":
            newdata[self.string][self.string2]["evaluation"] = int(self.ids["textbox1"].text)
#            newdata[self.string][self.string2]["index"] = int(self.ids["textbox2"].text)
            newdata[self.string][self.string2]["value"] = self.ids["textbox3"].text

        f = open(self.file_name, 'w')
        json.dump(newdata, f, indent=4)
        self.text = json.dumps(newdata,indent=4)


class NegotiationRoot(Widget):
    def __init__(self, **kwargs):
        super(NegotiationRoot, self).__init__(**kwargs)
        self.senarios.initdomainlist()

    def party_clicked(self):
        pass

    def domain_clicked(self, item):
        self.senarios.domain_clicked(item)

    def issue_clicked(self, item):
        self.senarios.issue_clicked(item)

    def item_clicked(self, item):
        self.senarios.item_clicked(item)

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Jupiter'

if __name__ == '__main__':
    MainApp().run()
