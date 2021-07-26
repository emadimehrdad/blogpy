from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *


class IndexPage(TemplateView):

    def get(self, request, **kwargs):
        article_data = []
        all_article = Article.objects.all().order_by("-created_at")[:9]

        for article in all_article:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })

        promote_data = []
        all_promote_articles = Article.objects.filter(promote=True)

        for promote_article in all_promote_articles:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'author': promote_article.author.user.first_name + ' ' + promote_article.author.user.last_name,
                'avatar': promote_article.author.avatar.url,
                'created_at': promote_article.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promote_article_data': promote_data,
        }

        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = "page-contact.html"


class AllArticleAPIView(APIView):

    def get(self, request, format=None):

        try:
            all_article = Article.objects.all().order_by("-created_at")[:10]
            data = []

            for article in all_article:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                    'created_at': article.created_at.date(),
                    'category': article.category.title,
                    'content': article.content,
                    'promote': article.promote,
                })

            context = {
                'data': data,
            }
            return Response(context, status=status.HTTP_200_OK)


        except:
            Response('status: Internal Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
