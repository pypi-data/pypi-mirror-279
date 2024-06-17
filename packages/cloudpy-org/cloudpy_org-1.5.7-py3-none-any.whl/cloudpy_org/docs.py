"""
███████████████████████████docs of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import cloudpy_org_version,processing_tools
from typing import Union
import inspect
import os
pt = processing_tools()
class auto_document:
    def __init__(self):
        self.load_classes_and_methods()
    #__________________________________________________________________________
    def automatic_documentation(self,module_name_or_invocation:str="", destiny_path:str=None)->None:
        if destiny_path != None:
            if destiny_path[::-1][0:1] == '/' or destiny_path[::-1][0:1] == '\\':
                ...
            elif '\\' in destiny_path:
                destiny_path += '\\'
            elif '/' in destiny_path:
                destiny_path += '/'
            pt.documentation_path = destiny_path
        else:
            pt.documentation_path = pt.local_directory + 'documentation/'
        pt.documentation_JSON_path = pt.documentation_path + "json/"
        if "from " in module_name_or_invocation or "import " in module_name_or_invocation:
            mod_name = module_name_or_invocation.split("import")[1].replace(' ','')
        else:
            mod_name = module_name_or_invocation
            module_name_or_invocation = "import " + mod_name
        
        dynamic_code = '@module_name_or_invocation\n'\
        'self.pre_gen_automatic_documentation(@mod_name,outputFileName="@mod_name")'
        dynamic_code = dynamic_code.replace("@module_name_or_invocation",module_name_or_invocation).replace("@mod_name",mod_name)
        exec(dynamic_code)
    #__________________________________________________________________________
    def load_classes_and_methods(self)->None:
        '''
        ***
        If classes_and_methods.json already exists in the documentation
        path, it is then being uploaded into the self.classes_and_methods
        instance class as a dict. Otherwhise the self.classes_and_methods dict
        will be by default empty.
        ***
        '''
        self.classes_and_methods = {}
        self.classes_and_methods_path = pt.documentation_path + "classes_and_methods.json"
        if os.path.exists(self.classes_and_methods_path):
            with open(self.classes_and_methods_path,'r') as f:
                self.classes_and_methods = json.loads(f.read())
    #__________________________________________________________________________
    def get_methods_and_functions(self,moduleObject:object,className:str)->set:
        '''
        ***
        Given an instance of a class, returns a set of it's availabla methods or functions.
        ***
        '''
        self.temp_methods_and_functions = set()
        dc = 'self.temp_methods_and_functions = '\
        'set([x for x in '\
        'list(dict(inspect.getmembers(moduleObject.' + className + '()'\
        ',predicate=inspect.ismethod)).keys()) '\
        'if len(x.split("__")) == 1])'
        try:
            exec(dc)
        except:
            ...
        return self.temp_methods_and_functions
    #__________________________________________________________________________
    def get_classes_names(self,moduleObject:object,nestLevel:int=0)->set:
        '''
        ***
        Given an instance of a module, returns a set with the names of all the existing classes within it.
        ***
        '''
        objectName = pt.retrieve_object_name(moduleObject)
        a = objectName + "."
        raw_set = set([str(x[0]) for x in inspect.getmembers(moduleObject,inspect.isclass) if len(str(x[1]).split('.')) == 2 + nestLevel])
        classes_set = set()
        for cn in raw_set:
            if len(self.get_methods_and_functions(moduleObject,cn)) > 0:
                classes_set.add(cn)
        return classes_set
    #__________________________________________________________________________
    def pre_gen_automatic_documentation(self,moduleOrLibraryInstance:object,onlyThisClassName:str=None,outputFileName:str=None)->None:
        '''
        ***
        Given an instance of a module (moduleOrLibraryInstance parameter), returns a dictionary with relevant information about it in the following format:
         {
             "classA":{
                 "methodOrFunctionA1":{
                     "source_code":"<the source code of the method or function>",
                     "arguments":"<if existing, the arguments of the method or function>"
                     "returns":"<in case is a function, the type of output it returns>"
                     "description":"<any text or description within the method of function source code that is written between acb123*acb123*acb123* and acb123*acb123*acb123*. Example: acb123*acb123*acb123*some description textacb123*acb123*acb123*>"
                     "dependencies": "<the other functions or methods within the same class that depend from this function or method>",
                 "methodOrFunctionA2":{
                     ...
                 }
                 },
            "classB":{
                "methodOrFunctionB1":{
                    ...,
            }
                 }

                }
         }
        Note: If onlyThisClassName argument is different than None, then only that className reference will be in scope as long as it belong to the given module
        ***
        '''

        rslt = {}
        theseClassesSet = set()
        if onlyThisClassName != None:
            theseClassesSet.add(onlyThisClassName)
        else:
            theseClassesSet = self.get_classes_names(moduleOrLibraryInstance)
        for a in theseClassesSet:
            rslt[a] = {}
            for b in self.get_methods_and_functions(moduleOrLibraryInstance,a):
                source_code,arguments,this_returns,description = self.method_or_function_insight(moduleOrLibraryInstance,a,b)
                source_code  = source_code.replace('"','\\"')
                rslt[a][b] = {}
                #rslt[a][b]["source_code"] = source_code
                rslt[a][b]["arguments"] = arguments
                rslt[a][b]["returns"] = this_returns.replace('Union[','').replace(']','')
                rslt[a][b]["description"] = description.replace("acb123*acb123*acb123*","***")
                rslt[a][b]["dependencies"] = self.source_code_dependencies(
                    moduleOrLibraryInstance=moduleOrLibraryInstance
                    ,source_code=source_code)
        if outputFileName == None:
            filename_without_ext = "methods_and_functions"
        else:
            filename_without_ext = outputFileName[::-1].split(".")[0][::-1]
        if not os.path.exists(pt.documentation_path):
            os.makedirs(pt.documentation_path)
        if not os.path.exists(pt.documentation_JSON_path):
            os.makedirs(pt.documentation_JSON_path)
        try:
            pt.standard_dict_to_json(jsonOrDictionary=rslt
                                             ,fileName=filename_without_ext + ".json"
                                             ,folderPath=pt.documentation_JSON_path)
            self.load_classes_and_methods()
            print("Documentation sucessfully created at:\n" + pt.documentation_path)
        except Exception as e:
            print(e)
    #__________________________________________________________________________
    def source_code_dependencies(self,moduleOrLibraryInstance:object,source_code:str)->None:
        '''
        ***
        Given a source_code within a module, returns the same module's functions or methods depencies within it.
        ***
        '''
        u = source_code
        classNames = self.get_classes_names(moduleOrLibraryInstance)
        dependencies = {}
        for className in classNames:
            methods_and_functions = self.get_methods_and_functions(moduleOrLibraryInstance,className)
            for x in methods_and_functions:
                y="." + x + "("
                if y in u:
                    if className not in set(dependencies.keys()):
                        dependencies[className] = []
                    if x not in dependencies[className]:
                        dependencies[className].append(x)
        if dependencies == {}:
            return "No dependencies"
        else:
            return dependencies
    #__________________________________________________________________________
    def method_or_function_insight(self,moduleOrLibraryInstance:object,className:str,methodOrFunction:str)->Union[str,dict,str,str]:
        '''
        ***
        Returns source code (st), arguments (dict), type (str) and description (str) of a given method or function name of a given class name.
        ***
        '''
        moduleOrLibraryInstanceName = pt.retrieve_object_name(moduleOrLibraryInstance)
        self.theseparams,self.this_source_code,self.this_returns,self.this_description = {},"N/A", "N/A", "N/A"
        dynamic_code='source_code = inspect.getsource('+ moduleOrLibraryInstanceName + '.' + className + "." + methodOrFunction + ')\n'\
        'params = source_code.split("(")[1].split(")")[0].replace("","").replace("self,","").split(",")\n'\
        'if "->" in source_code:\n'\
        '\tself.this_returns = source_code.split("->")[1].split(":")[0].strip()\n'\
        'if "***" in source_code:\n'\
        '\tself.this_description=source_code.split("***")[1].strip()\n'\
        'p={}\n'\
        'for i in range(0,len(params)):\n'\
        '\tj=i+1\n'\
        '\tp[j]={}\n'\
        '\tb=params[i].split(":")\n'\
        '\tp[j]["name"]=b[0].strip()\n'\
        '\tif p[j]["name"]!="self":\n'\
        '\t\tp[j]["datatype"]="N/A"\n'\
        '\t\tif len(b)>1:\n'\
        '\t\t\tif "=" in b[1]:\n'\
        '\t\t\t\tp[j]["datatype"]=b[1].split("=")[0].strip()\n'\
        '\t\t\t\tp[j]["default_value"]=b[1].split("=")[1].strip().replace("\\"","")\n'\
        '\t\t\telse:\n'\
        '\t\t\t\tp[j]["datatype"]=b[1].strip()\n'\
        '\t\t\t\tp[j]["default_value"]="N/A"\n'\
        '\t\t\tif p[j]["default_value"] != "None" and p[j]["datatype"] == "str":\n'\
        '\t\t\t\tp[j]["default_value"]=\"\\"\" + p[j]["default_value\"] + \"\\"\"\n'\
        '\telse:\n'\
        '\t\tp[j]="No parameters."\n'\
        'self.theseparams=p\n'\
        'self.this_source_code=source_code'
        self.this_description = self.this_description.replace("  "," ").replace("#","\n").strip()
        exec(dynamic_code)
        return self.this_source_code, self.theseparams, self.this_returns, self.this_description
def convert_jupiter_notebook_to_html(folder_path:str,jupyter_notebook_file_name:str):
    jupyter_notebook_file_name = jupyter_notebook_file_name.split(".")[0] + '.ipynb'
    command = 'jupyter nbconvert --to html ' + folder_path + jupyter_notebook_file_name
    os.system(command)
def documentation_from_folder(documentation_destiny_path:str,origin_folder_path:str=None):
    begin_comment = '<!--' 
    end_comment = '--><div class="jp-InputPrompt jp-InputArea-prompt"></div>'
    a = '<div class="jp-InputArea jp-Cell-inputArea">'
    b = '<div class="jp-CodeMirrorEditor jp-Editor jp-InputArea-editor" data-type="inline">'
    b_with_style = '<div class="jp-CodeMirrorEditor jp-Editor jp-InputArea-editor" data-type="inline" style="background-color:rgb(230,230,230);">'
    c = '<div class=" highlight hl-ipython3">'
    c_with_style = '<div class=" highlight hl-ipython3" style="background-color:rgb(230,230,230);">'
    d = '<!-- Load mathjax -->'
    if origin_folder_path == None:
        origin_folder_path = os.getcwd() + '/docs/'
    files = pt.find_files_in_folder(path=origin_folder_path,extension='ipynb')
    for file in files:
        u = origin_folder_path + file.replace('.ipynb','.html')
        convert_jupiter_notebook_to_html(folder_path=origin_folder_path,jupyter_notebook_file_name=file)
        with open(u,'rb') as f:
            x = f.read().decode()
            x = x.split(d)[1]
            x = x.replace(a + begin_comment,a).replace(a,a + begin_comment).replace(end_comment + b,b).replace(b,end_comment + b)
            x = x.replace(b,b_with_style)
            x = x.replace(c,c_with_style)
            x = x.replace('</html>','').replace('<body','<div').replace('</body','</div').replace('</head>','')
            x = x.replace('"',"'")
        my_path = documentation_destiny_path + file.replace('.ipynb','_doc.html')
        with open(my_path,'wb') as f:
            f.write(x.encode('utf-8'))