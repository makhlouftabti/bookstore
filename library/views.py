from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from .forms import BookForm,CategoryForm
# Create your views here.
def index(response):
    if response.method=='POST':
        add_book = BookForm(response.POST, response.FILES)
        if add_book.is_valid():
            add_book.save()
        add_category = CategoryForm(response.POST)
        if add_category.is_valid():
            add_category.save()







    context = {
        'categories': Category.objects.all(),
        'books': Book.objects.all(),
        'form' : BookForm(),
        'formcat': CategoryForm(),
        'allbooks':Book.objects.filter(active = True).count(),
        'booksold':Book.objects.filter(status='sold').count(),
        'bookrented':Book.objects.filter(status='rented').count(),
        'bookav':Book.objects.filter(status='available').count(),
    }
    
    return render(response, 'pages/index.html', context)


def books(response):
    title = None
    search = Book.objects.all()
    if 'search_name' in response.GET :
        title = response.GET['search_name']
        if title :
            search = search.filter(title__icontains = title)
    context = {
        'categories': Category.objects.all(),
        'books': search,
        'formcat': CategoryForm(),

    }
    return render(response, 'pages/books.html', context)


def update(response, id):
    book_id = Book.objects.get(id=id)
    if response.method == 'POST':
        book_save = BookForm(response.POST, response.FILES, instance = book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('/')
    else :
        book_save = BookForm(instance = book_id)
    context = {
        'form' : book_save,
    }
    return render(response, 'pages/update.html', context)
def delete(response, id):
    delete_book = get_object_or_404(Book, id=id)
    if response.method=='POST':
        delete_book.delete()
        return redirect('/')
    
    return render(response, 'pages/delete.html')