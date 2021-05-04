![Header ICG](./Header_ICG.svg)

# Лабораторный журнал

## Данные

* [Метрика экзомных данных](./data/SamplesData.csv)

## Проекты

* [Поиск вариантов в экзомных данных](./projects/ExomeVariants.md)
* [NIPT](./projects/NIPT.md)
* [Дипломная работа](./projects/Graduate.md)

[Архивные материалы](./archive)

## Инструменты

1. [MachineConfig](./tools/MachineConfig): полуавтоматическая конфигурация биоинформационной машины
2. [Scissors](./tools/Scissors): Пайплайн для обработки экзомных данных
3. [FastContext](./tools/FastContext): Инструмент для контекстного анализа ридов

## Активные задачи

| Task | Description | Status | Deadline |
|:-----|:------------|:-------|:---------|
| Баркодирование сайтов рестрикции | Подумать | - | - |
| Бенчмарк | Запустить тулзы у нас | - | - |
| Мензоров | Посмотреть кмеры в транскриптомах человека | - | - |
| LNCAP | Сравнить снипы наших и контрольных данных | - | - |
| Презентация | Неинвазивный пренатальный скрининг - технология, необходимые материалы и т.д. | В процессе | - |
| Форма информированного согласия | для обычного экзома, генома и Exo-С | В процессе | - |
| Написать в этический комитет | - | Ожидание | - |
| Доклад |  Взять экзом и ехос данные, разделить их на те, которые попадают в капчу, и те, которые не попадают. | Ожидание | - |
| Анализ | Процент мисматчей в дорожках А и B. Посмотреть, какого хуя там ещё какие-то последовательности. | Ожидание | - |
| Анализ | FR600+Illumina (если >5000 ридов с адаптером - сливаем с FR600 и смотрим) | Ожидание | - |
| Доработка Scissors | Добавить пол, а также warning по покрытию Y-хромосомы | Ожидание | - |

## Учёба

| Предмет | Отчётность | ФИО препода | Контакты | Долги |
|:---|:----|:----|:---|:---|
| Акушерство и гинекология | Зачет | Наталья Михайловна Пасман (лекции), Опарина Марина Петровна +79139190707 Дударева Алла Витальевна +79139227408 (семинар) |  | |
| Госпитальная терапия | Зачет | Воротников Иван Борисович +79139029927, Летягина Елена Алексеевна +79139874558, Омельченко Виталий Олегович +7 952 916-97-49 | | |
| Госпитальная хирургия | Зачет | Вернер | | |
| Инфекционные болезни, эпидемиология | Зачет | | | |
| Клеточные технологии в лечении заболеваний | Зачет | | | [тест](https://drive.google.com/file/d/1Hw7BlQH3BUjgCO1sVq3M5JleBHkVAIn5/view?usp=sharing), отправить на makar@niimbb.ru (5 мая 2021) |
| Нейроэндокринология | Дифференцированный зачет | | | |
| Неотложные состояния, симуляционный курс | Экзамен | Кочетков Евгений Станиславович +79137190483 | | |
| Общественное здоровье и здравоохранение, экономика здравоохранения | Дифференцированный зачет | Майер Екатерина Олеговна | +79139004449 | |
| Основы гемостаза и биохимические аспекты клинической гемостазиологии | Дифференцированный зачет | 
Виктор Геннадьевич Стуров | sturov@mail.ru | Реферат клиническая биохимия "Акушерские кровотечения: современные аспекты патогенеза, диагностика, Тактика ведения пациенток в аспекте клинических современных рекомендаций" (до 21 мая 2021, [скинуть на диск](https://drive.google.com/drive/u/1/folders/1XF7jHJj3cfrr8WrlfVJrPG2NsDGiPrLg)) |
| Подготовка к защите и защита выпускной квалификационной работы | Экзамен | | | |
| Подготовка к сдаче и сдача государственного экзамена | Экзамен | | | |
| Поликлиническая терапия | Дифференцированный зачет | Чугуров Александр Степанович +79137866242, Солдатова Галина Сергеевна +79139117164, Бочкова Юлия Валерьевна +7 913 717-41-96 | | |
| Производственная практика, научно-исследовательская практика | Экзамен | | | |
| Профессиональные болезни | Зачет | Долгова Нина Анатолеьвна +79139466299 | | |
| Роль опухолевого микроокружения в канцерогенезе | Зачет | | | |
| Травматология, ортопедия | Зачет | Сорокин Артем Николаевич +79133827474 | |  |


## Завершенные задачи

<details>
<summary>Tl;dr</summary>

[10/02/2021, 20:01:40]: Описания пациентов собрал в табличку, FastQ отдал ребятам из Сбера
[12/02/2021, 20:28:35]: Сделал HiC-карты для статьи
[12/02/2021, 20:29:25]: Настроил почту
[17/02/2021, 19:34:00]: Правки к статье готовы
[19/02/2021, 12:36:40]: Оформил всё к курсовой
[19/02/2021, 17:01:45]: Посчитал обогащение Exo-C-библиотеки (демультиплекс Алины)
[05/03/2021, 13:52:47]: Проанализировал микрочипы из Томска
[10/03/2021, 12:13:56]: Добавил аннотацию к микрочипам
[10/03/2021, 19:05:46]: Посчитал обогащение к получившимся образцам Exo-C
[16/03/2021, 18:54:43]: Прикрутил к пайплайну region-based аннотацию и проблемные регионы
[16/03/2021, 18:55:44]: Отправил данные двух братьев
[17/03/2021, 15:48:08]: Посчитал статики для диплома
[17/03/2021, 23:13:46]: Пересек контроль для диплома с экзомом и удивился
[17/03/2021, 23:14:09]: Валидировал варианты Exo-C библиотек
[19/03/2021, 17:21:37]: Сделал Динаре мутации
[22/03/2021, 14:53:28]: Сбер, сделал VCF аннотиванные анноваром
[26/03/2021, 21:25:15]: Сделал поздравлялочку по email
[31/03/2021, 13:44:48]: ROC-кривая для диплома
[19/04/2021, 15:13:25]: Сделал общую табличку



</details>

<!---

Дела по учёбе

- реферат бочковой метаболический синдром от руки
- 
- Отработки Дударевой?
- Майер тест, https://classroom.google.com/c/Mjg4ODMxMzk0MzM5, дедлайн 17 марта, ответы сюда: e.maier7@g.nsu.ru
- написать реферат (можно на компьютере) по одной из гипокоагуляционной тромбофилии (афс-синдром, двс-синдром, болезнь Мошковица) на почту ей Skvortsova-1963@bk.ru

Опарина Марина Петровна +7 913 919-07-07
Чугуров Александр Степанович +7 913 786-62-42
Рутковский Евгений Александрович +79618761115
Кочетков Евгений Станиславович +7 913 719-04-83
Долгова Нина Анатолеьвна +79139466299
Омельченко Виталий Олегович +7 952 916-97-49
Солдатова Галина Сергеевна +79139117164
Корбут Антон Иванович +79231777911

Бочкова Юлия Валерьевна +7 913 717-41-96
Сорокин Артем Николаевич +79133827474
Дударева Алла Витальевна +79139227408
Бухтуева Наталья Геннадьевна +79137760686
Воротников Иван Борисович +7 913 902-99-27
Летягина Елена Алексеевна +7 913 987-45-58
Вагнер Юлия Николаевна +7 983 320-33-06
Королев Максим Александрович +79137425577
Петухова Анна Владимировна +79139473380
-->
