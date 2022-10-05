from api.utils.jwt_auth import create_token
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from django.conf import settings
import os

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
        user_object = models.User.objects.filter(school=school,snumber=snumber,grade=grade,classes=classes,sex=sex,name=name).first()
        # print(school,snumber,grade,classes,sex,name)
        if not user_object:
            return Response({'code':1001,'error':'用户名或密码错误'})
        
		# 根据用户信息生成token
        user_token = models.Usertoken.objects.filter(user=user_object).first()
        if not user_token:
            token = create_token({'id':user_object.id,'school':user_object.school,'name':user_object.name})
            models.Usertoken.objects.create(user=user_object,token=token)
        else:
            token = user_token.token
        
        return Response({'code': 1000, 'token': token, 'userid' : user_object.id})

class BehaviorView(APIView):
    def post(self,request,*args,**kwargs):
        behavior_value = request.data.get('logvalue')
        info_list = request.data.get('snumber').split(',')
        snumber, question = info_list[0], info_list[1]
        file_name = f'{snumber}.log'
        if not os.path.exists(settings.LOG_UPLOAD):
            os.mkdir(settings.LOG_UPLOAD)
        with open(os.path.join(settings.LOG_UPLOAD, file_name), 'a+') as f:
            f.writelines("标题：" + question + "\n")
            for timestrap, content in behavior_value.items():
                f.writelines(timestrap + "\t" + content.replace("\n","") + "\n")
        f.close()
        user_log = models.UserLog.objects.filter(snumber=snumber).first()
        if not user_log:
            models.UserLog.objects.create(snumber=snumber,logname=os.path.join(settings.LOG_UPLOAD, file_name))
        return Response({'code': 1000, 'message':'success'})

