from random import random, shuffle

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Blog
from mailing.models import Mailing, Client
# Create your views here.


class BlogListView(ListView):
    model = Blog

class HomeListView(ListView):
    model = Blog
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = len(Mailing.objects.all())
        mailings_is_active = len(Mailing.objects.filter(is_active=True))
        unique_clients_count = Client.objects.values('email').distinct().count()
        context['mailings'] = mailings
        context['mailings_is_active'] = mailings_is_active
        context['unique_clients_count'] = unique_clients_count
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = list(queryset)
        shuffle(queryset)
        return queryset[:3]

class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'picture',)
    success_url = reverse_lazy('blog:blog_home')


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_home')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'picture',)
    success_url = reverse_lazy('blog:blog_home')
