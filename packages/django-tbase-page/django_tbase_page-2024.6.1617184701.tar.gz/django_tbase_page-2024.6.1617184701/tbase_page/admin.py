from django.contrib import admin

# Register your models here.
# Register your models here.
from solo.admin import SingletonModelAdmin

from .models import BasePage


class BasePageAdmin(SingletonModelAdmin):
    # 编辑页面字段定制
    fieldsets = [("ABOUT US:(/page/about-us)", {
        'fields': ['about_us']
    }), ("PRIVACY POLICY(/page/privacy-policy)", {
        'fields': ['privacy_policy']
    }),
                 ("TERMS & CONDITIONS(/page/terms-and-conditions)", {
                     'fields': ['terms_and_conditions']
                 }),
                 ("CONTACT US(/page/contact-us)", {
                     'fields': ['contact_us']
                 }),
                  ("robots.txt文件(/robots.txt)", {
                     'fields': ['robots_txt']
                 })
                 ]
    pass
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')

    # # 编辑页面字段定制
    # fieldsets = [("Base information", {
    #     'fields': [
    #         'site_title', 'site_header', "index_title", 'site_url',
    #         'enable_nav_sidebar', 'maintenance_mode'
    #     ]
    # }),
    #              (
    #                  'admin information',
    #                  {
    #                      'fields': ['admin_email'],
    #                      'classes': ['collapse']
    #                  },
    #              ),
    #              ('Plus information', {
    #                  'fields': ['header_script', 'footer_script']
    #              }), ('api information', {
    #                  'fields': ['api_thumbnail']
    #              }), ('analytics', {
    #                  'fields': ['analytics_id']
    #              })]
    # pass


# class DadminSite(admin.AdminSite):
#     site_title = '管理站点'
#     site_header = 'by'
#     index_title = '索引页顶部的文字，默认为“网站管理”'
#
# admin_site = DadminSite(name='admin')

# 注册配置页面
admin.site.register(BasePage, BasePageAdmin)