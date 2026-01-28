# Online Bookstore - E-Commerce Website

A fully functional, responsive online bookstore platform built with Flask, Bootstrap, and SQLAlchemy. Features user authentication, shopping cart, order management, and an admin panel for inventory control.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### User Features
- ✅ User Registration and Account Creation
- ✅ Secure Login/Logout with Password Hashing
- ✅ Browse Books with Pagination
- ✅ Search Books by Title/Author
- ✅ Filter Books by Category
- ✅ View Detailed Book Information
- ✅ Shopping Cart Management
- ✅ Secure Checkout
- ✅ Order History and Tracking
- ✅ Book Reviews and Ratings (1-5 stars)
- ✅ User Profile Management
- ✅ Contact Form

### Admin Features
- ✅ Admin Dashboard with Statistics
- ✅ Manage Books (Add, Edit, Delete)
- ✅ Manage Categories
- ✅ View and Update Orders
- ✅ Manage Users and Admin Privileges
- ✅ Low Stock Alerts
- ✅ Sales Analytics

### Technical Features
- ✅ Responsive Design (Mobile, Tablet, Desktop)
- ✅ Client & Server-side Form Validation
- ✅ Session Management
- ✅ User Authentication & Authorization
- ✅ CRUD Operations
- ✅ Database Relationships (1:N, M:N)
- ✅ Flash Messages & Error Handling
- ✅ SEO-friendly URLs

## 🛠 Tech Stack

### Frontend
- HTML5 (Semantic)
- CSS3 with Bootstrap 5
- JavaScript with client-side validation
- Bootstrap Icons
- Responsive Grid & Components

### Backend
- Python 3.8+
- Flask Web Framework
- Flask-Login (Session Management)
- Flask-SQLAlchemy (ORM)
- Flask-WTF (Form Handling)
- Jinja2 (Template Engine)
- Werkzeug (Security)

### Database
- SQLite (Development)
- Supports PostgreSQL/MySQL (Production)

### Tools & Libraries
- Git (Version Control)
- Pip (Package Management)
- Virtual Environment

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/online-bookstore.git
   cd online-bookstore
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables (Optional)**
   ```bash
   # Create .env file (optional)
   export FLASK_ENV=development
   export FLASK_APP=run.py
   ```

5. **Run the Application**
   ```bash
   python run.py
   ```

6. **Access the Application**
   - Open your browser
   - Navigate to: `http://localhost:5000`

## 🚀 Usage

### First Time Setup
1. The application will automatically create the database and sample data on first run
2. Admin account is created with:
   - **Email:** admin@bookstore.com
   - **Password:** admin123

### User Registration
1. Click "Register" in the navigation bar
2. Fill in the registration form
3. Click "Register"
4. Login with your new credentials

### Browsing Books
1. Navigate to "Books" page
2. Use search bar to find books
3. Filter by category using the sidebar
4. Paginate through results

### Shopping
1. Click "View Details" on a book
2. Click "Add to Cart"
3. View cart by clicking "Cart" in navigation
4. Proceed to checkout
5. Confirm order

### Writing Reviews
1. Login to your account
2. Go to book details
3. Scroll to reviews section
4. Fill in the review form
5. Submit (one review per book per user)

### Admin Access
1. Login with admin credentials
2. Click on your name dropdown
3. Select "Admin Panel"
4. Access management features

## 📁 Project Structure

```
online-bookstore/
├── app/
│   ├── templates/
│   │   ├── base.html (Base template)
│   │   ├── main/
│   │   │   ├── home.html
│   │   │   ├── books.html
│   │   │   ├── book_detail.html
│   │   │   ├── cart.html
│   │   │   ├── checkout.html
│   │   │   ├── dashboard.html
│   │   │   ├── order_detail.html
│   │   │   └── contact.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── profile.html
│   │   │   └── edit_profile.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── manage_books.html
│   │   │   ├── add_book.html
│   │   │   ├── edit_book.html
│   │   │   ├── manage_categories.html
│   │   │   ├── manage_orders.html
│   │   │   └── manage_users.html
│   │   └── errors/
│   │       ├── 404.html
│   │       ├── 500.html
│   │       └── 403.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css (Custom styles)
│   │   ├── js/
│   │   │   └── main.js (Client-side scripts)
│   │   ├── images/
│   │   └── uploads/ (User uploads)
│   ├── __init__.py (App factory)
│   ├── models.py (Database models)
│   ├── forms.py (WTForms)
│   ├── auth.py (Login manager)
│   ├── routes_auth.py (Auth routes)
│   ├── routes_main.py (Main routes)
│   └── routes_admin.py (Admin routes)
├── run.py (Entry point)
├── config.py (Configuration)
├── requirements.txt (Dependencies)
├── .gitignore (Git ignore rules)
├── bookstore.db (Database - auto-created)
└── documentation/
    ├── PROJECT_PROPOSAL.md
    ├── DATABASE_DESIGN.md
    ├── INSTALLATION_GUIDE.md
    └── USER_MANUAL.md
```

## 🗄 Database Schema

### Tables:
1. **User** - User accounts and authentication
2. **Book** - Book inventory
3. **Category** - Book categories
4. **Order** - Customer orders
5. **OrderItem** - Order line items (M:N join)
6. **Review** - User book reviews

See [DATABASE_DESIGN.md](documentation/DATABASE_DESIGN.md) for detailed schema.

## 📡 API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /books` - Browse books
- `GET /book/<id>` - Book details
- `GET /contact` - Contact form
- `GET /auth/register` - Registration page
- `GET /auth/login` - Login page

### Authenticated Routes (Login Required)
- `GET /auth/logout` - Logout
- `GET /auth/profile` - View profile
- `GET /auth/profile/edit` - Edit profile
- `GET /dashboard` - User dashboard
- `GET /order/<id>` - Order details
- `POST /cart/add/<book_id>` - Add to cart
- `POST /cart/remove/<book_id>` - Remove from cart
- `GET /cart` - View cart
- `POST /checkout` - Place order
- `POST /book/<book_id>/review` - Add review

### Admin Routes (Admin Required)
- `GET /admin/` - Admin dashboard
- `GET /admin/books` - Manage books
- `POST /admin/books/add` - Add book
- `POST /admin/books/<id>/edit` - Edit book
- `POST /admin/books/<id>/delete` - Delete book
- `GET /admin/categories` - Manage categories
- `POST /admin/categories/add` - Add category
- `POST /admin/categories/<id>/delete` - Delete category
- `GET /admin/orders` - Manage orders
- `POST /admin/orders/<id>/status` - Update order status
- `GET /admin/users` - Manage users
- `POST /admin/users/<id>/admin` - Toggle admin status

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration with validation
- [ ] User login/logout
- [ ] Browse books and search
- [ ] Filter by category
- [ ] Add/remove from cart
- [ ] Checkout process
- [ ] Order history
- [ ] Write reviews
- [ ] Admin dashboard access
- [ ] Book management (CRUD)
- [ ] Order status updates
- [ ] Responsive design (mobile, tablet)
- [ ] Form validation
- [ ] Error handling

### Browser Compatibility
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## 📸 Screenshots

### Home Page
- Hero section with call-to-action
- Featured books carousel
- Category section
- Features overview

### Books Listing
- Search and filter options
- Book cards with pricing
- Pagination controls
- Category sidebar

### Admin Dashboard
- Sales statistics
- Low stock alerts
- Recent orders
- Quick action buttons

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications
- [ ] Advanced recommendation engine
- [ ] Wishlist feature
- [ ] Social media integration
- [ ] Real-time notifications
- [ ] API documentation (Swagger)
- [ ] Unit and integration tests
- [ ] CI/CD pipeline
- [ ] Multi-language support
- [ ] Mobile app (React Native/Flutter)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, email support@bookstore.com or open an issue on GitHub.

## 👥 Authors

- **Developer:** Your Name
- **Course:** Web Development Project
- **Submission Date:** January 28, 2024

## 🙏 Acknowledgments

- Bootstrap framework for responsive design
- Flask documentation and community
- Bootstrap Icons for UI elements
- SQLAlchemy for ORM functionality

---

**Version:** 1.0.0  
**Last Updated:** January 28, 2024
