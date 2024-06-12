/* Добавление информации о токенизаторах */
INSERT INTO Tokenizer(tokenizer_title, tokenizer_description, tokenizer_is_archived) VALUES
('unknown', 'Неизвестный токенизатор. Пользователь обучал модель с помощью собственных векторов.', false),
('nltk-tokenizer', 'Токенизатор доступен благодаря библиотеке NLTK и функции nltk.tokenize.word_tokenize(), с помощью которой получаются токены. Функция возвращает слоги из одного слова, а одно слово может содержать один или больше слогов.',false),
('default-whitespace-tokenizer', 'Токенизатор реализуется функцией split в Python применённой к строке с текстом. Это означает, что токены выделяются путём разделения строки пробельным символом.' ,false),
('wordpunct-tokenizer', 'Используется токенизация текста функции nltk.tokenize.wordpunct_tokenize() из библиотеки NLTK. Функция возвращает токены путём разбиения текста по пробелам и с учетом знаков препинания.' ,false);

/* Добавление информации о векторизациях */
INSERT INTO Vectorization(vectorization_title, vectorization_description, vectorization_is_archived) VALUES
('unknown', 'Неизвестный метод векторизации. Пользователь самостоятельно получал векторы и обучал модель на их основе.', false),
('bag-of-words', 'Векторизация текста при помощи алгоритма "Мешок слов". Вектор содержит столько элементов, сколько анализируемых слов (возможно ограничение кол-ва анализируемых слов). Каждому слову присваивается код, который будет обозначать это слово. Присутствуют дополнительные коды: 0 - код заполнитель (используется для увеличения вектора до фиксированной длины), 1 - код, обозначающий неизвестное слово (в случае ограничения кол-ва анализируемых слов). Каждый элемент вектора соответствует определенному слову, а значение равно количеству раз, сколько слово встречается в тексте.', false),
('embeddings', 'Векторизация текста при помощи плотного векторного представления. Каждому токену соответствует вектор фиксированной длины. Элементами вектора могут быть любые действительные числа. Реализуется при помощи библиотеки Navec.', false);



