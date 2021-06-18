import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Polygon
from .utils import CoordsIterator

log = logging.Logger(name='ext')


class Index(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'polygon_list': Polygon.objects.all()
    }

    def get(self, request, *args, **kwargs):
        if kwargs.get('id', None):
            self.extra_context['obj'] = get_object_or_404(Polygon, pk=kwargs.get('id', None))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        coords = [x for x in CoordsIterator(request.POST.get("pol").split(','))]
        polygon = Polygon.objects.create(
            name=request.POST.get("polygon_name", "Undefined :0"),
            points=coords,
        )
        if bool(request.POST.get('for_save')):
            polygon.save()
        last_point_coords = request.POST.get("last_point").split(',')
        log.warning(coords)
        log.warning(last_point_coords)
        return render(
            request,
            self.template_name,
            {
                'message': polygon.in_polygon(check_point=last_point_coords)
            }
        )
