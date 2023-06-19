import instructions.cuffs as ins_cuff
import instructions.stich_set as ins_stich

SOCKS_TYPE = (
    '- Носки следки\n'
    '- Носки низкие\n'
    '- Носки средние\n'
    '- Носки высокие\n'
    '- Носки гольфы\n'
    '- Чулки низкие\n'
    '- Чулки высокие\n'
    '- Чулки сетка\n'
)

# dict size: number of stitch [four_thread_yarn, six_thread_yarn]
SIZE_DATA = {
    '20/21': [44, 32],
    '22/23': [44, 32],
    '24/25': [48, 36],
    '26/27': [48, 36],
    '28/29': [52, 40],
    '30/31': [52, 40],
    '32/33': [56, 44],
    '34/35': [56, 44],
    '36/37': [60, 48],
    '38/39': [60, 48],
    '40/41': [64, 52],
    '42/43': [64, 52],
    '44/45': [68, 52],
    '46/47': [72, 56],
    '48/49': [72, 56],
    '50/51': [76, 60],
}


def user_inputting_data():
    '''Функция ввода данных от пользователя'''
    dct = {}

    def size_input():
        '''Функция ввода данных/размеров и расчёта количества петель'''
        choice_text = ('Хотите выбрать размер из таблицы(1) или ввести'
                       'результаты снятия мерок(2)(окружность у ноги  у '
                       'косточки и окружность по подъёму)?\n'
                       'Введите цифру в соответствии с выбранным вариантом')
        way = input(choice_text)
        if way == '1':
            size = input('Выберите размер носка'
                         f'{SIZE_DATA.keys()}')
            yarn = int(input('Использете четырёхниточную(0) пряжу'
                             'или шестиниточную(1)?'))
            return {'size': size, 'yarn': yarn}
        elif way == '2':
            size_1, size_2 = input('Введите окружность ноги у косточки'
                         'и по подъёму через пробел в см')
            sample_length_sample = input('Введите длину образца(измерять вдоль рядов)')
            sample_stich_count = input('Введите количество петель в образце')
            return {'size_1': size_1,
                    'size_2': size_2,
                    'sample_lenght_sample': sample_length_sample,
                    'sample_stich_count': sample_stich_count}
        return 'SIZE INPUT ERROR NO WAY'
    

    
    def cuff_choice():
        '''Функция выбора манжеты'''

        cuff_type = input(ins_stich.type_stich_list)

    socks_type = input(
        'Какой вид носка вы хотите связать?\n'
        f'{SOCKS_TYPE}'
    )
    print(socks_type)
    # тут как бы от вида носка по хорошему должно что-то зависеть и нужно что-то менять
    # и меняться будет наличие паголёнка и его длина, а так же длина резинки
    quantity_stitch = size_input()
    print(quantity_stitch)
    return {
        'socks_type': socks_type,
        'quantity_stitch': quantity_stitch,
    }


def make_socks_instruction(*args):
    '''Функция генерации инструкции'''


# считаем количество петель в 1 см образце
            stich_in_cm = sample_stich_count / sample_length_sample 
            # считаем среднее от мерок и умножаем на количество петель в см
            stich_count = (size_1 + size_2) / 2 * stich_in_cm
    pass

    return f'asdasd \n' \
           f'Вид носка {args.get('socks_type')} asdasd' \
           f'Наберите {args.get('quantity_stich')}' 
        


make_socks_instruction()
