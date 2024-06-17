from cloudpy_org import processing_tools
import os
import json
this_dict = {}
#___________________________________________________
k = 'select'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<select id="@id" class="sensation inx" onchange="temp_input(this,'@k','');" onload="load_input(this,'@k','');">
@options
</select>
<br>
""".replace('@k',k)
this_dict[k]['object'] = "<option>@object</option>"
this_dict[k]['params'] = ['@id','@label_title','@options']
#___________________________________________________
k = 'radios_horizontal'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
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
<input type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="load_input(this,'@k','@object');">
<label for="@id_@n" class ="sensation">@object</label>
</span>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'radios_vertical'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
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
<input type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="load_input(this,'@k','@object');">
<label for="@id_@n" class ="sensation">@object</label>
</div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'text_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<input id="@id" class="sensation" type="text" value="@text_content" style="border-bottom-width:1px;" oninput="temp_input(this,'@k','');" onload="load_input(this,'@k','');">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'pwd_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<input id="@id" class="sensation" type="password" value="@text_content" style="border-bottom-width:1px;" oninput="temp_input(this,'@k','');" onload="load_input(this,'@k','');">
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
<button id="@id" class="submitrequest" style="width:100%;" onclick="temp_input(this,'@k','');" onload="load_input(this,'@k','');">@label_title</button>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'text_area'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation">@label_title</label>
<br>
<textarea id="@id" class="sensation inx" rows="@rowsnum" oninput="temp_input(this,'@k','');" onload="load_input(this,'@k','');">@text_content</textarea>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@rowsnum']
#___________________________________________________
k = 'acc_checkboxes'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<div class='accordion' id='acc_@id'>
<div class="accordion-item" style="font-size:14px;">
<h2 class="accordion-header" id="@id">
<button class="accordion-button collapsed sensation" style="font-size:14px;padding:7px;" type="button" data-bs-toggle="collapse" 
data-bs-target="#collapse_@id" aria-expanded="false" aria-controls="collapseOne">
@label_title
<a id="@id_counter_container" style="position:absolute;left:@counter_leftpx;color:#252F3E;display:none;"><span id="@id_counter" 
style="padding-right:10px;">0</span><span>selected</span></a>
</button>
</h2>
<div id="collapse_@id" class="accordion-collapse collapse" aria-labelledby="@id" 
data-bs-parent="#acc_@id" style="">
<div class="accordion-body">
@options
</div></div></div>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """<div style="padding:7px;"><input type="checkbox" id="@id_checkbox_@n" onclick="service_counter(this,'@id');"><label class="sensation" for="@id_checkbox_@n">@object</label></div>
"""
this_dict[k]['params'] = ['@id','@label_title','@options','@n','@counter_left']
#*******************************sections
this_sections = {}
k = 'right_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border-right:solid 1px orange;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
#___________________________________________________
k = 'left_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border-left:solid 1px orange;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']

#___________________________________________________
k = 'no_border'
this_sections[k] = {}
this_sections[k]['html'] = """
<div id="@section_id" class="col-lg-@n" style="padding-right:10px;border:none;">
<h5 class="sensation" style="color:#252F3E;font-weight:800;">@section_title</h5>
@content
</div>
""".replace('@k',k)
this_sections[k]['params'] = ['@section_title','@n','@content']
main_dict = {}
main_dict['sections'] = this_sections
main_dict['inputs'] = this_dict
class cloudpy_org_web_client:
    def __init__(self, **kwargs):
        self.main_dict = main_dict
        self.pt = processing_tools()
        self.current_path = os.getcwd() + '/'
        #with open (self.current_path + 'dynamic_html.json', 'r') as f:
        #    self.main_dict = json.loads(f.read())
    #___________________________________________________
    def create_section(self,section_title:str,section_type:str='right_border',size:int=2):
        a = self.pt.camel_to_snake(section_title).replace('?','').replace('.','_').replace(',','')
        section_id = a[0:6] + a[::-1][0:6][::-1]
        rslt = self.main_dict['sections'][section_type]['html']\
        .replace('@section_id',section_id)\
        .replace('@section_title',section_title)\
        .replace('@n',str(size))
        return rslt.replace('\n','')
    #___________________________________________________
    def create_input(self,input_type:str,label_title:str,options:list=[],text_content:str='',rowsnum:int=3,section_size:int=3):
        counter_left = (section_size-1)*120 + 20
        a = self.pt.camel_to_snake(label_title)[0:12].replace('?','').replace('.','_').replace(',','')
        this_id = a[0:6] + a[::-1][0:6][::-1]
        rslt = self.main_dict['inputs'][input_type]['html']\
        .replace('@id',this_id)\
        .replace('@label_title',label_title)
        if input_type in ['select','radios_horizontal','radios_vertical','acc_checkboxes']:
            opti = ''
            obj = self.main_dict['inputs'][input_type]['object']
            n = 0
            for this_option in options:
                n+=1
                opti += obj.replace('@object',this_option)\
                .replace('@n',str(n))\
                .replace('@id',this_id)
            rslt = rslt.replace('@options',opti).replace('@counter_left',str(counter_left))
        elif input_type in['text_input','pwd_input','text_area']:
            rslt = rslt.replace('@text_content',text_content)
            if input_type == 'text_area':
                rslt = rslt.replace('@rowsnum',str(rowsnum))
        return rslt.replace('\n','')
    #___________________________________________________
    def complete_dynamic_form(self,dynamic_form:dict):
        sections = ''
        section_nums = list(dynamic_form['sections'].keys())
        section_nums.sort()
        for i in section_nums:
            ts = dynamic_form['sections'][i]
            inputs = ts['inputs']
            section_size = ts['size']
            section = self.create_section(
                section_title=ts['section_title']
                ,section_type=ts['section_type']
                ,size=section_size)
            content = ""
            for j in inputs:
                if j['input_type'] in['text_input','pwd_input','text_area']:
                    text_content = ''
                    if 'text_content' in set(j.keys()):
                        text_content=j['text_content']
                    if j['input_type'] == 'text_area':
                        rowsnum = j['rowsnum']
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,rowsnum=rowsnum
                            ,section_size=section_size)
                    else:
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size)
                else:
                    options = []
                    if 'options' in set(j.keys()):
                        options=j['options']
                    content += self.create_input(
                        input_type=j['input_type']
                        ,label_title=j['label_title']
                        ,options=options
                        ,section_size=section_size)
            sections += section.replace('@content',content) 
        complete_form = '<div class="row" style="width:1600px;position:relative;left:50px;top:-10px;">@sections</div>'
        complete_form =complete_form.replace('@sections',sections)
        return complete_form
