from api.utils.jwt_auth import create_token
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from django.conf import settings
import os
import pandas as pd

# 登陆视图
class LoginView(APIView):
    # 登陆界面不用做验证
    authentication_classes = []

    def post(self,request,*args,**kwargs):
        school = request.data.get('school')
        snumber = request.data.get('snumber')
        grade = request.data.get('grade')
        classes = request.data.get('classes')
        sex = request.data.get('sex')
        name = request.data.get('name')
        # 查库返回Queryset类型对象
        status = 1 # 默认第一题
        user_object = models.User.objects.filter(school=school,snumber=snumber,grade=grade,classes=classes,sex=sex,name=name).first()
        # print(school,snumber,grade,classes,sex,name)
        if not user_object:
            if grade not in ["6","7","8","9"]:
                return Response({'code':1001,'error':'年级的话必须是数字6789'})
            elif sex not in ["男","女"]:
                return Response({'code':1001,'error':'请正确填写性别'})
            else:
                user_object = models.User.objects.create(school=school,snumber=snumber,grade=grade,classes=classes,sex=sex,name=name)
		# 根据用户信息生成token
        user_token = models.Usertoken.objects.filter(user=user_object).first()
        user_status = models.Userstatus.objects.filter(user_id=user_object.id).first()
        if not user_token:
            token = create_token({'id':user_object.id,'school':user_object.school,'name':user_object.name})
            models.Usertoken.objects.create(user=user_object,token=token)
        else:
            token = user_token.token
        if not user_status:
            models.Userstatus.objects.create(user_id=user_object.id,status=status)
        else:
            status = user_status.status
        return Response({'code': 1000, 'token': token, 'userid' : user_object.id, 'status':status})

class BehaviorView(APIView):
    def post(self,request,*args,**kwargs):
        behavior_value = request.data.get('logvalue')
        info_list = request.data.get('file').split(',')
        snumber, file_path, uid, question, page = info_list[0], info_list[1], info_list[2], info_list[3], info_list[4]
        file_name = f'{file_path}.log'
        if not os.path.exists(settings.LOG_UPLOAD):
            os.mkdir(settings.LOG_UPLOAD)
        deep_name = os.path.join(settings.LOG_UPLOAD, file_name)
        if os.path.exists(deep_name) and question == "煮食器皿" and page == "3":
            with open(deep_name, 'r+') as file:
                file.truncate(0)
        with open(deep_name, 'a+', encoding='utf-8') as f:
            if page == "3":
                f.writelines("标题：" + question + "\n")
            for i in behavior_value:
                f.writelines(i.replace("\n","") + "\n")
        f.close()
        user_log = models.UserLog.objects.filter(snumber=snumber).first()
        if not user_log:
            models.UserLog.objects.create(snumber=snumber,logname=os.path.join(settings.LOG_UPLOAD, file_name))
        # excel 整理
        Answer_UPLOAD = os.path.join(settings.BASE_DIR, 'static/Answer')
        if not os.path.exists(Answer_UPLOAD):
            os.mkdir(Answer_UPLOAD)
        file_name = f'{file_path}.xls'
        excel_name = os.path.join(Answer_UPLOAD, file_name)
        header_list = ['姓名','年级','性别','题号','回答类型','答案']
        if os.path.exists(excel_name):
            df = pd.read_excel(excel_name)
            if question == "煮食器皿" and page == "3":
                df.drop(df.index, inplace=True)
                df = df.append(pd.DataFrame(columns=header_list))
        else:
            df = pd.DataFrame()
            df = pd.DataFrame(columns=header_list)
        
        datalist = []
        dicf = {}
        for content in behavior_value:
            if "：" in content:
                content = content.replace("\n","")
                content_list = content.split("：")
                dicf[content_list[0][23:]] = content_list[1]
        file_list = file_path.split('_')
        for key, value in dicf.items():
            one_answer = []
            one_answer.append(file_list[2])
            one_answer.append(file_list[0])
            one_answer.append(file_list[1])
            one_answer.append(self.getqstitle(question,page))
            one_answer.append(key)
            one_answer.append(value)
            datalist.append(one_answer)
        for row in datalist:
            df = df.append(pd.Series(row, index=header_list), ignore_index=True)
        with pd.ExcelWriter(excel_name) as writer:
            df.to_excel(writer, index=False) 
        if int(page) == self.getallpage(question):
            userstatus = models.Userstatus.objects.get(user_id = int(uid))
            userstatus.status = self.getstatus(question)
            userstatus.save() 
        return Response({'code': 1000, 'message':'success'})
    
    def getstatus(self, question):
        dict = {
            "煮食器皿":2,
            "汽车刹车":3,
            "物质鉴别":4,
            "土壤组成":5,
            "植物生长":6,
            "航天器":7,
            "滑雪运动":8,
            "炮弹发射":1
        }
        return dict[question]

    def getallpage(self, question):
        dict = {
            "煮食器皿":4,
            "汽车刹车":6,
            "物质鉴别":6,
            "土壤组成":4,
            "植物生长":5,
            "航天器":4,
            "滑雪运动":4,
            "炮弹发射":4
        }
        return dict[question]

    def getqstitle(self, question, page):
        dict = {
            "煮食器皿":{
                "3":"1-1aC",
                "4":"2-1aC"
            },
            "汽车刹车":{
                "3":"3-1aF",
                "4":"4-1nC",
                "5":"5-2anF",
                "6":"6-1nF"
            },
            "物质鉴别":{
                "3":"7-1nC",
                "4":"8-1nF",
                "5":"9-2aaC",
                "6":"10-2aaF"
            },
             "土壤组成":{
                "3":"11-2aaC",
                "4":"12-2aaF"
            },
            "植物生长":{
                "3":"13-1aF",
                "4":"14-1nF",
                "5":"15-2anC"
            },
            "航天器":{
                "3":"16-2anC",
                "4":"17-2anF"
            },
            "滑雪运动":{
                "3":"18-2nnC",
                "4":"19-2nnF"
            },
            "炮弹发射":{
                "3":"20-2nnC",
                "4":"21-2nnF"
            }
        }
        return dict[question][page]
