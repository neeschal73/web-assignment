from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from app.models import db, Book, Category, Order, User, Review
from functools import wraps

"""
Admin Blueprint
Handles admin panel functionality: manage books, categories, orders, and users
"""

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """
    Admin dashboard with statistics
    """
    total_users = User.query.count()
    total_books = Book.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Low stock books
    low_stock_books = Book.query.filter(Book.stock < 5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_books=total_books,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         low_stock_books=low_stock_books)


@admin_bp.route('/books')
@login_required
@admin_required
def manage_books():
    """
    Manage books
    """
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/manage_books.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    """
    Add new book
    """
    categories = Category.query.all()
    
    if request.method == 'POST':
        # Validate form data
        if not request.form.get('title') or not request.form.get('author'):
            flash('Title and author are required.', 'danger')
            return render_template('admin/add_book.html', categories=categories)
        
        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            isbn=request.form.get('isbn'),
            description=request.form.get('description'),
            price=float(request.form.get('price', 0)),
            stock=int(request.form.get('stock', 0)),
            category_id=int(request.form.get('category_id')),
            publisher=request.form.get('publisher'),
            publication_year=int(request.form.get('publication_year', 2024)) if request.form.get('publication_year') else 2024,
            pages=int(request.form.get('pages', 0)) if request.form.get('pages') else 0,
            language=request.form.get('language', 'English')
        )
        
        db.session.add(book)
        try:
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('admin.manage_books'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the book. Please try again.', 'danger')
    
    return render_template('admin/add_book.html', categories=categories)


@admin_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    """
    Edit book
    """
    book = Book.query.get_or_404(book_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        book.title = request.form.get('title', book.title)
        book.author = request.form.get('author', book.author)
        book.isbn = request.form.get('isbn', book.isbn)
        book.description = request.form.get('description', book.description)
        book.price = float(request.form.get('price', book.price))
        book.stock = int(request.form.get('stock', book.stock))
        book.category_id = int(request.form.get('category_id', book.category_id))
        book.publisher = request.form.get('publisher', book.publisher)
        book.publication_year = int(request.form.get('publication_year', book.publication_year)) if request.form.get('publication_year') else book.publication_year
        book.pages = int(request.form.get('pages', book.pages)) if request.form.get('pages') else book.pages
        book.language = request.form.get('language', book.language)
        
        try:
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('admin.manage_books'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the book. Please try again.', 'danger')
    
    return render_template('admin/edit_book.html', book=book, categories=categories)


@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    """
    Delete book
    """
    book = Book.query.get_or_404(book_id)
    
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the book. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_books'))


@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    """
    Manage categories
    """
    categories = Category.query.all()
    return render_template('admin/manage_categories.html', categories=categories)


@admin_bp.route('/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    """
    Add new category
    """
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Category name is required.', 'danger')
        return redirect(url_for('admin.manage_categories'))
    
    # Check if category already exists
    if Category.query.filter_by(name=name).first():
        flash('Category already exists.', 'warning')
        return redirect(url_for('admin.manage_categories'))
    
    category = Category(name=name, description=description)
    db.session.add(category)
    
    try:
        db.session.commit()
        flash('Category added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the category. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(cat_id):
    """
    Delete category
    """
    category = Category.query.get_or_404(cat_id)
    
    # Check if category has books
    if category.books:
        flash('Cannot delete category with existing books.', 'warning')
        return redirect(url_for('admin.manage_categories'))
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the category. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    """
    Manage orders
    """
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/manage_orders.html', orders=orders)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """
    Update order status
    """
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status', order.status)
    
    if status not in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin.manage_orders'))
    
    order.status = status
    try:
        db.session.commit()
        flash(f'Order status updated to {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the order status. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_orders'))


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """
    Manage users
    """
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/manage_users.html', users=users)


@admin_bp.route('/users/<int:user_id>/admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """
    Toggle admin status
    """
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'warning')
        return redirect(url_for('admin.manage_users'))
    
    user.is_admin = not user.is_admin
    try:
        db.session.commit()
        flash(f'User admin status updated.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating user status. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_users'))
