import reference_data.size_data
import instructions.stich_set
import instructions.cuffs
import instructions.heels
import instructions.sole
import instructions.toe
import reference_data.some_text

def begin_text_end(about, text):
    '''Форматирует вывод данных'''
    begin = f'------------------НАЧАЛО СПРАВКИ ПО {about}------------------\n'
    end = f'------------------КОНЕЦ СПРАВКИ ПО {about}-------------------\n'
    return begin + text + end


def size_to_count_stich(size: str, type_yearn) -> int:
    '''Преобразует размер в количество петель для набора'''
    return reference_data.size_data.SIZE_DATA.get(size)[type_yearn]

def help_type_stich_set(type_stich_set):
    '''Выводит справку по набору'''
    about = 'НАБОРУ'
    text = instructions.stich_set.stich_dict.get(type_stich_set)
    return begin_text_end(about, text)

def help_type_cuff(type_cuff):
    about = 'РЕЗИНКЕ'
    text = instructions.cuffs.cuffs_dict.get(type_cuff)
    return begin_text_end(about, text)

def help_pagolenok():
    about = 'ПАГОЛЁНКУ'
    text = reference_data.some_text.pagolenok
    return begin_text_end(about, text)

def help_type_heel(type_heel):
    about = 'ПЯТКЕ'
    text = instructions.heels.heels_dict.get(type_heel)
    return begin_text_end(about, text)

def help_type_sole(type_sole):
    about = 'ПОДОШВЕ'
    text = instructions.sole.sole_dict.get(type_sole)
    return begin_text_end(about, text)

def help_type_toe(type_toe):
    about = 'МЫСКУ'
    text = instructions.toe.toe_dict.get(type_toe)
    return begin_text_end(about, text)

def make_instruction(
        type_socks: str, # вид носка
        size,   # размер обуви
        type_yarn, #вид пряжи четырёхниточная - 0, шести - 1
        type_stich_set: str, # вид набора
        type_cuff: str,  # вид манжеты
        type_heel: str,  # вид пятки
        type_sole: str, # вид подошвы
        type_toe: str,   # вид мыска
        ) -> str: 
    instruction = f'Выбранный вид носков: {type_socks} \n' \
                  f'Размер носка:  {size} \n' \
                  f'Вид пряжи: {type_yarn}'

    instruction += f'Наберите {str(size_to_count_stich(size, type_yarn))} петель на спицы ' \
                   f'{type_stich_set} методом \n' \
                   f'Распределение по спицам ERROR дописать функцию ERROR \n \n' \
                   f'{help_type_stich_set(type_stich_set)} \n' \
                   f'Вяжите резинку на необходимую высоту \n \n' \
                   f'{help_type_cuff(type_cuff)} \n' \
                   f'Вывяжите паголёнок на необходимую длину \n \n' \
                   f'{help_pagolenok()} \n' \
                   f'Распределение по спицам пятки ERROR дописать функцию ERROR \n \n' \
                   f'Вяжите пятку по инструкции \n' \
                   f'{help_type_heel(type_heel)} \n' \
                   f'Вяжите подошву по описанию \n' \
                   f'{help_type_sole(type_sole)} \n' \
                   f'Вяжите мысок по описанию \n' \
                   f'{help_type_toe(type_toe)} \n' \
                   f'Проденьте сквозь оставшиеся петли нитку, затяните и завяжите изнутри\n' \
                   f'Поздравляем, носок готов!  \n' \


    return instruction

print(make_instruction(
    'Носки средние', # вид носка
    '42/43', # размер обуви
    0, #вид пряжи четырёхниточная - 0, шести - 1
    'cross_classic', # вид набора
    'rubber_1x1', # вид манжеты
    'three_part_rounded_heel', # вид пятки
    'smooth_sole', # вид подошвы
    'tape_toe', # ленточный мысок
))