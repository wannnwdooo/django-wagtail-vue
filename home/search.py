from wagtail.search import index

class BlogPageIndex(index.Indexed, index.SearchBoost):
    text = index.SearchField(document=True, use_template=True)
    # Добавляем поля, по которым будет производиться поиск
    title = index.SearchField(boost=2.0)
    intro = index.SearchField(boost=1.5)
    body = index.SearchField(boost=1.2)