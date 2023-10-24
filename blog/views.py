from random import  shuffle
from django.core.cache import cache

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Blog
from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Client
# Create your views here.


class BlogListView(ListView):
    model = Blog

    def cache_example(self):
        if CACHE_ENABLED:
            blog_list = cache.get('blog_list_cache')
            if blog_list is None:
                blog_list = super().get_queryset()
                cache.set('blog_list_cache', blog_list)
        else:
            blog_list = super().get_queryset()
        return blog_list


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
        if CACHE_ENABLED:
            queryset = cache.get('home_list_cache')
            if queryset is None:
                queryset = super().get_queryset(*args, **kwargs)
                queryset = list(queryset)
                shuffle(queryset)
                cache.set('home_list_cache', queryset)
        else:
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
