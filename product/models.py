#! -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User 
 
from django.utils.translation import ugettext_lazy as _
from product.manager import AdaptorProductManager, AdaptorAttendcyManager
from basedatas.models import BaseDate, Pic

class Product(BaseDate):
    DRAFT = 0
    PUBLISHED = 1
    FALLDOWN = 2

    PAY = 1 # 付费活动
    FREE = 0# 免费活动
    # 标题
    title = models.CharField(_('title'), max_length = 2048)
    # 描述
    description = models.TextField(null=True)
    # 创建者
    user = models.ForeignKey(User)
    # 活动起止日期
    datefrom = models.DateTimeField(null = True)
    dateto = models.DateTimeField(null = True)

    # 活动起止价格
    pricefrom = models.SmallIntegerField(default = 0)
    priceto = models.SmallIntegerField(default = 0)
    # 活动地点
    location = models.CharField(_('location'), max_length = 4096)
    # 默认0草稿状态
    # 1 已发布
    # 2 隐藏状态 对于暂时隐藏状态的产品不提供用户搜索，下单操作
    status = models.SmallIntegerField(default=DRAFT)
    # 详情
    detail = models.TextField(_('detail'), null=True) 
    thumbnail = models.CharField(_('thumbnail'), max_length = 2048, null=True)

    type = models.SmallIntegerField(default=PAY)

    class Meta:
        abstract = True
        ordering = ('-date',)
          

class AdaptorProduct(Product):
    """Product 适配器""" 
    objects = AdaptorProductManager() 
    # 设置到首页，默认0是不放在首页的
    # 1 代表放在首页
    set_homepage = models.SmallIntegerField(default=0)
    # 设置到首页列表中，默认0是不放在首页列表中的
    # 1 代表放在首页列表中
    set_grid = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title  
 
class ProductPic(Pic): 
    """产品图片类"""
    SWIPER = 0
    DETAIL = 1
    product = models.ForeignKey(AdaptorProduct)
    # 默认0表示该图片是商品的轮播图图片
    # 1 详情页图片 
    type = models.SmallIntegerField(default=SWIPER)
    class Meta:
        db_table = 'productpic'
    def __str__(self):
        return self.name  
     
class DetailPic(Pic): 
    """全局图片类"""
    ref = models.SmallIntegerField(default=0) 
    def __str__(self):
        return self.name  

class Attendcy(models.Model):
    """
    出席活动的人
    """
    user = models.ForeignKey(User, null=True)
    product = models.ForeignKey(AdaptorProduct)
    # 名称 ：8G
    name = models.CharField(_('name'), max_length=1024, null=True)
    # 电话:6999
    phone = models.CharField(_('phone'), max_length = 4096, default='')
    # 数量：100
    quantity = models.PositiveIntegerField(_('inventory'), default = 0, null=True)
     
    class Meta:
        abstract = True
  
class AdaptorAttendcy(Attendcy):
    """Attendcy 适配器"""
    objects = AdaptorAttendcyManager()
    def __str__(self):
        return self.name  

