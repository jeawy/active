#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
import io
from datetime import datetime
from appuser.models import AdaptorUser as User 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from product.models import AdaptorProduct, AdaptorAttendcy, ProductPic, DetailPic
from common.fileupload import FileUpload
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
from excl import write_attendecies
from product.comm import handle_uploaded_file
from common.e_mail import EmailEx
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
import threading
from django.core.servers.basehttp import FileWrapper
dmb     = DetectMobileBrowser()


@login_required
@csrf_exempt
def change(request, pk):
    if not request.user.is_superuser:
        return HttpResponse("没有权限...")

    isMble  = dmb.process_request(request)
    content = {}
    content['mediaroot'] = settings.MEDIA_URL  

    if request.method == 'GET':
        try:
             product = AdaptorProduct.objects.get(pk=pk)
             content['product'] =product 
        except AdaptorProduct.DoesNotExist:
            raise Http404
        if 'pic' in request.GET:
                return render(request, 'pic.html', content)
        
        else: 
            return render(request, 'new.html', content)

    return HttpResponse()



@login_required
@csrf_exempt
def attendcies(request, pk):
    if not request.user.is_superuser and not request.user.is_staff :
        return HttpResponse("没有权限...")
    
    content = {}
    content['mediaroot'] = settings.MEDIA_URL  
    
    if request.method == 'GET':
        try:
             product = AdaptorProduct.objects.get(pk=pk)
             content['product'] =product 
             if 'output' in request.GET:
                # 导出excel
                filename = os.path.join(settings.MEDIA_URL,   'attendency.xls')
                d={}
                d['filename'] = filename
                d['attendencies'] = product.adaptorattendcy_set.all()
                excel_f = write_attendecies(**d)
                if os.path.isfile(filename):
                    try:
                        wrapper = FileWrapper(file(filename, 'rb'))
                    except IOError, e:
                        return HttpResponse(e)
                        
                    response    = HttpResponse(wrapper,content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename( filename )
                    response['Content-Length']      = os.path.getsize(filename)
                    return response
                else:
                    return HttpResponse(u'未找到文件...')
        except AdaptorProduct.DoesNotExist:
             raise Http404

        
             
        
      
    return render(request, 'attencies.html', content)
@login_required
@csrf_exempt
def setting(request, pk):
    if not request.user.is_superuser:
        return HttpResponse("没有权限...")
 
    content = {}
    content['mediaroot'] = settings.MEDIA_URL  

    if request.method == 'GET':
        try:
             product = AdaptorProduct.objects.get(pk=pk)
             content['product'] =product 
        except AdaptorProduct.DoesNotExist:
             raise Http404
      
    return render(request, 'setting.html', content)

@login_required
@csrf_exempt
def addatt(request, pk): 
    """
    提交出席人员
    """
    result = {} 
    if request.method == 'POST':
        if 'username' in request.POST and 'number' in request.POST  :
            try: 
                product = AdaptorProduct.objects.get(pk=pk)
                
                name = request.POST['username']
                quantity = request.POST['number'] 
                AdaptorAttendcy.objects.create(user=request.user, product=product,\
                                               name=name,quantity=quantity )
                subject = product.title 
                
                html = io.open(os.path.join(settings.TEMPLATES[0]['DIRS'][0] , 'email.html'), mode='r', encoding="utf-8")
                data = html.read() 
                html.close()   
                data = data.replace('###href###', request.scheme+'://'+request.get_host()+reverse('product:detail', args=(product.id,)))  
                data = data.replace('###title###', subject)  
                data = data.replace('###location###', product.location) 
                
                data = data.replace('###time###', datetime.strftime(product.datefrom, '%Y-%m-%d')  ) 
                
                userlist_html_template = '''
                <tr>
                    <td>###name###</td> 
                    <td>###number###</td>
                </tr>
                '''
                
                userlist_html = userlist_html_template.replace('###name###', name) 
                userlist_html = userlist_html.replace('###number###', quantity) 
                 
                content = data.replace('###tbody###', userlist_html)  
                
                userlist_html_super = ''
                for attendy in product.adaptorattendcy_set.all():
                    userlist_html_super_tmp = userlist_html_template.replace('###name###', attendy.name) 
                    userlist_html_super_tmp = userlist_html_super_tmp.replace('###number###', str(attendy.quantity))
                    userlist_html_super += userlist_html_super_tmp
                content_super = data.replace('###tbody###', userlist_html_super)  
                
                receivers = User.objects.getsuperuser_emails()
             
                t1 = threading.Thread(target=EmailEx.send_html_email, args=(subject, content, product.user.email)).start()
                if len(receivers) > 0:
                    t_super = threading.Thread(target=EmailEx.send_html_email, args=(subject, content_super, receivers)).start()
             
                result['status'] = 'OK' 
                result['msg'] = '报名成功' 
            except AdaptorProduct.DoesNotExist:
                raise Http404
        else:
            result['status'] = 'error' 
            result['msg'] = 'POST中需要username, number 和phone' 
       
    else:
        result['status'] = 'error' 
        result['msg'] = '请使用POST方法...'
    return HttpResponse(json.dumps(result), content_type='application/json')

class ProductDetailView(APIView):
    """product detail"""
    model = AdaptorProduct
    def get_object(self, pk):
        try:
            return AdaptorProduct.objects.get(pk=pk)
        except AdaptorProduct.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
         
        isMble  = dmb.process_request(request)
        
        content={
            'product':product
        }
        content['mediaroot'] = settings.MEDIA_URL
        if isMble:
            return render(request, 'detail.html', content)
        else:
            return render(request, 'detail.html', content)


    @method_decorator(csrf_exempt)
    def post(self, request, pk, format=None):
        product = self.get_object(pk)
         
        content={
            'product':product
        } 
        result = {}		 
        if request.method == 'POST': 
            user = request.user
            if 'method' in request.POST:
                method = request.POST['method']
                if method == 'delete':
                    picid = request.POST['picid']
                    productpic = ProductPic.objects.get(pk = picid)
                    productpic.delete()
                    result['status'] = 'OK'
                    result['msg']    = '删除成功...' 
            elif 'picid' in request.POST: # 说明是在设置主缩略图
                picid = request.POST['picid']
                productpic = ProductPic.objects.get(pk = picid)
                product.thumbnail = productpic.url 
                product.save()
                
                result['status'] = 'OK'
                result['msg']    = '设置成功...' 
            else: 
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(request.FILES['pic'], str(user.id)+'_'+ code)
                
                ProductPic.objects.create(product=product, url=filename.replace('\\', '/'))
                
                result['status'] = 'OK'
                result['msg']    = '上传成功...' 
        else:
            result['status'] = 'ERROR'
            result['msg']    = 'Method error..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         
   
class ProductView(View):
    
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        kwargs = {}
        if 'datefrom' in  request.GET:
            datefrom = request.GET['datefrom'].strip()
            if len(datefrom) > 0:
                kwargs['datefrom__gte'] = request.GET['datefrom']
                content['datefrom'] = request.GET['datefrom']
        if 'dateto' in  request.GET: 
            dateto = request.GET['dateto'].strip()
            if len(dateto) > 0:
                kwargs['datefrom__lte'] = request.GET['dateto']
                content['dateto'] = request.GET['dateto']
        if 'pricefrom' in request.GET:
            pricefrom = request.GET['pricefrom'].strip()
            if len(pricefrom) > 0:
                kwargs['pricefrom__gte'] = request.GET['pricefrom']
                content['pricefrom'] = request.GET['pricefrom']
        if 'priceto' in request.GET:
            priceto = request.GET['priceto'].strip()
            if len(priceto) > 0:
                kwargs['priceto__lte'] = request.GET['priceto']
                content['priceto'] = request.GET['priceto']
        
        products = AdaptorProduct.objects.filter(**kwargs) 
        
        content['products'] = products 
        content['mediaroot'] = settings.MEDIA_URL
        if 'new' in request.GET:
            if isMble:
                return render(request, 'new.html', content)
            else:
                return render(request, 'new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'new.html', content)
            else:
                return render(request, 'test.html', content)
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'pic.html', content)
            else:
                return render(request, 'pic.html', content)
        if 'detailpic' in request.GET:
            pics = DetailPic.objects.all()
            content['pics'] =pics 
            return render(request, 'detailpic.html', content)
        else:
            return render(request, 'list.html', content)
 
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建产品
            下架：参数中带有method，并且值是'fallback'，大小写不敏感
                # # id【必须字段】：商品id 
            删除：参数中带有method，并且值是'delete'，大小写不敏感
                # # id【必须字段】：商品id 
            修改：参数中带有method，并且值是'put'，大小写不敏感
                # id【必须字段】：商品id 
                # title【可选字段】：商品名称  
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个寄送数据
                # detail【可选字段】： 商品的详情
            新建: 参数中带没有method，或method的值不等于put或者delete
                # title【必须字段】：商品名称  
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个寄送数据
                # detail【可选字段】： 商品的详情
        
        修改产品
        """
        result = {} 
        
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除
                return self.delete(request)
            elif method == 'fallback': # 下架
                return self.fallback(request)
            elif method == 'create': # 创建
                return self.create(request)
            elif method == 'detail_file': # 上传详情图片
                return HttpResponse('geu')
        elif 'detailpic' in request.POST: # 说明是在上传图库图片 
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(request.FILES['pic'], str(request.user.id)+'_'+ code) 
                DetailPic.objects.create(url=filename.replace('\\', '/')) 
                result['status'] = 'OK'
                result['msg']    = '上传成功...'
                return self.httpjson(result)
        else:
            return self.create(request)
        
    
    def create(self, request):
        """创建"""
        # 新建商品
        # title\category字段是必须的
        user = request.user
        result = {}
        if 'title' in request.POST  : 
            title = request.POST['title'].strip() 
   
            # 创建商品 
            product = AdaptorProduct.objects.create(user=user, title=title    )
 
            if 'detail' in request.POST:
                detail = request.POST['detail'].strip()
                product.detail = detail 
            if 'description' in request.POST:
                description = request.POST['description'].strip()
                product.description = description 

            if 'pricefrom' in request.POST: 
                pricefrom = request.POST['pricefrom'].strip()
                if len(pricefrom) > 0:
                    product.pricefrom = pricefrom 
            if 'priceto' in request.POST: 
                priceto = request.POST['priceto'].strip()
                if len(priceto) > 0:
                    product.priceto = priceto 
            
            if 'datefrom' in request.POST:
                datefrom = request.POST['datefrom'].strip()
                product.datefrom = datetime.strptime(datefrom , '%Y-%m-%d %H:%M') 
             
            if 'location' in request.POST:
                location = request.POST['location'].strip()
                product.location = location  
  
            if 'status' in request.POST:
                status = request.POST['status'].strip()
                product.status = status

            if 'activetype' in request.POST:
                activetype = request.POST['activetype'].strip()
                product.type = activetype
            try:
                product.save()
                result['id'] = product.id
                result['status'] ='ok'
                result['msg'] ='保存成功...'
            except Exception as e: 
                product.delete()
                result['status'] ='error'
                result['msg'] = str(e )
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)

    def put(self, request):
        """
        修改 
        """
        result = {}   
        data = request.POST  
        if 'id' in data:
            productid = data['id']
            try:
                product = AdaptorProduct.objects.get(id=productid)
                if 'title' in data:
                    title = data['title']
                    product.title = title

                if 'description' in request.POST:
                    description = request.POST['description'].strip()
                    product.description = description 

                if 'pricefrom' in request.POST: 
                    pricefrom = request.POST['pricefrom'].strip()
                    if len(pricefrom) > 0:
                        product.pricefrom = pricefrom 
                if 'priceto' in request.POST: 
                    priceto = request.POST['priceto'].strip()
                    if len(priceto) > 0:
                        product.priceto = priceto 
                
                if 'datefrom' in request.POST:
                    datefrom = request.POST['datefrom'].strip()
                    product.datefrom = datetime.strptime(datefrom , '%Y-%m-%d %H:%M') 
         
                
                if 'location' in request.POST:
                    location = request.POST['location'].strip()
                    product.location = location  
                
                if 'activetype' in request.POST:
                    activetype = request.POST['activetype'].strip()
                    product.type = activetype

                if 'set_homepage' in request.POST:
                    set_homepage = request.POST['set_homepage'].strip()
                    product.set_homepage = set_homepage
                if 'set_grid' in request.POST:
                    set_grid = request.POST['set_grid'].strip()
                    product.set_grid = set_grid
                
                product.save() 
                result['status'] ='ok'
                result['msg'] ='操作成功...'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the Product ID:{}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id  in POST'

        return self.httpjson(result)

    def delete(self, request):
        """
        删除指定商品
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                product.delete() 
                result['status'] ='ok'
                result['msg'] ='删除成功...'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)

    def fallback(self, request):
        """下架商品"""
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                AdaptorProduct.objects.fallback(product)
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)
 
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")
