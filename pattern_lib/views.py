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
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
from sklearn.cluster import KMeans
from django.http import JsonResponse
from django.http import HttpResponse
import chardet




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


@csrf_exempt
def multi_part(request):
    if request.method == 'POST' and 'file' in request.FILES:
        try:
            uploaded_file = request.FILES['file']

            # Обработка загруженного файла
            image = Image.open(uploaded_file)

            # Чтение параметров из запроса
            new_width = int(request.POST.get('width', 100))  # Желаемая ширина (любое положительное целое число)
            new_height = int(request.POST.get('height', 100))  # Желаемая высота (любое положительное целое число)
            color_count = int(request.POST.get('color_count', 256))  # Желаемое количество цветов (от 1 до 256)
            brightness = float(request.POST.get('brightness', 1.0))  # Уровень яркости (от 0.0 до 2.0, 1.0 - без изменений)
            contrast = float(request.POST.get('contrast', 1.0))  # Уровень контрастности (от 0.0 до 2.0, 1.0 - без изменений)
            smoothness = request.POST.get('smoothness', False)  # Сглаживание изображения (True или False)
            grayscale = request.POST.get('grayscale', False)  # Преобразование в оттенки серого (True или False)
            rotation = request.POST.get('rotation', 0)  # Поворот изображения (0, 90, 180 или 270 градусов)
            flip_horizontal = request.POST.get('flip_horizontal', False)  # Отражение по горизонтали (True или False)
            flip_vertical = request.POST.get('flip_vertical', False)  # Отражение по вертикали (True или False)
            antialias = request.POST.get('antialias', False)  # Включение антиалиасинга (True или False)
            edge_detection = request.POST.get('edge_detection', False)  # Включение обнаружения границ (True или False)
            emboss = request.POST.get('emboss', False)  # Включение тиснения (True или False)
            gaussian_blur = request.POST.get('gaussian_blur', False)  # Включение размытия Гаусса (True или False)
            invert_colors = request.POST.get('invert_colors', False)  # Инверсия цветов (True или False)

            # Применяем параметры изображения
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)

            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)

            if smoothness:
                image = image.filter(ImageFilter.SMOOTH_MORE)

            if grayscale:
                image = ImageOps.grayscale(image)

            if rotation == 90:
                image = image.rotate(90)
            elif rotation == 180:
                image = image.rotate(180)
            elif rotation == 270:
                image = image.rotate(270)

            if flip_horizontal:
                image = ImageOps.mirror(image)

            if flip_vertical:
                image = ImageOps.flip(image)

            if antialias:
                image = image.resize((new_width, new_height), Image.ANTIALIAS)
            else:
                image = image.resize((new_width, new_height))

            if edge_detection:
                image = image.filter(ImageFilter.FIND_EDGES)

            if emboss:
                image = image.filter(ImageFilter.EMBOSS)

            if gaussian_blur:
                image = image.filter(ImageFilter.GaussianBlur)

            if invert_colors:
                image = ImageOps.invert(image)

            # Преобразуем изображение в режим "RGB", если это необходимо
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Уменьшаем количество цветов
            image_array = np.array(image)

            # Получаем все уникальные цвета и их частоту
            colors, counts = np.unique(image_array.reshape(-1,3), axis=0, return_counts=True)

             # Используем частоту цветов как веса для алгоритма k-средних
            kmeans = KMeans(n_clusters=color_count, random_state=0, n_init=10).fit(colors, sample_weight=counts)

            # Центры кластеров - это новые цвета
            new_colors = kmeans.cluster_centers_.astype(int)

            # Заменяем каждый пиксель на ближайший центр кластера
            closest_clusters = kmeans.predict(image_array.reshape(-1, 3))
            image_array = image_array.reshape(-1, 3)  # разворачиваем массив для корректного обращения к пикселям
            for i, cluster in enumerate(closest_clusters):
                image_array[i] = new_colors[cluster]
            image_array = image_array.reshape(new_height, new_width, 3)  # возвращаем массив к первоначальной форме
                        
            # Преобразуем массив обратно в изображение
            image = Image.fromarray(image_array)

            # Получаем палитру изображения
            palette = image.getpalette()
            # Разбиваем палитру на группы по три элемента (RGB)
            # palette = list(zip(*[iter(palette)]*3))
            # palette = [color for color in palette if color != (0, 0, 0)]

            # Конвертируем изображение в двумерный массив пикселей
            pixel_array = list(image.getdata())
            pixel_array = [pixel_array[n:n+new_width] for n in range(0, new_width*new_height, new_width)]
            palette = list(set(value for row in pixel_array for value in row))

            color_to_digit = {color: index for index, color in enumerate(palette)}
            pixel_array = [[color_to_digit[value] for value in row] for row in pixel_array]


            # Возвращаем двумерный массив пикселей и палитру в ответе
            return JsonResponse({"pixel_array": pixel_array, "palette": palette}, safe=False)
        except Exception as e:
            return JsonResponse({"errorCode":-1,
                                 "message": str(e),
                                 "description":"/api_django/pattern_lib/multi_part/",
                                 "time": None
                                 }, status=400)
    else:
        return JsonResponse({"errorCode": "POST request with file expected"}, status=400)
