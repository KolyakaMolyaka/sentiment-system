

LIMIT = 20 # до 100

classes_list = [
	0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1,
	1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0
][:LIMIT]

comments_list = [
	"Это не рубашка а фильм ужасов. Ранее покупала рубашку у этого продавца в размере xs что примечательно на мой М сидела отлично и далеко не в обтяг.. нареканий не было, ткань мягкая и тянется. Сейчас поправилась и решила заказать побольше, сразу L чтоб сидела оверсайз, так как знаю что они у них большемерят. Села то она хорошо но к качеству вопросов более чем много, ткань без намека на эластан, она вообще никак не тянется, хлопок как бумага, жесткий. Петли для пуговиц обработаны отвратительно, нитки торчат из каждой петли, сами пуговицы пришиты так, что торчат нитки потянув за которые пуговица просто отвалится.. вернула это безобразие ПЛАТНО, что печалит еле больше. Качество пошива и используемого материала катастрофически испортилось. Вывод - лучше переплатить но получить достойную вещь которая прослужит долго чем этот бумажно нитковый кусок ткани.",
	"Честно,мне всё понравилось,торчали нитки в некоторых местах но это норм,ещё очень мало просвечивает.Фотки в этой рубашке оставлю в низу.",
	"Рубашка по качеству хорошая. Раньше брали такую же. Но сейчас не подошёл размер, слишком оверсайс. В пункте выдачи не приняли, т. к. нет обозначения бренда. Но я же его не обрезала, вы сами его не пришиваете. Прошу помочь с возвратом.",
	"Рубашка классная. Я ожидала, что она будет чуть меньше, но тем не менее она прикольная, всем советую))",
	"Рубашка классная, хлопковая. Но из-за состава ткани, очень сильно мнется, сложно утюжить. Второй раз такую бы не заказала.",
	"Рубашка в целом неплоха. По совету продавца выбрала на свои параметры (ог110,от94) размер 3хл, но она оказалась не просто чуть чуть оверсайз, а прям огромной. Хотя это конечно мой косяк. Существенный минус - она красится от одежды надетой под неё. Надевала под неё топ с фото, за несколько летних дней носки окрасились область под мышками и спина. Пятна не отстирываются.  Рубашку советовать могу, но носите аккуратнее и подбирайте правильные низы",
	"Отличная рубашка, выполнена аккуратно, приятная к телу, слегка просвечивает, но с бежевым/белым бельем хорошо. Не угадала с размером, у меня рост 168, ог 102, от 80, взяла xxl, ну оочень большая, рукава просто до смешного, видимо, раз оверсайз, можно брать поменьше. Обязательно позже перезакажу.",
	"Очень хорошая рубашка. Ткань приятная, хлопок, плотная, не жесткая. Выглядит достойно. Манжеты достаточно широкие. На мой 44 размер заказала М, оверсайз с запасом, можно было S заказать. Но очень понравилась и не стала перезаказывать",
	"Отличная рубашка, ткань приятная к телу. Размер соответствует. И в пир, и в мир) Покупкой довольна. Спасибо????",
	"Это просто 100/10 нитки не торчат. К телу очень приятная. Заказала размер L хотя у меня размер M S и да нормально села прям как и хотела оверсайз, но немного просвечивает не критично",
	"Ужасная рубаха, качество как клеенка, пришла ужасно мятая, а про размер это отдельный разговор, мой размер 52, эта рубаха наверное 60-64, короче нет ничего общего с фото в карточке продавца, естественно возврат",
	"Вроде нормальная рубашка. Брала ххс и хс , чтоб выбрать. Отличия были в талии. Хс более широкая, рукава одинаковой длины. Взяла ххс в итоге. Шва на рукавах на фото. Ну в принципе с лицевой стороны не видно. Бал снижаю за швы и за то что мне 2 недели не возвращают деньги за некупленный товар",
	"За свои деньги рубашка неплохая, оверсайз Немного просвечивает, но не слишком критично Спасибо!",
	"кайф?? рубашка на размера 2 больше чем сама я, но мне такое нравиться. ношу уже больше месяца, раз испачкала ручкой, но всё хорошо отстиралось. но достаточно тонкая, поэтому чуть просвечивает и было небольшое количество торчащих ниток",
	"Отличная рубашка, в размер, рекомендую.",
	"Хорошая рубашка,  взяла на два размера меньше)) рост 152, ог 89, от 66, об 90. Качество хорошее не синтетика))",
	"брала на пару размеров больше, но показалась слегка коротковатой. Нитки на пуговицах торчат в разные стороны и цепляются. А так вполне себе неплохая рубашка.",
	"Действительно оверсайз. Даже sка на мой 44-46 слегка свободно. Всё так как и хотелось, спасибо.",
	"Заказываю не в первый раз, качество топовое, не бельшемерит не маломерит самый раз,за свою цену топ",
	"С размером не угадала, отказ , а так хорошая рубашка советую",
	"Рубашка клевая ?? оверсайз, как и хотела, можно носить по-разному???? ткань приятная, кожа дышит",
	"Рубашка и правда большемерит, но мне это самое то, носила её летом как второй слой",
	"Рубашка по качеству мне понравилась, но по размерной сетке лучше не выбирать. Мои параметры ОГ 116, ОТ 98. Почитала отзывы заказала ОГ 110, ОТ 90, переживала, думала не пройду в груди. Получила и увидела, что она огромная.... Перезакажу на два размера меньше.",
	"моя лучшая покупка, шикарная рубашка, правда пришла с опозданием в один день(06.09.23), немного, но я рассчитывала получить ее в срок(05.06) в связи с первым учебным днем и днем рождения, как итог - испорченный день. но пока забирала рубашку, нашла в раздевалке колечко с пробой, послание от бога или извинения от вб, может из пакета с рубашкой выпало, не знаю я счастлива??",
	"Думала будет большая ,так как ношу размер М ,но нет и размер L подошел Спасибо большое ??",
	"Ткань приятная,сшито качественно.Рекомендую к покупке??",
	"немного просвечивает, но фасон как и хотела, плюс несильно мнется и цена приятная",
	"Брака нет,качество ткани неплохое,но...я не оценила фасон,заказывала свой размер.вообщем нужно мерить)",
	"Материал не понравился, смотрится очень дёшево, просвечивает, петли для пуговиц не прометаны вообще. На модели совсем другая рубашка по виду...",
	"Теперь это одна из любимых вещей в гардеробе. Носить можно как угодно. То, что я хотела, спасибо??",
	"Рубашка хорошая, но решила не брать, а так просто 10/10 смотрите фото)",
	"Блузку от этой фирмы заказываю не в первый раз. До этого брала тоже белую и есть ещ? ч?рная. Об блузок в восторге!",
	"Рубашка хорошая, выбирала свой размер по таблице размеров, оказалась большеватая. А так качество хорошее, рубашка в целом отличная!??",
	"Отличная классическая рубашка, причем отсечь хорошего качества и без лишних элементов  Смотри фото",
	"Качество вроде бы нормальное заказывала чтоб было широкое но оно оказалась намного больше, и мне не дали покет",
	"ткань приятная,по плечам не широкая. очень комфортная. 100/10",
	"Сделали возврат, но деньги не вернули. Сумма 1875. Прикрепляю ответ по моему обращению",
	"Рубашка очень свободная , но я такую хотела ) качество понравилось",
	"Очень хорошая вещица. Давно искала такую рубашку: приятная к телу и нужная модель. НО! Пришла с небольшим коричневым пятном.",
	"Как из ?? доставили..Перезаказала на другой размер. Слишком Овер Овер сайз",
	"хорошая рубашка, ношу на работу и очень довольна покупкой, смотри фото",
	"Очень понравилась, просто белоснежная как и хотели .Спасибо",
	"Рубашка супер, простая классическая, то что нужно, смотрите фото",
	"симпатичная рубашка, недорого стоит, но жалко что рукава так заужены",
	"Очень Крутая рубашка,подходит под любой образ",
	"Вообще ношу 44, но почитала отзывы, взяла 42 и не прогадала. Качество отличное. Да синтетика, но мне качество ткани прямо очень нравится. Выглядит как будто мужская, но покороче. Купила ее еще в марте и все никак не могла придумать как и с чем носить (как смотрится под классику, по крайней мере под ту что есть у меня, мне не понравилось). При примерки заинтересовал фасон, но в голове картинка образа не сложилась. И тут наступило лето. Рубашка подходит ну просто под всё: шорты, юбку, джинсы. Можно заправить, завязать, надеть поверх топа в любом из вариантов смотрится великолепно. Продавцу огромное спасибо за такую универсальную вещь ????",
	"швы ровные, нитки не торчат хорошая рубашка, смотрите фото",
	"рубашка просто ашалеть ,как удобна и  красива, смотрите фото",
	"Классическая белая рубашка ?? я от нее в восторге ??????",
	"Очень нравится! Рубашка классная. Советую. Смотрите фото!",
	"На ОГ 88 и ОТ 70 сел хорошо. Оверсайз. Качество пошива хорошее.",
	"Рубпшка хорошая, легко гладится, как на картинке. Единственный минус дырочки для пуговец плохо обработанны",
	"Ужасная рубашка, чистая синтетика, хлопка нет вообще, по ощущению пакет надеваешь, по бёдрам в 54 размере 172 см, просто ужасно",
	"Пришла грязная рубашка, еще и размер М вместо S.",
	"супер мега оверсайз, берите свой размер лучш",
	"Подбирала рубашку под шорты. Радовалась, что она идеально подошла, еще и цена отличная. Единственное, пуговицы поменяла на белые. Но после первой стирки произошло то, что вы видите на фото. При том, что стирала в теплой воде вручную. И кстати, во время нОски, белые вещи, которые соприкасаются с рубашкой тоже окрашиваются. Имейте в виду.",
	"Заказала такую же чёрную",
	"Классная рубашка, качество хорошее.",
	"носила эту рубашку неделю, могу сказать что достаточно удобная, хорошо сшита и красиво сидит, но есть огромный минус. не знаю по какой причине так происходит, возможно из-за особенностей материала, но после стирки рубашка сильно помялась и ее стало вообще невозможно отгладить. полчаса мучений с утюгом и еще полчаса пыток с отпаривателем, итог видно на фото. если бы я оставила это дело на утро, я бы опоздала везде где только можно, я считаю, что гладить и отпаривать одну рубашку без преувеличений целый час это издевательство над собой и утюгом. это первая моя рубашка, с которой такое произошло. при этом до стирки все было замечательно.. может дело во мне и можно это как-то исправить?",
	"Классная. Подошла. Смотрите фото",
	"Классная рубашка,но немного просвечивает:(",
	"афигенная рубашка, только немного большеватая)",
	"классная рубашка, очень удобная????СМОТРИТЕ ФОТО",
	"очень стильно смотрится. качество супер",
	"Отличная рубашка! Приятная к телу, купили уже 3 штуки, себе и ребёнку в школу! Хороший фасон, свободный крой, все идеально. Хорошо отстирывается, ткань после стирки не мнется. Видеообзор оставила в своем Инстаграм sofi_prostyle. Подписывайтесь и смотрите обзоры качественных вещей с wildberries!",
	"ваще супер, качество огонь. не просвечивает, не слишком большая (у меня XS-S) брала М. добрая милая прекрасная рубашка ?? если есть ещё какие то вопросики по рубашке, то inst, тг: slavnichek",
	"шикарная базовая белая рубашка, не к чему придраться, прошито аккуратно, никаких торчащих ниток, заказала ее отсюда почти год назад - до сих пор в идеальном состоянии :)",
	"Рубашка прекрасная, но слегка большемерит, я совершила ошибку и заказала на пару размеров больше, но она изначально оверсайз, будьте внимательны!!!??",
	"Рубашка конечно очень оверсайз и пришла с прошитой недодыркой для рукава",
	"За 700 рублей отличная рубашка! Ношу обычно размер s, заказала xs, всё подошло. ОТ 70, на грудь не больше 2 размера. Носить можно всяко разно, как классическую рубашку, так и как верхний слой. В составе 95% хлопок, гладится легко. Сходила вчера в ней в +30, не вспотела, хорошо продувается и не замёрзла в охлаждаемом кинотеатре. На пройме рукава с лицевой стороны торчали нитки от оверлока, просто обрезала, за такую цену не критичный дефект. В общем, спасибо большое продавцу, я довольна. Рекомендую к покупке. Слегка просвечивает.",
	"Мой обычный размер - М, но тк я люблю оверсайз и у меня рост 180, то решила заказать L и XL. На данных фотографиях размер XL и меня устраивает как рубашка смотрится. Качество хорошее, всё понравилось. Спасибо ??",
	"Прикольная рубашка. Нам понравилась.",
	"я в полном разочаровании. рубашку НИ РАЗУ не надела! после покупки рубашку постирала (как все новые вещи) и обнаружила на ней белые разводы. подумала: может не прополоскалось как следует. в итоге полоскала ее отдельно и простирывала на бережной 4 раза. и каждый раз разводы на новых местах. встречаю такое вообще впервые. но это жуть!",
	"Рубашка хорошего качества, заказывала два раза, всё было отлично. В этот раз заказала тот же размер L, но рубашка пришла большего размера, хотя на бирке указан такой же.  Не понимаю как ориентироваться на размеры, написано одно, на деле совсем не соответствует. Будем делать возврат.",
	"Хорошая удобная рубашка в школу самое то",
	"Швы все ровные. Никаких торчащих ниток не нашла. Посадка оверсайз). Пока читала отзывы, боялась взять или слишком оверсайз или впритык. Доверилась чувству и заказала свой S (ог 78, от 67, об 89) как выглядит на мне можете увидеть сами) Единственное не нашла, где здесь лайкра, рубашка совсем не тянется ??, но это не минус. Брала для вечерних прогулок. Покупкой довольна. Продавцу удачи.",
	"Хорошая базовая рубашка. Легко поддается глажке и почти не мнется в носке. Влюблена в нее. И в пир и в мир. Торчат кое где нитки, но за такую цену это вполне естественно.",
	"Моя самая любимая вещь в гардеробе. Очень советую! Размер М. Заказывала такую же черную-пришла вообще другая рубашка, ее даже мерить не стала и вернула обратно",
	"рубашка хорошая, замучусь гладить оооооой, говорят большая и это правда я заказала 4xl и xxl взяла тот что поменьше, но мне понравилась, с галстуком брюками и лоферами огонь ??",
	"Пожалела что оставила. Смотрится как костюм медсестры. Когда заправляешь вся топорщица. Носить только завязывать и на запах.  Думала отгладиться, обляжется, но нет, синтетики много.",
	"офигенная, спасибо ??????",
	"За такую цену вообще пушка ??",
	"В целом за такую цену очень даже. Есть запах, аллергикам лучше выпить таблетку сразу, а то будете чесаться от кол-вы краски) но после стирки гуд) Все пишут большая большая, но это просто фасон такой под оверсайз. На мои параметры ОГ108 ОТ90 ОБ105 Рост 153, ношу 50-52р, 3xl самое то, поскольку люблю свободно, с загибами и под футболку/платье. Если хотите более прилегающее, то лучше брать 2xl, поскольку рукава действительно широкие, но это такой фасон. В целом очень достойно за такую стоимость (750-900р). Пойду теперь за белой)",
	"хорошая оверсайз рубашка !!!",
	"Очень довольно покупкой) ??????",
	"Рубашки выше всех похвал!?????? Купила  сперва белую, р.50  на мой р-р 50-52 ОГ 106 см,  ОБ -110 см. Брала ее как верхний слой и свободной как оверсайз. Так и села как хотела. 48 р-р свободно,  отлично пойдет под заправку в юбку, брюки.  Настолько понравилась рубашка, выкупила черную. Ткань шикарная, держит форму. Хлопок. В жару комфортно.Обе рубашки 50 р-ра одинаковые. Мне достались без брака , с ровными фабричными строчками.Рубашки пушка !!!??????",
	"Хорошая классическая рубашка. Ткань синтетика, хорошо гладится с отпариванием. Ношу верх размер М, на мне XL сел прям свободно, можно было бы на один размер поменьше взять.",
	"очень кайфовая, приятный материал, именно то, что я и искала ????????ог114, от108, об122, размер 58 прекрасный оверсайз, возьму ещё)))",
	"Отличная рубашка,по размеру,",
	"очень большая, смотри фото",
	"хорошего качества, заказывала специально на несколько размеров больше, чтобы была оверсайз",
	"Хорошая рубашка!",
	"Модель ростом 162, размер s. Рубашку взяли М, получился очень оверсайз, великовата по спине, но не критично. качество хорошее",
	"Легко отпаривается, также как и мнётся, что в принципе очевидно. Люблю и на роспуск носить и заправлять. Материал чуточку просвечивает, но не критично. За такую цену ??",
	"Мне вот интересно по каким размерам кроили эту рубашку. Вы  хотите сказать что это оверсайз?  Вы хотите сказать что это 46 размер!!!??? Вы пишите что на высоких, мой рост 175 см обхват груди 91, талии 71. Вы сами бы одели такую вещь и пошли бы в ней куда нибудь!? поставила одну звезду, т к не поставить не возможно.",
	"самая любимая рубашка. брала S на рост 155, села оверсайз, все супер! НО учтите, что материал не дышит от слова совсем, в ней пипец как жарко. inst:powlxq",
	"отличная рубашка, ткань не плотная, писали, что большемерит, но вроде норм. у меня рост 157 и длина та, которую я и хотела, буду носить поверх топа или футболок",
	"хорошая рубашка,качество нормальное.Удобная,красиво смотрится и с топом и застегнутая с юбкой,в общем универсальная подходит ко всему???",
	"Рубашка хорошая. На ОТ65 и ОБ88 взяли размер L. В меру свободная. Можно носить как первый слой, так поверх топа. Советую ??",
	"Ну что сказать, слов нет от ужаса. На первый взгляд при примерке было всё отлично. Мнётся она просто молниеносно, и после первой стирки ткань на Манжете по швам разошлась. Мой совет ни в коем случае не покупайте!!!"
][:LIMIT]