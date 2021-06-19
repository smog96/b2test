import logging

from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Polygon
from .utils import CoordsIterator, get_or_none

log = logging.Logger(name='default')


class PolygonViewBase(TemplateView):
    template_name = 'create_update.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
        self.polygon = None

    def setup(self, request, *args, **kwargs):
        """
            Инициализация в CBV в setup > __init__
        """

        super().setup(request, *args, **kwargs)
        if self.kwargs.get('id', None) is not None:
            self.object = get_object_or_404(
                Polygon,
                pk=kwargs.get('id', None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_check"] = self.request.session.pop('last_check', None)
        if self.object:
            context['object'] = self.object
            context['points'] = get_object_or_404(
                Polygon,
                pk=kwargs.get('id', None)).points
        else:
            context['points'] = []
        return context


class PolygonView(PolygonViewBase):
    """
        Контроллер просмотра готового полигона
    """
    extra_context = {
        "title": "Просмотр полигона"
    }


class PolygonPostView(PolygonViewBase):
    """
        Контроллер обработки POST запроса.
        Сделано, чтобы избежать повторной отправки данных.
    """

    def validate(self) -> None:
        data = self.request.POST
        try:
            if len(data.get("pol").split(',')) % 2 != 0:
                raise ValidationError
        except ValueError:
            raise ValidationError
        return

    def post(self, request, *args, **kwargs):
        self.validate()
        coords = [x for x in CoordsIterator(request.POST.get("pol").split(','))]    # js отдает координаты в str
        self.polygon = get_or_none(Polygon, id=request.POST.get('object_id'))

        if not self.polygon:
            self.polygon = Polygon(
                points=coords,
                name=request.POST.get("polygon_name", "Undefined"),
            )
        request.session['last_check'] = self.polygon.in_polygon(
            check_point=request.POST.get("last_point").split(','))

        # обрабатываем возможность сохранения полигона
        if bool(request.POST.get('for_save')):
            self.polygon.save()
        if hasattr(self.polygon, "id") and self.polygon.id:
            return HttpResponseRedirect(self.polygon.get_absolute_url())
        return HttpResponseRedirect(reverse('create'))


class PolygonList(ListView):
    """
        Контроллер списка полигонов
    """
    template_name = 'polygon_list.html'
    queryset = Polygon.objects.all()
    paginate_by = 15
    model = Polygon
    extra_context = {
        "title": "Список полигонов"
    }

    def get_context_data(self, **kwargs):
        context = super(PolygonList, self).get_context_data()

        # Контекст для Vue.js, чтобы в списке полигонов построить
        # canvas элементы
        context["js_pols"] = Polygon.get_pols_js(self.object_list)
        return context
