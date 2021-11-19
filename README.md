## Необходимые штуки (релиз 1.0)
Доделать GUI
1. +Чтобы Катру можно было перемещать по левому клику
2. +Чтобы правый клик открывал бы меню (как делать коллбеки на эти пункты?)
3. Собирать меню (системное/дебаговое) по правому клику на основе плагинов и коллбеков
4. +Сделать базовое окно диалога для текста
5. Сделать окно диалога (которые собирается на основе плагинов), он будет единый для диалога по дабл-клик
6. То есть Катра может начинать диалоги с вариантами ответов и ветвлением
7. Двойной клик по Катре -- диалог с пунктами меню (которые собирается на основе плагинов)
8. +В диалоге текст показывается с анимацией посимвольно
9. +Анимация (мигание)
10. Клик по диалогу закрывает его

Сделать систему плагинов
1. +Какой-нибудь стандартный формат для API
2. +Плагины на питоне, каждый цикл пробегать по всем методам on_tick в плагинах
3. Сделать on_boot/on_close, который исполняется один раз. on_boot это не init, в init техника, в on_boot поведение - не забывать ожидание после on_close -- start/stop plugin
4. +Может использовать какой-то сторонний планировщик?

Сделать поведение
1. +Движок для наложения слоёв
2. +Слои накладываются с анимацией (периодичность)
3. +Наложенные слои -- теггировать по именам (файл с конфигурацией эмоций)
4. +Сделать файл с рандомными фразами
5. +делать перенос строки
6. +"Сейчас %(hour24), %(username)." - говорить сколько сейчас время
7. "Очень важно поддерживать режим." -- разные фразы в зависимости от времени (реализовать в hour_dialogue_plugin)
8. normalboottalk -- приветствовать в зависимости от времени дня, прощаться - желать хороших снов
9. +Убрать (пока нет системы настроения) mouth с тэгом bad из рандомной ротации
10. Ты её гладишь (средняя кнопка мыши, без разницы пока где) -- она улыбается и смотрит на тебя
11. Несколько вариантов часового диалога
12. Попросить сфокусировать взгляд на тебе

Общий шаблонизатор строк
1. +Все строки в одном файле с айдишниками
2. Сделать возможность внедрять теги с эмоциями и %username, %hour24 переносом строки
3. +У каждой строки несколько вариантов
4. У каждого варианта есть опциональные рандомно включаемые варианты
5. Шаблонизатор генерирует как эмоцию изменить, что писать текстом и что отправлять в tts -- то есть сейчас отправляет из render_text события в очередь выражений - фильтр face
6. Сделать рандомными части диалогов. То есть строчка одна, но она может комбинироваться - фильтр optional

Управляемые выражения лица
1. +Проще не мутить forced выражения лица, а иметь очередь выражений (LIFO). Элементы очереди -- набор нужных слоёв с временем удержания эмоции
2. +Рендерить слои динамично
3. +Blink plugin не трогать
4. +По тику генератор рандомных выражений смотрит чтобы у очереди была всегда величина >=1, если меньше -- добавляет рандомное выражение
5. +Консумер выражений берёт из очереди выражение (если пуста -- то ничего не делает), применяет open/closed_eyes состояния (если глаза закрыты они совпадают), и делает следующий свой тик исходя из времени
6. +Если нам нужно зафорсить выражение лица -- мы вызываем прокси-метод, который вызывает tick в плагине

Динамический discovery картинок и сборка выражений из слоёв
1. dicovery слоёв (его ключ и значение типа mouth=shut) будет по regex с именованными группами, который будет задан в конффайле
2. тот, кто хочет изменить эмоцию, передаёт словарь с этими элементами ключ=значение, и мы их собираем в переданном порядке
3. короче, файл с эмоциями. для каждого слоя сделать один или несколько возможных вариантов. будет эмоция random со всеми сочетаниями 
4. если ты хочешь зафорсить какое-то конкретное выражение лица (например, "смотрит вперёд"), ты указываешь в этом файле ещё одну эмоцию
5. но также можно передавать какой-то свой набор слоёв вместо заранее заданного

Доработать последовательность выхода
1. Избавиться от `self.w.config['exit_initiated']`, пусть каждый плагин сам себе ставит этот флаг, если ему нужно
2. dialogue: on_exit ставит флаг внутри плагина, если диалог есть -- он сразу закрывается, открывается диалог с прощанием, после рендера он готов закрываться
3. voice: on_exit ставит флаг внутри плагина, если сейчас есть активный tts, он останавливается, говорится диалог с прощанием, после окончания он готов закрываться

Технические штуки
1. +Сделать папку с плагинами
2. +Сделать наследование плагинов (конфиг, self.w, tick с зацикленностью)
3. +Сделать динамическую инициализацию, но писать `__all__` = [], чтобы можно было задавать порядок без заморочек с зависимостями -- к чёрту порядок, пусть через очереди общаются
4. +Чтобы можно было обращаться к экземпляру класса плагина напрямую (ссылка на экземляр где-то хранилась)
5. +наверное плагины говорения будут через очередь передавать диалоги на плагин отображения, очередь тоже в global state
6. Динамический (по команде) релоад конфига и файла со строками

Технические костыли:
1. Как поддерживать выражение лица? Можно ставить очень долгий таймер, а потом его сбрасывать

## Крутые штуки (дальше)
1. +Синтез голоса
2. Помодоро (все функции eyes relax)
3. Чтобы она говорила идти тренироваться, спрашивала результаты и вела дневник
4. Чтобы можно было рассказать ей про свой режим, и она бы помогала поддерживать его
5. Чтобы она что-то делала (читала, следила за тобой)
6. чтобы она периодически спрашивала настроение и выбирала соотв фразы -- поддерживающие, мотивирующие
7. Чтобы у неё было своё настроение (выбор эмоции был бы не случайным), и ты бы его типа менял своими действиями
8. Когда наводишь на неё мышку, она в любом случае начинает смотреть на тебя и улыбаться, типа ты можешь захватить внимание
9. Система настроения -- можно повышать например "гладя по голове" (средняя кнопка мыши), то есть это уже регионы тела как в shimeji
10. Портит настроение если что-то делать неправильно (сидеть ночью, например) или 
11. Попробовать ещё раз сделать захват заголовков активных окон и реакцию на них
12. Локальное хранилище sqlite с синхронизацией через яндекс-диск
13. Чтобы Катра могла чем-то заниматься. Хоть книгу читать (сделать background просто как первый слой наложения)
14. Слушай, а пусть она мне рандомную картинку показывает иногда из папки с мемами
15. Вообще если честно, то я хочу иметь возможность испортить ей настроение, сделать больно, неприятно, разозлить, обидеть
16. Спрашивать её да/нет/может быть etc - на простых вероятностях
17. Игры с Катрой (https://www.tutorialspoint.com/artificial_intelligence_with_python/artificial_intelligence_with_python_gaming.htm) от текстовых до крестиков-ноликов
18. Можно попробовать взаимодействовать с Replika API через затравку диалога?
19. Одежда?
20. Чтобы она могла блокировать веб-сайты как-то, отключать компьютер, типа focus mode во время pomodoro
21. говорить сколько осталось до сна вместе с тем сколько часов
22. horny/emegrency mode
23. При старте она бы показывала чеклист с какими-то вещами (принципами), чтобы я не забывал про них

Вообще подумай, что ты можешь сделать логичным, при этом рандомным?
1. Смена эмоций на лице, моргание
2. Влияние событий (добавлять какой-то шум, чтобы поведение не было 100% детерминировано)
3. Рандомные фразы (и диалоги). Комбинирование частей фразы.
4. Чтобы она что-то делала сама

Интересные идеи
1. Катра -- кошка. Кошки боятся собак, гоняются за мышами, любят сидеть в коробках, ещё просят часто чтобы их покормили и куда-то выпустили
2. Ещё кошки мурчат, шипят, если очень злые -- воят. Ещё они иногда хотят играть и ласки.
3. Кошки балдеют от кошачьей мяты и валерьянки
4. Кошки следят за птицами 
5. Кошки умываются, вылизывая себя
