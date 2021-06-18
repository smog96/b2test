from django import template

register = template.Library()

page_count = 3


@register.filter
def pervious_page(cur_page):
    end_page = cur_page
    if cur_page < page_count:
        start_page = 2
    else:
        if cur_page == page_count:
            start_page = cur_page - page_count + 2
        else:
            start_page = cur_page - page_count + 1
    return [x for x in range(start_page, end_page)]


@register.filter
def next_pages(info_page):
    cur_page = info_page.number
    last_page = info_page.paginator.num_pages

    if last_page - cur_page < page_count:
        end_page = last_page
    else:
        end_page = cur_page + page_count
    return [x for x in range(cur_page, end_page)[1:]]
