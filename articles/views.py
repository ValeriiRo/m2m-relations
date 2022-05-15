from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    article = Article.objects.all()
    context = {'object_list': article}

    return render(request, template, context)
