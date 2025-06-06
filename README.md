# Отчет к лабораторным работам

## Лабораторная работа №1

![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20084634.png)

# Краткое описание алгоритмов

## Алгоритм ЦДА (DDA)
Последовательно продвигается от начала к концу, равномерно увеличивая координаты и на каждом шаге выбирая ближайший пиксель.
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/cda.png)

## Алгоритм Брезенхема
Использует целочисленный счётчик ошибки для решения, в каком направлении сдвинуться (по X или по Y), чтобы линия шла максимально близко к идеалу.
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/b.png)

## Алгоритм Ву
Строит сглаженную линию, распределяя яркость между двумя соседними пикселями для устранения «ступенек» и получения более плавного контура.

![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/wu.png)



## Лабораторная работа №2

![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20084656.png)

# Краткое описание алгоритмов

## Алгоритм построения окружности
Использует метод симметрии восьми октантов для равномерного построения окружности. Текущая точка выбирается на основе знака ошибки, что позволяет минимизировать вычисления и сохранить целочисленность. Алгоритм последовательно определяет, нужно ли сместить текущую точку вверх или вправо.  
![Пример окружности](https://github.com/MariiaKandaurova/sem6/blob/main/images/c.png)

## Алгоритм построения эллипса
Основывается на методе деления эллипса на два региона для упрощения расчетов. В первом регионе вычисляется начальная точка с использованием вертикальной полуоси, во втором — с горизонтальной. Использует целочисленные вычисления для повышения скорости работы.  
![Пример эллипса](https://github.com/MariiaKandaurova/sem6/blob/main/images/e.png)

## Алгоритм построения параболы
Построение осуществляется на основе уравнения параболы. Использует итеративный подсчет координат для достижения высокой точности и симметрии.  
![Пример параболы](https://github.com/MariiaKandaurova/sem6/blob/main/images/p.png)

## Алгоритм построения гиперболы
Использует метод аппроксимации гиперболы с точным расчетом координат. Работает с двумя ветвями, каждая из которых формируется от начальной точки до заданного предела.  
![Пример гиперболы](https://github.com/MariiaKandaurova/sem6/blob/main/images/h.png)

# Лабораторная работа №3

![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20084710.png)

# Краткое описание алгоритмов

## Метод Эрмита
Создаёт плавную кривую между заданными точками с учётом направлений касательных. Использует кубические полиномы для построения сегментов кривой.  


## Форма Безье
Построение кривой на основе четырёх контрольных точек: двух концевых и двух опорных. Кривая плавно следует за опорными точками, обеспечивая интуитивное управление формой.  

## B-сплайн
Генерирует гладкие кривые, проходящие рядом с заданными точками. Обеспечивает непрерывность первой и второй производных на стыках сегментов, делая кривую гибкой и плавной.  
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/curve.png)

# Лабораторная работа №4

![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw4.png)

# Краткое описание алгоритмов

### Поворот
Метод **rotate_axis** поворачивает модель вокруг выбранной оси на заданный угол:
- **Поворот X 30°** — поворот на 30 градусов вокруг оси X;
- **Поворот Y 45°** — поворот на 45 градусов вокруг оси Y;
- **Поворот Z 30°** — поворот на 30 градусов вокруг оси Z.

### Масштабирование
Метод **uniform_scale** изменяет размер модели пропорционально заданному множителю:
- **Масштаб ×1.5** — увеличение масштаба в 1.5 раза.

### Отражение
Метод **reflect** отражает модель относительно выбранной координатной оси:
- **Отразить X** — отражение относительно оси X;
- **Отразить Y** — отражение относительно оси Y;
- **Отразить Z** — отражение относительно оси Z.

### Перспектива
Метод **toggle_perspective** включает или отключает перспективное проецирование:
- **Перспектива ON/OFF** — переключение режима перспективы.

### Сброс
Метод **reset** восстанавливает начальное положение модели, сбрасывая все преобразования:
- **Сброс** — возврат к исходным координатам и масштабу модели.
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/cube.png)

# Лабораторная работа №5 и №6
![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw5.png)
![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw7.png)

## Построение полигонов (Лабораторная работа №5)

### Основные возможности

- **Построение полигонов:** Создание замкнутых многоугольников с произвольным числом вершин. Вершины добавляются щелчком мыши, а завершение полигона происходит при двойном щелчке.

- **Проверка выпуклости:** Определяет, является ли текущий полигон выпуклым, анализируя изменение знака векторов нормалей. Если все векторы направлены в одну сторону, полигон считается выпуклым.

- **Построение выпуклых оболочек:** 
  - **Метод Грэхема:** Строит выпуклую оболочку путём сортировки точек по углу относительно самой левой нижней точки и последовательного обхода множества.
  - **Метод Джарвиса:** Последовательно добавляет вершины, формируя минимальную выпуклую оболочку, используя алгоритм обхода точек.

- **Вычисление внутренних нормалей:** Определяет направления нормалей для рёбер выпуклого полигона. Нормали направлены внутрь фигуры, что позволяет использовать их для последующих геометрических вычислений.

- **Определение пересечений:** Вычисляет точки пересечения заданного отрезка с рёбрами полигона, используя метод детерминантов для проверки пересечений.


## Алгоритмы заливки (Лабораторная работа №6)

Реализованы четыре основных алгоритма для закраски областей:

- **Простой алгоритм заполнения с затравкой**  
  Работает путём проверки цвета текущего пикселя и, если он совпадает с целевым, заливает его, добавляя соседние пиксели в стек для дальнейшей проверки.

- **Построчный алгоритм заполнения с затравкой**  
  Ищет левые и правые границы строки, заливает область между ними и переходит к соседним строкам. Хранит координаты уже посещённых пикселей для предотвращения повторной обработки.

- **Алгоритм растровой развертки с упорядоченным списком рёбер**  
  Использует упорядоченный список рёбер для определения точек пересечения горизонтальной строки с рёбрами многоугольника. Заливает область между парными пересечениями, обновляя список рёбер для каждой строки.

- **Алгоритм растровой развертки с упорядоченным списком активных рёбер**  
  Поддерживает динамическое добавление и удаление рёбер в процессе заливки. Работает с горизонтальными строками, находя пересечения рёбер с текущей строкой и заполняя пиксели между этими пересечениями.
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20073910.png)
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20073950.png)
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw1.png)
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw3.png)
![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw6.png)

  # Лабораторная работа №7

![Условие](https://github.com/MariiaKandaurova/sem6/blob/main/images/lw2.png)

# Краткое описание алгоритмов

## Триангуляция Делоне
Построение сети треугольников для заданного множества точек, обладающей следующими свойствами:
- Треугольники образуют планарный граф, где никакие рёбра не пересекаются.
- Для каждого треугольника существует описанная окружность, которая не содержит других точек множества внутри себя.
## Диаграмма Вороного
Разбиение плоскости на ячейки, каждая из которых состоит из всех точек, ближе расположенных к данному узлу, чем к любому другому узлу. Основные свойства:
- Каждая ячейка — выпуклый многоугольник.
- Рёбра находятся на серединных перпендикулярах рёбер триангуляции Делоне.


![Пример](https://github.com/MariiaKandaurova/sem6/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-13%20082926.png)






