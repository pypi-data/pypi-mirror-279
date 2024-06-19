def function1():

    # import shutil
    # from flask import render_template, url_for, flash, redirect, request, send_file
    # from flask_login import login_user, current_user, logout_user, login_required
    # from werkzeug.utils import secure_filename
    # from werkzeug.security import generate_password_hash
    # import os
    # import pandas as pd
    # from app import db, app
    # from app.models import User, Order, OrderItem, Shift
    # from app.forms import LoginForm, UserForm, ShiftForm
    # from datetime import datetime
    # from config import Config

    # @app.route('/')
    # def home():
    #     try:
    #         if current_user.role == 'админ':
    #             return redirect(url_for('admin_dashboard'))
    #         elif current_user.role == 'официант':
    #             return redirect(url_for('waiter_dashboard'))
    #         elif current_user.role == 'повар':
    #             return redirect(url_for('cook_dashboard'))
    #     except:
    #         return redirect(url_for('login'))

    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     if current_user.is_authenticated:
    #         return redirect(url_for('home'))

    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         user = User.query.filter_by(email=form.email.data).first()
    #         if user and user.check_password(form.password.data):
    #             login_user(user, remember=form.remember.data)
    #             flash('Login successful!', 'success')
    #             next_page = request.args.get('next')
    #             return redirect(next_page) if next_page else redirect(url_for('home'))
    #         else:
    #             flash('Login Unsuccessful. Please check email and password', 'danger')

    #     return render_template('login.html', form=form)

    # @app.route('/logout')
    # def logout():
    #     logout_user()
    #     return redirect(url_for('home'))

    # @app.route('/admin/dashboard')
    # @login_required
    # def admin_dashboard():
    #     if current_user.role != 'админ':
    #         flash('Access denied.', 'danger')
    #         return redirect(url_for('home'))
    #     users = User.query.all()
    #     orders = Order.query.all()
    #     shifts = Shift.query.all()
    #     return render_template('admin_dashboard.html', users=users, orders=orders, shifts=shifts)

    # @app.route('/admin/create_user', methods=['GET', 'POST'])
    # @login_required
    # def create_user():
    #     if current_user.role != 'админ':
    #         flash('Access denied.', 'danger')
    #         return redirect(url_for('home'))
    #     form = UserForm()
    #     if form.validate_on_submit():
    #         user = User(first_name=form.first_name.data, last_name=form.last_name.data,
    #                     email=form.email.data, role=form.role.data)
    #         user.set_password(form.password.data)
    #         db.session.add(user)
    #         db.session.commit()
    #         flash('User created successfully!', 'success')
    #         return redirect(url_for('admin_dashboard'))
    #     return render_template('create_user.html', form=form)

    # @app.route('/admin/deactivate_user/<int:user_id>', methods=['POST'])
    # @login_required
    # def deactivate_user(user_id):
    #     if current_user.role != 'админ':
    #         flash('Access denied.', 'danger')
    #         return redirect(url_for('home'))
    #     user = User.query.get(user_id)
    #     if user:
    #         user.deactivate()
    #         flash('User deactivated successfully!', 'success')
    #     return redirect(url_for('admin_dashboard'))

    # @app.route('/admin/view_shifts')
    # @login_required
    # def view_shifts():
    #     if current_user.role != 'админ':
    #         flash('Unauthorized access', 'danger')
    #         return redirect(url_for('home'))

    #     shifts = Shift.query.all()
    #     return render_template('view_shifts.html', shifts=shifts)

    # @app.route('/admin/assign_shift', methods=['GET', 'POST'])
    # @login_required
    # def assign_shift():
    #     if current_user.role != 'админ':
    #         flash('Unauthorized access', 'danger')
    #         return redirect(url_for('home'))

    #     if request.method == 'POST':
    #         user_id = request.form['user_id']
    #         shift_date = datetime.strptime(request.form['shift_date'], '%Y-%m-%d')
    #         role = request.form['role']

    #         shift = Shift(user_id=user_id, shift_date=shift_date, role=role)
    #         db.session.add(shift)
    #         db.session.commit()
    #         flash('Shift assigned successfully!', 'success')
    #         return redirect(url_for('assign_shift'))

    #     users = User.query.filter_by(status='работает').all()
    #     shifts = Shift.query.all()
    #     return render_template('assign_shift.html', users=users, shifts=shifts)

    # @app.route('/admin/orders')
    # @login_required
    # def admin_view_orders():
    #     if current_user.role != 'админ':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))

    #     orders = Order.query.all()
    #     order_items = {order.id: OrderItem.query.filter_by(
    #         order_id=order.id).all() for order in orders}
    #     return render_template('admin_view_orders.html', orders=orders, order_items=order_items)

    # def allowed_file(filename):
    #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    # @app.route('/admin/upload', methods=['GET', 'POST'])
    # def upload_file():
    #     if current_user.role != 'админ':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))
    #     if request.method == 'POST':
    #         # Проверяем, был ли файл загружен
    #         if 'file' not in request.files:
    #             flash('Файл не найден в запросе', 'danger')
    #             return redirect(request.url)

    #         file = request.files['file']

    #         # Проверяем, выбран ли файл
    #         if file.filename == '':
    #             flash('Файл не выбран', 'danger')
    #             return redirect(request.url)

    #         if file and allowed_file(file.filename):
    #             filename = secure_filename(file.filename)
    #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #             file.save(filepath)

    #             # Чтение данных из Excel файла
    #             df = pd.read_excel(filepath)

    #             # Проверка на наличие необходимых столбцов
    #             required_columns = ['ФИО', 'Роль', 'Логин', 'Пароль']
    #             if not all(col in df.columns for col in required_columns):
    #                 flash('В Excel файле отсутствуют необходимые столбцы')
    #                 return redirect(request.url)

    #             # Преобразование данных
    #             users = []
    #             for index, row in df.iterrows():
    #                 try:
    #                     # Делим ФИО на first_name и last_name
    #                     first_name, last_name = row['ФИО'].split()[:2]
    #                 except ValueError:
    #                     flash(f'Невозможно разделить ФИО: {row["ФИО"]}')
    #                     continue

    #                 user = User(
    #                     first_name=first_name,
    #                     last_name=last_name,
    #                     email=row['Логин'],
    #                     # Предполагается, что пароли уже захешированы в файле
    #                     password_hash=generate_password_hash(row['Пароль']),
    #                     role=row['Роль'],
    #                     status='работает'  # Используем значение по умолчанию
    #                 )
    #                 users.append(user)

    #             # Вставка данных в базу данных
    #             try:
    #                 db.session.bulk_save_objects(users)
    #                 db.session.commit()
    #                 flash(
    #                     'Файл успешно загружен и данные вставлены в базу данных', 'success')
    #             except Exception as e:
    #                 db.session.rollback()
    #                 flash(f'Ошибка при вставке данных в базу данных: {str(e)}')

    #             return redirect(url_for('home'))

    #     return render_template('upload.html')

    # @app.route('/admin/backup', methods=['GET'])
    # def backup_database():
    #     if current_user.role != 'админ':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))
    #     try:
    #         # Создаем имя файла для резервной копии
    #         backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    #         backup_path = os.path.join(Config.BACKUP_FOLDER, backup_filename)

    #         # Копируем файл базы данных
    #         shutil.copy2(Config.DB_PATH, backup_path)

    #         flash('Резервная копия базы данных успешно создана', 'success')
    #         return send_file(backup_path, as_attachment=True)
    #     except Exception as e:
    #         flash(f'Ошибка при создании резервной копии: {str(e)}', 'danger')
    #         # Предположим, что у вас есть маршрут 'index'
    #         return redirect(url_for('home'))

    # @app.route('/waiter/dashboard')
    # @login_required
    # def waiter_dashboard():
    #     if current_user.role != 'официант':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))

    #     orders = Order.query.filter(
    #         Order.waiter_id == current_user.id,
    #         Order.status.in_(['принят', 'готовится', 'готов'])
    #     ).all()
    #     order_items = {order.id: OrderItem.query.filter_by(
    #         order_id=order.id).all() for order in orders}
    #     return render_template('waiter_dashboard.html', orders=orders, order_items=order_items)

    # @app.route('/waiter/shifts')
    # @login_required
    # def waiter_shifts():
    #     return render_template('waiter_shifts.html', shifts=current_user.shifts)

    # @app.route('/waiter/orders/create', methods=['GET', 'POST'])
    # @login_required
    # def create_order():
    #     if current_user.role != 'официант':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))

    #     if request.method == 'POST':
    #         table_number = request.form.get('table_number')
    #         dish_names = request.form.getlist('dish_name')
    #         quantities = request.form.getlist('quantity')

    #         if not table_number or not dish_names or not quantities or len(dish_names) != len(quantities):
    #             flash('All fields are required', 'danger')
    #             return redirect(url_for('create_order'))

    #         new_order = Order(
    #             table_number=table_number,
    #             status='принят',
    #             created_at=datetime.utcnow().replace(microsecond=0),
    #             updated_at=datetime.utcnow().replace(microsecond=0),
    #             waiter_id=current_user.id
    #         )
    #         db.session.add(new_order)
    #         db.session.commit()

    #         for dish_name, quantity in zip(dish_names, quantities):
    #             order_item = OrderItem(
    #                 order_id=new_order.id,
    #                 dish_name=dish_name,
    #                 quantity=int(quantity)
    #             )
    #             db.session.add(order_item)
    #         db.session.commit()

    #         flash('Order created successfully', 'success')
    #         return redirect(url_for('waiter_dashboard'))

    #     return render_template('create_order.html')

    # @app.route('/waiter/orders/<int:order_id>/update_status', methods=['GET', 'POST'])
    # @login_required
    # def update_order_status(order_id):
    #     order = Order.query.get_or_404(order_id)
    #     if order.waiter_id != current_user.id:
    #         flash('You are not authorized to update this order', 'danger')
    #         return redirect(url_for('waiter_dashboard'))

    #     if request.method == 'POST':
    #         new_status = request.form.get('status')
    #         if new_status not in ['принят', 'оплачен']:
    #             flash('Invalid status', 'danger')
    #             return redirect(url_for('waiter_dashboard'))

    #         order.status = new_status
    #         order.updated_at = datetime.utcnow().replace(microsecond=0)
    #         db.session.commit()

    #         flash('Order status updated successfully', 'success')
    #         return redirect(url_for('waiter_dashboard'))

    #     return render_template('order_status.html', order=order)

    # @app.route('/cook/dashboard')
    # @login_required
    # def cook_dashboard():
    #     if current_user.role != 'повар':
    #         flash('You are not authorized to access this page', 'danger')
    #         return redirect(url_for('home'))
    #     orders = Order.query.filter(
    #         Order.status.in_(['принят', 'готовится'])).all()
    #     order_items = {order.id: OrderItem.query.filter_by(
    #         order_id=order.id).all() for order in orders}
    #     return render_template('cook_dashboard.html', orders=orders, order_items=order_items)

    # @app.route('/cook/shifts')
    # @login_required
    # def cook_shifts():
    #     return render_template('cook_shifts.html', shifts=current_user.shifts)

    # @app.route('/cook/orders/<int:order_id>/update_status', methods=['GET', 'POST'])
    # @login_required
    # def cook_update_order_status(order_id):
    #     order = Order.query.get_or_404(order_id)
    #     if current_user.role != 'повар':
    #         flash('You are not authorized to update this order', 'danger')
    #         return redirect(url_for('cook_dashboard'))

    #     if request.method == 'POST':
    #         new_status = request.form.get('status')
    #         if new_status not in ['готовится', 'готов']:
    #             flash('Invalid status', 'danger')
    #             return redirect(url_for('cook_dashboard'))

    #         order.status = new_status
    #         order.updated_at = datetime.utcnow().replace(microsecond=0)
    #         db.session.commit()

    #         flash('Order status updated successfully', 'success')
    #         return redirect(url_for('cook_dashboard'))

    #     return render_template('cook_update_order_status.html', order=order)

    return "contents of the routes.py file"
