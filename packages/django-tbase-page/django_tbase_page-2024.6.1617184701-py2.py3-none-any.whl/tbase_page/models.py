from django.db import models

# Create your models here.
from solo.models import SingletonModel
from martor.models import MartorField

class BasePage(SingletonModel):
    """
    添加基本页面
    """
    # ABOUT US
    about_us = MartorField(blank=True)
    # PRIVACY POLICY
    privacy_policy = MartorField(blank=True)
    # TERMS & CONDITIONS
    terms_and_conditions = MartorField(blank=True)
    # CONTACT US
    contact_us = MartorField(blank=True)
    # robots_txt
    robots_txt = MartorField("robots.txt协议",blank=True)
    # ads_txt
    ads_txt = MartorField("ads.txt协议",blank=True)



    def __str__(self):
        return "Base Page"

    class Meta:
        verbose_name = "Base Page"
