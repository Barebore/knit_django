from rest_framework import viewsets
from .models import Pattern, Category
from .serializers import (PatternSerializer, CategorySerializer,
                          PatternDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import io
from PIL import Image
from django.http import JsonResponse



class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    # pagination_class = None
    filterset_fields = ('category', )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = LimitOffsetPagination

    # для обработки запроса формата pattern/3, где 3 - id поста
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PatternDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class CattegoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = ()

@csrf_exempt
def image_process(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        data = json.loads(request.body)
        image_base64 = data.get('image')  # Картинка в формате base64
        new_width = int(data.get('width'))  # Желаемая ширина
        new_height = int(data.get('height'))  # Желаемая высота
        color_count = int(data.get('color_count'))  # Желаемое количество цветов
        if image_base64 is None or new_width is None or new_height is None or color_count is None:
            return JsonResponse({"error": "one of the parameters is not specified"}, status=400)

        # Конвертируем base64 в PIL Image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

        # Изменяем размер изображения
        image = image.resize((new_width, new_height))

        # Преобразуем изображение в режим "RGB", если это необходимо
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Уменьшаем количество цветов
        image = image.quantize(colors=color_count)

        # Получаем палитру изображения
        palette = image.getpalette()

        # Преобразуем изображение обратно в режим "RGB" для base64 кодирования
        image_rgb = image.convert('RGB')

        # Конвертируем изображение в base64
        buffered = io.BytesIO()
        image_rgb.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Конвертируем изображение в двумерный массив пикселей
        pixel_array = list(image.getdata())
        pixel_array = [pixel_array[n:n+new_width] for n in range(0, new_width*new_height, new_width)]

        # Возвращаем двумерный массив пикселей, палитру и base64 строку в ответе
        return JsonResponse({"pixel_array": pixel_array, "palette": palette, "image_base64": img_str}, safe=False)
    else:
        return JsonResponse({"error": "POST request expected"}, status=400)

