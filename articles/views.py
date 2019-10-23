from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import ArticleForm, CommentForm
from .models import Article, Comment


@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

@require_GET
def detail(request, article_pk):
    # 사용자가 url 에 적어보낸 article_pk 를 통해 디테일 페이지를 보여준다.
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    comments = article.comments.all()
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        }
    return render(request, 'articles/detail.html', context)


@login_required 
# 로그인 안 되어있으면 /accounts/login/ 보내줌, 로그인 url 을 다르게 설정했다면 @login_required(login_url='users/login/')
# 로그인 안된 상태로 url 통해서 create 접속할 경우 http://127.0.0.1:8000/accounts/login/?next=/articles/create/ 경로로 login 화면을 보여주는데 ?next는 로그인 한 이후에 create 화면으로 보내주라는 뜻
def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()
        context = {'form': form}  # 비어있는 폼을 보내서 사용자가 html에서 볼 수 있도록 함
        return render(request, 'articles/create.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:detail', article_pk)
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        # article_pk 에 맞는 article 을 가져온다. 삭제한다.
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    
    return redirect('articles:index')



@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # push 전의 상태를 담아둠
            comment.article_id = article_pk  # 빠진 필드 채워넣기
            comment.user = request.user
            comment.save()
        # comment = Comment(article_id = article_pk)
        # form = CommentForm(request.POST, instance=comment)
        # if form.is_valid():
        #     form.save()
    return redirect('articles:detail', article_pk)


@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment = article.comments.get(pk=comment_pk)
        # comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('articles:detail', article_pk)
    return HttpResponse('You are Unauthorized', status=401)


def like(request, article_pk):
    if request.user.is_authenticated:
        user = request.user
        article = get_object_or_404(Article, pk=article_pk)
        # article.liked_user.add(user)
        # if user in article.liked_users.all():
        if article.liked_users.filter(pk=user.pk).exists():
            article.liked_users.remove(user)
        else:
            user.liked_articles.add(article)
        return redirect('articles:detail', article_pk)

def follow(request, article_pk, user_pk):
    # if request.user.is_authenticated:
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk)

    if user in person.followers.all(): # 이미 팔로워임
        person.followers.remove(user)
    else: # 팔로우 하겠음.
        person.followers.add(user)
    return redirect('articles:detail', article_pk)
