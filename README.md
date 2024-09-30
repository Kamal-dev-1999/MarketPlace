# Marketplace Web App

This project is a feature-rich, scalable web application built using Django to simulate a marketplace. Users can create, browse, and manage listings for items, initiate conversations with sellers, and manage their profiles. The platform supports core marketplace functionalities like item CRUD (Create, Read, Update, Delete) operations, user authentication, and a real-time chat system for sellers and buyers.

## Introduction

This project leverages modern web development technologies to build a dynamic and interactive marketplace. With a focus on providing a seamless user experience, the application includes essential features like user authentication, secure browsing, and real-time communication. 

### Technologies Used:

1. **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
2. **Django ORM**: Object-relational mapping for database interaction, making database queries and operations easier.
3. **SQLite** (default, can be replaced with PostgreSQL or MySQL): Lightweight, file-based database used during development.
4. **Bootstrap**: CSS framework for responsive and modern UI components.
5. **JavaScript/jQuery**: To enhance user interactions and make asynchronous calls.
6. **HTML5/CSS3**: For structuring and styling web pages.
7. **Django Forms**: Simplified form handling for user inputs like creating new items, registering users, etc.
8. **Django Messages Framework**: Provides temporary, one-time notifications to users, such as form success messages.
9. **Pillow**: A Python Imaging Library used for handling image uploads for items.
10. **Django's Authentication System**: Built-in security to handle user sign-up, login, and logout.
11. **Django Templating Language**: For dynamic rendering of HTML pages with Python variables.

## Features

### 1. User Authentication
   - **Signup & Login**: New users can sign up and create accounts. Authentication is handled securely with Django’s built-in user authentication system.
   - **Logout**: Users can log out securely, and the session is properly terminated.
   - **Dashboard**: Logged-in users can access a personalized dashboard to view their listed items.

### 2. Item Browsing & Search
   - **Homepage**: Displays available items and categories in a grid format. Users can browse newly listed items and filter by category.
   - **Search Items**: Users can search for items based on keywords in the item name or description. Both category and keyword filters can be applied simultaneously.

### 3. Item CRUD (Create, Read, Update, Delete)
   - **Create New Items**: Authenticated users can list new items for sale. This feature allows uploading images, setting prices, and selecting categories.
   - **Edit Items**: Users can edit their existing listings, updating the item’s details, images, or status.
   - **Delete Items**: Users can delete their listed items, with proper permission handling to ensure only the owner can perform this action.
   - **Detail View**: Item detail pages show item information and related items based on the category.

### 4. Categories and Related Items
   - **Category Filter**: Users can filter items by category, simplifying the browsing experience for specific product types.
   - **Related Items**: Item detail pages show related items from the same category, enhancing discovery.

### 5. Conversation & Messaging System
   - **Initiate Conversations**: Buyers can start conversations with sellers directly from the item detail page. This opens a private communication channel between the buyer and seller.
   - **Inbox**: Users can view ongoing conversations and participate in them via their inbox.
   - **Conversation Detail View**: Detailed view of the conversation, allowing the user to send and receive messages in real-time.

### 6. Dashboard
   - **User Dashboard**: Displays items listed by the logged-in user. This acts as a management interface for users to view, edit, or delete their own listings.
   - **Stats & Overview**: View a summary of active and sold items to track your marketplace performance.

### 7. Static & Media Files Handling
   - **Image Uploads**: Users can upload images when creating items. Django's `FileField` and `ImageField` are used to manage these media files.
   - **Static Files Management**: CSS, JavaScript, and image files are served efficiently using Django's static files handling mechanism.

### 8. Responsive UI
   - **Bootstrap Integration**: The entire app layout is built using Bootstrap, ensuring it is mobile-friendly and fully responsive across different devices.
   - **Customizable Templates**: The UI is built using Django's template system, which allows customization of pages like the homepage, item detail, and conversation views.

## Detailed Breakdown of Views

### **Conversation Views**
- **`new_conversation(request, item_pk)`**: This view allows users to initiate a conversation with a seller. If the user tries to start a conversation about their own item, they are redirected to their dashboard. If a conversation already exists, the user is redirected to the conversation detail page.
- **`inbox(request)`**: Displays all active conversations that involve the current user. Users can view and respond to messages here.
- **`detail(request, pk)`**: Shows the details of a specific conversation. Users can continue chatting and view the conversation history.

### **Core Views**
- **`index(request)`**: The homepage displays six unsold items and all item categories. It acts as the entry point for browsing items and categories.
- **`contact(request)`**: A simple contact page that displays contact information or a contact form.
- **`SignupView(request)`**: Handles user registration using the custom signup form. On successful registration, users are redirected to the login page.
- **`logoutView(request)`**: Logs out the user and redirects them back to the homepage.

### **Dashboard Views**
- **`DashboardView(request)`**: Displays all items created by the logged-in user. Users can manage their listings directly from this page.

### **Item CRUD Views**
- **`browse(request)`**: Users can browse items by category or search for items using keywords. This view handles filtering and searching with user-friendly navigation.
- **`details(request, pk)`**: Displays details of a specific item, including related items from the same category. The item owner can edit or delete their item from this page.
- **`new_item(request)`**: Allows users to create new items by filling out a form. This view handles both form submission and file uploads for item images.
- **`edit_item(request, item_id)`**: Enables users to edit their item details and upload new images if needed.
- **`delete(request, pk)`**: Allows users to delete an item they own. This ensures proper permission handling, as only the item’s creator can perform this action.
- **`view_items_category_wise(request, category_id)`**: Displays items based on the selected category, allowing users to filter the items accordingly.
- **`search_items(request)`**: A search functionality that lets users find items by keywords in the item name or description.

## Installation

### Step-by-Step Guide:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/marketplace-webapp.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd marketplace-webapp
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the app**:
   Open your browser and go to `http://127.0.0.1:8000/` to start using the marketplace web app.

## Project Structure

- **`views.py`**: Contains the logic for handling requests and rendering templates.
- **`models.py`**: Defines the database structure for items, categories, conversations, and users.
- **`forms.py`**: Manages form submissions, such as user signup and item creation.
- **`templates/`**: Contains the HTML files that define the UI of the website.
- **`static/`**: Holds static files like CSS, JavaScript, and images.
- **`media/`**: Stores uploaded images for items.

## License

This project is licensed under the MIT License.
MIT License

Copyright (c) [year] [author]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


