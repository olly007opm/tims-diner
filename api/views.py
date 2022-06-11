from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from api.models import Table, Item, Category, Order
from api.app import db

views = Blueprint('views', __name__)


# Home page
@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("index.html", current_user=current_user, page="home")
    else:
        return redirect(url_for('auth.login'))


# Example page
@login_required
@views.route('/example')
def example_page():
    return render_template("example.html", current_user=current_user, page="example")


# Tables page
@login_required
@views.route('/tables')
def tables():
    tables = Table.query.all()
    return render_template("table/tables.html", current_user=current_user, page="tables", tables=tables)


# Add table page
@login_required
@views.route('/addtable', methods=['GET', 'POST'])
def addtable():
    if request.method == 'POST':
        # Get fields from form
        seats = request.form.get('seats')
        new_table = Table(seats=seats)
        db.session.add(new_table)
        db.session.commit()
        flash('Table created successfully.', category='success')
        return redirect(url_for('views.tables'))

    return render_template("table/addtable.html", current_user=current_user, page="addtable")


# Edit table page
@login_required
@views.route('/edittable/<tableid>', methods=['GET', 'POST'])
def edittable(tableid):
    table = Table.query.filter_by(id=tableid).first()
    if not table:
        flash('Table does not exist.', category='danger')
        return redirect(url_for('views.tables'))

    if request.method == 'POST':
        # Get fields from form
        seats = request.form.get('seats')
        table.seats = seats
        db.session.add(table)
        db.session.commit()
        flash('Table updated successfully.', category='success')
        return redirect(url_for('views.tables'))

    return render_template("table/edittable.html", current_user=current_user, page="edittable", table=table)


# Delete table page
@login_required
@views.route('/deletetable/<tableid>')
def deletetable(tableid):
    table = Table.query.filter_by(id=tableid).first()
    if not table:
        flash('Table does not exist.', category='danger')
        return redirect(url_for('views.tables'))
    db.session.delete(table)
    db.session.commit()
    flash('Table deleted successfully.', category='success')
    return redirect(url_for('views.tables'))


# Menu page
@login_required
@views.route('/menu')
def menu():
    items = Item.query.all()
    categories = Category.query.all()
    return render_template("item/items.html", current_user=current_user, page="menu", items=items,
                           categories=categories)


# Add item page
@login_required
@views.route('/additem', methods=['GET', 'POST'])
def additem():
    categories = Category.query.all()
    if request.method == 'POST':
        # Get fields from form
        name = request.form.get('name')
        icon = request.form.get('icon')
        category = request.form.get('category')
        price = request.form.get('price')
        new_item = Item(name=name, price=price, icon=icon, orders=0, category=category)
        db.session.add(new_item)
        db.session.commit()
        flash('Item created successfully.', category='success')
        return redirect(url_for('views.menu'))

    return render_template("item/additem.html", current_user=current_user, page="additem", categories=categories)


# Edit item page
@login_required
@views.route('/edititem/<itemid>', methods=['GET', 'POST'])
def edititem(itemid):
    item = Item.query.filter_by(id=itemid).first()
    categories = Category.query.all()
    if not item:
        flash('Item does not exist.', category='danger')
        return redirect(url_for('views.items'))

    if request.method == 'POST':
        # Get fields from form
        name = request.form.get('name')
        icon = request.form.get('icon')
        category = request.form.get('category')
        price = request.form.get('price')
        item.name = name
        item.icon = icon
        item.category = category
        item.price = price
        db.session.add(item)
        db.session.commit()
        flash('Item updated successfully.', category='success')
        return redirect(url_for('views.menu'))

    return render_template("item/edititem.html", current_user=current_user, page="edititem", item=item,
                           categories=categories)


# Delete item page
@login_required
@views.route('/deleteitem/<itemid>')
def deleteitem(itemid):
    item = Item.query.filter_by(id=itemid).first()
    if not item:
        flash('Item does not exist.', category='danger')
        return redirect(url_for('views.items'))
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', category='success')
    return redirect(url_for('views.menu'))


# Category page
@login_required
@views.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template("item/categories.html", current_user=current_user, page="categories", categories=categories)


# Add category page
@login_required
@views.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == 'POST':
        # Get fields from form
        name = request.form.get('name')
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category created successfully.', category='success')
        return redirect(url_for('views.categories'))

    return render_template("item/addcategory.html", current_user=current_user, page="addcategory")


# Edit category page
@login_required
@views.route('/editcategory/<categoryid>', methods=['GET', 'POST'])
def editcategory(categoryid):
    category = Category.query.filter_by(id=categoryid).first()
    if not category:
        flash('Category does not exist.', category='danger')
        return redirect(url_for('views.categories'))

    if request.method == 'POST':
        # Get fields from form
        name = request.form.get('name')
        category.name = name
        db.session.add(category)
        db.session.commit()
        flash('Category updated successfully.', category='success')
        return redirect(url_for('views.categories'))

    return render_template("item/editcategory.html", current_user=current_user, page="editcategory", category=category)


# Delete category page
@login_required
@views.route('/deletecategory/<categoryid>')
def deletecategory(categoryid):
    category = Category.query.filter_by(id=categoryid).first()
    if not category:
        flash('Category does not exist.', category='danger')
        return redirect(url_for('views.categories'))
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', category='success')
    return redirect(url_for('views.categories'))


# Order page
@login_required
@views.route('/orders')
def orders():
    items = {}
    for item in Item.query.all():
        items[item.id] = item
    return render_template("orders/orders.html", current_user=current_user, page="orders", orders=Order.query.all(),
                           items=items, categories=Category.query.all())


# Add order page
@login_required
@views.route('/neworder', methods=['GET', 'POST'])
def neworder():
    items = Item.query.all()
    categories = Category.query.all()
    tables = Table.query.all()
    if request.method == 'POST':
        # Get fields from form
        table = request.form.get('table')
        order_items = {}
        for item in items:
            id = item.id
            quantity = int(request.form.get(f'item-{id}'))
            if quantity:
                order_items[id] = quantity

        new_order = Order(table=table, items=order_items, total=calculate_total(order_items))
        db.session.add(new_order)
        db.session.commit()
        flash('Order created successfully.', category='success')
        return redirect(url_for('views.orders'))

    return render_template("orders/neworder.html", current_user=current_user, page="addorder", items=items,
                           tables=tables, categories=categories)


# Edit order page
@login_required
@views.route('/editorder/<orderid>', methods=['GET', 'POST'])
def editorder(orderid):
    order = Order.query.filter_by(id=orderid).first()
    items = Item.query.all()
    categories = Category.query.all()
    tables = Table.query.all()
    if not order:
        flash('Order does not exist.', category='danger')
        return redirect(url_for('views.orders'))

    if request.method == 'POST':
        # Get fields from form
        table = request.form.get('table')
        order_items = {}
        for item in items:
            id = item.id
            quantity = int(request.form.get(f'item-{id}'))
            if quantity:
                order_items[id] = quantity

        order.table = table
        order.items = order_items
        order.total = calculate_total(order_items)
        db.session.add(order)
        db.session.commit()
        flash('Order updated successfully.', category='success')
        return redirect(url_for('views.orders'))

    return render_template("orders/editorder.html", current_user=current_user, page="editorder", order=order,
                           items=items, tables=tables, categories=categories)


# Delete order page
@login_required
@views.route('/deleteorder/<orderid>')
def deleteorder(orderid):
    order = Order.query.filter_by(id=orderid).first()
    if not order:
        flash('Order does not exist.', category='danger')
        return redirect(url_for('views.orders'))
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully.', category='success')
    return redirect(url_for('views.orders'))


# Print order page
@login_required
@views.route('/printorder/<orderid>')
def printorder(orderid):
    order = Order.query.filter_by(id=orderid).first()
    items = {}
    for item in Item.query.all():
        items[item.id] = item
    if not order:
        flash('Order does not exist.', category='danger')
        return redirect(url_for('views.orders'))

    return render_template("orders/printorder.html", current_user=current_user, page="editorder", order=order,
                           items=items, tables=Table.query.all(), categories=Category.query.all())


def calculate_total(order_items):
    total = 0
    for order_item in order_items:
        id = order_item
        quantity = order_items[id]
        price = Item.query.filter_by(id=id).first().price
        total += price * quantity
    return total


# ──────────────────────────────────────── CODE SNIPPETS ────────────────────────────────────────
# ──────────────────── GENERAL ────────────────────
# Redirect to page                                              redirect(url_for('views.page'))
# Requires login decorator (redirects to 403 page)              @login_required
# Check if current user is authenticated                        if current_user.is_authenticated:
# Route with parameters                                         @views.route('/withparams/<param>')
#                                                               def paramroute(param):
# Cancel request with error code (in this case 403)             abort(403)

# ──────────────────── DATABASE ────────────────────
# Get all records                                               Table.query.all()
# Query a table with filter options and return first match      Table.query.filter_by( <QUERY OPTIONS> ).first()
#                                                                   <QUERY OPTIONS> id=123 name='test'
# Query a table and sort by descending id (last record first)   Table.query.order_by(Table.id.desc())
# Get a linked record from a user                               current_user.linkedtable
# Create a new record                                           new_record = Record(field=data, field2=data2)
# Update a record                                               new_record.field3 = data3
# Delete a record                                               db.session.delete(new_record)
# Add a record to the database                                  db.session.add(new_record)
# Commit changes (done after all operations are complete)       db.session.commit()

# ──────────────────── REQUESTS ────────────────────
# Route with both GET and POST methods                          @views.route('/path', methods=['GET', 'POST'])
# Check if request method is post                               if request.method == 'POST':
# Get data from form for regular inputs                         request.form.get('input name')
# Get data from form for common input names                     request.form.getlist('common input name')

# ──────────────────── FLASHING MESSAGES ────────────────────
# Flash a normal message                                        flash('Flashed message content')
# Flash a message with a category                               flash('Flashed message content', category='success')

# ──────────────────── TEMPLATE SNIPPETS (FOR USE IN .html TEMPLATE FILES) ────────────────────
# Link a static file                                            {{ url_for('static', filename='path/to/file.txt') }}

# Flashed messages without categories:
#       {% with messages = get_flashed_messages() %}
#           {% if messages %}
#               {% for message in messages %}
#                   <div class="alert mb-10" role="alert">
#                       <button class="close" data-dismiss="alert" type="button" aria-label="Close">
#                           <span aria-hidden="true">&times;</span>
#                       </button>
#                       {{ message }}
#                   </div>
#               {% endfor %}
#           {% endif %}
#       {% endwith %}

# Flashed messages with categories:
#       {% with messages = get_flashed_messages(with_categories=true) %}
#           {% if messages %}
#               {% for category, message in messages %}
#                   <div class="alert alert-{{ category }} mb-10" role="alert">
#                       <button class="close" data-dismiss="alert" type="button" aria-label="Close">
#                           <span aria-hidden="true">&times;</span>
#                       </button>
#                       {{ message }}
#                   </div>
#               {% endfor %}
#           {% endif %}
#       {% endwith %}
