# 使用celery
from django.conf import settings
from django.core.mail import send_mail
from celery import Celery
import time
from django.template import loader, RequestContext
from django_redis import get_redis_connection

# 在任务处理者一端加入这几句代码，初始化django变量
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner

# 创建一个Celery类的实例对象
# broker 任务队列（中间人）
app = Celery('celery_tasks.tasks', broker='redis://192.168.5.130:6379/8')
# app = Celery('celery_tasks.tasks', broker='redis://8.131.77.106:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(email, username, token):
    '''发送激活邮件'''
    # 发邮件
    # 组织邮件信息
    # subject：邮件标题
    subject = '天天生鲜欢迎信息'
    # message：邮件正文
    message = ''
    # message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/usr/active/%s">http://127.0.0.1:8000/usr/active/%s</a>'%(username, token, token)
    # from_email:发件人
    sender = settings.EMAIL_FROM
    # recipient_list：收件人列表
    receiver = [email]
    # html_message:自动解析为html格式文本,需自己指定
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)


@app.task
def generate_static_index_html():
    # 获取商品种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
        # 动态给type增加属性，将这两个属性加到type中
        type.image_banners = image_banners
        type.title_banners = title_banners

    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banner}
    # 使用模板
    # 1.加载模板文件, 返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(static_index_html)

# from celery_tasks.tasks import generate_static_index_html
# generate_static_index_html.delay()