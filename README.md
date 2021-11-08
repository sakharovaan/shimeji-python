## Необходимые штуки (релиз 1.0)
Доделать GUI
1. + Чтобы Катру можно было перемещать по левому клику
2. + Чтобы правый клик открывал бы меню (как делать коллбеки на эти пункты?)
3. Собирать меню (системное/дебаговое) по правому клику на основе плагинов и коллбеков
4. Сделать окно диалога (которые собирается на основе плагинов), он будет единый для диалога по дабл-клик и для фраз
5. То есть Катра может начинать диалоги с вариантами ответов и ветвлением
6. Двойной клик по Катре -- диалог с пунктами меню (которые собирается на основе плагинов)
7. В диалоге текст показывается с анимацией посимвольно
8. + Анимация (мигание)

Сделать систему плагинов
1. + Какой-нибудь стандартный формат для API
2. + Плагины на питоне, каждый цикл пробегать по всем методам on_tick в плагинах
3. Сделать on_boot/on_close, который исполняется один раз
4. + Может использовать какой-то сторонний планировщик?

Сделать поведение
1. + Движок для наложения слоёв
2. + Слои накладываются с анимацией (периодичность)
3. + Наложенные слои -- теггировать по именам (файл с конфигурацией эмоций)
4. Сделать файл с рандомными фразами и возможностью внедрять теги с эмоциями (forced) и %username, делать перенос строки
5. Сделать рандомными части диалогов. То есть строчка одна, но она может комбинироваться.
6. "Сейчас %(hour12), %(username). Очень важно поддерживать режим." - говорить сколько сейчас время
7. normalboottalk -- приветствовать в зависимости от времени дня, прощаться - желать хороших снов
8. + Убрать (пока нет системы настроения) mouth с тэгом bad из рандомной ротации

Технические штуки
1. Сделать папку с плагинами, сделать категории плагинов, сделать наследование (конфиг, self.w)
2. Сделать динамическую инициализацию, но писать `__all__` = [], чтобы можно было задавать порядок без заморочек с зависимостями
3. Чтобы можно было обращаться к экземпляру класса плагина напрямую (ссылка на экземляр где-то хранилась)
4. Глобальное хранилище состояния -- там будет текущий expr, forced expr, desired expr
5. наверное плагины говорения будут через очередь передавать диалоги на плагин отображения, очередь тоже в global state
6. Придётся всё-таки делать динамический discovery слоёв, но не линковать их динамически, а указывать фрагмент имени файла (имя слоя) вместо файла
7. По поводу pdn -- сделать так чтобы у каждой группы было обязательно по одному элементу всегда, и они бы не конфликтовали (каждый элемент стыковывался бы с любыми из другой группы)


## Крутые штуки (дальше)
1. Синтез голоса
2. Помодоро
3. Чтобы она говорила идти тренироваться, спрашивала результаты и вела дневник
4. Чтобы она что-то делала (читала, следила за тобой)
5. чтобы она периодически спрашивала настроение и выбирала соотв фразы -- поддерживающие, мотивирующие
6. Чтобы у неё было своё настроение (выбор эмоции был бы не случайным), и ты бы его типа менял своими действиями
7. Когда наводишь на неё мышку, она в любом случае начинает смотреть на тебя и улыбаться, типа ты можешь захватить внимание
8. Система настроения -- можно повышать например "гладя по голове" (средняя кнопка мыши), то есть это уже регионы тела как в shimeji
9. Портит настроение если что-то делать неправильно (сидеть ночью, например) или 
10. Попробовать ещё раз сделать захват заголовков активных окон и реакцию на них
11. Локальное хранилище sqlite с синхронизацией через яндекс-диск
12. Чтобы Катра могла чем-то заниматься. Хоть книгу читать (сделать background просто как первый слой наложения)
13. Слушай, а пусть она мне рандомную картинку показывает иногда из папки с мемами
14. Вообще если честно, то я хочу иметь возможность испортить ей настроение, сделать больно, неприятно, разозлить, обидеть
15. Спрашивать её да/нет/может быть etc - на простых вероятностях
16. Игры с Катрой (https://www.tutorialspoint.com/artificial_intelligence_with_python/artificial_intelligence_with_python_gaming.htm) от текстовых до крестиков-ноликов
17. Можно попробовать взаимодействовать с Replika API через затравку диалога?

Вообще подумай, что ты можешь сделать логичным, при этом рандомным?
1. Смена эмоций на лице
2. Влияние событий (добавлять какой-то шум, чтобы поведение не было 100% детерминировано)
3. Рандомные фразы (и диалоги). Комбинирование частей фразы.

Интересные идеи
1. Катра -- кошка. Кошки боятся собак, гоняются за мышами, любят сидеть в коробках, ещё просят часто чтобы их покормили и куда-то выпустили
2. Ещё кошки мурчат, шипят, если очень злые -- воят. Ещё они иногда хотят играть и ласки.