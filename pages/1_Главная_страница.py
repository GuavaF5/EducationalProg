import streamlit as st

st.title("***ОБУЧАЮЩИЙ ВЕБ-САЙТ***")

st.write("Этот сайт создан с помощью фреймворка Streamlit и нейросети Gigachat Api")
st.write("Он состоит из нескольких частей: Главная страница (на который Вы сейчас находитесь), Миниигры, Сюжетная игра. Все задания и вопросы генерируются нейросетью при запуске игр, каждый раз заново. В проверке ответов также учавствует нейросеть. (При запуске происходит генерация заданий и ответов к ним, и при вводе ответа он сверяется с ответом нейросети).")
st.write("Чтобы переключиться на миниигры, воспользуйтесь меню, которое расположенно слева")
st.write("Ниже распологается краткая история нейросетей (часть 1 главы моего проекта). Удачного пользования сайтом!")

st.title("История развития нейронных сетей")
st.write("Идея создания искусственных нейронных сетей возникла под влиянием исследований человеческого мозга. В 1943 году американский нейрофизиолог Уоррен Мак-Каллок и математик Уолтер Питтс опубликовали работу «Логическое исчисление идей, относящихся к нервной активности», в которой предложили упрощённую модель нейрона. Их модель, названная «пороговым элементом», могла выполнять простые логические операции и стала основой для дальнейших исследований. В 1948 году опубликована книга Н. Винера о кибернетике. Основной идеей стало представление сложных биологических процессов математическими моделями. В 1949 году канадский психолог Дональд Хебб сформулировал правило Хебба, которое описывало, как нейроны могут обучаться, усиливая связи между собой. Это правило стало важным шагом в понимании процессов обучения в нейронных сетях. В 1957 году американский учёный Фрэнк Розенблатт разработал перцептрон — одну из первых моделей искусственной нейронной сети. Перцептрон мог распознавать простые образы и стал первым устройством, способным к обучению. Однако его возможности были ограничены, что позже привело к критике со стороны исследователей, таких как Марвин Минский и Сеймур Паперт. В своей книге «Перцептроны» (1969) они доказали, что однослойные перцептроны не способны решать задачи, требующие нелинейного разделения данных.")
zzz = "pages/frank.webp"
st.image(zzz, caption='Фрэнк Розенблатт')
st.write("После критики перцептронов интерес к нейронным сетям временно угас. Этот период известен как «зима искусственного интеллекта». Другие методы машинного обучения стали более популярными. Однако в 1974 году Пол Вербос предложил алгоритм обратного распространения ошибки (backpropagation), который стал ключевым для обучения многослойных нейронных сетей. Этот алгоритм позволял эффективно корректировать веса нейронов, что открыло новые возможности для развития глубоких сетей. В том же году независимо от Вербоса подобный метод предложил А.И. Галушкин. В 1980-х годах интерес к нейронным сетям возродился благодаря развитию вычислительной техники и новым теоретическим открытиям. В 1986 году Дэвид Румельхарт, Джеффри Хинтон и Рональд Уильямс популяризировали алгоритм обратного распространения, что привело к созданию многослойных перцептронов. В это же время появились новые архитектуры, такие как сети Хопфилда и машины Больцмана.")
st.write("С началом XXI века нейронные сети пережили настоящий бум благодаря увеличению вычислительной мощности, появлению больших объёмов данных и развитию алгоритмов. В начале 2000-х годов нейронные сети начали возвращаться в фокус внимания исследователей. Одним из ключевых событий стало появление глубокого обучения (deep learning). В 2006 году Джеффри Хинтон и его коллеги предложили метод глубокого обучения, который позволил эффективно обучать нейронные сети. Также в этот период начали активно развиваться свёрточные нейронные сети (Convolutional Neural Networks, CNN), которые были предложены ещё в 1980-х годах Яном Лекуном. CNN стали особенно популярны благодаря их способности эффективно обрабатывать изображения, извлекать признаки и распознавать объекты.")
st.write("2010-е годы стали временем настоящего бума нейронных сетей. В 2012 году свёрточная нейронная сеть AlexNet, разработанная Алексом Крижевским, Ильёй Суцкевером и Джеффри Хинтоном, одержала победу в соревновании ImageNet Large Scale Visual Recognition Challenge (ILSVRC). AlexNet значительно превзошла традиционные методы компьютерного зрения, снизив ошибку классификации с 26% до 15%. Это событие стало поворотным моментом, после которого глубокое обучение стало доминирующим подходом в задачах компьютерного зрения. В 2017 году исследователи из Google предложили архитектуру трансформеров (Transformers), которая произвела революцию в обработке естественного языка (NLP). Трансформеры используют механизм внимания (attention mechanism), что позволяет им эффективно обрабатывать длинные последовательности и учитывать контекст и фокусироваться на различных частях входной последовательности при генерации выходных данных. Это особенно полезно в задачах перевода текста, где важно учитывать контекст каждого слова (поэтому трансформеры используются во многих онлайн-переводчиках, таких как Яндекс Переводчик и Google Переводчик). На основе трансформеров также были созданы такие модели, как BERT и GPT, которые достигли высочайших результатов в задачах перевода, классификации текста и генерации.")
xx = "alex.png"
st.image(xx, caption='Архитектура AlexNet')
st.write("В 2020-х годах скорость развития технологий, связанных с нейронными сетями, растёт. В 2020 году OpenAI представила GPT-3, одну из самых мощных языковых моделей на тот момент. GPT-3 способна генерировать тексты, отвечать на вопросы, писать код и выполнять множество других задач. В 2023 году появился GPT-4, который ещё больше расширил возможности обработки естественного языка. Помимо этого, стали популярны диффузионные модели (Diffusion Models), которые используются для генерации изображений. Эти модели, такие как DALL-E (2021) и Stable Diffusion (2022), позволяют создавать высококачественные изображения на основе текстовых описаний. Подобные картинки стали повсеместно использоваться людьми: их можно встретить в рекламе, на различных веб-ресурсах в качестве элементов оформления и так далее.")
cc = "rob.png"
st.image(cc, caption='Изображение, сгенерированное нейросетью Craiyon')
st.write("Из вышеописанной истории нейросетей можно сделать вывод, что они появились ещё довольно давно. Они постепенно улучшались, и по итогу в последнее десятилетие произошёл настоящий «бум», и нейронные сети стали развиваться ещё быстрее, открыв человечеству новые горизонты и возможности. Будущее обещает ещё больше инноваций и создания всё более крупных и мощных моделей, способных выполнять более сложные и ёмкие задачи.")
