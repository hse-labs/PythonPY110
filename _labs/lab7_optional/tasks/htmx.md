# Использование HTMX 

В папке `_labs/lab7_optional/files` содержится приложение `app_htmx` скопируйте его
и зарегистрируйте в `settings.py` в `INSTALLED_APPS`. 

```python
INSTALLED_APPS = [
    ...,
    'app_htmx',
]
```

В `urls.py` папки project пропишите маршрут

```python
path('htmx/', include('app_htmx.urls')),
```
Пройдите по адресу
http://127.0.0.1:8000/htmx/products/

Появятся 2 кнопки, нажав на которые подгрузятся случайные 4 товара, при повторном нажатии 
появятся другие товары без перезагрузки страницы, ровно тоже самое, что было когда использовали 
бы JS для этого. Можете посмотреть в терминал, что запросы на сервер отправлялись, а страница не перезагружалась.

Чтобы разобраться с этим зайдите в `app_htmx/templates/app_htmx/products.html`, здесь будет важным момент работы с `htmx`

![img.png](img.png)

Так загружаются скрипты для работы htmx
```html
<script src="https://unpkg.com/htmx.org@2.0.0"></script>
```
А дальше в атрибутах начинающегося с `hx-...` прописывают взаимодействие с библиотекой

Самая простая связка это HTMX отправит запрос на какой-то адрес, сервер отправит информацию (HTML файл), а HTMX подставит
эту информацию в нужное место.

> Важное замечание HTMX подставляет только данные из пришедшего HTML файла, работать с JSON он не умеет как JS, поэтому при работе 
> с HTMX с сервера возвращается только HTML

В целом в общем случае часто используются эти 4 атрибута:

* `hx-get`: URL-адрес, который элемент будет использовать для отправки запроса AJAX GET.
* `hx-target`: элемент для замены в ответе AJAX, по умолчанию — innerHTML того, кто отправляет запрос AJAX.
* `hx-swap`: как ответ будет заменен относительно цели запроса AJAX, по умолчанию — innerHTML.
* `hx-trigger`: что запускает запрос AJAX, по умолчанию — click.

Другими словами, `hx-get` — это ЧТО, `hx-target` — это КТО, `hx-swap` — это КАК и `hx-trigger` — это КОГДА.

Ниже, более подробно рассмотрим эти атрибуты

## 1. Атрибуты hx-... для отправления запросов

Самые ходовой атрибут это `hx-get` тут прописывается на какой адрес будет сделан `get` запрос. 

*Пример* 

здесь прописывается отправка `get` запроса на адрес `/htmx/load_products/`
```html
hx-get="/htmx/load_products/"
```

или как пример работы через Django шаблоны

```html
hx-get="{% url 'app_htmx:load_products_with_render' %}"
```

Всего есть 5 возможных типов запросов

* `hx-get` для `GET` запроса
* `hx-post` для `POST` запроса
* `hx-put` для `PUT` запроса
* `hx-patch` для `PATCH` запроса
* `hx-delete` для `DELETE` запроса

## 2. Атрибут hx-target для указания куда будет подставлен ответ

Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_target.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке 

http://127.0.0.1:8000/htmx/hx-target/

Значение атрибута `hx-target` может быть:

* Значение селектора запроса CSS целевого элемента (например `hx-target=#products` вставить в тот блок у которого id=products).

```html
<div id="products">
  <!-- сюда будет вставлен ответ -->
</div>
<div class="box">Обычный блок</div>

<button hx-get="/htmx/load_products/" hx-target="#products" hx-swap="innerHTML">
Загрузить товары
</button>
<!-- Ответ сервера вставится в элемент с id="products" -->
```

* `"this"`, который указывает, что элемент, на котором находится атрибут hx-target, является целевым.

```html
<button hx-get="/htmx/hx-target/load-status/" hx-target="this" hx-swap="outerHTML">
    Проверить статус
</button>
<!-- Ответ заменит саму кнопку -->
```
* `"closest <селектор CSS>"`, который найдет ближайший элемент-предок или себя самого, который соответствует заданному селектору CSS (например, closest tr будет указывать на ближайшую строку таблицы к элементу).

```html
<table>
  <tr> <!-- Ответ заменит всю строку таблицы, содержащую кнопку.-->
    <td>Товар A</td>
      <td>Вся строка заменится, так как она ближайшая к кнопке</td>
      <td>
        <button hx-get="/htmx/hx-target/row-details/" hx-target="closest tr" hx-swap="outerHTML">
          Подробнее
        </button>
      </td>
    </tr>
    <tr>
      <td>Товар Б</td>
      <td>А тут не поменяется</td>
      <td>Кнопки нет</td>
    </tr>
</table>

```

* `"find <селектор CSS>"`, который найдет первый дочерний элемент-потомок, который соответствует заданному селектору CSS.

```html
<div class="details"><!-- Ничего не произойдет--></div>
  <div class="product box" hx-get="/htmx/hx-target/product-details/" hx-target="find .details"
       hx-swap="innerHTML" hx-trigger="click .load-btn">
    <button class="load-btn">Показать детали</button>
      
    <div class="details"><!-- Здесь появится ответ--></div>
    <div class="details"><!-- Ничего не произойдет--></div>
    <div class="details"><!-- Ничего не произойдет--></div>
  </div>
```

* `"next"`, который разрешается в element.nextElementSibling

```html
<button 
  hx-get="/more-info/" 
  hx-target="next" 
  hx-swap="innerHTML">
  Подробнее
</button>

<div> <!-- Ответ попадет в этот элемент, так как он следующий элемент после кнопки.-->
  (пусто)
</div>

<div> 
  (пусто)
</div>
```

* `"next <селектор CSS>"`, который будет сканировать DOM вперед для первого элемента, который соответствует заданному селектору CSS. (например, next .error будет нацелен на ближайший следующий элемент-брат с классом ошибки)

```html
<!-- Ответ от сервера попадёт в ближайший следующий .error-блок. -->
<form hx-post="/htmx/hx-target/validate/" hx-target="next .error" hx-swap="innerHTML">
    <input name="email" placeholder="Введите email" />
    <button type="submit">Проверить</button>
  </form>

  <div class="error box"><!-- Но не здесь --></div>
  <div class="error box"><!-- Здесь будет ответ --></div>
  <div class="error box"><!-- Но не здесь --></div>
```

* `"previous"`, который преобразуется в element.previousElementSibling

```html
<div class="input box"><!-- Здесь не будет ответа --></div>
<div class="output box"><!-- Здесь будет ответ --></div>
<button
hx-get="/htmx/hx-target/result/"
hx-target="previous"
hx-swap="innerHTML">
Обновить
</button>
```

* `"previous <селектор CSS>"`, который будет сканировать DOM в обратном направлении для первого элемента, соответствующего заданному селектору CSS. (например, previous .error будет нацелен на ближайший предыдущий элемент-брат с классом ошибки)

```html
<!-- HTMX найдёт предыдущий .msg внутри родительского элемента и вставит туда ответ -->
<div class="msg box">блок .msg</div>
<div class="tmp box">блок .tmp</div>
<div class="msg box">блок .msg</div>
<div class="tmp box">блок .tmp</div>
<button hx-get="/htmx/hx-target/note/" hx-target="previous .msg" hx-swap="innerHTML">
Показать сообщение
</button>
<div class="tmp box">блок .tmp</div>
<div class="msg box">блок .msg</div>

```

## 3. Атрибут hx-swap для указания куда будет подставлен ответ

Атрибут `hx-swap` позволяет указать, как ответ будет заменен относительно цели (`hx-target`) запроса AJAX. 
Если вы не укажете этот параметр, по умолчанию будет `innerHTML`.

Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_swap.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/hx-swap/

Возможные значения этого атрибута:

* `"innerHTML"` — заменяет внутренний `html` целевого элемента

```html
<div class="demo-block">
  <div class="response" id="inner"><!--Данный текст заменится на ответ--></div>
  <button
    hx-get="/htmx/hx-swap/inner"
    hx-target="#inner"
    hx-swap="innerHTML">
    innerHTML
  </button>
</div>
```

* `"outerHTML"` — заменяет весь целевой элемент ответом

```html
<div class="demo-block">
  <div class="response" id="outer"><!--Весь этот блок div class="response" id="outer" полностью заменится--></div>
  <button
    hx-get="/htmx/hx-swap/outer"
    hx-target="#outer"
    hx-swap="outerHTML">
    outerHTML
  </button>
</div>
```

* `"textContent"` — заменяет текстовое содержимое целевого элемента без анализа ответа как HTML

```html
<div class="demo-block">
  <div class="response" id="text"><b>Жирный текст</b></div>
  <button
    hx-get="/htmx/hx-swap/text"
    hx-target="#text"
    hx-swap="textContent">
    textContent
  </button>
</div>
```

* `"beforebegin"` — вставляет ответ перед целевым элементом

```html
<div class="demo-block">
  <div class="response" id="before">Контейнер</div>
  <button
    hx-get="/htmx/hx-swap/before"
    hx-target="#before"
    hx-swap="beforebegin">
    beforebegin
  </button>
</div>
```

* `"afterbegin"` — вставляет ответ перед первым дочерним элементом целевого элемента

```html
<div class="demo-block">
  <div class="response" id="after-begin">Вставка будет первой внутри</div>
  <button
    hx-get="/htmx/hx-swap/after-begin"
    hx-target="#after-begin"
    hx-swap="afterbegin">
    afterbegin
  </button>
</div>
```

* `"beforeend"` — вставляет ответ после последнего дочернего элемента целевого элемента

```html
<div class="demo-block">
  <div class="response" id="before-end">Вставка будет последней внутри</div>
  <button
    hx-get="/htmx/hx-swap/before-end"
    hx-target="#before-end"
    hx-swap="beforeend">
    beforeend
  </button>
</div>
```

* `"afterend"` — вставляет ответ после целевого элемента

```html
<div class="demo-block">
  <div class="response" id="after">Элемент</div>
  <button
    hx-get="/htmx/hx-swap/after"
    hx-target="#after"
    hx-swap="afterend">
    afterend
  </button>
</div>
```

* `"delete"` — удаляет целевой элемент независимо от ответа

```html
<div class="demo-block">
  <div class="response" id="delete">Этот элемент будет удалён</div>
  <button
    hx-get="/htmx/hx-swap/delete"
    hx-target="#delete"
    hx-swap="delete">
    delete
  </button>
</div>
```

* `"none"` — не добавляет содержимое из ответа (внешние элементы все равно будут обработаны).

```html
<div class="demo-block">
  <div class="response" id="none">Ничего не изменится</div>
  <button
    hx-get="/htmx/hx-swap/none"
    hx-target="#none"
    hx-swap="none">
    none
  </button>
</div>
```

## 4. Атрибут hx-trigger для указания при каком действии будет выполнено условие

Атрибут `hx-trigger` позволяет указать, каком действии и когда будет выполняться условие. По умолчанию это
`click`, т.е. при нажатии мышкой или нажатии `Enter`.

### 4.1 На что может реагировать триггер

#### События мыши

Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_trigger_mouse.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/hx-trigger/mouse/

| Событие       | Когда срабатывает             | Применение                           |
|---------------|-------------------------------|--------------------------------------|
| `click`       | Клик мыши или Enter на кнопке | Кнопки, ссылки, переключатели        |
| `dblclick`    | Двойной клик                  | Открытие (как в файловых менеджерах) |
| `mousedown`   | Нажатие кнопки мыши           | Визуальные эффекты                   |
| `mouseup`     | Отпускание кнопки мыши        | Завершение drag-and-drop             |
| `mouseover`   | Наведение курсора             | Подсказки (tooltip), навигация       |
| `mouseout`    | Уход курсора                  | Скрытие подсказки                    |
| `mousemove`   | Движение мыши                 | Отслеживание передвижение мыши       |
| `contextmenu` | Правая кнопка мыши            | Контекстные меню                     |

```html
<!-- click -->
<h2>click</h2>
<div class="box">
  <div>click (нажми)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/click"
    hx-trigger="click"
    hx-target="#click-response">
    Кликни
  </button>
  <div id="click-response" class="response"></div>
</div>

<!-- dblclick -->
<h2>dblclick</h2>
<div class="box">
  <div>dblclick (двойной клик)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/dblclick"
    hx-trigger="dblclick"
    hx-target="#dblclick-response">
    Двойной клик
  </button>
  <div id="dblclick-response" class="response"></div>
</div>

<!-- mousedown -->
<h2>mousedown</h2>
<div class="box">
  <div>mousedown (зажми кнопку)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/mousedown"
    hx-trigger="mousedown"
    hx-target="#mousedown-response">
    Зажми кнопку
  </button>
  <div id="mousedown-response" class="response"></div>
</div>

<!-- mouseup -->
<h2>mouseup</h2>
<div class="box">
  <div>mouseup (отпусти кнопку)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/mouseup"
    hx-trigger="mouseup"
    hx-target="#mouseup-response">
    Отпусти кнопку
  </button>
  <div id="mouseup-response" class="response"></div>
</div>

<!-- mouseover -->
<h2>mouseover</h2>
<div class="box">
  <div>mouseover (наведение)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/mouseover"
    hx-trigger="mouseover once"
    hx-target="#mouseover-response">
    Наведи курсор
  </button>
  <div id="mouseover-response" class="response"></div>
</div>

<!-- mouseout -->
<h2>mouseout</h2>
<div class="box">
  <div>mouseout (уход курсора)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/mouseout"
    hx-trigger="mouseout"
    hx-target="#mouseout-response">
    Наведи и уведи
  </button>
  <div id="mouseout-response" class="response"></div>
</div>

<!-- mousemove -->
<h2>mousemove</h2>
<div class="box">
  <div>mousemove (движение мыши)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/mousemove"
    hx-trigger="mousemove throttle:1000ms"
    hx-target="#mousemove-response">
    Двигай мышь
  </button>
  <div id="mousemove-response" class="response"></div>
</div>

<!-- contextmenu -->
<h2>contextmenu</h2>
<div class="box">
  <div>contextmenu (правая кнопка)</div>
  <button
    hx-get="/htmx/hx-trigger/mouse/contextmenu"
    hx-trigger="contextmenu"
    hx-target="#contextmenu-response">
    ПКМ
  </button>
  <div id="contextmenu-response" class="response"></div>
</div>
```

#### События клавиатуры и ввода

| Событие   | Когда срабатывает      | Применение                  |
|-----------|------------------------|-----------------------------|
| `input`   | При вводе текста       | Поиск, валидация            |
| `change`  | После завершения ввода | Выпадающие списки, чекбоксы |
| `keydown` | Кнопка нажата          | Горячие клавиши             |
| `keyup`   | Кнопка отпущена        | Поиск, фильтрация по буквам |
| `submit`  | Форма отправлена       | Отправка данных             |
| `reset`   | Сброс формы            |                             |
| `focus`   | Получение фокуса       |                             |
| `blur`    | Потеря фокуса          |                             |


**События фокуса (формы)**

| Событие    | Когда срабатывает            | Применение |
|------------|------------------------------|------------|
| `focusin`  | Когда потомок получает фокус |            |
| `focusout` | После завершения ввода       |            |


**События клипа и буфера обмена**

| Событие | Когда срабатывает | Применение |
|---------|-------------------|------------|
| `copy`  | Копирование       |            |
| `cut`   | Вырезание         |            |
| `paste` | Вставка           |            |

Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_trigger_input.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/hx-trigger/input/

```html
<h2>1. input — поиск при вводе</h2>
  <input name="query"
         placeholder="Поиск..."
         hx-get="/htmx/hx-trigger/input/search/"
         hx-trigger="input changed delay:300ms"
         hx-target="#results"
         hx-swap="innerHTML">
  <div id="results"></div>


  <h2>2. change — выбор из списка</h2>
  <select name="category"
          hx-get="/htmx/hx-trigger/input/filter/"
          hx-trigger="change"
          hx-target="#category-result">
    <option value="">-- выбрать --</option>
    <option value="books">Книги</option>
    <option value="music">Музыка</option>
  </select>
  <div id="category-result"></div>

  <h2>3. keydown — реакция на Enter</h2>
  <input name="keytest"
         placeholder="Нажми Enter"
         hx-get="/htmx/hx-trigger/input/keydown/"
         hx-trigger="keydown"
         hx-target="#keydown-result">
  <div id="keydown-result"></div>


  <h2>4. keyup — живой поиск</h2>
  <input name="search"
         placeholder="Живой поиск..."
         hx-get="/htmx/hx-trigger/input/live-search/"
         hx-trigger="keyup changed delay:300ms"
         hx-target="#live-result">
  <div id="live-result"></div>


  <h2>5. submit — отправка формы</h2>
  <form>
    <input name="name" placeholder="Имя">
    <button hx-post="/htmx/hx-trigger/input/submit-form/"
        hx-target="#submit-result"
        hx-swap="innerHTML">Отправить</button>
  </form>
  <div id="submit-result"></div>

  <h2>6. reset — сброс формы</h2>
  <form>
    <input name="email" placeholder="Email">
    <button hx-trigger="reset"
        hx-post="/htmx/hx-trigger/input/form-reset/"
        hx-target="#reset-result">Сбросить</button>
  </form>
  <div id="reset-result"></div>


  <h2>7. focus — получение фокуса</h2>
  <input name="username"
         placeholder="Логин"
         hx-get="/htmx/hx-trigger/input/username-help/"
         hx-trigger="focus"
         hx-target="#focus-result">
  <div id="focus-result"></div>

  <h2>8. blur — проверка email при выходе</h2>
  <input name="email"
         placeholder="Email"
         hx-post="/htmx/hx-trigger/input/validate-email/"
         hx-trigger="blur changed"
         hx-target="#blur-result">
  <div id="blur-result"></div>


  <h2>9. focusin / focusout — отслеживание фокуса в группе полей</h2>
  <div hx-get="/htmx/hx-trigger/input/focus-event/"
       hx-trigger="focusin from:input, textarea"
       hx-target="#focus-info">
    <input placeholder="Фокус здесь...">
    <textarea placeholder="Или тут..."></textarea>
  </div>
  <div id="focus-info"></div>

  <div hx-get="/htmx/hx-trigger/input/blur-event/"
       hx-trigger="focusout from:input, textarea"
       hx-target="#blur-info">
    <input placeholder="Ушёл отсюда...">
    <textarea placeholder="Или отсюда..."></textarea>
  </div>
  <div id="blur-info"></div>


  <h2>10. copy / cut / paste — события буфера обмена</h2>
  <input placeholder="Попробуй скопировать комбинацией Ctrl+C"
         hx-get="/htmx/hx-trigger/input/clipboard-event/"
         hx-trigger="copy"
         hx-vals='{"action": "copy"}'
         hx-target="#clipboard-result">

  <input placeholder="Попробуй вырезать комбинацией Ctrl+X"
         hx-get="/htmx/hx-trigger/input/clipboard-event/"
         hx-trigger="cut"
         hx-vals='{"action": "cut"}'
         hx-target="#clipboard-result">

  <input placeholder="Попробуй вставить комбинацией Ctrl+V"
         hx-get="/htmx/hx-trigger/input/clipboard-event/"
         hx-trigger="paste"
         hx-vals='{"action": "paste"}'
         hx-target="#clipboard-result">

  <div id="clipboard-result"></div>
```

#### События drag & drop

| Событие     | Когда срабатывает            | Применение |
|-------------|------------------------------|------------|
| `drag`      | Перетаскивание               |            |
| `dragstart` | Начало перетаскивания        |            |
| `dragend`   | Завершение                   |            |
| `dragenter` | Наведение на область         |            |
| `dragover`  | Перетаскивание над элементом |            |
| `dragleave` | Покидание элемента           |            |
| `drop`      | Отпускание мышки в области   |            |


Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_trigger_drag.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/hx-trigger/drag/

```html
<!-- Зона сброса -->
<h2>Зона сброса</h2>
<!-- ondragover="event.preventDefault()" — нужно для работы drop-->
<div class="dropzone" ondragover="event.preventDefault()">
  <!-- Перехватываем все события -->
  <!-- Событие над объектом -->
  <div hx-get="/htmx/hx-trigger/drag/drag-over/"
     hx-trigger="dragover"
     hx-target="#drag-events"
     style="margin-top: -35px;">Выше зоны
  </div>
  <!-- Событие входа -->
  <div hx-get="/htmx/hx-trigger/drag/drag-enter/"
     hx-trigger="dragenter"
     hx-target="#drag-events"
       style="height: 20px;">Вошли в зону
  </div>
  <!-- Событие drop-->
  <div hx-post="/htmx/hx-trigger/drag/drop/"
     hx-trigger="drop"
     hx-target="#drag-events"
     hx-vals='{"name": "Тяни меня"}'
  style="height: 170px; align-content: center;">
  Перетащи сюда
  </div>
  <!-- Событие на выход -->
  <div hx-get="/htmx/hx-trigger/drag/drag-leave/"
       hx-trigger="dragleave"
       hx-target="#drag-events"
       style="height: 20px;">Вышли
  </div>
</div>

<!-- Отображение событий -->
<h2>Отображение событий</h2>
<div id="drag-events" style="margin-top: 1rem;"></div>
```

#### События загрузки элементов

| Событие           | Когда срабатывает                       | Применение                                                                                                                        |
|-------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `load`            | Когда элемент загружается в DOM         | Автозагрузка данных                                                                                                               |
| `revealed`        | Когда элемент впервые виден на экране   | Подгрузка при прокрутке (lazy)                                                                                                    |
| `intersect`       | При пересечении с viewport (наблюдение) | Ленивые запросы, инф. блоки                                                                                                       |
| `delay:500ms`     | Выполнение действия с задержкой 500ms   | Старт загрузки через определенное время                                                                                           |
| `once`            | Выполнить действие только 1 раз         |                                                                                                                                   |
| `every 1s`        | Выполнить действие каждые 1 секунду     | Удобно для обновления статуса, уведомлений, датчиков и т.п                                                                        |
| `throttle:1s`     | Ограничение частоты (не чаще чем 1 сек) | Используется для ограничения частоты запросов, допустим когда объект в зоне, чтобы не перегружать сервер огромным числом запросов |
| `from:<selector>` | Слушает событие от другого элемента     |                                                                                                                                   |

*События изменения* 

| Событие     | Когда срабатывает                           | Применение                                    |
|-------------|---------------------------------------------|-----------------------------------------------|
| `resize`    | Изменение размера окна                      | Адаптивная верстка                            |
| `scroll`    | Прокрутка страницы                          | Lazy loading, sticky header                   |
| `changed`   | Выполнение действий при изменений состояния | Для адаптивных фильтров или динамических форм |


Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_trigger_load.html` или `demo_hx_trigger_adaptive.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/hx-trigger/load/

А также 

http://127.0.0.1:8000/htmx/hx-trigger/adaptive/


## 5. Дополнительные полезные атрибуты

#### Передача данных

| Событие       | Когда срабатывает                                          |
|---------------|------------------------------------------------------------|
| `hx-params`   | Какие параметры отправлять (*, none, список через запятую) | 
| `hx-vals`     | Добавляет дополнительные данные к запросу (в JSON-формате) | 
| `hx-include`  | Включает значения других элементов формы/DOM               | 
| `hx-encoding` | Тип кодировки (обычно multipart/form-data для файлов)      | 

#### Управление запросом

| Событие         | Когда срабатывает                                      |
|-----------------|--------------------------------------------------------|
| `hx-push-url`   | Меняет адрес в адресной строке                         | 
| `hx-select`     | Выбрать часть ответа для вставки                       | 
| `hx-select-oob` | Out-of-band: вставка за пределами hx-target            | 
| `hx-ext`        | Включение расширений (например, client-side-templates) | 
| `hx-confirm`    | Показывает confirm() перед отправкой запроса           | 
| `hx-disable`    | Отключает элемент до завершения запроса                | 
| `hx-indicator`  | Показать индикатор загрузки (например, spinner)        | 
| `hx-headers`    | Добавить заголовки (JSON-строка)                       | 
| `hx-boost`      | Превращает ссылки и формы в HTMX-запросы               | 
| `hx-on`         | Обработчик событий в виде атрибута                     | 
| `hx-timeout`    | Прерывает запрос, если не ответил за N мс              | 
| `hx-history`    | Управление историей: false — не сохранять              | 

Ниже приведены коды для различных задач и примеров их использования. Данный код уже 
реализован в `demo_hx_features.html` приложения `app_htmx`. Интерактивно ознакомиться можете по ссылке

http://127.0.0.1:8000/htmx/features/

