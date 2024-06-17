"""
███████████████████████████client_usage of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import aws_framework_manager_client,processing_tools
import os
import awswrangler as wr
import pandas as pd
import re
import random as rand
from flask import Flask, render_template,request,jsonify,make_response,redirect
import json
import requests
this_dict = {}
#___________________________________________________
k = 'select'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label for="@id" class="sensation" id="@id_label" style="@custom_style02">@label_title</label>
<br>
<select action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation inx" onchange="temp_input(this,'@k','');" onload="">
@options
</select>
<br>
""".replace('@k',k)
this_dict[k]['object'] = "<option style='font-size:15px;padding:5px;'>@object</option>"
this_dict[k]['params'] = ['@id','@label_title','@options']
#___________________________________________________
k = 'radios_horizontal'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<h2 id="@id_radios_title" class="sensation" style="@custom_style02">@label_title</h2>
<br>
<br>
<div>
<a>
@options
</a>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """&nbsp;&nbsp;&nbsp;
<span style="padding-right:10px;">
<input action_id="@action_id" action_item="@action_item" k="@k" isidentifier="@isidentifier" order="@order" obj="@object" enter_key='@enter_key' labelkey="@label_title" type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="">
<label for="@id_@n" class ="sensation" id="@id_@n_label">@object</label>
</span>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'radios_vertical'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<h2 id="@id_radios_title" class="sensation" style="@custom_style02">@label_title</h2>
<a>@subtitle</a>
<br>
<br>
<div>
<a>
@options
</a>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """&nbsp;&nbsp;&nbsp;
<div style="padding-right:10px;">
<input action_id="@action_id" action_item="@action_item" k="@k" isidentifier="@isidentifier" order="@order" obj="@object" labelkey="@label_title" type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="">
<label for="@id_@n" class ="sensation" id="@id_@n_label">@object</label>
</div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'num_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" us="@us" type="number" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'text_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" us="@us" type="text" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'pwd_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" type="password" autocomplete="off" cpw="@cpw" cpwconf="@cpwconf" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="" >
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'btn_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<br>
<br>
<a class="sensation" id="@id_label" style="display:none;font-size:16px;color:gray;"><a/>
<button action_id="@action_id" action_item="@action_item" id="@id" class="submitrequest" event_type='@event_type' style="width:100%;@custom_style01" onclick="temp_input(this,'@k','');" onload="">@label_title</button>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'text_area'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<textarea action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation inx" rows="@rowsnum" oninput="temp_input(this,'@k','');" onload="" style="@custom_style01">@text_content</textarea>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@rowsnum']
#___________________________________________________
k = 'acc_checkboxes'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<div action_id="@action_id" action_item="@action_item" class='accordion' id='acc_@id'>
<div class="accordion-item" style="font-size:14px;">
<h2 class="accordion-header" id="@id">
<button class="accordion-button collapsed sensation" style="font-size:14px;padding:7px;" type="button" data-bs-toggle="collapse" 
data-bs-target="#collapse_@id" aria-expanded="false" aria-controls="collapseOne">
<a id="@id_checkboxes_title" style="@custom_style02">@label_title</a>
<a>@subtitle</a>
<a id="@id_counter_container" style="position:absolute;left:@counter_leftpx;color:#252F3E;display:none;"><span id="@id_counter" 
style="padding-right:10px;">0</span><span>selected</span></a>
</button>
</h2>
<div id="collapse_@id" class="accordion-collapse collapse" aria-labelledby="@id" 
data-bs-parent="#acc_@id" style="">
<div id='acc_@id_body' class="accordion-body" style="@custom_style01">
@options
</div></div></div>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """<div style="padding:7px;"><input isidentifier="@isidentifier" order="@order" labelkey="@label_title" type="checkbox" id="@id_checkbox_@n" onclick="temp_input(this,'@k','');service_counter(this,'@id');" onload=""><label class="sensation" for="@id_checkbox_@n" id="@id_@n_label">@object</label></div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@options','@n','@counter_left']
#___________________________________________________
k = 'multi_checkboxes'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<div action_id="@action_id" action_item="@action_item" class='accordion' id='acc_@id'>
<div class="" style="font-size:14px;">
<h2 class="accordion-header" id="@id">
<div class="sensation" style="font-size:14px;padding:7px;">
<a id="@id_checkboxes_title" style="@custom_style02">@label_title</a>
<a>@subtitle</a>
<a id="@id_counter_container" style="position:absolute;left:@counter_leftpx;color:#252F3E;display:none;"><span id="@id_counter" 
style="padding-right:10px;">0</span><span>selected</span></a>
</div>
</h2>
<div id="collapse_@id" class="accordion-collapse collapse show" aria-labelledby="@id" 
data-bs-parent="#acc_@id" style="">
<div id='acc_@id_body' class="accordion-body" style="@custom_style01">
@options
</div></div></div>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """<div style="padding:7px;"><input isidentifier="@isidentifier" order="@order" labelkey="@label_title" type="checkbox" id="@id_checkbox_@n" onclick="temp_input(this,'@k','');service_counter(this,'@id');" onload=""><label class="sensation" for="@id_checkbox_@n" id="@id_@n_label">@object</label></div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@options','@n','@counter_left']
#*******************************sections
this_sections = {}
k = 'right_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div name="section" sectionname="@section_title" id="@section_id" class="col-lg-@n" style="padding-right:10px;border-right:solid 1px orange;@section_style">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">
<a id="title_@section_id" style="@sec_title_style">@section_title</a>
@custom_title_html
<a id="@section_id_a" class="sensation"  style="position:relative;left:0px;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:@editvisibility;float:right;" 
 onclick="save_load_edit_undo('@section_id','edit');">edit</a> 
<a id="@section_id_b1" edition="@section_id" edition_type="undo" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_b2" edition="@section_id" edition_type="undo" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','undo');">undo</a>
<a id="@section_id_c1" edition="@section_id" edition_type="save" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_c2" edition="@section_id" edition_type="save" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','save');">save</a>
</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
#___________________________________________________
k = 'left_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div name="section" sectionname="@section_title" id="@section_id" class="col-lg-@n" style="padding-right:10px;border-left:solid 1px orange;@section_style">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">
<a id="title_@section_id" style="@sec_title_style">@section_title</a>
@custom_title_html
<a id="@section_id_a" class="sensation"  style="position:relative;left:0px;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:@editvisibility;float:right;" 
 onclick="save_load_edit_undo('@section_id','edit');">edit</a> 
<a id="@section_id_b1" edition="@section_id" edition_type="undo" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_b2" edition="@section_id" edition_type="undo" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','undo');">undo</a>
<a id="@section_id_c1" edition="@section_id" edition_type="save" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_c2" edition="@section_id" edition_type="save" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','save');">save</a>
</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']

#___________________________________________________
k = 'no_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div name="section" sectionname="@section_title" id="@section_id" class="col-lg-@n" style="padding-right:10px;border:none;@section_style">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">
<a id="title_@section_id" style="@sec_title_style">@section_title</a>
@custom_title_html
<a id="@section_id_a" class="sensation"  style="position:relative;left:0px;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:@editvisibility;float:right;" 
 onclick="save_load_edit_undo('@section_id','edit');">edit</a> 
<a id="@section_id_b1" edition="@section_id" edition_type="undo" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_b2" edition="@section_id" edition_type="undo" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','undo');">undo</a>
<a id="@section_id_c1" edition="@section_id" edition_type="save" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_c2" edition="@section_id" edition_type="save" class="sensation" 
style="position:relative;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','save')">save</a>


</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
#****************************************************
this_common_menu = {}
k = 'menubar'
this_common_menu[k] = {}
this_common_menu[k]['html'] = """
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="padding:0px;height:37px;background-color:@menu_background_color;color:@menu_font_color;">
<div class="container-fluid">
<a class="navbar-brand" href="#"><img src="static/img/@menu_left_img" alt="" style="@img_style"></a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#main_nav">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse sensation" id="main_nav">
<ul class="navbar-nav ms-auto" style="right:53px;position:absolute;">
@items
</ul>
</div> <!-- navbar-collapse.// -->
</div> <!-- container-fluid.// -->
</nav>
"""
this_common_menu[k]['default_img_style']='max-width:175px;top:-30px;position:absolute;left:53px;'
k1 = 'items'
this_common_menu[k][k1] = {}
k2 = 'single'
this_common_menu[k][k1][k2] = """<li class="nav-item"><a class="nav-link" href="@href" onclick="@onclick" style="color:inherit;">@item_name</a></li>"""
k2 = 'multiple'
this_common_menu[k][k1][k2] = {}
this_common_menu[k][k1][k2]['dropdown_list'] = """
<li class="nav-item dropdown">
<a class="nav-link  dropdown-toggle" href="#" data-bs-toggle="dropdown" style="color:inherit;">@item_name</a>
<ul class="dropdown-menu dropdown-menu-right" style="top:33px;background-color:@menu_background_color;color:@menu_font_color;">
@objects
</ul>
</li>
"""
this_common_menu[k][k1][k2]['object'] = """
<li><a class="dropdown-item" href="@href" onclick="@onclick" style="color:inherit;font-size:14px;">@object</a></li>
"""
this_common_menu[k]['params'] = ['@menu_background_color','@menu_font_color','@menu_left_img','@item_name','@object','@href']
main_dict = {}
main_dict['sections'] = this_sections
main_dict['inputs'] = this_dict
main_dict['common_menu'] = this_common_menu

dynamic_js = {}
dynamic_js['load_data_dynamic_code'] = "@dynamic_js"
dynamic_js['load_data_dynamic_routine'] = """
oridat["@k"] = @v;
"""

class cloudpy_org_web_client:
    def __init__(self, **kwargs):
        self.main_dict = main_dict
        self.dynamic_js = dynamic_js
        self.pt = processing_tools()
        self.current_path = os.getcwd() + '/'
        #with open (self.current_path + 'dynamic_html.json', 'r') as f:
        #    self.main_dict = json.loads(f.read())
    #___________________________________________________
    def create_section(self,section_title:str,section_type:str='right_border',section_style:str='',size:int=2):
        a = self.pt.camel_to_snake(section_title).replace('?','').replace('.','_').replace(',','')
        section_id = a[0:6] + a[::-1][0:6][::-1]
        section_id = section_id.replace("'","").replace('"','')
        rslt = self.main_dict['sections'][section_type]['html']\
        .replace('@section_id',section_id)\
        .replace('@section_title',section_title)\
        .replace('@section_style',section_style)\
        .replace('@n',str(size))
        
        return rslt.replace('\n','')
    #___________________________________________________
    def create_menu_item(self
                         ,item_name:str
                         ,options:object
                         ,menu_background_color:str='black'
                         ,menu_font_color:str='white'
                        ):
        if type(options) != list:
            options = [options]
        lo = len(options)
        menu_background_color = menu_background_color.lower().replace(' ','')
        menu_font_color = menu_font_color.lower().replace(' ','')
        if lo < 1:
            return ''
        else:
            if lo == 1:
                item_type = 'single'
                onclick = ''
                if 'onclick' in set(options[0].keys()):
                    onclick = options[0]['onclick']
                rslt = self.main_dict['common_menu']['menubar']['items'][item_type]\
                .replace('@href',options[0]['href'])\
                .replace('@onclick',onclick)

            else:
                item_type = 'multiple'
                rslt = self.main_dict['common_menu']['menubar']['items'][item_type]['dropdown_list']\
                .replace('@menu_background_color',menu_background_color)\
                .replace('@menu_font_color',menu_font_color)
                objects = ''
                obj = self.main_dict['common_menu']['menubar']['items'][item_type]['object']
                for i in options:
                    onclick = ''
                    if 'onclick' in set(i.keys()):
                        onclick = i['onclick']
                    objects += obj.replace('@object',i['name'])\
                    .replace('@href',i['href'])\
                    .replace('@onclick',onclick)
                rslt = rslt.replace('@objects',objects)    
            rslt = rslt.replace('@item_name',item_name)
            return rslt.replace('\n','')
    #___________________________________________________
    def create_common_menu(self,menu_structure:dict,auth:bool=False,username:str=''):
        menu_background_color = menu_structure['menu_background_color']
        menu_font_color = menu_structure['menu_font_color']
        menu_left_img = menu_structure['menu_left_img']
        keys = set(menu_structure.keys())
        if 'img_style' in keys and menu_structure['img_style'].lower().replace(' ','') != 'default':
            img_style = menu_structure['img_style']
        else:
            img_style = self.main_dict['common_menu']['menubar']['default_img_style']
            
        rslt = self.main_dict['common_menu']['menubar']['html']\
        .replace('@menu_background_color',menu_background_color)\
        .replace('@menu_font_color',menu_font_color)\
        .replace('@menu_left_img',menu_left_img)\
        .replace('@img_style',img_style)

        items = ''
        items_nums = list(menu_structure['items'].keys())
        items_nums.sort()
        for i in items_nums:
            if 'after_authentication' in set(menu_structure['items'][i].keys()) and auth == True:
                w = 'after_authentication'
                items += self.create_menu_item(
                    item_name=menu_structure['items'][i][w]['item_name'].replace('@username',username)
                    ,options=menu_structure['items'][i][w]['options']
                    ,menu_background_color=menu_background_color
                    ,menu_font_color=menu_font_color
            )
            else:
                items += self.create_menu_item(
                    item_name=menu_structure['items'][i]['item_name']
                    ,options=menu_structure['items'][i]['options']
                    ,menu_background_color=menu_background_color
                    ,menu_font_color=menu_font_color
                )
        
        rslt = rslt.replace('@items',items)
        return rslt.replace('\n','')
        
    #___________________________________________________
    def create_input(self
                     ,input_type:str
                     ,label_title:str
                     ,options:list=[]
                     ,text_content:str=''
                     ,rowsnum:int=3
                     ,section_size:int=3
                     ,event_type:str='save'
                     ,us:str='no'
                     ,cpw:str='no'
                     ,cpwconf:str='no'
                     ,enter_key:str='no'
                     ,action_id:str=''
                     ,action_item:str=''
                     ,subtitle:str=''
                     ,custom_style01:str=''
                     ,custom_style02:str=''
                     ,custom_style03:str=''
                     ,order:str=''
                     ,isidentifier:str=''):
        counter_left = (section_size-1)*120 + 20
        a = self.pt.camel_to_snake(label_title)[0:12].replace('?','').replace('.','_').replace(',','')
        this_id = a[0:6] + a[::-1][0:6][::-1]
        this_id = this_id.replace("'","").replace('"','')
        rslt = self.main_dict['inputs'][input_type]['html']\
        .replace('@id',this_id)\
        .replace('@label_title',label_title)\
        .replace('@us',us)\
        .replace('@cpwconf',cpwconf)\
        .replace('@cpw',cpw)\
        .replace('@enter_key',enter_key)\
        .replace('@action_id',action_id)\
        .replace('@action_item',action_item)\
        .replace('@subtitle',subtitle)\
        .replace('@custom_style01',custom_style01)\
        .replace('@custom_style02',custom_style02)\
        .replace('@custom_style03',custom_style03)\
        .replace('@order',str(order))\
        .replace('@isidentifier',isidentifier)
        if input_type in ['select','radios_horizontal','radios_vertical','acc_checkboxes','multi_checkboxes']:
            opti = ''
            obj = self.main_dict['inputs'][input_type]['object']
            n = 0
            for this_option in options:
                n+=1
                opti += obj.replace('@object',this_option)\
                .replace('@n',str(n))\
                .replace('@id',this_id)\
                .replace('@label_title',label_title)\
                .replace('@action_id',action_id)\
                .replace('@action_item',action_item)\
                .replace('@order',str(order))\
                .replace('@isidentifier',isidentifier)
            rslt = rslt.replace('@options',opti).replace('@counter_left',str(counter_left))
        elif input_type in['text_input','num_input','pwd_input','text_area']:
            rslt = rslt.replace('@text_content',text_content)
            if input_type == 'text_area':
                rslt = rslt.replace('@rowsnum',str(rowsnum))
        elif input_type in ['btn_input']:
            rslt = rslt.replace('@event_type',event_type)
        return rslt.replace('\n','')
    #___________________________________________________
    def complete_dynamic_form(self,dynamic_form:dict):
        
        custom_title_html = ''
        if 'custom_title_html' in set(dynamic_form.keys()):
            if len(dynamic_form['custom_title_html']) > 0:
                custom_title_html = dynamic_form['custom_title_html']
        row_style = ''
        if 'row_style' in set(dynamic_form.keys()):
            if len(dynamic_form['row_style']) > 0:
                row_style = dynamic_form['row_style']
        sections = ''
        section_nums = list(dynamic_form['sections'].keys())
        section_nums.sort()
        for i in section_nums:
            ts = dynamic_form['sections'][i]
            tskeys = set(ts.keys())  
            inputs = ts['inputs']
            section_size = ts['size']
            section_style = ''
            if 'section_style' in tskeys:
                section_style = ts['section_style']
            section = self.create_section(
                section_title=ts['section_title']
                ,section_type=ts['section_type']
                ,section_style=section_style
                ,size=section_size)
             
            editvisibility = 'hidden'
            if 'edit_enabled' in tskeys:
                if len(ts['section_title']) > 0 and ts['edit_enabled'].lower().replace(' ','') == 'yes':
                    editvisibility = 'visible'
            
            sec_title_style = 'float:left;'
            if 'sec_title_style' in tskeys and ts['sec_title_style'].lower().replace(' ','') != 'default':
                sec_title_style=ts['sec_title_style']
            section = section.replace('@editvisibility',editvisibility).replace('@sec_title_style',sec_title_style)
            content = ""
            for j in inputs:
                jkeys = set(j.keys())
                
                custom_style01=''
                if 'custom_style01' in jkeys:
                    custom_style01=j['custom_style01']
                
                custom_style02=''
                if 'custom_style02' in jkeys:
                    custom_style02=j['custom_style02']
                
                custom_style03=''
                if 'custom_style03' in jkeys:
                    custom_style03=j['custom_style03']
                
                order=''
                if 'order' in jkeys:
                    order=j['order']
                
                isidentifier='no'
                if 'isidentifier' in jkeys:
                    if str(j['isidentifier']).lower().replace(' ','') == 'yes':
                        isidentifier = 'yes'
                
                subtitle = ''
                if 'subtitle' in jkeys:
                    subtitle=j['subtitle']
                action_id = ''
                if 'action_id' in jkeys:
                    action_id=j['action_id'].lower().replace(' ','')
                action_item= ''
                if 'action_item' in jkeys:
                    action_item=j['action_item'].lower().replace(' ','')
                
                if 'custom_content' in jkeys:
                    content += j['custom_content']
                elif j['input_type'] in ['text_input','pwd_input','text_area']:
                    enter_key = 'no'
                    if 'enter_key' in jkeys:
                        enter_key = j['enter_key'].lower().replace(' ','')
                            
                    text_content = ''
                    if 'text_content' in jkeys:
                        text_content=j['text_content']
                    if j['input_type'] == 'text_area':
                        rowsnum = j['rowsnum']
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,rowsnum=rowsnum
                            ,section_size=section_size
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier)
                    elif j['input_type'] == 'text_input':
                        us = 'no'
                        if 'us' in jkeys:
                            us=j['us'].lower().replace(' ','')
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,us=us
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                        )
                    elif j['input_type'] == 'pwd_input':
                        cpw = 'no'
                        if 'cpw' in jkeys:
                            cpw=j['cpw'].lower().replace(' ','')
                        cpwconf = 'no'
                        if 'cpwconf' in jkeys:
                            cpwconf=j['cpwconf'].lower().replace(' ','')
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,cpw=cpw
                            ,cpwconf=cpwconf
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                        )
                    else:
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                        )
                elif j['input_type'] in ['btn_input']:
                    event_type = None
                    if 'event_type' in jkeys:
                        event_type=j['event_type']
                    content += self.create_input(
                        input_type=j['input_type']
                        ,label_title=j['label_title']
                        ,section_size=section_size
                        ,event_type=str(event_type)
                        ,action_id=action_id
                        ,action_item=action_item
                        ,subtitle=subtitle
                        ,custom_style01=custom_style01
                        ,custom_style02=custom_style02
                        ,custom_style03=custom_style03
                        ,order=order
                        ,isidentifier=isidentifier
                    )
                else:
                    options = []
                    if 'options' in jkeys:
                        options=j['options']
                    content += self.create_input(
                        input_type=j['input_type']
                        ,label_title=j['label_title']
                        ,options=options
                        ,section_size=section_size
                        ,action_id=action_id
                        ,action_item=action_item
                        ,subtitle=subtitle
                        ,custom_style01=custom_style01
                        ,custom_style02=custom_style02
                        ,custom_style03=custom_style03
                        ,order=order
                        ,isidentifier=isidentifier
                    )
            sections += section.replace('@content',content)
        
        complete_form = '<div id="main_row" class="row" style="@row_style">@sections</div>'
        
        complete_form =complete_form.replace('@sections',sections)\
        .replace('@row_style',row_style)\
        .replace('@custom_title_html',custom_title_html)
        dynamic_form_keys = set(dynamic_form.keys())
        
        if 'display_banner' in dynamic_form_keys and dynamic_form['display_banner'].lower().replace(' ','') == 'no':
            display_banner = 'none'
        else:
            display_banner = 'block'
        if 'body_style' in dynamic_form_keys and dynamic_form['body_style'].lower().replace(' ','') != 'default':
            body_style=dynamic_form['body_style']
        elif 'body_background_color' in dynamic_form_keys and len(dynamic_form['body_background_color']) > 0:
            body_style="padding:0px;background-color:" + dynamic_form['body_background_color'].lower().replace(' ','') + ";"
        else:
            body_style="padding:0px;"
        bannertitle,banner_subtitle,bannerbackground,topcontent = '','','',''
        requires_authentication = True
        if 'bannertitle' in dynamic_form_keys:
            bannertitle = dynamic_form['bannertitle']
        if 'banner_subtitle' in dynamic_form_keys:
            banner_subtitle = dynamic_form['banner_subtitle']
        if 'bannerbackground' in dynamic_form_keys:
            bannerbackground = dynamic_form['bannerbackground']
        if 'topcontent' in dynamic_form_keys:
            topcontent = dynamic_form['topcontent']
        if 'requires_authentication' in dynamic_form_keys:
            requires_authentication = dynamic_form['requires_authentication']
        return complete_form,body_style,display_banner,bannertitle,banner_subtitle,bannerbackground,topcontent,requires_authentication

class cloudpy_org_aws_framework_client:
    def __init__(self,aws_namespace:str,env:str='dev',region_name:str="us-east-2",token_path:str=None):
        self.web = cloudpy_org_web_client()
        self.aws_namespace = aws_namespace
        self.sufix = env
        self.region_name = region_name
        self.token_path = token_path
        self.__define_constants()
        self.set_user_authentication_minutes_to_expire(30,print_res=False)
        self.aws_framework()
    #_________________________________________________________________________
    def __define_constants(self):
        self.domain_to_restrict_access_to = ''
        self.email_banner_img = ''
        self.favicon_ico = ''
        self.notifications_email = ''
        self.default_redirect_if_not_authenticated ='/login'
        self.web_portal_id = ''
        self.web_portal_title = ''
        self.auth_token_max_age_minutes = 30
        self.__jscode={}
        self.__jscode["after_saving_data"] = """
        function after_saving_data(){
        document.getElementById("@savebtn").style.display = "None";
        document.getElementById("@savebtn_label").style.display = "block";
        document.getElementById("@savebtn_label").innerHTML = "Data successfully saved.";
        }
        setTimeout(after_saving_data,300);
        """
        self.__jscode["after_editing_data"] = """
        document.getElementById("@savebtn").style.display = "block";
        document.getElementById("@savebtn_label").style.display = "None";
        document.getElementById("@savebtn_label").innerHTML = "";
        """
        self.current_path = os.getcwd() + '/'
        if self.token_path == None:
            self.token_path = self.current_path + self.aws_namespace + '.txt'
        self.aws = None
        self.errors = {}
        self.errors[1] = 'Invalid service token.'
        self.errors[2] = 'No aws framework client has been initialized yet.'
        self.errors[3] = 'Provided data format cannot be converted to json.'
        self._catalog_base_description = """GLUE Data Catalog '@catalog_name'.
        Created programmatically with cloudpy_org_aws_framework_client under the following criteria:
        cloudpy.org_aws_namespace = '@namespace', cloudpy.org_aws_env = '@env', region = '@region', creation_date='@creation_date'.
        Visit https://www.cloudpy.org/documentation.
        Additional custom description:@desc"""
        self.__letters = list('abcdefghijklmnopqrstuvwxyz0123456789')
        self.__letters.append('_')
        self.__letters.append('-')
        
    #_________________________________________________________________________
    def set_user_authentication_minutes_to_expire(self,minutes:int,print_res:bool=True):
        self.user_authentication_minutes_to_expire = minutes
        if print_res:
            print('Temporal authentication token expiration for framework users has been set to ' + str(minutes) + ' minutes.')
    #_________________________________________________________________________
    def get_full_path(self,relative_path:str):
        relative_path = relative_path.replace('\\','/').replace('//','/').replace('//','')
        l = len(relative_path)
        if relative_path[l-1:l] == '/':
            relative_path = relative_path[0:l-1]
            l = len(relative_path)
        if relative_path[0:1] == '/':
            relative_path = relative_path[1:l]
        return self.s3_root_path + relative_path + '/'
    #_________________________________________________________________________
    def ofuscate(self,str_input:str):
        rslt = ''
        u = list(self.aws.ypt.decrypt(self._unique_of,self.__gen_key))
        for i in str_input:
            if i in self.__letters:
                rslt += u[self.__letters.index(i)]
            else:
                rslt += i
        return rslt
    #_________________________________________________________________________
    def deofuscate(self,str_input:str):
        rslt = ''
        u = list(self.aws.ypt.decrypt(self._unique_of,self.__gen_key))
        for i in str_input:
            if i in u:
                rslt += self.__letters[u.index(i)]
            else:
                rslt += i
        return rslt
    #_________________________________________________________________________
    def _suok(self):
        file_name = self.aws_namespace + '_o_key.txt'
        x = self.get_s3_file_content(file_name=file_name,relative_path=self._secrets_relative_path)
        if x != None and len(x) > 1:
            self._unique_of = x
            print('Security was previously set. Security in place.')
        else:
            try:
                random_numbers,b,l=[],'',len(self.__letters)
                while len(random_numbers) < l:
                    this_rn = rand.randint(0,l-1)
                    if this_rn not in random_numbers:
                        random_numbers.append(this_rn)
                for i in range(l):
                    b += self.__letters[random_numbers[i]]
                self._unique_of = self.aws.ypt.encrypt(b,self.__gen_key)
                self.write_in_s3_folder(
                    data=self._unique_of
                    ,file_name=file_name
                    ,relative_path=self._secrets_relative_path,print_res=False)
                print('Security in place.')
            except Exception as e:
                print(str(e))
                self._unique_of = None
                print('Could not set unique file ofuscation.')
        
    #_________________________________________________________________________
    def aws_framework(self):
        try:
            with open(self.token_path, 'r') as f:
                self.aws = aws_framework_manager_client(service_token=f.read(),aws_namespace=self.aws_namespace,region_name=self.region_name)
            try:
                self.bucket_name = self.aws.get_bucket_name(sufix=self.sufix,region=self.region_name)
                self.s3_root_path = 's3://' + self.bucket_name + '/'
                self._secrets_relative_path = '/settings/secrets/'
                self._users_relative_path = self._secrets_relative_path + 'users'
                self.__gen_key = self.get_s3_file_content(file_name='general_key.txt',relative_path=self._secrets_relative_path)
                self.athena = self.aws.ypt.b3session.client('athena',region_name=self.region_name)
                self.ses = self.aws.ypt.b3session.client('ses',region_name=self.region_name)
                self.data_catalog_sufix = self.bucket_name.replace('cloudpy.org-','')
                banned_relative_paths = ['settings/','settings/secrets/users/','metadata/']
                self.banned_paths = [self.get_full_path(i) for i in banned_relative_paths]
            except Exception as e:
                print('Error AFW01:',str(e))
            
        except Exception as e:
            print('Error AFW02:', self.errors[1])
        self._suok()
    #_________________________________________________________________________
    def get_s3_file_content(self,file_name:str,relative_path:str):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            rslt = None
            if ext == 'json':
                try:
                    rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=False)
                except:
                    try:
                        rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
                    except Exception as e:
                        print(str(e))
            else:
                rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
            return rslt
        else:
            print(self.errors[2])
            return None
    #_________________________________________________________________________
    def __treat_file_name(self,file_name:str):
        file_name = file_name.lower()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')
        ext = file_name[::-1].split('.')[0][::-1]
        file_name = file_name.replace('.' + file_name[::-1].split('.')[0][::-1],'') + '.' + ext
        return file_name,ext
    #_________________________________________________________________________    
    def write_in_s3_folder(self,data:object,file_name:str,relative_path:str,print_res:bool=True):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            if ext != 'json':
                if type(data) != str:
                    data = str(data)
                self.aws.ypt.store_str_as_file_in_s3_folder(
                    strInput=data
                    ,fileName=file_name
                    ,s3FullFolderPath=s3FullFolderPath
                    ,region_name=self.region_name
                    ,print_res=print_res)
            elif ext == 'json':
                cont = True
                if type(data) != dict:
                    data = str(data)
                    try:
                        data = self.aws.dictstr_to_dict(data)
                    except:
                        cont = False
                        print(self.errors[3])
                if cont:
                    try:
                        self.aws.ypt.standard_dict_to_json(jsonOrDictionary=data,fileName=file_name,folderPath=s3FullFolderPath,print_res=print_res)
                    except Exception as e:
                        print(str(e))
        else:
            print(self.errors[2])
    #_________________________________________________________________________        
    def create_user(self,username:str,email:str,pwd:str):
        rslt = self.aws.create_new_user(sufix=self.sufix,region=self.region_name,username=username,email=email,pwd=pwd)
        return rslt
    #_________________________________________________________________________
    def check_user(self,username_or_email:str='not_authenticated_person'):
        sufix=self.sufix
        region=self.region_name
        print('sufix:*' + sufix + '*')
        print('region:*' + region + '*')
        if username_or_email == None:
            username_or_email = 'not_authenticated_person'
        print('username_or_email:*' + username_or_email + '*')
        rslt = self.aws.check_if_user_exists_and_was_confirmed(username_or_email=username_or_email,sufix=sufix,region=region)
        return rslt
    #_________________________________________________________________________
    def confirm_user(self,username_or_email:str):
        user_check = self.check_user(username_or_email)
        uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['confirmed'] == 0:
                rslt = self.get_s3_file_content(file_name=user_check['file_name'],relative_path=self._users_relative_path)
                rslt['confirmed_email'] = 1
                self.write_in_s3_folder(data=rslt,file_name=user_check['file_name'],relative_path=self._users_relative_path,print_res=False)
    #_________________________________________________________________________            
    def get_user_temp_token(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        if email_notification:
            return self._gut(username_or_email=username_or_email,email_notification=email_notification,temp_token=temp_token)
        else:
            return self._gut(username_or_email=username_or_email,pwd=pwd)
    #_________________________________________________________________________
    def _gut(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        user_check = self.check_user(username_or_email)
        uck = set()
        if type(user_check) == dict:
            uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    cont = False
                    if email_notification:
                        this_key = 'email_notification_token'
                        minutes_to_expire = 30
                        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token,email_notification=False):
                            cont = True
                    elif pwd == self.aws.ypt.decrypt(data['encrypted_pwd'],self.__gen_key):
                        cont = True
                    if cont:
                        temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        data[this_key] = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=temp_token,minutes_to_expire=minutes_to_expire)
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return temp_token
                    else:
                        return 'Wrong password.'
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #_________________________________________________________________________        
    def user_token_authentication(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        return self.__uta(username_or_email=username_or_email,temp_token=temp_token,email_notification=email_notification)
    #_________________________________________________________________________
    def __uta(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        user_check = self.check_user(username_or_email)
        uck = set()
        if type(user_check) == dict:
            uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    what = 'Token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    if email_notification:
                        this_key = 'email_notification_token'
                        what = 'Link'
                        minutes_to_expire = 30
                    try:
                        enc_data = data[this_key]
                        stored_token = self.aws.ypt.decrypt_before_expiration(data=enc_data)
                        if stored_token.lower().replace('.','').strip() == 'encryption expired':
                            print(what + ' expired.')
                    except Exception as e:
                        stored_token = None
                    if temp_token == stored_token:
                        return True
                    else:
                        new_temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        new_enc_data = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=new_temp_token,minutes_to_expire=minutes_to_expire)
                        data[this_key] = new_enc_data
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return False
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #__________________________________________________________________________
    def update_user_password(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        self.__up(username_or_email=username_or_email,email_temp_token=email_temp_token,new_pwd=new_pwd)
    #__________________________________________________________________________
    def __up(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=email_temp_token,email_notification=True):
            try:
                user_check = self.check_user(username_or_email)
                f = user_check['file_name']
                r = self._users_relative_path
                data = self.get_s3_file_content(file_name=f,relative_path=r)
                data['encrypted_pwd'] = self.aws.ypt.encrypt(new_pwd,self.__gen_key)
                self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                print('Password successfully updated')
                return True
            except:
                print('Error while trying to modify password.')
                return False
        else:
            print('Could not modify password.')
            return  False
    #__________________________________________________________________________
    def df_to_big_data_hive(self,df_input:pd.DataFrame,table_name:str,sink_relative_path:str='sinks',partition_cols:list=None):
        path = self.get_full_path(relative_path=sink_relative_path + table_name)
        wr.s3.to_parquet(
            df=df_input
            ,dataset=True
            ,path=path
            ,boto3_session=aws.aws.ypt.b3session
            ,partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def create_data_catalog(self,catalog_name:str=None,description:str='',include_environment_tag:bool=True,catalog_id:str=None):
        if catalog_name == None:
            catalog_name = self.data_catalog_sufix + '-data-catalog'
        else:
            catalog_name = self._treat_name(catalog_name)
            if include_environment_tag:
                catalog_name = self.data_catalog_sufix + '-' + catalog_name
        
        date_id,time_id = self.aws.ypt.date_time_id(local=True)
        creation_date = self.aws.ypt.date_time_str(date_id,time_id)
        new_description = self._catalog_base_description\
        .replace('@catalog_name',catalog_name)\
        .replace('@namespace',self.aws_namespace)\
        .replace('@env',self.sufix)\
        .replace('@region',self.region_name)\
        .replace('@creation_date',creation_date)\
        .replace('@desc',description)
        try:
            if catalog_id == None:
                account_id = wr.sts.get_account_id(boto3_session=self.aws.ypt.b3session)
                catalog_id = account_id
            self.athena.create_data_catalog(
                Name=catalog_name
                ,Type='GLUE'
                ,Description=new_description
                ,Parameters={'catalog-id': catalog_id}
            )
            print('catalog_name: ',catalog_name)
            print('description: ',new_description)
        except Exception as e:
            r = str(e)
            if ': DataCatalog' in r:
                r = 'DataCatalog' + r.split(': DataCatalog')[1]
            print(r)
    #__________________________________________________________________________
    def _treat_name(self,name:str):
        name = name.lower().strip()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')\
        .replace('--','-')\
        .replace('--','-')\
        .replace('--','')
        return name
    #__________________________________________________________________________
    def create_big_data_db(self,db_name:str,description:str):
        db_name = self._treat_name(db_name)
        try:
            wr.catalog.create_database(name=db_name,description=description,boto3_session=self.aws.ypt.b3session)
            return 'Database ' + db_name + ' succesfully created.'
        except Exception as e:
            return str(e).split('already exists')[0] + 'already exists.'
    #__________________________________________________________________________   
    def _update_get_datasources_schemas(self):
        catalogs = self.athena.list_data_catalogs()
        cats = {}
        for this_cat in [i['CatalogName'] for i in catalogs['DataCatalogsSummary']]:
            d = self.athena.list_databases(CatalogName=this_cat)
            cats[this_cat] = {}
            databases = {j['Name'] for j in d['DatabaseList']}
            for this_db in databases:
                cats[this_cat][this_db] = {}
                dd = self.athena.list_table_metadata(CatalogName=this_cat,DatabaseName=this_db)
                these_tables = [i['Name'] for i in dd['TableMetadataList']]
                for this_table in these_tables:
                    cats[this_cat][this_db][this_table] = {}
                    for m in dd['TableMetadataList']:
                        if m['Name'] == this_table:
                            this_metadata = m
                            these_keys = [x for x in set(this_metadata.keys()) if x != 'Name']
                            for this_key in these_keys:
                                cats[this_cat][this_db][this_table][self.aws.ypt.camel_to_snake(this_key)] = this_metadata[this_key]
                            break
        rslt = {}
        rslt['simple'] = {}
        rslt['complete'] = {}
        version = ['simple','complete']
        for a,b in cats.items():
            for u in version:
                rslt[u][a] = {}
            for c,d in b.items():
                for u in version:
                    rslt[u][a][c] = {}
                for e,f in d.items():
                    for u in version:
                        rslt[u][a][c][e] = {}
                    for g,h in f.items():
                        if g == 'columns':
                            for u in version:
                                rslt[u][a][c][e][g] = {hh['Name']:hh['Type'] for hh in h}
                        else:
                            rslt['complete'][a][c][e][g] = h
        self._datasources_schemas = rslt
    def show_datasources_schemas(self,version:bool='simple'):
        self._update_get_datasources_schemas()
        rslt = {}
        for k,v in self._datasources_schemas[version].items():
            if self.data_catalog_sufix in k:
                rslt[k] = v
        return rslt
    #__________________________________________________________________________    
    def create_athena_table(self,sink_path:str,db_name:str,table_name,columns_schema:dict,partition_cols:list):
        wr.athena.create_table(
            database=db_name,
            table=table_name,
            path=sink_path,
            columns_types=columns_schema,
            partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def list_s3_object(self,relative_path:str=''):
        try:
            fp = self.get_full_path(relative_path)
            l = wr.s3.list_objects(path=fp,boto3_session=self.aws.ypt.b3session)
            rslt = [i.replace(fp,'') for i in l if '/' not in i.replace(fp,'')]
            rslt = set(rslt)
            rslt = list(rslt)
            rslt.sort()
        except Exception as e:
            print(str(e))
            rslt = []
        return rslt
    #__________________________________________________________________________
    def delete_s3_objects(self,relative_path:str,file_names:list=[],clear_all_directory:bool=False):
        folder_path = self.get_full_path(relative_path)
        if folder_path not in self.banned_paths:
            existing_files = self.list_s3_object(relative_path)
            if clear_all_directory:
                file_names = [folder_path + i for i in existing_files]
            else:
                file_names = [folder_path + i for i in file_names if i in existing_files]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(str(len(file_names)) + ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            m = "The directory path: '@folder_path' \n"\
            "constitutes an integral component of the foundational framework structure, thus precluding direct programmatic deletion.\n"\
            "While manual removal of objects within this directory is feasible within your AWS account, we strongly advise against such "\
            "action, as it may compromise the functionalities of your cloudpy.org environment framework.\n"\
            "For comprehensive guidelines on the proper deletion procedure for a cloudpy.org framework, we "\
            "recommend consulting our documentation at https://www.cloudpy.org/documentation."
            m = m.replace('@folder_path',folder_path)
            print(m)  
    #__________________________________________________________________________        
    def delete_user(self,username_or_email:str):
        folder_path = self.get_full_path(self._users_relative_path)
        this_check = self.check_user(username_or_email=username_or_email)
        if 'file_name' in set(this_check.keys()):
            file_names = [folder_path + this_check['file_name']]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(this_check, ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            print(this_check)
    #__________________________________________________________________________
    def user_ref(self,username_or_email:str):
        c = self.check_user(username_or_email)
        if 'file_name' in c:
            return c['file_name'].replace('.json','')
        else:
            return 'Invalid username or email.'
    #__________________________________________________________________________
    def store_json_data(self,username_or_email:str,temp_token:str,form_name:str,json_data:dict):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            try:
                a = self.user_ref(username_or_email)
                b = self.ofuscate(a)
                if len(b) > 1:
                    self.write_in_s3_folder(
                        data=json_data
                        ,file_name= b + '.json'
                        ,relative_path=self._secrets_relative_path + self.ofuscate(self._treat_name(form_name))
                        ,print_res=False)
                    return {"stored":True}
                else:
                    return {"stored":False,"error_message":"Invalid username or email."}
            except Exception as e:
                print(str(e))
        else:
            return {"stored":False,"error_message":"Invalid token."}
        
        #__________________________________________________________________________
    def store_web_portal_json_data(self
                                   ,username_or_email:str
                                   ,folder_reference:str
                                   ,json_data:dict
                                   ,requires_auth:bool=True
                                   ,temp_token:str=None
                                   ,redirect:bool=False
                                  ):
        if self.web_portal_id != None and type(self.web_portal_id) == str and len(self.web_portal_id) > 0:
            if requires_auth:
                if temp_token == None:
                    x = False
                    return {"error_message":"Temporal token not created. Prior authentication is required."}
                else:
                    x = self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token)
            else:
                x = True
            print('x:',x)
            if x:
                try:
                    a = self.user_ref(username_or_email)
                    b = self.ofuscate(a)
                    form_name = request.cookies.get('form_name')
                    if len(b) > 1:
                        relative_path=self._secrets_relative_path + self.web_portal_id + '/' + self.ofuscate(self._treat_name(folder_reference))
                        print('relative_path:',relative_path)
                        self.write_in_s3_folder(
                            data=json_data
                            ,file_name= b + '.json'
                            ,relative_path=relative_path
                            ,print_res=True)
                        #jscode = self.__jscode["after_saving_data"].replace('@savebtn',savebtn)
                        if redirect:
                            return self.dynamic_site(page_name=form_name)
                        else:
                            return {"stored":True}
                    else:
                        return {"stored":False,"error_message":"Invalid username or email."}
                except Exception as e:
                    print(str(e))
                    return {"stored":False,"error_message":str(e)}
            else:
                return {"stored":False,"error_message":"Invalid token."}
        else:
            return {"error_message":"'cloudpy_org_aws_framework_client.web_portal_id has not been set.'"}
            
    #__________________________________________________________________________
    def read_form_data(self,username_or_email:str,temp_token:str,form_name:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            try:
                a = self.user_ref(username_or_email)
                b = self.ofuscate(a)
                if len(b) > 1:
                    rslt = self.get_s3_file_content(
                        file_name=b + '.json'
                        ,relative_path=self._secrets_relative_path + self.ofuscate(self._treat_name(form_name))
                    )
                    return rslt
                else:
                    return {"error_message":"Invalid username or email."}
            except Exception as e:
                print(str(e))
        else:
            return {"error_message":"Invalid token."}
    #__________________________________________________________________________
    def read_web_portal_json_data(self,username_or_email:str,temp_token:str,folder_reference:str):
        if self.web_portal_id != None and type(self.web_portal_id) == str and len(self.web_portal_id) > 0:
            if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
                try:
                    a = self.user_ref(username_or_email)
                    b = self.ofuscate(a)
                    if len(b) > 1:
                        rslt = self.get_s3_file_content(
                            file_name=b + '.json'
                            ,relative_path=self._secrets_relative_path + self.web_portal_id + '/' + self.ofuscate(self._treat_name(folder_reference))
                        )
                        return rslt
                    else:
                        return {"error_message":"Invalid username or email."}
                except Exception as e:
                    print(str(e))
            else:
                return {"error_message":"Invalid token."}
        else:
            return {"error_message":"'cloudpy_org_aws_framework_client.web_portal_id has not been set.'"}    
    #__________________________________________________________________________
    def write_in_web_portal_s3_folder(self,data:object,file_name:str,relative_path:str):
        if self.web_portal_id != None and self.web_portal_id != '':
            relative_path = self.ofuscate(self._treat_name(relative_path))
            relative_path = self._secrets_relative_path + self.web_portal_id + relative_path
            self.write_in_s3_folder(data=data,file_name=file_name,relative_path=relative_path)
        else:
            print('cloudpy_org_aws_framework_client.web_portal_id has not been set.')
    #__________________________________________________________________________
    def read_from_web_portal_s3_folder(self,file_name:str,relative_path:str):
        if self.web_portal_id != None and self.web_portal_id != '':
            relative_path = self.ofuscate(self._treat_name(relative_path))
            relative_path = self._secrets_relative_path + self.web_portal_id + relative_path
            return self.get_s3_file_content(file_name=file_name,relative_path=relative_path)
        else:
            print('cloudpy_org_aws_framework_client.web_portal_id has not been set.')
    #__________________________________________________________________________
    def _stud(self,storage_label:str,username_or_email:str,temp_token:str,page_name:str,structured_data:dict,full_refresh:bool=False):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            try:
                a = page_name
                b = self.ofuscate(a)
                if len(b) > 1:
                    relative_path=self._secrets_relative_path + self.ofuscate(storage_label)
                    file_name=b + '.json'
                    updates_log = []
                    if full_refresh:
                        previous_version = None
                    else: 
                        previous_version = self.get_s3_file_content(file_name=file_name,relative_path=relative_path)
                        if type(previous_version) == dict:
                            try:
                                updates_log = previous_version['updates_log']
                            except:
                                updates_log = []
                            previous_version.pop('updates_log', None)
                        else:
                            previous_version = None
                    date_id,time_id = self.aws.ypt.date_time_id(local=True)
                    creation_date = self.aws.ypt.date_time_str(date_id,time_id)
                    if self.aws.ypt.compare_dicts(structured_data,previous_version):
                        print('No changes detected.')
                    else:
                        updates_log.append({creation_date:{'username_or_email':username_or_email,'previous_version':previous_version}})
                    if len(updates_log) > 0:
                        structured_data['updates_log'] = updates_log
                    self.write_in_s3_folder(
                        data=structured_data
                        ,file_name=file_name
                        ,relative_path=relative_path
                        ,print_res=False)
                    return {"stored":True}
                else:
                    return {"stored":False,"error_message":"Invalid username or email."}
            except Exception as e:
                print(str(e))
        else:
            return {"stored":False,"error_message":"Invalid token."}
        
    #__________________________________________________________________________
    def get_page_structure(self,page_name:str):
        return self.get_s3_file_content(
            file_name=self.ofuscate(page_name) + '.json'
            ,relative_path=self._secrets_relative_path + self.ofuscate('dynamic_pages')
        )
    #__________________________________________________________________________
    def define_dynamic_page_structure(self,username_or_email:str,temp_token:str,page_name:str,page_structure:dict,full_refresh:bool=False):
        return self._stud(
            storage_label='dynamic_pages'
            ,username_or_email=username_or_email
            ,temp_token=temp_token
            ,page_name=page_name
            ,structured_data=page_structure
            ,full_refresh=full_refresh
        )
        #__________________________________________________________________________
    def define_common_menu(self,username_or_email:str,temp_token:str,menu_structure:dict,full_refresh:bool=False):
        if self.web_portal_id != None and self.web_portal_id != '':
            return self._stud(
                storage_label='common_menus'
                ,username_or_email=username_or_email
                ,temp_token=temp_token
                ,page_name=self.web_portal_id
                ,structured_data=menu_structure
                ,full_refresh=full_refresh
            )
        else:
            return 'cloudpy_org_aws_framework_client.web_portal_id has not been set.'
        
    #__________________________________________________________________________
    def _gds(self,structure_name:str,storage_label:str):
        try:
            a = structure_name
            b = self.ofuscate(a)
            if len(b) > 1:
                relative_path=self._secrets_relative_path + self.ofuscate(storage_label)
                file_name= b + '.json'
                page_structure = self.get_s3_file_content(
                    file_name=file_name
                    ,relative_path=relative_path
                )
                return page_structure
            else:
                return {"error_message":"Structure definition not found."}
        except Exception as e:
            print(str(e))
            return {"error_message":"Structure definition not found."}
    #__________________________________________________________________________
    def get_dynamic_page_structure(self,page_name:str):
        return self._gds(structure_name=page_name,storage_label='dynamic_pages')
        #__________________________________________________________________________
    def get_common_menu(self,web_portal_id:str):
        return self._gds(structure_name=web_portal_id,storage_label='common_menus')
        
    #___________________________________________________
    def dynamic_site(self
                     ,bannertitle:str=''
                     ,banner_subtitle:str=''
                     ,bannerbackground:str=''
                     ,topcontent:str=''
                     ,cookie_max_age_minutes:int=30,jscode:str='',page_name:str=None):
        if page_name == None or page_name == '':
            page_name = request.base_url[::-1].split('/')[0][::-1]
        dynamic_form = self.get_dynamic_page_structure(page_name)
        menu_structure = self.get_common_menu(web_portal_id=self.web_portal_id)
        maincontent,body_style,display_banner,bannertitle_x,banner_subtitle_x,bannerbackground_x,topcontent_x,requires_authentication = self.web.complete_dynamic_form(dynamic_form)
        always_editable = False
        if 'always_editable' in set(dynamic_form.keys()):
            if dynamic_form['always_editable'].lower().replace(' ','') == 'yes':
                always_editable = True
        section_ids = list(dynamic_form['sections'].keys());
        section_load_base = """
        setTimeout(function(){ load_section_by_name("@section_title","load"); },300);
        setTimeout(function(){ load_section_by_name("@section_title","undox"); },2100);
        """
        
        jscode2 = "";
        k = 'sections'
        for i in section_ids:
            isrt = str(i)
            edit_enabled = 'no'
            if 'edit_enabled' in set(dynamic_form[k][isrt].keys()):
                edit_enabled = dynamic_form[k][isrt]['edit_enabled']
            if edit_enabled == 'yes':
                section_title = dynamic_form[k][isrt]['section_title']
                print('section_title:',section_title)
                jscode2 += section_load_base.replace('@section_title',section_title)
            
        jscode2 += """
        """
        if bannertitle == None or bannertitle == '':
            bannertitle = bannertitle_x
            
        if banner_subtitle == None or banner_subtitle == '':
            banner_subtitle = banner_subtitle_x
            
        if bannerbackground == None or bannerbackground == '':
            bannerbackground = bannerbackground_x
            
        if topcontent == None or topcontent == '':
            topcontent = topcontent_x
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        try:
            username = us.split('@')[0]
        except:
            username = us
        common_menu = self.web.create_common_menu(menu_structure,auth=auth,username=username)
        resp = make_response(
            render_template(
                'canvas.html'
                ,web_portal_title=self.web_portal_title
                ,favicon_ico = self.favicon_ico
                ,bannerbackground=bannerbackground
                ,bannertitle=bannertitle
                ,banner_subtitle=banner_subtitle
                ,topcontent=topcontent
                ,common_menu = common_menu
                ,maincontent = maincontent
                ,body_style=body_style
                ,display_banner=display_banner
                ,jscode=jscode
                ,jscode2=jscode2))
        print('page_name: *' + page_name + '*')
        max_age = cookie_max_age_minutes*60
        resp.set_cookie('form_name',page_name,max_age=max_age)
        resp.set_cookie('requires_authentication',str(requires_authentication),max_age=max_age)
        return resp
    #___________________________________________________
    def secure(self):
        json_data = request.json
        if 'data' in set(json_data.keys()):
            try:
                rslt = self.aws.ypt.encrypt(json_data['data'],self.__gen_key)
                print('Secure ok.')
            except:
                rslt = 'Wrong input.'
        else:
            rslt = 'Key not found.'
        return {"co_data":rslt}
    #___________________________________________________
    def ttk(self):
        resp = make_response(redirect('/auth'))
        try:
            us = request.cookies.get('us')
            cpw = request.cookies.get('cpw')
            ttk = self.get_user_temp_token(username_or_email=us,pwd=cpw)
            print('us:',us)
            print('cpw:',cpw)
            print('ttk:',ttk)
            max_age = self.auth_token_max_age_minutes*60
            resp.set_cookie('ttk',ttk,max_age=max_age)
            resp.set_cookie('cpw','')
        except Exception as e:
            print('Error:',str(e))
            resp.set_cookie('ttk','')
            resp.set_cookie('cpw','')
        return resp
    def auth(self,if_authenticated:str,if_not_authenticated:str):
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        if auth == True:
            resp = make_response(redirect(if_authenticated))
        else:
            resp = make_response(redirect(if_not_authenticated))
        return resp
    #___________________________________________________
    def authenticated_endpoint(self
                               ,bannertitle:str=''
                               ,banner_subtitle:str=''
                               ,bannerbackground:str=''
                               ,topcontent:str=''
                               ,redirect_if_not_authenticated:str=None):
        if redirect_if_not_authenticated == None:
            redirect_if_not_authenticated = self.default_redirect_if_not_authenticated
            
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        if auth == True:
            return self.dynamic_site(
                bannertitle=bannertitle
                ,banner_subtitle=banner_subtitle
                ,bannerbackground=bannerbackground
                ,topcontent=topcontent)
        else:
            resp = make_response(redirect(redirect_if_not_authenticated))
            return resp
    #___________________________________________________
    def obtain(self):
        json_data = request.json
        if 'data' in set(json_data.keys()):
            us = request.cookies.get('us')
            ttk = request.cookies.get('ttk')
            folder_reference = json_data['data']
            co_data = self.read_web_portal_json_data(username_or_email=us,temp_token=ttk,folder_reference=folder_reference)
            return {"co_data":co_data}
        else:
            return {"co_data":{"Error:":"Post request not allowed."}}
    #___________________________________________________
    def secure_read_form_data(self,redirect_if_not_authenticated:str=None):
        if redirect_if_not_authenticated == None:
            redirect_if_not_authenticated = self.default_redirect_if_not_authenticated
        if redirect_if_not_authenticated[0:1] == '/':
            l = len(redirect_if_not_authenticated)
            redirect_if_not_authenticated = redirect_if_not_authenticated[1:l]
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        form_name = request.base_url[::-1].split('/')[0][::-1]
        if form_name != None or len(form_name) > 0:
            if ttk != None and ttk != '':
                data = self.read_web_portal_json_data(
                    username_or_email=us
                    ,temp_token=ttk
                    ,folder_reference=form_name
                )
                dynamic_js = ''
                base_code = self.web.dynamic_js['load_data_dynamic_routine']
                jscode = ''
                print('loaded data:',data)
                if type(data) == dict:
                    for k,v in data.items():
                        if type(v) == str:
                            dynamic_js += base_code.replace('@k',k).replace('@v','"' + str(v) + '"')
                        elif type(v) ==  list:
                            dynamic_js += base_code.replace('@k',k).replace('@v','[]')
                            dj = ''
                            for i in v:
                                dj += base_code.replace('@k',k).replace(' = @v;','.push("' + i + '");')
                            dynamic_js += dj
                    jscode = self.web.dynamic_js['load_data_dynamic_code'].replace('@dynamic_js',dynamic_js)
                    print('jscode:',jscode)
                return self.dynamic_site(jscode=jscode,page_name=form_name)
            else:
                return self.dynamic_site(page_name=redirect_if_not_authenticated)
        else:
            return 'Page name not defined.'
    #___________________________________________________
    def secure_save_form_data(self,redirect:bool=False):
        json_data = request.json
        us = request.cookies.get('us')
        form_name = request.cookies.get('form_name')
        requires_auth = request.cookies.get('requires_authentication')
        if requires_auth.lower().replace(' ','') == 'false':
            temp_token = None
            requires_auth = False
        else:
            temp_token = request.cookies.get('ttk')
            requires_auth = True
        if form_name == 'register':
            requires_auth = False
        print('us:',us)
        print('form_name:',form_name)
        print('requires_auth:',requires_auth)
        print('************************************')
        date_id,time_id = self.aws.ypt.date_time_id(local=True)
        last_update = self.aws.ypt.date_time_str(date_id,time_id)
        if json_data != None and json_data != {}:
            print('json_data:',json_data)
            json_data_keys = set(json_data.keys())
            if 'co_main_identifier' in json_data_keys and json_data['co_main_identifier'] in json_data_keys:
                sub_json_data = json_data
                sub_json_data['co_last_update'] = last_update
                co_main_identifier = json_data[json_data['co_main_identifier']]
                sub_json_data.pop('co_main_identifier', None)
                co_sort_order = {}
                if 'co_sort_order' in json_data_keys:
                    co_sort_order = json_data['co_sort_order']
                    sub_json_data.pop('co_sort_order', None)
                us = request.cookies.get('us')
                ttk = request.cookies.get('ttk')
                co_data = {}
                co_data = self.read_web_portal_json_data(username_or_email=us,temp_token=ttk,folder_reference=form_name)
                co_data.pop('co_main_identifier', None)
                co_data.pop('co_sort_order', None)
                co_data[co_main_identifier] = sub_json_data
                co_data['co_sort_order'] = co_sort_order
            else:
                co_data = json_data
                co_data['co_last_update'] = last_update
            print('co_data:',co_data)
            print('folder_reference (where data is being saved):',form_name)
            return self.store_web_portal_json_data(
                username_or_email=us
                ,folder_reference=form_name
                ,json_data=co_data
                ,requires_auth=requires_auth
                ,temp_token=temp_token
                ,redirect=redirect
            )
        else:
            return 'Error SFD01: No storage took place.'
    def get_root_url(self,local:bool=False):
        if local:
            root_url = 'http://localhost'
        else:
            form_name = request.base_url[::-1].split('/')[0][::-1]
            root_url = request.base_url.replace('/' + form_name + '/','').replace('/' + form_name,'') 
        return root_url
    #___________________________________________________
    def generate_confirmation_link(self,username_or_email:str,local:bool=False):
        root_url = self.get_root_url(local=local)
        confirmartion_url = root_url + '/confirm_email?email_confirmation_token='
        dictstr = str(self.aws.ypt.gen_encrypted_data_with_expiration(original_message=username_or_email,minutes_to_expire=60))
        encdat = self.aws.ypt.encrypt(dictstr,self.__gen_key)
        return confirmartion_url + encdat
    #___________________________________________________
    def validate_email_confirmation_link(self):
        try:
            encdat = str(request.args.get("email_confirmation_token"))
            try:
                decdat = self.aws.ypt.decrypt(encdat,self.__gen_key)
                data = self.aws.dictstr_to_dict(decdat)
                username_or_email = self.aws.ypt.decrypt_before_expiration(data)
                response_message = ''
            except:
                response_message = 'Invalid confirmation link.'
            if 'encryption expired' in username_or_email:
                response_message = 'The confirmation link has expired.'
            elif response_message == '' and len(username_or_email) > 4:
                try:
                    self.confirm_user(username_or_email=username_or_email)
                    ch = self.check_user(username_or_email=username_or_email)
                    if str(ch['exists']).lower().replace(' ','') == 'true':
                        if str(ch['confirmed']) == '1':
                            match_type = ch['match_type']
                            what = match_type[0:1].upper() + match_type[1:len(match_type)]
                            response_message = '<h2>' + what + '<br>' + username_or_email + ''\
                            '<br>has been confirmed.<br><p><a style="font-size:20px;color:rgb(19,25,33);" href="/login">'\
                            'Click here to go to login.</a></p></h2>'
                        else:
                            response_message = 'Error CE01: Could not confirm user.'
                    else:
                        response_message = "User does not exist."
                except:
                    response_message = 'Error CE02: Could not confirm user.'
        except:
            response_message = 'Error CE03: email_confirmation_token not provided.'
            
        response_message = response_message.replace('\n','')
        modal_jscode = "setTimeout(pop_content('@response_message'),200);"
        modal_jscode = modal_jscode.replace('@response_message',response_message)
        resp = make_response(
            render_template(
                'canvas.html'
                ,web_portal_title=self.web_portal_title
                ,favicon_ico = self.favicon_ico
                ,modal_jscode=modal_jscode
            ))

        return resp
    #___________________________________________________
    def send_confirmation_email(self):
        local = False
        if 'localhost' in request.base_url.lower().replace(' ',''):
            local = True
        json_data = request.json
        email_banner_img = self.email_banner_img
        if 'email' not in set(json_data.keys()):
            return {'error_message':'email not provided.'}
        else:
            email = json_data['email']
            email_notification_sender = self.notifications_email
            if email_notification_sender == None or email_notification_sender == '':
                return {'error_message':'cloudpy_org_aws_framework_client.notifications_email not set yet.'}
            else:
                confirmation_link = self.generate_confirmation_link(username_or_email=email,local=local)
                root_url = self.get_root_url(local=local)
                SENDER = email_notification_sender
                RECIPIENT = email
                #AWS_REGION = self.region_name
                SUBJECT = self.web_portal_title + " - Email Confirmation"
                BODY_TEXT = ("")
                BODY_HTML = """<html>
                <head>
                <style>
                @font-face {
                  font-family: sensationLight;
                  src: url("@root_url/static/fonts/sansation_light.woff");
                }
                </style>
                </head>
                <body>
                <div class="text-center" style="width:800px;">
                  <img src="@root_url/static/img/@email_banner_img" alt="" style="max-width:800px;">
                  <br>
                  <h3 style="color:gray;font-family:sensationLight;">Thank you for registering!</h3>
                  <br>
                  <h2 style="color:black;font-family:sensationLight;">Please click 
                  <a href="@confirmation_link" style="color:blue;font-family:sensationLight;">
                  HERE
                  </a> to confirm your email.</h2>
                  </div>
                </body>
                </html>
                """
                BODY_HTML = BODY_HTML.replace("@root_url",root_url)\
                .replace("@confirmation_link",confirmation_link)\
                .replace("@email_banner_img",email_banner_img)
                CHARSET = "UTF-8"
                client = self.ses
                try:
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': CHARSET,
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': CHARSET,
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                        #ConfigurationSetName=CONFIGURATION_SET,
                    )
                    return {'success':'email sent'}
                except Exception as e:
                    return {'error_message':str(e)}
                
    #___________________________________________________
    def register_new_user(self):
        rslt_template = '<textarea class="sensation" onclick="pop_off();" style="cursor:default;font-size:16px;width:500px;height:200px;border:none" rowsnum=5>@rslt</textarea>'
        try:
            email = request.cookies.get('us').lower().strip()
            pwd = request.cookies.get('cpw').strip()
            cpwconf = request.cookies.get('cpwconf').strip()
        except Exception as e:
            email = ''
            pwd = ''
            cpwconf = ''
        rslt = ''
        if email != None and email != '' and pwd != None and pwd != '' and cpwconf != None and cpwconf != '': 
            if self.aws.ypt.validate_str_as_email(email):
                username = email.split('@')[0]
                if self.domain_to_restrict_access_to != None and self.domain_to_restrict_access_to != '':
                    if self.domain_to_restrict_access_to in email:
                        if email.split('@')[1] != self.domain_to_restrict_access_to:
                            rslt = 'The email provided does not belong to the "' + self.domain_to_restrict_access_to + '" domain.'
                    else:
                        rslt = 'The email provided does not belong to the "' + self.domain_to_restrict_access_to + '" domain.'
                if rslt == '':
                    pwd_validation = self.aws.ypt.validate_password_format(pwd)
                    if  pwd_validation.lower().replace(' ','') == 'ok':
                        print('pwd validated')
                        if pwd == cpwconf:
                            rslt = self.create_user(username=username,email=email,pwd=pwd)
                            json_data={}
                            json_data['email'] = email
                            local = False
                            if 'localhost' in request.base_url.lower().replace(' ',''):
                                local = True
                            root_url = self.get_root_url(local=local)
                            url = root_url + '/send_confirmation_email'
                            confirmation_rslt = requests.post(url=url,json=json_data ,verify=False).json()
                            print('confirmation_rslt:',confirmation_rslt)

                        else:
                            rslt = 'Password and password confirmation must match.'
                    else:
                        rslt = pwd_validation
                        print(rslt)
            else:
                rslt = 'Invalid email input. Please make sure you typed a valid email address.'
        else:
            rslt = 'Missing input.'
        rslt = rslt_template.replace('@rslt',rslt)
        return {"co_data":rslt}