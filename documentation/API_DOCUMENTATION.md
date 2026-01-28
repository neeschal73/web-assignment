# API Documentation - Online Bookstore

## Base URL
```
http://localhost:5000
```

## Authentication
Most endpoints require user authentication. Include session cookies or authentication tokens with requests.

---

## Authentication Endpoints

### 1. User Registration
**Endpoint**: `POST /register`

**Description**: Create a new user account

**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response** (200 OK):
```json
{
  "message": "Registration successful! Please log in.",
  "redirect": "/login"
}
```

**Response** (400 Bad Request):
```json
{
  "errors": {
    "username": ["Username already exists"],
    "email": ["Email already registered"]
  }
}
```

---

### 2. User Login
**Endpoint**: `POST /login`

**Description**: Authenticate user and create session

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securepassword123",
  "remember_me": true
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful!",
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_admin": false
}
```

**Response** (401 Unauthorized):
```json
{
  "error": "Invalid email or password"
}
```

---

### 3. User Logout
**Endpoint**: `GET /logout`

**Description**: Clear user session and log out

**Authentication**: Required

**Response** (200 OK):
```json
{
  "message": "You have been logged out successfully."
}
```

---

## User Profile Endpoints

### 4. Get User Profile
**Endpoint**: `GET /profile`

**Description**: Retrieve current user's profile information

**Authentication**: Required

**Response** (200 OK):
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone": "555-1234",
  "address": "123 Main St",
  "city": "Springfield",
  "postal_code": "12345",
  "member_since": "2024-01-15",
  "total_orders": 5,
  "total_spent": 299.99
}
```

---

### 5. Update User Profile
**Endpoint**: `POST /profile/edit`

**Description**: Update user profile information

**Authentication**: Required

**Request Body**:
```json
{
  "full_name": "John Doe Updated",
  "email": "newemail@example.com",
  "phone": "555-5678",
  "address": "456 Oak Ave",
  "city": "Shelbyville",
  "postal_code": "54321"
}
```

**Response** (200 OK):
```json
{
  "message": "Profile updated successfully",
  "user": {
    "user_id": 1,
    "full_name": "John Doe Updated",
    "email": "newemail@example.com",
    "phone": "555-5678",
    "address": "456 Oak Ave",
    "city": "Shelbyville",
    "postal_code": "54321"
  }
}
```

---

## Book Endpoints

### 6. Get All Books
**Endpoint**: `GET /books`

**Description**: Retrieve paginated list of books with filtering and search

**Query Parameters**:
- `page` (int, optional): Page number (default: 1)
- `per_page` (int, optional): Books per page (default: 12)
- `search` (string, optional): Search in title and author
- `category` (int, optional): Filter by category ID

**Response** (200 OK):
```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "price": 12.99,
      "stock": 25,
      "category": {
        "id": 1,
        "name": "Fiction"
      },
      "average_rating": 4.5,
      "review_count": 12,
      "description": "A novel of the Jazz Age..."
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 12,
    "total": 45,
    "pages": 4
  }
}
```

---

### 7. Get Book Details
**Endpoint**: `GET /book/<book_id>`

**Description**: Retrieve detailed information about a specific book

**Parameters**:
- `book_id` (int): Book ID

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0743273565",
  "price": 12.99,
  "stock": 25,
  "category": {
    "id": 1,
    "name": "Fiction"
  },
  "description": "A novel of the Jazz Age...",
  "publisher": "Scribner",
  "publication_year": 1925,
  "pages": 180,
  "language": "English",
  "average_rating": 4.5,
  "reviews": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "jane_doe"
      },
      "rating": 5,
      "title": "Excellent Classic",
      "content": "A masterpiece of American literature...",
      "created_at": "2024-01-20T10:30:00"
    }
  ]
}
```

---

## Review Endpoints

### 8. Add Book Review
**Endpoint**: `POST /book/<book_id>/review`

**Description**: Add or update a review for a book

**Authentication**: Required

**Parameters**:
- `book_id` (int): Book ID

**Request Body**:
```json
{
  "rating": 5,
  "title": "Excellent Book",
  "content": "This is a wonderful book that I highly recommend..."
}
```

**Response** (201 Created):
```json
{
  "message": "Review added successfully",
  "review": {
    "id": 5,
    "book_id": 1,
    "user_id": 1,
    "rating": 5,
    "title": "Excellent Book",
    "content": "This is a wonderful book...",
    "created_at": "2024-01-25T15:45:00"
  }
}
```

**Response** (400 Bad Request):
```json
{
  "errors": {
    "rating": ["Rating must be between 1 and 5"],
    "content": ["Review must be at least 10 characters"]
  }
}
```

---

## Shopping Cart Endpoints

### 9. Get Shopping Cart
**Endpoint**: `GET /cart`

**Description**: Retrieve current user's shopping cart

**Authentication**: Required

**Response** (200 OK):
```json
{
  "cart": [
    {
      "book_id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "price": 12.99,
      "quantity": 2,
      "subtotal": 25.98
    },
    {
      "book_id": 3,
      "title": "1984",
      "author": "George Orwell",
      "price": 13.99,
      "quantity": 1,
      "subtotal": 13.99
    }
  ],
  "total": 39.97,
  "item_count": 3
}
```

---

### 10. Add to Cart
**Endpoint**: `POST /cart/add/<book_id>`

**Description**: Add a book to shopping cart

**Authentication**: Required

**Parameters**:
- `book_id` (int): Book ID to add

**Request Body**:
```json
{
  "quantity": 1
}
```

**Response** (200 OK):
```json
{
  "message": "Added to cart successfully",
  "cart_total": 39.97,
  "item_count": 3
}
```

**Response** (400 Bad Request):
```json
{
  "error": "Insufficient stock available. Only 5 copies available."
}
```

---

### 11. Remove from Cart
**Endpoint**: `POST /cart/remove/<book_id>`

**Description**: Remove a book from shopping cart

**Authentication**: Required

**Parameters**:
- `book_id` (int): Book ID to remove

**Response** (200 OK):
```json
{
  "message": "Removed from cart successfully",
  "cart_total": 25.98,
  "item_count": 2
}
```

---

## Order Endpoints

### 12. Checkout
**Endpoint**: `POST /checkout`

**Description**: Place an order with items in shopping cart

**Authentication**: Required

**Request Body**:
```json
{
  "shipping_address": "123 Main St",
  "shipping_city": "Springfield",
  "shipping_postal": "12345"
}
```

**Response** (201 Created):
```json
{
  "message": "Order placed successfully",
  "order": {
    "id": 15,
    "order_number": "ORD-20240125-001",
    "total_price": 39.97,
    "status": "Pending",
    "created_at": "2024-01-25T16:30:00",
    "items": [
      {
        "book_id": 1,
        "title": "The Great Gatsby",
        "quantity": 2,
        "price_at_purchase": 12.99
      }
    ]
  }
}
```

---

### 13. Get User Orders
**Endpoint**: `GET /dashboard`

**Description**: Retrieve all orders for current user

**Authentication**: Required

**Query Parameters**:
- `page` (int, optional): Page number (default: 1)

**Response** (200 OK):
```json
{
  "orders": [
    {
      "id": 15,
      "order_number": "ORD-20240125-001",
      "total_price": 39.97,
      "status": "Shipped",
      "created_at": "2024-01-25T16:30:00",
      "item_count": 3
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 5,
    "pages": 1
  }
}
```

---

### 14. Get Order Details
**Endpoint**: `GET /order/<order_id>`

**Description**: Retrieve detailed information about a specific order

**Authentication**: Required

**Parameters**:
- `order_id` (int): Order ID

**Response** (200 OK):
```json
{
  "order": {
    "id": 15,
    "order_number": "ORD-20240125-001",
    "total_price": 39.97,
    "status": "Shipped",
    "shipping_address": "123 Main St",
    "shipping_city": "Springfield",
    "shipping_postal": "12345",
    "created_at": "2024-01-25T16:30:00",
    "updated_at": "2024-01-26T10:15:00",
    "items": [
      {
        "id": 1,
        "book": {
          "id": 1,
          "title": "The Great Gatsby",
          "author": "F. Scott Fitzgerald",
          "isbn": "978-0743273565"
        },
        "quantity": 2,
        "price_at_purchase": 12.99,
        "subtotal": 25.98
      }
    ]
  }
}
```

---

## Admin Endpoints

### 15. Admin Dashboard
**Endpoint**: `GET /admin/`

**Description**: Get admin dashboard with statistics

**Authentication**: Required (Admin only)

**Response** (200 OK):
```json
{
  "total_users": 150,
  "total_orders": 450,
  "total_revenue": 15234.50,
  "total_books": 250,
  "low_stock_books": [
    {
      "id": 5,
      "title": "Popular Book",
      "stock": 2
    }
  ],
  "recent_orders": [
    {
      "id": 15,
      "order_number": "ORD-20240125-001",
      "total_price": 39.97,
      "status": "Pending",
      "created_at": "2024-01-25T16:30:00"
    }
  ]
}
```

---

### 16. Add Book (Admin)
**Endpoint**: `POST /admin/books/add`

**Description**: Add a new book to the catalog

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "title": "New Book",
  "author": "Author Name",
  "isbn": "978-1234567890",
  "description": "Book description...",
  "price": 24.99,
  "stock": 50,
  "category_id": 1,
  "publisher": "Publisher Name",
  "publication_year": 2024,
  "pages": 300,
  "language": "English"
}
```

**Response** (201 Created):
```json
{
  "message": "Book added successfully",
  "book": {
    "id": 251,
    "title": "New Book",
    "author": "Author Name",
    "isbn": "978-1234567890",
    "price": 24.99,
    "stock": 50
  }
}
```

---

### 17. Update Book (Admin)
**Endpoint**: `POST /admin/books/edit/<book_id>`

**Description**: Update book information

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "title": "Updated Title",
  "price": 22.99,
  "stock": 45
}
```

**Response** (200 OK):
```json
{
  "message": "Book updated successfully",
  "book": {
    "id": 1,
    "title": "Updated Title",
    "price": 22.99,
    "stock": 45
  }
}
```

---

### 18. Delete Book (Admin)
**Endpoint**: `POST /admin/books/delete/<book_id>`

**Description**: Delete a book from catalog

**Authentication**: Required (Admin only)

**Response** (200 OK):
```json
{
  "message": "Book deleted successfully"
}
```

---

### 19. Manage Orders (Admin)
**Endpoint**: `GET /admin/orders`

**Description**: Get all orders for admin management

**Authentication**: Required (Admin only)

**Query Parameters**:
- `status` (string, optional): Filter by order status
- `page` (int, optional): Page number (default: 1)

**Response** (200 OK):
```json
{
  "orders": [
    {
      "id": 15,
      "order_number": "ORD-20240125-001",
      "customer": "john_doe",
      "total_price": 39.97,
      "status": "Pending",
      "created_at": "2024-01-25T16:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 450,
    "pages": 23
  }
}
```

---

### 20. Update Order Status (Admin)
**Endpoint**: `POST /admin/order/<order_id>/status`

**Description**: Update order status

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "status": "Shipped"
}
```

**Response** (200 OK):
```json
{
  "message": "Order status updated successfully",
  "order": {
    "id": 15,
    "status": "Shipped",
    "updated_at": "2024-01-25T17:00:00"
  }
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "Please log in to access this resource"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied",
  "message": "Admin access required for this operation"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "The requested book/order was not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred. Please try again later."
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## Rate Limiting

- **Login attempts**: Max 5 per minute per IP
- **Search queries**: Max 10 per minute per user
- **API calls**: Max 100 per minute per user

---

## Pagination

All list endpoints support pagination:

```json
{
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Query Parameters**:
- `page`: Current page (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

---

## Best Practices

1. **Always use HTTPS** in production
2. **Include proper error handling** in client code
3. **Implement request/response logging** for debugging
4. **Cache responses** when appropriate
5. **Validate input** before sending to API
6. **Handle authentication tokens** securely
7. **Implement exponential backoff** for retries
8. **Test endpoints** thoroughly before production

---

**Last Updated**: December 2024
**Version**: 1.0
**API Stability**: Stable
