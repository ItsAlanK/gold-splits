from posts.models import Category


def category_list(request):
    category_list = Category.objects.all()
    return {'categorys': category_list}
