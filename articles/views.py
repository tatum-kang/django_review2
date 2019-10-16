from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article
from IPython import embed
from django.views.decorators.http import require_GET, require_POST

# Create your views here.
@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

# GET, POST

def create(request):
    #Article을 생성해달라고 하는 요청
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        # embed()
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else: # GET
        # Article을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()
    context = {'form':form}
    return render(request, 'articles/create.html', context)

@require_GET
def detail(request, article_pk):
    # Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    context = {'article':article}
    return render(request, 'articles/detail.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
    else:
        form = ArticleForm(instance=article)
    context = {'article': article, 'form':form}
    return render(request, 'articles/update.html', context)

@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')

