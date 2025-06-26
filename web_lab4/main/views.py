from django.shortcuts import render

news = [
    {"id": 1, "title": "Новина 1", "content": "Текст 1"},
    {"id": 2, "title": "Новина 2", "content": "Текст 2"},
    {"id": 3, "title": "Новина 3", "content": "Текст 3"},
]

def index(request):
    return render(request, 'index.html', {"news": news})

def news_detail(request, id):
    item = next((n for n in news if n["id"] == id), None)
    return render(request, 'detail.html', {"news_item": item})
