from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
# Create your views here.


# Create your views here.
def index(request):
    return HttpResponse('''index''')


class HomePageView(TemplateView):
    """
    设置首页开发
    """
    template_name = 'home.html'


class PageAboutUsView(TemplateView):
    """
    设置首页开发
    """
    template_name = 'about_us.html'


class PagePrivacyPolicyView(TemplateView):
    """
    设置首页开发
    """
    template_name = 'privacy_policy.html'


class PageTermsAndConditionsView(TemplateView):
    """
    设置首页开发
    """
    template_name = 'terms_and_conditions.html'


class PageContactUsView(TemplateView):
    """
    设置首页开发
    """
    template_name = 'contact_us.html'


class RobotsTxtView(TemplateView):
    """
    rebots.txt文件
    """
    template_name = 'robots_txt.html'


class AdsTxtView(TemplateView):
    """
    ads.txt文件
    """
    template_name = 'ads_txt.html'
