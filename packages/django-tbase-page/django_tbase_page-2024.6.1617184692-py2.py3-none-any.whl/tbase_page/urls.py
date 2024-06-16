from django.urls import path

from . import views

urlpatterns = [
    path('about-us', views.PageAboutUsView.as_view(), name='about_us'),
    path('privacy-policy',
         views.PagePrivacyPolicyView.as_view(),
         name='privacy_policy'),
    path('terms-and-conditions',
         views.PageTermsAndConditionsView.as_view(),
         name='terms_and_conditions'),
    path('contact-us', views.PageContactUsView.as_view(), name='contact_us'),
    # path('', views.IndexView.as_view(), name='detail_index'),
    # path('detail/<int:pk>/', views.DetailView.as_view(), name='detail_view'),
    # path('tag/<slug:tag_slug>/',
    #      views.TagListView.as_view(),
    #      name='article_list_by_tag'),
    # # path('detail/<int:pk>', views.DetailView.as_view(), name='post_view'),
    # # path('<int:pk>/', views.PostView.as_view(), name='post'),
]