def function7():

    # admin_dashboard.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <div class="admin-dashboard">
    #     <h2>Пользователи</h2>
    #     <a class="btn btn-primary" href="{{ url_for('create_user') }}">Новый пользователь</a>
    #     <a class="btn btn-primary" href="{{ url_for('backup_database') }}">Создать бекап</a>
    #     <table class="table">
    #         <thead>
    #             <tr>
    #                 <th>Имя</th>
    #                 <th>Фамилия</th>
    #                 <th>Роль</th>
    #                 <th>Статус</th>
    #                 <th>Изменить</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {% for user in users %}
    #             <tr>
    #                 <td>{{ user.first_name }}</td>
    #                 <td>{{ user.last_name }}</td>
    #                 <td>{{ user.role }}</td>
    #                 <td>{{ user.status }}</td>
    #                 <td>
    #                     {% if user.status == 'работает' %}
    #                     <form method="post" action="{{ url_for('deactivate_user', user_id=user.id) }}" class="d-inline">
    #                         <button type="submit" class="btn btn-warning btn-sm">Удалить</button>
    #                     </form>
    #                     {% endif %}
    #                 </td>
    #             </tr>
    #             {% endfor %}
    #         </tbody>
    #     </table>
    # </div>
    # {% endblock %}

    # admin_view_orders.html

    # {% extends "layout.html" %}
    # {% block content %}
    #     <h2>Заказы</h2>
    #     <table class="table">
    #         <thead>
    #             <tr>
    #                 <th>ID заказа</th>
    #                 <th>Номер стола</th>
    #                 <th>Статус</th>
    #                 <th>Создан</th>
    #                 <th>Состав заказа</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {% for order in orders %}
    #                 <tr>
    #                     <td>{{ order.id }}</td>
    #                     <td>{{ order.table_number }}</td>
    #                     <td>{{ order.status }}</td>
    #                     <td>{{ order.created_at }}</td>
    #                     <td>
    #                         <ul>
    #                             {% for item in order_items[order.id] %}
    #                                 <li>{{ item.dish_name }}: {{ item.quantity }}</li>
    #                             {% endfor %}
    #                         </ul>
    #                     </td>
    #                 </tr>
    #             {% endfor %}
    #         </tbody>
    #     </table>
    # {% endblock %}

    # assign_shift.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <div class="assign-shift">
    #     <h2>Добавить смену</h2>
    #     <form method="post" action="{{ url_for('assign_shift') }}">
    #         <div class="form-group">
    #             <label for="user_id">Пользователь</label>
    #             <select id="user_id" name="user_id" class="form-control-assign" required>
    #                 {% for user in users %}
    #                 <option value="{{ user.id }}">{{ user.first_name }} {{ user.last_name }} ({{ user.role }})</option>
    #                 {% endfor %}
    #             </select>
    #         </div>
    #         <div class="form-group">
    #             <label for="shift_date">Дата смены</label>
    #             <input type="date" id="shift_date" name="shift_date" class="form-control-assign" required>
    #         </div>
    #         <div class="form-group">
    #             <label for="role">Роль</label>
    #             <select id="role" name="role" class="form-control-assign" required>
    #                 <option value="официант">Официант</option>
    #                 <option value="повар">Повар</option>
    #             </select>
    #         </div>
    #         <button type="submit" class="btn btn-primary">Добавить смену</button>
    #     </form>
    # </div>
    # {% endblock %}

    # cook_dashboard.html

    # {% extends "layout.html" %}
    # {% block content %}
    #     <h2>Заказы</h2>
    #     <table class="table">
    #         <thead>
    #             <tr>
    #                 <th>ID заказа</th>
    #                 <th>Номер столика</th>
    #                 <th>Статус</th>
    #                 <th>Создан</th>
    #                 <th>Состав заказа</th>
    #                 <th>Изменить</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {% for order in orders %}
    #                 <tr>
    #                     <td>{{ order.id }}</td>
    #                     <td>{{ order.table_number }}</td>
    #                     <td>{{ order.status }}</td>
    #                     <td>{{ order.created_at }}</td>
    #                     <td>
    #                         <ul>
    #                             {% for item in order_items[order.id] %}
    #                                 <li>{{ item.dish_name }}: {{ item.quantity }}</li>
    #                             {% endfor %}
    #                         </ul>
    #                     </td>
    #                     <td>
    #                         <a href="{{ url_for('cook_update_order_status', order_id=order.id) }}" class="btn btn-primary">Изменить статус</a>
    #                     </td>
    #                 </tr>
    #             {% endfor %}
    #         </tbody>
    #     </table>
    # {% endblock %}

    # cook_shifts.html

    # {% extends 'layout.html' %}
    # {% block content %}
    # <h2>Ваши смены:</h2>
    # <table class="table">
    #     <thead>
    #         <tr>
    #             <th>Дата</th>
    #             <th>Роль</th>
    #         </tr>
    #     </thead>
    #     {% for shift in current_user.shifts %}
    #     <tbody>

    #         <tr>
    #             <td>{{ shift.shift_date }}</td>
    #             <td>{{ shift.role }}</td>
    #         </tr>

    #     </tbody>
    #     {% endfor %}
    # </table>
    # {% endblock %}

    # cook_update_order_status.html

    # {% extends "layout.html" %}
    # {% block content %}
    #     <h2>Изменить статус заказа</h2>
    #     <form method="POST" action="{{ url_for('cook_update_order_status', order_id=order.id) }}">
    #         <div class="form-group">
    #             <label for="status">Статус:</label>
    #             <select id="status" name="status" class="form-control-status" required>
    #                 <option value="готовится" {% if order.status == 'готовится' %}selected{% endif %}>Готовится</option>
    #                 <option value="готов" {% if order.status == 'готов' %}selected{% endif %}>Готов</option>
    #             </select>
    #         </div>
    #         <button type="submit" class="btn btn-primary">Изменить статус</button>
    #     </form>
    # {% endblock %}

    # create_order.html

    # {% extends "layout.html" %}
    # {% block content %}
    #     <h2>Создать заказ</h2>
    #     <form method="POST" action="{{ url_for('create_order') }}">
    #         <div class="form-group">
    #             <label for="table_number">Номер стола:</label>
    #             <input type="number" id="table_number" placeholder="Номер стола" name="table_number" class="form-control-table" required>
    #         </div>
    #         <h3>Состав заказа:</h3>
    #         <div id="items">
    #             <div class="item form-group flex-items">
    #                 <input type="text" name="dish_name" class="form-control-dish" placeholder="Название блюда" required>
    #                 <input type="number" name="quantity" class="form-control-quantity" placeholder="Кол-во" required>
    #             </div>
    #         </div>
    #         <button type="button" class="btn btn-secondary" onclick="addItem()">Добавить</button>
    #         <button type="submit" class="btn btn-primary">Создать заказ</button>
    #     </form>
    #     <script>
    #         function addItem() {
    #             const itemsDiv = document.getElementById('items');
    #             const newItem = document.createElement('div');
    #             newItem.classList.add('item', 'form-group');
    #             newItem.innerHTML = `
    #                 <input type="text" name="dish_name" class="form-control-dish" placeholder="Название блюда" required>
    #                 <input type="number" name="quantity" class="form-control-quantity" placeholder="Кол-во" required>
    #             `;
    #             itemsDiv.appendChild(newItem);
    #         }
    #     </script>
    # {% endblock %}

    # create_user.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <div class="create-user">
    #     <h1>Создать пользователя</h1>
    #     <a class="btn btn-primary" href="{{ url_for('upload_file') }}">Загрузить из файла</a>
    #     <form method="POST">
    #         {{ form.hidden_tag() }}
    #             <div class="flex-items">
    #                 <div class="block-items-name">
    #                     <div class="form-label-name-div-first">{{ form.first_name.label(class="form-label-name") }}</div>
    #                     <div class="form-label-name-div">{{ form.last_name.label(class="form-label-name") }}</div>
    #                     <div class="form-label-name-div">{{ form.email.label(class="form-label-name") }}</div>
    #                     <div class="form-label-name-div">{{ form.password.label(class="form-label-name") }}</div>
    #                     <div class="form-label-name-div">{{ form.role.label(class="form-label-name") }}</div>
    #                 </div>
    #                 <div class="block-items">
    #                     <div>{{ form.first_name(class="form-control-create") }}</div>
    #                     <div>{{ form.last_name(class="form-control-create") }}</div>
    #                     <div>{{ form.email(class="form-control-create") }}</div>
    #                     <div>{{ form.password(class="form-control-create") }}</div>
    #                     <div>{{ form.role(class="form-control-create-role") }}</div>
    #                 </div>
    #             </div>

    #         </div>
    #         {{ form.submit(class="btn btn-primary") }}
    #     </form>
    # </div>
    # {% endblock %}

    # layout.html

    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="UTF-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <title>Cafe Management</title>
    #     <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    # </head>
    # <body>
    #     <nav class="navbar navbar-expand-lg navbar-light bg-light">
    #         <a class="navbar-brand" href="{{ url_for('home') }}">Cafe Management</a>
    #         <div class="collapse navbar-collapse">
    #             <ul class="navbar-nav ml-auto">
    #                 {% if current_user.is_authenticated %}
    #                     {% if current_user.role == 'админ' %}
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('admin_dashboard') }}">Пользователи</a>
    #                         </li>
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('view_shifts') }}">Смены</a>
    #                         </li>
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('admin_view_orders') }}">Заказы</a>
    #                         </li>
    #                     {% elif current_user.role == 'официант' %}
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('waiter_dashboard') }}">Заказы</a>
    #                         </li>
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('create_order') }}">Создать заказ</a>
    #                         </li>
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('waiter_shifts') }}">Смены</a>
    #                         </li>
    #                     {% elif current_user.role == 'повар' %}
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('cook_dashboard') }}">Заказы</a>
    #                         </li>
    #                         <li class="nav-item">
    #                             <a class="nav-link" href="{{ url_for('cook_shifts') }}">Смены</a>
    #                         </li>
    #                     {% endif %}
    #                     <li class="nav-item">
    #                         <a class="nav-link last" href="{{ url_for('logout') }}">Выйти</a>
    #                     </li>
    #                 {% else %}
    #                     <li class="nav-item">
    #                         <a class="nav-link" href="{{ url_for('login') }}">Войти</a>
    #                     </li>
    #                 {% endif %}
    #             </ul>
    #         </div>
    #     </nav>
    #     <div class="container">
    #         {% with messages = get_flashed_messages(with_categories=true) %}
    #             {% if messages %}
    #                 {% for category, message in messages %}
    #                     <div class="alert alert-{{ category }}">
    #                         {{ message }}
    #                     </div>
    #                 {% endfor %}
    #             {% endif %}
    #         {% endwith %}
    #         {% block content %}{% endblock %}
    #     </div>
    # </body>
    # </html>

    # login.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <div class="container">
    #     <div class="row justify-content-center">
    #         <div class="col-md-6">
    #             <h1 class="text-center">Войти</h1>
    #             <form method="POST" action="{{ url_for('login') }}">
    #                 {{ form.hidden_tag() }}
    #                 <div class="form-group-login">
    #                     {{ form.email.label(class="form-control-label") }}
    #                     {{ form.email(class="form-control") }}
    #                 </div>
    #                 <div class="form-group-login">
    #                     {{ form.password.label(class="form-control-label") }}
    #                     {{ form.password(class="form-control") }}
    #                 </div>
    #                 <div class="form-group-remember flex-items">
    #                     {{ form.remember(class="form-check-input") }}
    #                     {{ form.remember.label(class="form-check-label") }}
    #                 </div>
    #                 <div class="form-group">
    #                     {{ form.submit(class="btn btn-primary") }}
    #                 </div>
    #             </form>
    #         </div>
    #     </div>
    # </div>
    # {% endblock %}

    # order_status.html

    # {% extends "layout.html" %}
    # {% block content %}
    #     <h2>Изменить статус заказа</h2>
    #     <form method="POST" action="{{ url_for('update_order_status', order_id=order.id) }}">
    #         <div class="form-group">
    #             <label for="status">Статус:</label>
    #             <select id="status" name="status" class="form-control-status" required>
    #                 <option value="принят">принят</option>
    #                 <option value="оплачен">оплачен</option>
    #             </select>
    #         </div>
    #         <button type="submit" class="btn btn-primary">Изменить статус</button>
    #     </form>
    # {% endblock %}

    # upload.html

    # {% extends 'layout.html' %}

    # {% block content %}
    # <h1>Upload new File</h1>
    # <form method="post" enctype="multipart/form-data">
    # <input type="file" name="file">
    # <input type="submit" value="Upload">
    # </form>
    # {% with messages = get_flashed_messages() %}
    # {% if messages %}
    #     <ul>
    #     {% for message in messages %}
    #         <li>{{ message }}</li>
    #     {% endfor %}
    #     </ul>
    # {% endif %}
    # {% endwith %}

    # {% endblock %}

    # view_shifts.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <div class="view-shifts">
    #     <h2>Просмотр смен</h2>
    #     <a class="btn btn-primary" href="{{ url_for('assign_shift') }}">Новая смена</a>
    #     <table class="table">
    #         <thead>
    #             <tr>
    #                 <th>Пользователь</th>
    #                 <th>Дата смены</th>
    #                 <th>Роль</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {% for shift in shifts %}
    #             <tr>
    #                 <td>{{ shift.user.first_name }} {{ shift.user.last_name }}</td>
    #                 <td>{{ shift.shift_date }}</td>
    #                 <td>{{ shift.role }}</td>
    #             </tr>
    #             {% endfor %}
    #         </tbody>
    #     </table>
    # </div>
    # {% endblock %}

    # waiter_dashboard.html

    # {% extends "layout.html" %}
    # {% block content %}
    # <h1>Dashboard</h1>
    #     <h2>Your Orders</h2>
    #     <table class="table">
    #         <thead>
    #             <tr>
    #                 <th>ID заказа</th>
    #                 <th>Номер стола</th>
    #                 <th>Статус</th>
    #                 <th>Создан</th>
    #                 <th>Состав заказа</th>
    #                 <th>Изменить</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             {% for order in orders %}
    #                 <tr>
    #                     <td>{{ order.id }}</td>
    #                     <td>{{ order.table_number }}</td>
    #                     <td>{{ order.status }}</td>
    #                     <td>{{ order.created_at }}</td>
    #                     <td>
    #                         <ul>
    #                             {% for item in order_items[order.id] %}
    #                                 <li>{{ item.dish_name }}: {{ item.quantity }}</li>
    #                             {% endfor %}
    #                         </ul>
    #                     </td>
    #                     <td>
    #                         <a href="{{ url_for('update_order_status', order_id=order.id) }}" class="btn btn-primary">Изменить статус</a>
    #                     </td>
    #                 </tr>
    #             {% endfor %}
    #         </tbody>
    #     </table>
    # {% endblock %}

    # waiter_shifts.html

    # {% extends 'layout.html' %}
    # {% block content %}
    # <h2>Ваши смены:</h2>
    # <table class="table">
    #     <thead>
    #         <tr>
    #             <th>Дата</th>
    #             <th>Роль</th>
    #         </tr>
    #     </thead>
    #     {% for shift in current_user.shifts %}
    #     <tbody>

    #         <tr>
    #             <td>{{ shift.shift_date }}</td>
    #             <td>{{ shift.role }}</td>
    #         </tr>

    #     </tbody>
    #     {% endfor %}
    # </table>

    # {% endblock %}

    return "contents of all HTML documents"
