from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.views.generic import View
from books.models import Book
from .forms import UserForm, BookForm, UpdateUserForm
from django.db.models import Q
import os
import datetime
import smtplib

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def charts(request):
        return render(request, 'books/charts.html')


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'books/login.html')
    else:
        books = Book.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query),
            ).exclude(user=request.user).distinct()
            return render(request, 'books/search_form.html', {
                'books': books
            })
        else:
            return render(request, 'books/index.html', {'books': books})


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'


def create_book(request):
    if not request.user.is_authenticated():
        return render(request, 'books/login.html')
    else:
        form = BookForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.cover = request.FILES['cover']
            file_type = book.cover.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'book': book,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'books/book_form.html', context)
            book.save()
            return render(request, 'books/detail.html', {'book': book})
        context = {
            "form": form,
        }
        return render(request, 'books/book_form.html', context)


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'publisher', 'edition', 'condition', 'cost', 'category', 'cover']


def update_user(request):
    if not request.user.is_authenticated():
        return render(request, 'books/login.html')
    else:
        form = UpdateUserForm(request.POST or None)
        if form.is_valid():
            edited_user = form.save(commit=False)
            user = request.user
            username = user.username
            password = form.cleaned_data['password']
            user.email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    books = Book.objects.filter(user=request.user)
                    return render(request, 'books/index.html', {'books': books})
        context = {
            "form": form,
        }
        return render(request, 'books/update_user.html', context)


def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.user == request.user:
        book.delete()
    books = Book.objects.filter(user=request.user)
    return render(request, 'books/index.html', {'books': books})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                books = Book.objects.filter(user=request.user)
                return render(request, 'books/index.html', {'books': books})
    context = {
        "form": form,
    }
    return render(request, 'books/user_form.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'books/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                books = Book.objects.filter(user=request.user)
                return render(request, 'books/index.html', {'books': books})
            else:
                return render(request, 'books/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'books/login.html', {'error_message': 'Invalid login'})
    return render(request, 'books/login.html')


def send_email(request, book_id):
    book = Book.objects.get(pk=book_id)
    to_email = str(book.user.email)

    if book.buy_sell == 1:
        subject = "Seller for Book: " + book.title
        message = ("Hey "+str(book.user.email)+",\n\nYour requested book: "+book.title+" is being sold by: "+request.user.email+".")
    else:
        subject = "Buyer for Book: " + book.title
        message = ("Hey "+str(book.user.email)+",\n\nYour book: "+book.title+" is being requested by: "+request.user.email+".")

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("noodleportal819@gmail.com", "")  # enter password
    s.sendmail("noodleportal819@gmail.com", to_email, message)
    s.quit()

    return render(request, 'books/index.html')
