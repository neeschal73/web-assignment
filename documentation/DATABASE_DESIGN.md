# Database Design Document

## Entity-Relationship (ER) Diagram

```
┌─────────────────┐
│     User        │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password_hash   │
│ full_name       │
│ phone           │
│ address         │
│ city            │
│ postal_code     │
│ is_admin        │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         ├─────────────┬─────────────┐
         │             │             │
    ┌────▼─────┐  ┌───▼──────┐ ┌───▼─────┐
    │  Order    │  │  Review  │ │  Other  │
    └───────────┘  └──────────┘ └─────────┘


┌──────────────────┐
│    Category      │
├──────────────────┤
│ id (PK)          │
│ name             │
│ description      │
│ created_at       │
└────────┬─────────┘
         │
         │ 1:N
         │
    ┌────▼──────┐
    │   Book     │
    └────────────┘


┌──────────────────┐
│      Book        │
├──────────────────┤
│ id (PK)          │
│ title            │
│ author           │
│ isbn             │
│ description      │
│ price            │
│ stock            │
│ category_id (FK) │
│ cover_image      │
│ publisher        │
│ publication_year │
│ pages            │
│ language         │
│ created_at       │
│ updated_at       │
└────┬──────┬──────┘
     │      │
     │ 1:N  │ 1:N
     │      │
┌────▼──┐ ┌─▼──────────┐
│Review │ │ OrderItem  │
└───────┘ └────────────┘


┌─────────────────┐
│     Order       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ total_price     │
│ status          │
│ shipping_addr   │
│ shipping_city   │
│ shipping_postal │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────▼──────────┐
    │  OrderItem     │
    │  (Join Table)  │
    └────────────────┘


┌──────────────────┐
│     Review       │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │
│ book_id (FK)     │
│ rating           │
│ title            │
│ content          │
│ created_at       │
│ updated_at       │
└──────────────────┘
```

---

## Database Schema

### Table 1: User
**Purpose:** Store user account information and authentication details

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | User unique identifier |
| username | String(80) | UNIQUE, NOT NULL | Username for login |
| email | String(120) | UNIQUE, NOT NULL, INDEX | Email address |
| password_hash | String(255) | NOT NULL | Hashed password (Werkzeug) |
| full_name | String(120) | NOT NULL | User's full name |
| phone | String(20) | | Phone number |
| address | String(255) | | Street address |
| city | String(100) | | City name |
| postal_code | String(20) | | Postal/ZIP code |
| is_admin | Boolean | DEFAULT False | Admin privilege flag |
| created_at | DateTime | DEFAULT CURRENT | Account creation timestamp |
| updated_at | DateTime | DEFAULT CURRENT | Last update timestamp |

**Relationships:**
- 1:N with Order (user_id foreign key in Order)
- 1:N with Review (user_id foreign key in Review)

---

### Table 2: Category
**Purpose:** Organize books into categories for browsing and filtering

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Category unique identifier |
| name | String(100) | UNIQUE, NOT NULL, INDEX | Category name |
| description | Text | | Category description |
| created_at | DateTime | DEFAULT CURRENT | Creation timestamp |

**Relationships:**
- 1:N with Book (category_id foreign key in Book)

---

### Table 3: Book
**Purpose:** Store book details and inventory information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Book unique identifier |
| title | String(255) | NOT NULL, INDEX | Book title |
| author | String(120) | NOT NULL, INDEX | Author name |
| isbn | String(20) | UNIQUE, NOT NULL | ISBN code |
| description | Text | | Book description |
| price | Float | NOT NULL | Book price in USD |
| stock | Integer | DEFAULT 0 | Available quantity |
| category_id | Integer | FK, NOT NULL | Category reference |
| cover_image | String(255) | | Cover image filename |
| publisher | String(120) | | Publisher name |
| publication_year | Integer | | Year of publication |
| pages | Integer | | Number of pages |
| language | String(50) | DEFAULT 'English' | Book language |
| created_at | DateTime | DEFAULT CURRENT | Creation timestamp |
| updated_at | DateTime | DEFAULT CURRENT | Last update timestamp |

**Relationships:**
- Many-to-One with Category
- 1:N with Review
- 1:N with OrderItem (through Order)

---

### Table 4: Order
**Purpose:** Track customer orders and transaction history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Order unique identifier |
| user_id | Integer | FK, NOT NULL, INDEX | Customer reference |
| total_price | Float | NOT NULL | Order total amount |
| status | String(50) | DEFAULT 'Pending' | Order status |
| shipping_address | String(255) | | Delivery address |
| shipping_city | String(100) | | Delivery city |
| shipping_postal | String(20) | | Delivery postal code |
| created_at | DateTime | DEFAULT CURRENT, INDEX | Order creation time |
| updated_at | DateTime | DEFAULT CURRENT | Last modification time |

**Status Values:** Pending, Processing, Shipped, Delivered, Cancelled

**Relationships:**
- Many-to-One with User
- 1:N with OrderItem

---

### Table 5: OrderItem
**Purpose:** Join table linking orders to books (M:N relationship)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Item unique identifier |
| order_id | Integer | FK, NOT NULL, INDEX | Order reference |
| book_id | Integer | FK, NOT NULL, INDEX | Book reference |
| quantity | Integer | NOT NULL | Quantity ordered |
| price_at_purchase | Float | NOT NULL | Price at time of purchase |

**Relationships:**
- Many-to-One with Order
- Many-to-One with Book

---

### Table 6: Review
**Purpose:** Store user reviews and ratings for books

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Review unique identifier |
| user_id | Integer | FK, NOT NULL, INDEX | Reviewer reference |
| book_id | Integer | FK, NOT NULL, INDEX | Book reference |
| rating | Integer | NOT NULL (1-5) | Star rating |
| title | String(200) | NOT NULL | Review title |
| content | Text | NOT NULL | Review content |
| created_at | DateTime | DEFAULT CURRENT, INDEX | Creation timestamp |
| updated_at | DateTime | DEFAULT CURRENT | Last update timestamp |

**Constraints:**
- rating must be between 1 and 5
- User can only leave one review per book

**Relationships:**
- Many-to-One with User
- Many-to-One with Book

---

## Relationship Definitions

### One-to-Many (1:N):
1. **User → Order:** One user can have many orders
2. **User → Review:** One user can write many reviews
3. **Category → Book:** One category contains many books
4. **Book → Review:** One book can have many reviews
5. **Order → OrderItem:** One order can have many items

### Many-to-Many (M:N):
- **Book ↔ Order:** Many books in many orders (implemented via OrderItem join table)

---

## Sample Data

### Categories:
- Fiction
- Science Fiction
- Mystery
- Self-Help
- Technology

### Sample Books:
| Title | Author | Price | Stock | Category |
|-------|--------|-------|-------|----------|
| The Great Gatsby | F. Scott Fitzgerald | 12.99 | 50 | Fiction |
| 1984 | George Orwell | 13.99 | 40 | Science Fiction |
| The Hobbit | J.R.R. Tolkien | 15.99 | 55 | Science Fiction |
| Girl with Dragon Tattoo | Stieg Larsson | 16.99 | 35 | Mystery |
| Atomic Habits | James Clear | 17.99 | 60 | Self-Help |
| Clean Code | Robert C. Martin | 32.99 | 30 | Technology |
| Python Crash Course | Eric Matthes | 35.99 | 25 | Technology |

### Sample Users:
- admin (is_admin: True)
- john_doe (is_admin: False)
- jane_smith (is_admin: False)

---

## Database Constraints and Validations

### Constraints:
1. **Primary Key Constraints:** All IDs are unique and auto-incremented
2. **Foreign Key Constraints:** Referential integrity between tables
3. **Unique Constraints:** username, email, ISBN
4. **Not Null Constraints:** All essential fields
5. **Check Constraints:** rating (1-5), price (>= 0), stock (>= 0)

### Data Validation:
1. **Email:** Valid email format (server-side)
2. **Username:** 3-20 characters, alphanumeric + underscore
3. **Password:** Minimum 6 characters, hashed before storage
4. **Price:** Must be positive number
5. **Stock:** Non-negative integer
6. **Rating:** Integer between 1 and 5
7. **ISBN:** Valid format check (13 digits)

---

## Indexes

**Indexes created for performance optimization:**
- user.username
- user.email
- book.title
- book.author
- category.name
- order.user_id
- order.created_at
- review.user_id
- review.book_id
- review.created_at
- orderitem.order_id
- orderitem.book_id

---

**Document Version:** 1.0  
**Last Updated:** January 28, 2024
