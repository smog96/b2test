from django.db import models
from django.contrib.postgres.fields import ArrayField


class Polygon(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    points = ArrayField(ArrayField(models.IntegerField(), size=2), size=10)
    name = models.CharField("Наименование", max_length=255)

    def __check_point(self, check_point: [int, int]) -> bool:
        x, y = int(check_point[0]), int(check_point[1])
        res = False
        for index, vec in enumerate(self.points):
            x_point, y_point = int(vec[0]), int(vec[1])
            x_point_previous, y_point_previous = int(self.points[index - 1][0]), int(self.points[index - 1][1])
            if (((y_point <= y < y_point_previous) or (y_point_previous <= y < y_point)) and
                    (x > (x_point_previous - x_point) * (y - y_point) / (y_point_previous - y_point) + x_point)):
                res = not res
        return res

    def in_polygon(self, check_point: [int, int]) -> str:
        if self.__check_point(check_point):
            return "Точка внутри полигона"
        return "Точка вне полигона"

    class Meta:
        db_table = 'polygon'
        verbose_name = 'Полигон'
        verbose_name_plural = 'Полигоны'
