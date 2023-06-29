import base64
import os
import io
import json

import numpy as np
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from rest_framework.decorators import api_view
from rest_framework.request import Request
from sklearn.cluster import KMeans


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
            smoothness = request.POST.get('smoothness', False) == 'true'  # Сглаживание изображения (True или False)
            grayscale = request.POST.get('grayscale', False) == 'true'  # Преобразование в оттенки серого (True или False)
            rotation = int(request.POST.get('rotation', 0)) # Поворот изображения (0, 90, 180 или 270 градусов)
            flip_horizontal = request.POST.get('flip_horizontal', False) == 'true'  # Отражение по горизонтали (True или False)
            flip_vertical = request.POST.get('flip_vertical', False) == 'true'  # Отражение по вертикали (True или False)
            antialias = request.POST.get('antialias', False) == 'true'  # Включение антиалиасинга (True или False)
            edge_detection = request.POST.get('edge_detection', False) == 'true'  # Включение обнаружения границ (True или False)
            emboss = request.POST.get('emboss', False) == 'true' # Включение тиснения (True или False)
            gaussian_blur = request.POST.get('gaussian_blur', False) == 'true'  # Включение размытия Гаусса (True или False)
            invert_colors = request.POST.get('invert_colors', False) == 'true' # Инверсия цветов (True или False)

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

from django.http import FileResponse
from PIL import Image, ImageDraw, ImageFont
from rest_framework.decorators import api_view
from rest_framework.request import Request
import json
import numpy as np

from django.http import FileResponse
from PIL import Image, ImageDraw, ImageFont
from rest_framework.decorators import api_view
from rest_framework.request import Request
import json
import numpy as np
from io import BytesIO

@api_view(['POST'])
def create_image(request: Request):
    data = json.loads(request.body)

    pixel_array = data.get('pixel_array')
    border_color = tuple(data.get('border_color'))
    palette = {item['id']: item for item in data.get('palette')}

    pixel_size = 15
    border_size = 1
    grid_size = pixel_size + border_size
    legend_height = grid_size * len(palette) // 100 * 50
    top_bottom_margin = 30  # Increase/decrease for more/less space
    axis_margin = 10  # Increase for more space between axis labels and image
    color_label_spacing = 30  # Increase for more space between color labels

    img_width = len(pixel_array[0]) * grid_size + 2 * top_bottom_margin
    img_height = len(pixel_array) * grid_size + 2 * axis_margin + 2 * top_bottom_margin + legend_height

    img = Image.new('RGB', (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    current_path = os.path.dirname(os.path.realpath(__file__))
    font_path = os.path.join(current_path, "Manrope-Regular.ttf")
    # font_path = 'Manrope-Regular.ttf'
    font = ImageFont.truetype(font_path, 14)

    # Draw grid lines

    # Draw pixels
    for y, row in enumerate(pixel_array):
        for x, pixel in enumerate(row):
            color = tuple(palette[pixel]['color'])
            rect_start = (x*grid_size + top_bottom_margin, y*grid_size + top_bottom_margin + axis_margin)
            rect_end = (rect_start[0] + pixel_size, rect_start[1] + pixel_size)
            draw.rectangle([rect_start, rect_end], fill=color, outline=border_color)

     # Draw axis labels and dotted lines
    dash_length = 5
    dash_width = 3  # Increase/decrease for thicker/thinner dash lines
    for i in range(0, len(pixel_array[0]), 10):
        # Draw dotted lines
        for j in range(top_bottom_margin + axis_margin, len(pixel_array) * grid_size + top_bottom_margin + axis_margin, dash_length * 4):
            draw.line((i * grid_size + top_bottom_margin, j, i * grid_size + top_bottom_margin, j + dash_length), fill='white', width=dash_width)
            draw.line((i * grid_size + top_bottom_margin, j + dash_length * 2, i * grid_size + top_bottom_margin, j + dash_length * 3), fill=border_color, width=dash_width)
        # Draw labels
        draw.text((i*grid_size + top_bottom_margin, top_bottom_margin // 2), str(i), fill='black', font=font)
        draw.text((i*grid_size + top_bottom_margin, len(pixel_array)*grid_size + top_bottom_margin + axis_margin + axis_margin // 2), str(i), fill='black', font=font)
    
    for i in range(0, len(pixel_array), 10):
        # Draw dotted lines
        for j in range(top_bottom_margin + axis_margin, len(pixel_array[0]) * grid_size + top_bottom_margin + axis_margin, dash_length * 4):
            draw.line((j, i * grid_size + top_bottom_margin + axis_margin, j + dash_length, i * grid_size + top_bottom_margin + axis_margin), fill='white', width=dash_width)
            draw.line((j + dash_length * 2, i * grid_size + top_bottom_margin + axis_margin, j + dash_length * 3, i * grid_size + top_bottom_margin + axis_margin), fill=border_color, width=dash_width)
        # Draw labels
        draw.text((top_bottom_margin // 2, i*grid_size + top_bottom_margin + axis_margin), str(i), fill='black', font=font)
        draw.text((len(pixel_array[0])*grid_size + top_bottom_margin + axis_margin // 2, i*grid_size + top_bottom_margin + axis_margin), str(i), fill='black', font=font)

    # Calculate max length of label
    max_label_length = max([draw.textsize(color['name'], font=font)[0] for color in palette.values()])
    max_legend_per_row = img_width // (grid_size + max_label_length + color_label_spacing)  # Maximum number of colors that can fit in a row

    # Draw legend
    for i, color in enumerate(palette.values()):
        row = i // max_legend_per_row
        column = i % max_legend_per_row
        rect_start = (column * (grid_size + max_label_length + color_label_spacing) + top_bottom_margin, 
                      len(pixel_array)*grid_size + row * (grid_size + color_label_spacing) + 2 * top_bottom_margin + axis_margin)
        rect_end = (rect_start[0] + pixel_size, rect_start[1] + pixel_size)
        draw.rectangle([rect_start, rect_end], fill=tuple(color['color']), outline='black')
        draw.text((rect_end[0] + border_size+5, rect_start[1]), color['name'], fill='black', font=font)

    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    return FileResponse(img_io, content_type='image/png')