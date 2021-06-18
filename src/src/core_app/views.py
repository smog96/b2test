import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Polygon
from .utils import CoordsIterator

log = logging.Logger(name='ext')


class CreateUpdate(TemplateView):
    template_name = 'create_update.html'
    extra_context = {
        'polygon_list': Polygon.objects.all()
    }
    object = None

    def setup(self, request, *args, **kwargs):
        super(CreateUpdate, self).setup(request, *args, **kwargs)
        if self.kwargs.get('id', None) is not None:
            self.object = get_object_or_404(
                Polygon,
                pk=kwargs.get('id', None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['object'] = self.object
            context['points'] = get_object_or_404(
                Polygon,
                pk=kwargs.get('id', None)).points
        else:
            context['points'] = []
        return context

    def post(self, request, *args, **kwargs):
        coords = [x for x in CoordsIterator(request.POST.get("pol").split(','))]
        polygon = Polygon(
            points=coords,
            name=request.POST.get("polygon_name", "Undefined :0"),
        )
        if bool(request.POST.get('for_save')):
            polygon.save()
        last_point_coords = request.POST.get("last_point").split(',')
        return render(
            request,
            self.template_name,
            self.get_context_data(message=polygon.in_polygon(check_point=last_point_coords))
        )


class PolygonList(ListView):
    template_name = 'polygon_list.html'
    queryset = Polygon.objects.all()
    paginate_by = 15
    model = Polygon

    def get_context_data(self, **kwargs):
        context = super(PolygonList, self).get_context_data()
        context["js_pols"] = [
            {
                'id': x.id,
                'points': x.points
            } for x in self.object_list
        ]
        return context
