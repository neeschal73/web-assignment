from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import current_user, login_required
from app.models import db, Book, Category, Order, OrderItem, Review
from app.forms import ReviewForm, ContactForm

"""
Main Blueprint
Handles main website pages: home, books, book details, shopping cart, and orders
"""

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """
    Home page route
    Displays featured books and categories
    """
    # Get featured books (limit to 8)
    featured_books = Book.query.order_by(Book.created_at.desc()).limit(8).all()
    # Get all categories
    categories = Category.query.all()
    
    return render_template('main/home.html', 
                         featured_books=featured_books, 
                         categories=categories)


@main_bp.route('/books')
def books():
    """
    Books listing page route
    Displays all books with pagination and filtering
    """
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', 0, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Book.query
    
    # Filter by category if specified
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Search by title or author
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%'))
        )
    
    # Paginate results (12 books per page)
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    books = pagination.items
    categories = Category.query.all()
    
    return render_template('main/books.html',
                         books=books,
                         pagination=pagination,
                         categories=categories,
                         search=search,
                         category_id=category_id)


@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Book detail page route
    Displays book information and reviews
    """
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).all()
    form = ReviewForm()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    
    return render_template('main/book_detail.html',
                         book=book,
                         reviews=reviews,
                         avg_rating=avg_rating,
                         form=form)


@main_bp.route('/book/<int:book_id>/review', methods=['POST'])
@login_required
def add_review(book_id):
    """
    Add review to book
    """
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if user already reviewed this book
        existing_review = Review.query.filter_by(
            user_id=current_user.id,
            book_id=book_id
        ).first()
        
        if existing_review:
            flash('You have already reviewed this book.', 'warning')
            return redirect(url_for('main.book_detail', book_id=book_id))
        
        # Create new review
        review = Review(
            user_id=current_user.id,
            book_id=book_id,
            rating=form.rating.data,
            title=form.title.data,
            content=form.content.data
        )
        
        db.session.add(review)
        try:
            db.session.commit()
            flash('Your review has been posted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while posting your review. Please try again.', 'danger')
    
    return redirect(url_for('main.book_detail', book_id=book_id))


@main_bp.route('/cart')
def view_cart():
    """
    View shopping cart
    """
    cart = session.get('cart', {})
    books = []
    total_price = 0
    
    if not cart:
        return render_template('main/cart.html', books=[], total_price=0)
    
    for book_id, quantity in cart.items():
        book = Book.query.get(book_id)
        if book:
            item_total = book.price * quantity
            books.append({
                'book': book,
                'quantity': quantity,
                'item_total': item_total
            })
            total_price += item_total
    
    return render_template('main/cart.html', books=books, total_price=total_price)


@main_bp.route('/cart/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    """
    Add book to shopping cart
    """
    book = Book.query.get_or_404(book_id)
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    if str(book_id) in cart:
        cart[str(book_id)] += 1
    else:
        cart[str(book_id)] = 1
    
    session.modified = True
    flash(f'"{book.title}" added to cart!', 'success')
    return redirect(request.referrer or url_for('main.books'))


@main_bp.route('/cart/remove/<int:book_id>', methods=['POST'])
def remove_from_cart(book_id):
    """
    Remove book from shopping cart
    """
    if 'cart' in session and str(book_id) in session['cart']:
        del session['cart'][str(book_id)]
        session.modified = True
        flash('Item removed from cart.', 'info')
    
    return redirect(url_for('main.view_cart'))


@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """
    Checkout and place order
    """
    cart = session.get('cart', {})
    
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.books'))
    
    if request.method == 'POST':
        # Calculate total price
        total_price = 0
        order_items = []
        
        for book_id, quantity in cart.items():
            book = Book.query.get(book_id)
            if book:
                total_price += book.price * quantity
                order_items.append({
                    'book_id': book_id,
                    'quantity': quantity,
                    'price': book.price
                })
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_price=total_price,
            status='Pending',
            shipping_address=current_user.address,
            shipping_city=current_user.city,
            shipping_postal=current_user.postal_code
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID without committing
        
        # Add order items
        for item in order_items:
            book = Book.query.get(item['book_id'])
            if book and book.stock >= item['quantity']:
                order_item = OrderItem(
                    order_id=order.id,
                    book_id=item['book_id'],
                    quantity=item['quantity'],
                    price_at_purchase=item['price']
                )
                book.stock -= item['quantity']
                db.session.add(order_item)
            else:
                db.session.rollback()
                flash(f'Insufficient stock for {book.title if book else "this book"}.', 'danger')
                return redirect(url_for('main.view_cart'))
        
        try:
            db.session.commit()
            session['cart'] = {}
            session.modified = True
            flash('Order placed successfully!', 'success')
            return redirect(url_for('main.order_detail', order_id=order.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while placing your order. Please try again.', 'danger')
            return redirect(url_for('main.view_cart'))
    
    # Calculate cart total
    total_price = 0
    for book_id, quantity in cart.items():
        book = Book.query.get(book_id)
        if book:
            total_price += book.price * quantity
    
    return render_template('main/checkout.html', total_price=total_price)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard
    """
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('main/dashboard.html', orders=orders)


@main_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """
    View order details
    """
    order = Order.query.get_or_404(order_id)
    
    # Check if order belongs to current user
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/order_detail.html', order=order)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact page with form
    """
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email here
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('main/contact.html', form=form)
