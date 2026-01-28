# User Manual - Online Bookstore

## Quick Start Guide

Welcome to the Online Bookstore! This manual will help you navigate and use all features of our platform.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Account](#user-account)
3. [Browsing Books](#browsing-books)
4. [Shopping Cart](#shopping-cart)
5. [Making Purchases](#making-purchases)
6. [Account Management](#account-management)
7. [Reviews and Ratings](#reviews-and-ratings)
8. [Admin Guide](#admin-guide)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Getting Started

### Accessing the Website

1. Open your web browser
2. Navigate to: `http://localhost:5000` (development) or your deployed URL
3. You'll see the home page with featured books

### Home Page Features

- **Navigation Bar:** Access to main sections, login, and user menu
- **Hero Section:** Welcome message and quick search
- **Featured Books:** Latest and popular books
- **Category Section:** Browse books by category
- **Features Overview:** Learn about our service

---

## User Account

### Creating an Account (Registration)

1. Click **"Register"** in the top navigation bar
2. Fill in the registration form:
   - **Full Name:** Your complete name
   - **Username:** Unique identifier (3-20 characters)
   - **Email:** Valid email address
   - **Password:** At least 6 characters
   - **Confirm Password:** Must match password
3. Click **"Register"**
4. You'll see a success message
5. **Login** with your new credentials

### Logging In

1. Click **"Login"** in the navigation bar
2. Enter your email address
3. Enter your password
4. (Optional) Check "Remember Me" to stay logged in
5. Click **"Login"**

### Demo Account

You can test with the pre-created admin account:
- **Email:** admin@bookstore.com
- **Password:** admin123

### Logging Out

1. Click your name in the top-right corner
2. Select **"Logout"**
3. Your session will end, and you'll return to the home page

---

## Browsing Books

### Viewing All Books

1. Click **"Books"** in the navigation bar
2. You'll see all available books with pagination

### Searching for Books

1. Use the **search bar** on the Books page
2. Type the book title or author name
3. Press Enter or click the search icon
4. Results will display matching books

### Filtering by Category

1. On the Books page, look at the **sidebar**
2. Click a category name
3. Only books in that category will display
4. Click "All Categories" to reset filter

### Pagination

- View books in sets of 12
- Click page numbers at the bottom to navigate
- Use "Previous" and "Next" buttons

### Viewing Book Details

1. Click on any book card
2. You'll see:
   - Full book information (author, publisher, etc.)
   - Book price and stock status
   - Customer reviews and ratings
   - "Add to Cart" button

---

## Shopping Cart

### Adding Books to Cart

1. Find the book you want
2. Click **"View Details"**
3. Click the **"Add to Cart"** button
4. You'll see a success message
5. The item is now in your cart

### Viewing Your Cart

1. Click **"Cart"** in the navigation bar
2. You'll see all items with:
   - Book title and author
   - Unit price
   - Quantity
   - Total per item
   - Delete button

### Removing Items from Cart

1. Go to your cart
2. Find the item you want to remove
3. Click the **"Delete"** button (trash icon)
4. The item is removed immediately

### Viewing Cart Summary

At the bottom of your cart page:
- **Subtotal:** Total before tax
- **Shipping:** Free on all orders
- **Tax:** Calculated automatically
- **Grand Total:** Final amount

---

## Making Purchases

### Checkout Process

1. From your cart, click **"Proceed to Checkout"**
2. Review your shipping information:
   - Name, email, phone
   - Address and location
3. All fields are pre-filled from your profile
4. Click **"Place Order"** to complete purchase

### Order Confirmation

After placing an order:
1. You'll see your order confirmation page
2. Your **Order ID** is displayed
3. You'll receive order details in your email (future feature)

### Viewing Order History

1. Click on your name in the top-right
2. Select **"Dashboard"**
3. You'll see:
   - Your order statistics
   - Recent orders list
   - Order status

### Order Status

Orders progress through these statuses:
- **Pending:** Order received, being processed
- **Processing:** Order is being prepared
- **Shipped:** Order is on the way
- **Delivered:** Order has arrived
- **Cancelled:** Order was cancelled

---

## Account Management

### Viewing Your Profile

1. Click on your name in the top-right
2. Select **"Profile"**
3. You'll see all your account information:
   - Personal details
   - Contact information
   - Account statistics

### Editing Your Profile

1. Click on your name → **"Profile"**
2. Click **"Edit Profile"** button
3. Update any of these fields:
   - Full Name
   - Email Address
   - Phone Number
   - Street Address
   - City
   - Postal Code
4. Click **"Update Profile"**
5. You'll see a success message

### Changing Password

To change your password (future enhancement):
- Feature coming soon
- For now, contact support: support@bookstore.com

---

## Reviews and Ratings

### Writing a Review

1. Go to any book's detail page
2. Scroll to the **"Reviews"** section
3. Click **"Write a Review"**
4. Fill in:
   - **Rating:** Select 1-5 stars
   - **Review Title:** Brief summary (5-200 characters)
   - **Review Content:** Your detailed review (10-1000 characters)
5. Click **"Submit Review"**

### Important Notes

- **One review per book:** You can only review each book once
- **Must be logged in:** Log in before writing a review
- **Moderation:** Reviews are published immediately

### Viewing Reviews

- Reviews appear immediately after submission
- See average rating and review count
- Display sorted by most recent
- See reviewer name and date

### Editing Your Review

To edit a review (future enhancement):
- Feature coming soon
- Delete and rewrite if needed

---

## Admin Guide

### Accessing Admin Panel

1. Login with admin credentials
2. Click on your name in the top-right
3. Select **"Admin Panel"**
4. You'll see the admin dashboard

### Admin Dashboard

The dashboard shows:
- **Statistics:** Total users, books, orders, revenue
- **Low Stock Alerts:** Books with stock < 5
- **Recent Orders:** Latest customer orders
- **Quick Action Buttons:** Access management pages

### Managing Books

#### Add New Book
1. Click **"Manage Books"** → **"Add New Book"**
2. Fill in book details:
   - Title, author, ISBN
   - Price, stock quantity
   - Category, publisher
   - Publication year, pages
   - Language, description
3. Click **"Add Book"**

#### Edit Book
1. Click **"Manage Books"**
2. Click the edit button (pencil icon)
3. Update any field
4. Click **"Save Changes"**

#### Delete Book
1. Click **"Manage Books"**
2. Click the delete button (trash icon)
3. Confirm deletion

### Managing Categories

#### Add Category
1. Click **"Manage Categories"**
2. Click **"Add New Category"**
3. Enter category name and description
4. Click **"Add Category"**

#### Delete Category
1. Click **"Manage Categories"**
2. Click delete button next to category
3. Note: Can only delete empty categories

### Managing Orders

1. Click **"Manage Orders"**
2. View all customer orders
3. To update order status:
   - Select new status from dropdown
   - Click **"Update"** button

### Managing Users

1. Click **"Manage Users"**
2. View all registered users
3. To make user an admin:
   - Click **"Make Admin"** button
4. To revoke admin:
   - Click **"Revoke Admin"** button

---

## Troubleshooting

### I Forgot My Password

**Solution:**
1. Click "Forgot Password?" on login page (coming soon)
2. Or contact: support@bookstore.com
3. We'll help you recover your account

### My Cart is Empty After Refresh

**Solution:**
- Cart data is saved in browser session
- Clear browser cache
- Add items again if needed

### "Stock Not Available" Error During Checkout

**Solution:**
1. The book might have sold out
2. Go back to cart
3. Remove the item and choose another book
4. Try checkout again

### I Can't Access the Admin Panel

**Solution:**
1. Verify you're logged in as admin
2. Check if your account has admin privileges
3. Contact the original admin to grant access

### Page Not Loading or Very Slow

**Solution:**
1. Refresh the page (Ctrl+R or Cmd+R)
2. Clear browser cache
3. Try a different browser
4. Check your internet connection

### Form Shows Validation Errors

**Solution:**
1. Read the error message carefully
2. Check field requirements (marked with *)
3. Example errors:
   - Email must be valid: user@example.com
   - Password minimum 6 characters
   - Username 3-20 characters
4. Correct the fields and resubmit

---

## FAQ

### General Questions

**Q: Is the website free to use?**
A: Yes, creating an account and browsing is free. Demo purchase feature is available.

**Q: What payment methods do you accept?**
A: Currently in demo mode (no real payment). Production version will support major credit cards.

**Q: Is my personal information safe?**
A: Yes, we use password hashing and secure session management.

**Q: How long does shipping take?**
A: Currently demo (no shipping). Future versions will have tracking.

### Account Questions

**Q: Can I have multiple accounts?**
A: One account per email address. Use "Register" to create a new account.

**Q: Can I delete my account?**
A: Contact support@bookstore.com to request account deletion.

**Q: What if I enter the wrong email during registration?**
A: You can update it in your profile settings.

**Q: Is there a referral program?**
A: Coming soon! Check back for updates.

### Shopping Questions

**Q: Can I modify an order after placing it?**
A: Orders can't be modified, but you can place new orders.

**Q: How do I track my order?**
A: Coming soon - real-time tracking will be available.

**Q: What's your return policy?**
A: This is a digital bookstore (no returns in demo mode).

**Q: Can I gift books to someone?**
A: Wishlist and gifting coming in next version.

### Technical Questions

**Q: What browsers are supported?**
A: Chrome, Firefox, Safari, Edge, and mobile browsers.

**Q: Can I access on mobile?**
A: Yes, the site is fully responsive on phones and tablets.

**Q: Do you have a mobile app?**
A: Mobile apps coming soon for iOS and Android.

**Q: What if I find a bug?**
A: Report it to: bugs@bookstore.com

### Review Questions

**Q: Can I edit my review?**
A: Currently, delete and rewrite. Edit feature coming soon.

**Q: Are reviews moderated?**
A: Reviews are published immediately. Abusive reviews may be removed.

**Q: Can I see reviews from other users?**
A: Yes, all reviews are visible on book detail pages.

### Admin Questions

**Q: How do I become an admin?**
A: Contact the original admin. They can grant admin privileges.

**Q: Can I undo a book deletion?**
A: No, deletions are permanent. Use caution when deleting.

**Q: How often should I update inventory?**
A: Update stock levels regularly to avoid overselling.

**Q: Can I generate sales reports?**
A: Yes, admin dashboard shows statistics. Detailed reports coming soon.

---

## Contact & Support

### Help & Support
- **Email:** support@bookstore.com
- **Phone:** +1 (555) 123-4567
- **Hours:** Monday-Friday, 9 AM - 5 PM EST

### Bug Reports
- **Email:** bugs@bookstore.com
- **Include:** Screenshots, browser info, steps to reproduce

### Feature Requests
- **Email:** features@bookstore.com
- **We love your suggestions!**

---

## Version Information

- **Application Version:** 1.0.0
- **Last Updated:** January 28, 2024
- **Documentation Version:** 1.0

---

**Thank you for using Online Bookstore! Happy reading! 📚**
