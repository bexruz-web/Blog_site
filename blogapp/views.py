from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Post
from .forms import CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status="published", publish__year=year, publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    # print(comments)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(
                commit=False)  ### commit=False ni ishlatib, ma'lumotlar bazasiga yozilishdan oldin obyekt ustida ishlash imkoniyatiga ega bo'lasiz.
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   })
