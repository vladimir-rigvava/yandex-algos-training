# https://contest.yandex.ru/contest/27883/problems/C/
#
# Будем решать с помощью сортировки событий.
# События в данном случае будут следующими:
# 1. Студент появился на позиции x;
# 2. Достигнуто максимальное расстояние (x + D), на котором мог переговариваться студент.
# Составим список таких событий для всех студентов, для каждого будет ровно два события.
# Отсортируем этот список, чтобы событие 1 шло раньше события 2.
# Теперь пройдём по всем событиям и для событий 1 будем назначать студенту минимальный доступный номер билета,
# а для событий 2 будем разрешать снова использовать номер билета студента.
# В конце выведем назначенные номера билетов в порядке появления студентов в исходном массиве координат.
#
# Рассмотрим пример [1, 2, 3, 4, 5, 6, 8, 10, 11, 13, 16] при D=2
#   __ __
#  __ __   __ __
# __ __  __ __    __
# 1.3.5.7.9.........
# Ответом будет [1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 1]
#
# Сложность сортировки O(N*log(N)), цикл O(N), внутри цикла операции над кучей за O(log(N)).
# Итоговая асимптотика O(N*log(N)).
from heapq import heappop, heappush


def exam(xs, d):
    n = len(xs)
    # Сразу создаём массив необходимой длины – в два раза больше чем количество студентов.
    events = [None] * (n * 2)
    # Используем константы для корректной сортировки пар значений (координата студента, событие).
    STUDENT_START = -1
    STUDENT_END = 1
    # Заполняем массив событий и сортируем его.
    for i, x in enumerate(xs):
        events[i * 2] = (x, STUDENT_START)
        events[i * 2 + 1] = (x + d, STUDENT_END)
    sorted_events = sorted(events)

    # Будем решать задачу за один проход, поэтому сразу создаём все переменные,
    # которые будем обновлять на каждом шаге итерации.

    # Далее exam_number – номер билета.
    max_exam_number = 0

    # Координаты студентов могут принимать значения от 0 до 10^6 включительно.
    # Сразу создадим массив решений максимального размера,
    # по координате студента храним в этом массиве номер его билета.
    students_exam_numbers = [None] * (1_000_000 + 1)

    # Для получения текущего минимального номера билета будем использовать минимальную кучу (min heap).
    # Основные операции этой структуры данных – это удаление минимума и добавление нового элемента за O(log(N)).
    # Максимум билетов может быть столько же сколько студентов, то есть N.
    heap = list(range(1, n + 1))

    # Итерируемся по всем событиям.
    for x, event in sorted_events:
        if event == STUDENT_START:
            # Получаем минимальный доступный номер билета.
            next_exam_number = heappop(heap)
            max_exam_number = max(max_exam_number, next_exam_number)
            students_exam_numbers[x] = next_exam_number
        elif event == STUDENT_END:
            # Получаем номер билета текущего студента.
            student_exam_number = students_exam_numbers[x - d]
            # Добавляем этот номер билета в кучу.
            heappush(heap, student_exam_number)

    # Нам надо вывести номера билетов студентов в том порядке,
    # в котором они были перечислены в исходном списке.
    # Для этого пройдёмся по исходному списку и по координате студента
    # получим номер его билета из students_exam_numbers.
    return max_exam_number, [students_exam_numbers[x] for x in xs]


assert exam([11, 1, 12, 2], 1) == (2, [1, 1, 2, 2])
assert exam([11, 1, 12, 2], 0) == (1, [1, 1, 1, 1])
assert exam([1, 2, 3, 4, 5, 6, 8, 10, 11, 13, 16], 2) == (3, [1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 1])
assert exam([1, 2, 3, 4, 5, 6, 9, 12, 13, 16, 20], 3) == (4, [1, 2, 3, 4, 1, 2, 1, 2, 1, 2, 1])
assert exam([20, 16, 13, 12, 9, 6, 5, 4, 3, 2, 1], 3) == (4, [1, 2, 1, 2, 1, 2, 1, 4, 3, 2, 1])
assert exam([1, 101, 201, 301, 401], 100) == (2, [1, 2, 1, 2, 1])
assert exam([1, 5, 6, 7, 8], 5) == (4, [1, 2, 3, 1, 4])
assert exam([1, 6, 7, 8], 5) == (3, [1, 2, 1, 3])
assert exam([1, 101, 102, 103, 104], 100) == (4, [1, 2, 1, 3, 4])


def main():
    n, d = map(int, input().split())
    xs = list(map(int, input().split()))
    result = exam(xs, d)
    print(result[0])
    print(*result[1])


if __name__ == '__main__':
    main()