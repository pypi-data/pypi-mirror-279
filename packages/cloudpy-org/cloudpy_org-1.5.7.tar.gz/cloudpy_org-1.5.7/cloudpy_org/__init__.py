"""
███████████████████████████cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
aws_regions = {'us-east-1': {'long_name': 'US East (N. Virginia)', 'code': 'use1'},
 'us-east-2': {'long_name': 'US East (Ohio)', 'code': 'use2'},
 'us-west-1': {'long_name': 'US West (N. California)', 'code': 'usw1'},
 'us-west-2': {'long_name': 'US West (Oregon)', 'code': 'usw2'},
 'ap-south-1': {'long_name': 'Asia Pacific (Mumbai)', 'code': 'aps1'},
 'ap-northeast-3': {'long_name': 'Asia Pacific (Osaka)', 'code': 'apne3'},
 'ap-northeast-2': {'long_name': 'Asia Pacific (Seoul)', 'code': 'apne2'},
 'ap-southeast-1': {'long_name': 'Asia Pacific (Singapore)', 'code': 'apse1'},
 'ap-southeast-2': {'long_name': 'Asia Pacific (Sydney)', 'code': 'apse2'},
 'ap-northeast-1': {'long_name': 'Asia Pacific (Tokyo)', 'code': 'apne1'},
 'ca-central-1': {'long_name': 'Canada (Central)', 'code': 'cac1'},
 'eu-central-1': {'long_name': 'Europe (Frankfurt)', 'code': 'euc1'},
 'eu-west-1': {'long_name': 'Europe (Ireland)', 'code': 'euw1'},
 'eu-west-2': {'long_name': 'Europe (London)', 'code': 'euw2'},
 'eu-west-3': {'long_name': 'Europe (Paris)', 'code': 'euw3'},
 'eu-north-1': {'long_name': 'Europe (Stockholm)', 'code': 'eun1'},
 'sa-east-1': {'long_name': 'South America (São Paulo)', 'code': 'sae1'}}
subscription_url = 'https://www.cloudpy.org'
msh = 'secure'
cloudpy_org_version='1.5.7'
gsep = {'user_email_sep': '-0-', '@': '-1-', '.': '-2-'}
from cloudpy_org.tools import processing_tools,unique_id
from cloudpy_org.docs import auto_document,convert_jupiter_notebook_to_html,documentation_from_folder
from cloudpy_org.aws import aws_framework_manager,aws_framework_manager_client,gen_aws_auth_token,gen_new_service_token,configure_aws,get_my_aws_service_token,authenticate_with_token,delete_biscuit,co_token_auth
from cloudpy_org.web import flask_website
from cloudpy_org.imgedit import colors
from cloudpy_org.client_usage import cloudpy_org_aws_framework_client
#from cloudpy_org.web_client_usage import cloudpy_org_web_client
