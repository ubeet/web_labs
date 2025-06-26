from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm

def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'news': news})

def is_admin(request):
    return request.GET.get('admin') == '1'

def news_detail(request, id):
    item = get_object_or_404(News, id=id)
    return render(request, 'detail.html', {'news_item': item})

def news_create(request):
    if not is_admin(request):
        return redirect('home')

    form = NewsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form.html', {'form': form, 'action': 'Створити'})


def news_edit(request, id):
    if not is_admin(request):
        return redirect('home')

    item = get_object_or_404(News, id=id)
    form = NewsForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form.html', {'form': form, 'action': 'Редагувати'})


def news_delete(request, id):
    if not is_admin(request):
        return redirect('home')

    item = get_object_or_404(News, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'news_item': item})

def set_admin_mode(request):
    request.session['is_admin'] = True
    return redirect('home')

def logout_admin_mode(request):
    if 'is_admin' in request.session:
        del request.session['is_admin']
    return redirect('home')


def is_admin(request):
    return request.session.get('is_admin', False)

