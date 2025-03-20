from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Blog

app_name = 'blog'


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'preview_image', 'is_published', ]

class BlogModeratorForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['is_published']


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'

    def get_queryset(self):
        "Возвращение опубликованных статей"
        queryset = Blog.objects.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        "Счетчик просмотров"
        obj = super().get_object(queryset)
        if obj is not None:
            obj.view_count += 1
            obj.save()
        return obj


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        "Возвращение после создания статьи"
        return reverse_lazy("blog:blogpost_detail", kwargs={"pk": self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blogpost_form.html'

    def get_form_class(self):
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            return BlogModeratorForm
        return BlogForm

    def get_success_url(self):
        "Просмотр обновленной статьи"
        return reverse('blog:blogpost_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.owner or self.request.user.has_perm('catalog.can_unpublish_product')


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')


