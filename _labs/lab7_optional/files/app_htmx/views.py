from django.shortcuts import render
from django.http import HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from time import sleep
import random


def load_products_html(request):  # Возвращаем список продуктов через html
    products = ["Телефон", "Ноутбук", "Наушники", "Клавиатура", "Мышь", "Монитор"]
    html = "".join(f"<li>{product}</li>" for product in
                   random.sample(products, 4))  # Получаем 4 случайных товара из списка и формируем html
    return HttpResponse(html)


def load_products_with_render(request):  # Возвращаем список продуктов через render шаблона list_products.html
    products = ["Телефон", "Ноутбук", "Наушники", "Клавиатура", "Мышь", "Монитор"]
    return render(request, 'app_htmx/list_products.html', {'products': random.sample(products, 4)})


def product_list_view(request):  # Основной шаблон с кнопкой перезагрузки продуктов
    return render(request, 'app_htmx/products.html')


# ____________ представления для demo_hx_target
def hx_target_view(request):
    return render(request, 'app_htmx/demo_hx_target.html')


def load_status(request):
    return HttpResponse('<button disabled>Статус: OK</button>')


def row_details(request):
    return HttpResponse("""
    <tr>
        <td colspan="3">Подробности: Товар A, Цена: 100₽</td>
    </tr>
    """)


def product_details(request):
    return HttpResponse("Описание: Это классный товар!")


def more_info(request):
    return HttpResponse("Дополнительная информация загружена.")


@csrf_exempt
def validate_email(request):
    email = request.POST.get("email", "")
    if "@" not in email:
        return HttpResponse("<span style='color: red'>Ошибка: Некорректный email</span>")
    return HttpResponse("<span style='color: green'>Email корректен!</span>")


def get_result(request):
    return HttpResponse("Результат обновлён!")


def show_note(request):
    return HttpResponse("Новое сообщение: добро пожаловать!")


# __________ представления для demo_hx_swap

def hx_swap_view(request):
    return render(request, 'app_htmx/demo_hx_swap.html')


def swap_inner(request):
    return HttpResponse("<b>Заменённый innerHTML</b>")


def swap_outer(request):
    return HttpResponse(
        "<div class='response' id='outer' style='color: red; background: #7abaff;'>Полностью заменён outerHTML</div>")


def swap_text(request):
    return HttpResponse("<b>Это будет видно как текст, а не HTML</b>")


def swap_before(request):
    return HttpResponse("<div style='color: green;'>→ ДО элемента</div>")


def swap_after_begin(request):
    return HttpResponse("<div style='color: blue;'>⇨ ВСТАВКА В НАЧАЛО</div>")


def swap_before_end(request):
    return HttpResponse("<div style='color: purple;'>⇦ ВСТАВКА В КОНЕЦ</div>")


def swap_after(request):
    return HttpResponse("<div style='color: orange;'>→ ПОСЛЕ элемента</div>")


def swap_delete(request):
    return HttpResponse("")  # HTMX просто удалит элемент


def swap_none(request):
    # Код выполнится
    return HttpResponse("<div style='color: gray;'>Этот ответ не будет вставлен</div>")


# __________ представления для demo_hx_trigger_mouse


def hx_trigger_mouse_view(request):
    return render(request, 'app_htmx/demo_hx_trigger_mouse.html')


def mouse_event(request, event_name):
    messages = {
        "click": "✔ Клик сработал!",
        "dblclick": "✔ Двойной клик сработал!",
        "mousedown": "✔ Нажатие кнопки мыши (mousedown)",
        "mouseup": "✔ Отпускание кнопки мыши (mouseup)",
        "mouseover": "✔ Наведение мыши (mouseover)",
        "mouseout": "✔ Уход мыши (mouseout)",
        "mousemove": "✔ Движение мыши (mousemove)",
        "contextmenu": "✔ Правая кнопка мыши (contextmenu)",
    }

    message = messages.get(event_name, f"Событие: {event_name}")
    return HttpResponse(message)


# __________ представления для demo_hx_trigger_input

def hx_trigger_input_view(request):
    return render(request, 'app_htmx/demo_hx_trigger_input.html')


def search(request):
    query = request.GET.get("query", "")
    return HttpResponse(f"🔎 Поиск по: {query}")


def filter_category(request):
    category = request.GET.get("category", "")
    return HttpResponse(f"📚 Категория выбрана: {category}")


def keydown_event(request):
    return HttpResponse("⏎ Нажат Enter")


def live_search(request):
    term = request.GET.get("search", "")
    return HttpResponse(f"🔍 Живой поиск: {term}")


@csrf_exempt
def submit_form(request):
    name = request.POST.get("name", "")
    return HttpResponse(f"✅ Форма отправлена: {name}")


@csrf_exempt
def form_reset(request):
    return HttpResponse("🔄 Форма сброшена")


def username_help(request):
    return HttpResponse("👤 Логин должен быть от 3 до 20 символов.")


@csrf_exempt
def focus_event(request):
    return HttpResponse("🔍 Кто-то получил фокус внутри блока.")


@csrf_exempt
def blur_event(request):
    return HttpResponse("💨 Потеря фокуса в блоке.")


@csrf_exempt
def validate_email(request):
    email = request.POST.get("email", "")
    return HttpResponse(f"📧 Email проверен: {email}")


def clipboard_event(request):
    action = request.GET.get("action", "")
    match action:
        case "copy":
            return HttpResponse("📄 Вы скопировали текст!")
        case "cut":
            return HttpResponse("✂️ Вы вырезали текст!")
        case "paste":
            return HttpResponse("📥 Вы вставили текст!")
        case _:
            return HttpResponse("🤷 Неизвестное действие.")


# __________ представления для demo_hx_trigger_drag

def hx_trigger_drag_view(request):
    return render(request, 'app_htmx/demo_hx_trigger_drag.html')


def drag_start(request):
    return HttpResponse("🚚 Перетаскивание началось (dragstart)")


def drag_enter(request):
    return HttpResponse("📥 Навели на зону сброса (dragenter)")


def drag_over(request):
    return HttpResponse("🌀 Перетаскиваем над зоной (dragover)")


def drag_leave(request):
    return HttpResponse("🏃 Покинули зону сброса (dragleave)")


@csrf_exempt
def drop(request):
    name_file = request.POST.get('name', '')
    return HttpResponse(f"✅ Объект {name_file!r} сброшен! (drop)")


# __________ представления для demo_hx_trigger_load

def hx_trigger_load_view(request):
    return render(request, 'app_htmx/demo_hx_trigger_load.html')


def load_auto(request):
    return HttpResponse("<b>✅ Данные загружены автоматически</b>")


def load_revealed(request):
    return HttpResponse("<b>👁️ Элемент стал видимым в viewport!</b>")


def load_intersect(request):
    return HttpResponse("<b>🚀 Загружено при прокрутке и пересечении</b>")


# __________ представления для demo_hx_trigger_adaptive

def hx_trigger_adaptive_view(request):
    return render(request, 'app_htmx/demo_hx_trigger_adaptive.html')


def adaptive_every(request):
    now = datetime.now().strftime("%H:%M:%S")
    return HttpResponse(f"⏰ Обновлено в {now}")


def adaptive_delayed(request):
    return HttpResponse("✅ Загружено после задержки")


def adaptive_resize(request):
    return HttpResponse("📐 Размер окна изменён!")


def adaptive_input(request):
    value = request.GET.get("search", "")
    return HttpResponse(f"🔎 Введено: {value}")


def adaptive_revealed(request):
    return HttpResponse("📦 Элемент стал видимым (lazy loaded)")


def adaptive_scroll(request):
    now = datetime.now().strftime("%H:%M:%S")
    return HttpResponse(f"🧭 Scroll сработал в {now}")


# Список цветов
COLORS = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#9D4EDD"]

counter = 0  # глобальный, если хотите ограничить


def next_box(request):
    global counter
    if counter >= 10:
        return HttpResponse('<div class="box">✅ Всё загружено</div>')

    sleep(0.7)  # имитация задержки
    color = random.choice(COLORS)
    counter += 1

    html = f'''
    <div class="box" style="background-color: {color};">Прямоугольник #{counter}</div>

    <div id="lazy-scroll-trigger"
         hx-get="/htmx/hx-trigger/adaptive/next/"
         hx-trigger="revealed"
         hx-target="#lazy-scroll-trigger"
         hx-swap="outerHTML"
         class="loading-trigger">
      👀 Прокрутите ниже для подгрузки...
    </div>'''
    return HttpResponse(html)


# __________ представления для demo_hx_features

def hx_features_view(request):
    return render(request, 'app_htmx/demo_hx_features.html')


@csrf_exempt
def params_view(request):
    return HttpResponse(f"hx-params: {dict(request.POST)}")


@csrf_exempt
def vals_view(request):
    return HttpResponse(f"hx-vals: {dict(request.POST)}")


@csrf_exempt
def include_view(request):
    included = request.POST.get('shared', '')
    return HttpResponse(f"hx-include value: {included}")


@csrf_exempt
def upload_view(request):
    uploaded_file = request.FILES.get('myfile')
    if uploaded_file:
        # Получаем параметры файла
        filename = uploaded_file.name
        content_type = uploaded_file.content_type
        size = uploaded_file.size
        content = uploaded_file.read()  # Содержимое файла

        return HttpResponse(
            f"<b>Имя файла:</b> {filename}<br>"
            f"<b>Тип:</b> {content_type}<br>"
            f"<b>Размер:</b> {size / 1024:.2f} KB"
        )

    return HttpResponse("Файл не был загружен.")


def push_url_view(request):
    return HttpResponse("<div>New content with push URL</div>")


def select_view(request):
    return HttpResponse("<div><span id='selected'>Selected Content Only</span><p>Ignored</p></div>")


def select_oob_view(request):
    html = """
    <div hx-swap-oob="true" id="oob-target">🔄 Out of Band Updated!</div>
    <div>Normal content</div>
    """
    return HttpResponse(html)


def ext_view(request):
    return HttpResponse("Custom extension triggered!")


@csrf_exempt
def confirm_view(request):
    return HttpResponse("hx-confirm: Пользователь подтвердил действие")


@csrf_exempt
def disable_view(request):
    sleep(2)  # имитация задержки
    return HttpResponse("Кнопка была отключена")


def indicator_view(request):
    sleep(1.5)
    return HttpResponse("✅ Загрузка завершена")


@csrf_exempt
def headers_view(request):
    custom = request.headers.get("X-Custom-Header", "Нет заголовка")
    return HttpResponse(f"Custom header: {custom}")


def boost_page(request):
    return HttpResponse("<h2>📄 Перешли по hx-boost ссылке!</h2>")


@csrf_exempt
def on_event_view(request):
    sleep(1)
    return HttpResponse("🎉 Событие обработано через hx-on")


def timeout_view(request):
    sleep(2)
    return HttpResponse("⌛ Задержка завершилась успешно")


def history_view(request):
    return HttpResponse("<h3>🕘 Это состояние истории</h3>")


def oob_from_cart_view(request):
    return render(request, 'app_htmx/oob_from_cart.html')


@csrf_exempt
def cart_add_view(request):
    html = """
    <!-- Корзина: заменяется через hx-swap-oob -->
    <div id="cart" hx-swap-oob="true"> В корзине: 1 товар</div>

    <!-- Уведомление: также oob -->
    <div id="notification" hx-swap-oob="true">Товар добавлен в корзину!</div>

    <!-- Основной отклик -->
    <div>Товар обрабатывается...</div>
    """
    return HttpResponse(html)
