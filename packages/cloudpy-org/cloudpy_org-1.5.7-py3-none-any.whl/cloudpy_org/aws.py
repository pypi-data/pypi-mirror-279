"""
███████████████████████████aws of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import cloudpy_org_version,gsep,processing_tools,aws_regions,subscription_url,msh
import requests
import inspect
import json
import os
import random
import time
unique_id = lambda: int(round(time.time() * 100000))
xpt = processing_tools()
xpt.environment = "s3"
class aws_framework_manager:
    def __init__(self,secret_key:str,aws_auth_token:str="",aws_namespace:str="",region_name:str="us-east-2"):
        self.region_name = region_name
        self.msh = subscription_url.replace('w'*3,msh) + '/'
        self.regions = aws_regions
        self.aws_namespace = aws_namespace
        self.__deconstructor_token = 'JQxrs8sWqn3JIWlIL8nTlw-302SfmV7RmlZ-T-gB5c4=oiwn8TU5-NcDKzVq'
        uuu = "1V44bjdzKODcN50jdz00c4="
        self.__sc = secret_key[::-1].split(uuu)
        self.__at = aws_auth_token[::-1].split(uuu)
        self.cppt_construction(self.__sc[1])
        self.cppt.environment = "s3"
        self.ypt_construction(self.__at[1])
        self.ypt.environment = "s3"
        self.general_info = {}
        self.service_name = "cloudpy-org-service-beta"
        self.delimiters = ["pZo-9xH9oEO2B2OEo","2nZzN01wtktk10N","VhMxT-9xVVZzN01w","_Shv-4F86Co981h"]
        self.general_separators = gsep
        self.special_separators = self.general_separators
        self.__service_initialized = False
        self.__not_initialized_message ='Service not initialized yet.\n'\
        'Use initialize_service(service_token="<your service_token>") function to active the service.\n'
    #___________________________________________________________________
    def __do(self,a,n,upper:bool=True):
        a = a[::-1]
        b,c = "",""
        r = int(len(a)/n) + 1
        for i in range(0,r):
            b += a[2*i*n:(2*i+1)*n]
            c += (a[(2*i+1)*n:(2*i+2)*n][::-1])
            if i == r-1:
                b += c[::-1][0:n]
                c = c.replace(c[::-1][0:n][::-1],'')
        if upper:
            c = c.upper()
        return c,b
    #___________________________________________________________________
    def cppt_construction(self,secret_key:str=""):
        if len(secret_key) > 10:
            k = self.__deconstructor_token
            self.cppt = processing_tools(data=xpt.basic_dicstr_to_dict(xpt.decrypt(secret_key,self.__do(k,10,False)[1] + self.__do(k,10,False)[0][0:4]))
                                         ,region_name=self.region_name)
        else:
            self.cppt = processing_tools(region_name=self.region_name)
    def ypt_construction(self,aws_auth_token:str=""):
        if len(aws_auth_token) > 10:
            k = self.__deconstructor_token
            self.ypt = processing_tools(data=xpt.basic_dicstr_to_dict(xpt.decrypt(aws_auth_token,self.__do(k,10,False)[1] + self.__do(k,10,False)[0][0:4]))
                                        ,region_name=self.region_name)
        else:
            self.ypt = processing_tools(region_name=self.region_name)
    #___________________________________________________________________
    def initialize_service(self,service_token:str,version:str=cloudpy_org_version,test_file_name:str=None,test_folder_path:str=None):
        self.__initialize_error_message = 'Could not initialize the service. Please verify you are using the right service token.'
        self.args_by_key,self.dx = {},{}
        succes_message =  'cloudpy-org AWS framework manager client: service initialized.'
        try:
            for i in range(0,1):
                self.args_by_key,self.dx = {},{}
                self.__api_encrypted_caller = self.__sc[2]
                self.__get_dynamic_response(service_token=service_token,version=version,test_file_name=test_file_name,test_folder_path=test_folder_path)
                self.find_methods_arguments()
                self.set_valid_characters()
                self.version = self.get_version()
            if self.__service_initialized:
                messagex = succes_message
                if self.ypt.aws_auth_error_message != None and self.ypt.aws_auth_error_message != "":
                    messagex += "\nThe following exceptions have been found:\n" +  self.ypt.aws_auth_error_message
                return messagex
            else:
                return self.__initialize_error_message
        except Exception as e:
            print("error 01:",str(e))
            return self.__initialize_error_message
    #___________________________________________________________________
    def _load_local_code(self,file_name,folder_path:str=None):
        if folder_path == None:
            folder_path = os.getcwd() + "/"
        with open(folder_path + file_name, 'r') as f:
            rslt = json.loads(f.read())
        return rslt
    #___________________________________________________________________
    def __k(self,tagStr:str):
        self.last_k = self.cppt.gen_encrypted_data_with_expiration(self.cppt.get_s3_file_content(referenceName=tagStr,s3FullFolderPath="s3://" + self.service_name + "/settings/secrets/"),1)
    
    #___________________________________________________________________
    def __get_dynamic_response(self,service_token:str,version:str,test_file_name:str=None,test_folder_path:str=None):
        self.__k("service_key")
        dc = self.cppt.decrypt(self.__api_encrypted_caller,self.cppt.decrypt_before_expiration(self.last_k))\
        .replace("@version",version)\
        .replace("@gsm",self.__gsm(service_token))
        self.__k("cloudpy_org_2023")
        if test_file_name != None and len(test_file_name) > 4:
            replace_this = "x = self.cppt.get_s3_file_content(referenceName=referenceName,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)"
            if test_folder_path == None:
                with_this = "x = self._load_local_code(file_name = '" + test_file_name + "')"
            else:
                with_this = "x = self._load_local_code(file_name = '" + test_file_name + "',folder_path = '" + test_folder_path + "')"
            dc = dc.replace(replace_this,with_this)
        try:
            exec(dc)
            del self.last_k
            self.__service_initialized = True
        except Exception as e:
            print("error 02:",str(e))
            if test_file_name != None:
                print('printing from test_file_name:')
                print(dc)
            self.__service_initialized = False
        try:
            self.dynamic_code_response = self.ddxx[service_token + self.ddkk]
            del self.ddkk
            del self.ddxx
        except:
            self.dynamic_code_response = {}
        try:
            del self.ddkk
            del self.ddxx
        except:
            ...
    #___________________________________________________________________
    def _decorator(decorator_param):
        def inner_func(self,dk):
            k = dk + "_is_function"
            dc = "self.dx['@k'] = self.dynamic_exec(dynamic_key='@dynamic_key'@these_args)"
            dc = dc.replace("@dynamic_key",dk)\
            .replace("@k",k)\
            .replace("@these_args",self.__args_applied[dk])
            exec(dc)
            is_function = self.dx[k]
            self.dx.pop(k, None)
            rslt = None
            if dk in set(self.dx.keys()):
                if is_function:
                    rslt = self.dx[dk]
                self.dx.pop(dk, None)
            self.reset_args_applied(dk)
            if rslt == None:
                rslt = "Encryption expired."
            return rslt
        return inner_func
    #___________________________________________________________________
    @_decorator
    def deco(self,dk:str):
        ...
    #___________________________________________________________________
    def get_methods(self):
        return {method for method in dir(aws_framework_manager) if method.startswith('_') is False}
    #___________________________________________________________________
    def find_methods_arguments(self):
        self.methods_args,self.__args_applied,dc,x = {},{},"","self.methods_args['@i'] = self.arguments_list(self.@i)\n"
        for i in self.get_methods():
            dc += x.replace("@i",i)
        exec(dc)
        self.reset_args_applied()
    #___________________________________________________________________
    def reset_args_applied(self,only_this_case:str=None):
        if only_this_case != None and only_this_case in set(self.methods_args.keys()):
            x = ""
            for i in self.methods_args[only_this_case]:
                x +=  "," + i + " = @" + i
            self.__args_applied[only_this_case] = x
        else:
            for k,v in self.methods_args.items():
                x = ""
                for i in v:
                    x +=  "," + i + " = @" + i
                self.__args_applied[k] = x
    #___________________________________________________________________
    def arguments_list(self,func):
        return [i for i in func.__code__.co_varnames[:func.__code__.co_argcount] if i != "self"]
    #___________________________________________________________________
    def dynamic_exec(self,dynamic_key:str,**kwargs):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            dc_enc = self.dynamic_code_response[dk]["val"]
            dc = self.cppt.decrypt_before_expiration(dc_enc)
            dc = dc.replace("@dynamic_key",dynamic_key)
            self.args_by_key[dynamic_key] = kwargs
            try:
                exec(dc.replace("self.__dynamic_code_response","self.dynamic_code_response"))
            except Exception as e:
                print("error 03:",str(e))
                self.dx[dk] = ''
            return self.dx[dk]
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def set_valid_characters(self):
        if self.__service_initialized:
            return self.deco(dk=str(inspect.getframeinfo(inspect.currentframe()).function))
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def get_version(self):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def format_folder_or_file_name(self,strInput:str,isFile:bool=False):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@strInput","'" + strInput + "'")\
            .replace("@isFile",str(isFile))
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________  
    def create_s3_framework(self,sufix:str,region:str="us-east-2",local:bool=False):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@sufix","'" + sufix + "'")\
            .replace("@region","'" + region + "'")\
            .replace("@local",str(local))
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def create_folder(self,bucket_name:str,folder_name:str,format_folder_or_file_name:bool=False):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@bucket_name","'" + bucket_name + "'")\
            .replace("@folder_name","'" + folder_name + "'")\
            .replace("@format_folder_or_file_name",str(format_folder_or_file_name))
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def load_s3_framework(self,bucket_name:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@bucket_name","'" + bucket_name + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def create_new_user(self,sufix:str=None,region:str=None,username:str=None,email:str=None,pwd:str=None):
        if sufix != None and region != None and username != None and email != None and pwd != None:
            if self.__service_initialized:
                dk=str(inspect.getframeinfo(inspect.currentframe()).function)
                self.__args_applied[dk]= self.__args_applied[dk]\
                .replace("@sufix","'" + sufix + "'")\
                .replace("@region","'" + region + "'")\
                .replace("@username","'" + username + "'")\
                .replace("@email","'" + email + "'")\
                .replace("@pwd","'" + pwd + "'")
                return self.deco(dk=dk)
            else:
                return self.__not_initialized_message
        else:
            return 'Wrong parameters input.'
    #___________________________________________________________________
    def treat_none_strings(self,object_str:str,paramName:str,paramValue:str):
        if paramValue != None:
            object_str = object_str.replace("@" + paramName,"'" + paramValue + "'")
        else:
            object_str = object_str.replace("@" + paramName,str(paramValue))
        return object_str
    #___________________________________________________________________
    def check_if_user_exists_and_was_confirmed(self,username_or_email:list,bucket_name:str=None,sufix:str=None,region:str=None):
        if type(username_or_email) == str:
            username_or_email = [username_or_email]
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk] = self.__args_applied[dk]\
            .replace("@username_or_email",str(username_or_email))
            self.__args_applied[dk] = self.treat_none_strings(self.__args_applied[dk],'bucket_name',bucket_name)
            self.__args_applied[dk] = self.treat_none_strings(self.__args_applied[dk],'sufix',sufix)
            self.__args_applied[dk] = self.treat_none_strings(self.__args_applied[dk],'region',region)
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    def service_check_if_user_exists_and_was_confirmed(self,username_or_email:list,bucket_name:str):
        if type(username_or_email) == str:
            username_or_email = [username_or_email]
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@username_or_email",str(username_or_email))\
            .replace("@bucket_name","'" + bucket_name + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def framework_loaded(self,bucket_name:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@bucket_name","'" + bucket_name + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def load_user_data(self,username:str,bucket_name:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@username","'" + username + "'")\
            .replace("@bucket_name","'" + bucket_name + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def create_token_with_expiration(self,username:str,pwd:str,bucket_name:str,minutes_to_expire:int=10):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@username","'" + username + "'")\
            .replace("@pwd","'" + pwd + "'")\
            .replace("@bucket_name","'" + bucket_name + "'")\
            .replace("@minutes_to_expire",str(minutes_to_expire))
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def dictstr_to_dict(self,dictstr:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@dictstr","'''" + dictstr + "'''")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message
    #___________________________________________________________________
    def validate_token(self,username:str,token:str,bucket_name:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@username","'" + username + "'")\
            .replace("@token","'" + token + "'")\
            .replace("@bucket_name","'" + bucket_name + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message

#*format_bucket_name*begin
    #___________________________________________________________________
    def format_bucket_name(self,sufix:str,region:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@sufix","'" + sufix + "'")\
            .replace("@region","'" + region + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message

#*format_bucket_name*end
#*get_bucket_name*begin
    #___________________________________________________________________
    def get_bucket_name(self,sufix:str,region:str):
        if self.__service_initialized:
            dk=str(inspect.getframeinfo(inspect.currentframe()).function)
            self.__args_applied[dk]= self.__args_applied[dk]\
            .replace("@sufix","'" + sufix + "'")\
            .replace("@region","'" + region + "'")
            return self.deco(dk=dk)
        else:
            return self.__not_initialized_message

#*get_bucket_name*end
#new function here
    
    #*******************************************************************
    
    #___________________________________________________________________
    def get_s3_reference_name(self,username:str,email:str):
        referenceName = username + self.general_separators["user_email_sep"] + email
        for i in {x for x in set(self.general_separators.keys()) if x != "user_email_sep"}:
            referenceName = referenceName.replace(i,self.general_separators[i])
        return referenceName
    #___________________________________________________________________
    def gen_service_token(self,username:str,email:str):
        date_id,time_id = self.cppt.date_time_id()
        n = random.randint(1,100)
        inputStr = str(random.randint(0,10000)) 
        inputStr += str(time_id)[::-1] 
        inputStr += "-3-cloudpy-org-3-" 
        inputStr += self.get_s3_reference_name(username=username,email=email) 
        inputStr += "-3-cloudpy-org-3-" + str(date_id) + "_" + str(time_id)
        rslt = self.cppt.encrypt(inputStr = inputStr,keyStr=self.cppt.get_s3_file_content(referenceName="tek",s3FullFolderPath="s3://" + self.service_name + "/settings/secrets/")[str(n)])
        part1 = rslt[0:int(len(rslt)/2)]
        part2 = rslt.replace(part1,"")
        delimiter = self.delimiters[random.randint(0,3)] 
        rslt = part1 + delimiter + str(n) + delimiter + part2
        return rslt
    #___________________________________________________________________
    def reference_from_service_token(self,service_token:str):
        delimiter,u,error_message = "","-3-cloudpy-org-3-","Invalid service token."
        for i in self.delimiters:
            x = service_token.split(i)
            if len(x) == 3:
                delimiter = i
                break
        if delimiter != "":
            service_token = x[0] + x[2]
            rslt = self.cppt.decrypt(inputStr=service_token,keyStr=self.cppt.get_s3_file_content(referenceName="tek",s3FullFolderPath="s3://" + self.service_name + "/settings/secrets/")[x[1]])
            if u in rslt:
                rslt = rslt.split(u)[1]
            else:
                rslt = error_message
        else:
            rslt = error_message
        return rslt
    #___________________________________________________________________
    def get_service_data(self,service_token:str):
        data = self.cppt.get_s3_file_content(
            referenceName = self.reference_from_service_token(service_token=service_token)
            ,s3FullFolderPath="s3://" + self.service_name + "/settings/secrets/users/")
        del data["encrypted_pwd"]
        del data["token"]
        data["service_token"] = service_token
        return data
    #___________________________________________________________________
    def test_data(self,service_token:str):
        print(self.reference_from_service_token(service_token=service_token))
        print("s3://" + self.service_name + "/settings/secrets/users/")
        return self.cppt.get_s3_file_content(
            referenceName = self.reference_from_service_token(service_token=service_token)
            ,s3FullFolderPath="s3://" + self.service_name + "/settings/secrets/users/")
    #___________________________________________________________________    
    def __gsm(self,service_token:str):
        date_id,time_id = self.cppt.date_time_id()
        dat = self.ypt.basic_dicstr_to_dict(self.__sc[0])
        rslt = {'encrypted_content': dat['encrypted_content']
                ,'keystr_with_expiration': dat['keystr_with_expiration']
                ,'date_id': date_id
                ,'timestr': self.cppt.seconds_to_timestr(time_id)
                ,'service_token': service_token}
        del dat
        return str(rslt)


def aws_framework_manager_client(
    service_token:str = ""
    ,aws_namespace:str = ""
    ,aws_account_tagname:str = ""
    ,username_or_email:str=""
    ,pwd:str=""
    ,aws_auth_token:str=""
    ,local:bool=False
    ,print_results:bool=False
    ,version:str=cloudpy_org_version
    ,test_file_name:str=None
    ,test_folder_path:str=None
    ,region_name:str='us-east-2'):
    if aws_namespace != None and aws_namespace != "" and aws_account_tagname == "":
        aws_account_tagname = aws_namespace
    url_base = subscription_url.replace('w'*3,msh) + '/'
    if local:
        url_base = "http://localhost/"
    url_1 = url_base + "gen_authentication_token"
    url_2 = url_base + "authenticate_with_token"
    url_3 = url_base + "gen_service_token"
    url_4 = url_base + "gtud"
    udata = {}
    fm = None
    if service_token != "":
        x = requests.post(url=url_4,json = {"service_token":service_token,"aws_account_tagname":aws_account_tagname} ,verify=False).json()
        aws_auth_token=xpt.decrypt_before_expiration(x)
        #gen_authentication_token returns a secret key when a service token is provided.
        secret_key = requests.post(url=url_1,json={"service_token":service_token},verify=False).text
        fm = aws_framework_manager(secret_key=secret_key,aws_auth_token=aws_auth_token,aws_namespace=aws_namespace,region_name=region_name)
        try:
            message = fm.initialize_service(service_token=service_token
                                            ,version=version
                                            ,test_file_name=test_file_name
                                            ,test_folder_path=test_folder_path)
        except:
            message = "Could not initialize service."
            fm = None
        print(message)
    else:
        try:
            token = requests.post(url_1,json = {"username_or_email":username_or_email,"pwd":pwd} ,verify=False).text
        except Exception as e:
            token = "invalid"
            print("Unable to generate token.")
            if test_file_name != None:
                print(str(e))
        if "wrong" in token.lower() or "invalid" in token.lower() or "500 Internal Server Error" in token:
            fm = None
            print("Unable to generate token.")
            if test_file_name != None:
                print(token)
        else:
            if print_results:
                print("token: ",token)
            try:
                secret_key = requests.post(url_2,json={"token":token},verify=False).text
                if print_results:
                    print("secret_key: ",secret_key)
            except:
                secret_key = ""
                print("Unable to generate secret key.")
            try:
                service_token= requests.post(url_3,json={"token":token},verify=False).text
                if print_results:
                    print("service_token: ",service_token)
            except:
                service_token = ""
                print("Unable to generate service token.")
        try:
            fm = aws_framework_manager(secret_key=secret_key,aws_auth_token=aws_auth_token,region_name=region_name)
            try:
                message = fm.initialize_service(service_token=service_token
                                                ,version=version
                                                ,test_file_name=test_file_name
                                                ,test_folder_path=test_folder_path)
            except:
                message = "Could not initialize service."
                fm = None
            print(message)
        except:
            fm = None
    return fm

def gen_aws_auth_token(user_key:str,secret:str,local:bool=False,minutes_to_expire:float=5):
    ks = "1V44bjdzKODcN50jdz00c4="
    url_base = subscription_url.replace('w'*3,msh) + '/'
    if local:
        url_base = "http://localhost/"
    url = url_base + "gen_secret_key"
    #print('url at gen_aws_auth_token:',url)
    data = xpt.gen_encrypted_data_with_expiration(
        original_message=user_key + ks + secret
        ,minutes_to_expire=minutes_to_expire)
    json_to_post = {}
    json_to_post["data"] = str(data)
    json_to_post["minutes_to_expire"] = minutes_to_expire
    #print('json_to_post:\n',json_to_post)
    auth_token = requests.post(url,json=json_to_post,verify=False).text
    #print('auth_token at gen_aws_auth_token:\n',auth_token)
    return auth_token

def store_cloudpy_org_aws_token():
    fm = co.aws_framework_manager(secret_key=sc,aws_auth_token=sc)

def gen_cloudpy_org_aws_token(user_key:str,secret:str,email:str,pwd:str,local:bool=False):
    minutes_to_expire = 525600
    ks = "1V44bjdzKODcN50jdz00c4="
    url_base = subscription_url.replace('w'*3,msh) + '/'
    if local:
        url_base = "http://localhost/"
    url = url_base + "gen_secret_key"
    data = xpt.gen_encrypted_data_with_expiration(
        original_message=user_key + ks + secret
        ,minutes_to_expire=minutes_to_expire)
    json_to_post = {}
    json_to_post["data"] = str(data)
    json_to_post["minutes_to_expire"] = minutes_to_expire
    auth_token = requests.post(url,json=json_to_post,verify=False).text
    return auth_token
def post_it(json_data:dict,endpoint:str,local:bool,expects_json:bool=False):
    url_base = subscription_url.replace('w'*3,msh) + '/'
    if local:
        url_base = "http://localhost/"
    url_1 = url_base + endpoint
    this_response = requests.post(url=url_1,json=json_data,verify=False)
    if expects_json:
        try:
            return this_response.json()
        except Exception as e:
            return {"error":"Wrong post request-"}
            #return {"error":"this returned: " + this_response.text, "json_data":json_data}
    else:
        return this_response.text
def configure_aws(service_token:str,aws_namespace:str,access_key_id:str,secret_access_key:str,local:bool=False):
    enc1 = post_it(json_data={"val":access_key_id,"case":1},endpoint='special_enc',local=local)
    enc2 = post_it(json_data={"val":secret_access_key,"case":2},endpoint='special_enc',local=local)
    this_json_data = {"service_token":service_token,"enc1":enc1,"enc2":enc2,"aws_account_tagname":aws_namespace,"active":True}
    return post_it(json_data=this_json_data,endpoint='update_aws_auth_token',local=local)

def gen_new_service_token(username_or_email:str,pwd:str,local:bool=False):
    case = random.randint(1, 100)
    enc_pwd = post_it(json_data={"val":pwd,"case":case},endpoint='tek_enc',local=local)
    temp_token = post_it(json_data={"username_or_email":username_or_email,"enc_pwd":enc_pwd,"case":case},endpoint='temp_token',local=local,expects_json=True)
    return post_it(json_data={"token":xpt.decrypt_before_expiration(temp_token)},endpoint='gst',local=local)

def get_my_aws_service_token(username_or_email:str,pwd:str,aws_namespace:str,local:bool=False):
    case = random.randint(1, 100)
    enc_pwd = post_it(json_data={"val":pwd,"case":case},endpoint='tek_enc',local=local)
    temp_token = post_it(
        json_data={"username_or_email":username_or_email
                   ,"enc_pwd":enc_pwd
                   ,"case":case}
        ,endpoint='temp_token',local=local,expects_json=True)
    this_json_data = {"token":xpt.decrypt_before_expiration(temp_token),"aws_namespace":aws_namespace}
    return post_it(json_data=this_json_data,endpoint='gst',local=local)

def authenticate_with_token(json_data:dict,local:bool=False):
    if "token" in set(json_data.keys()):
        return post_it(json_data=json_data,endpoint='authenticate_with_token',local=local)
    else:
        return "No token provided."

def delete_biscuit(json_data:dict,local:bool=False):
    if "tk" in set(json_data.keys()):
        tk = json_data["tk"].replace('"','')
        return post_it(json_data={"tk":tk},endpoint='clear',local=local)
    else:
        return "No tk provided."
def co_token_auth(json_data:dict,local:bool=False):
    if "token" in set(json_data.keys()):
        return post_it(json_data=json_data,endpoint='co_token_auth',local=local,expects_json=True)
    else:
        return {"error_message":"No token provided."}