# Personal Blog

## Description
This is a simple Flask-based blog that allows users to create, edit, view, and delete articles. It includes an admin panel with basic authentication.  
project for roadmap.sh https://roadmap.sh/projects/personal-blog

## Installation

### Clone the repository
```bash
git clone https://github.com/anton3029941/PersonalBlog.git
cd PersonalBlog
```

### (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python server.py
```
The application will start at `http://127.0.0.1:5500/`

## Usage
- **Homepage**: `/` — Displays a list of articles  
- **View an article**: `/articles/<title>`  
- **Admin Panel**: `/admin` (Username: `admin`, Password: `admin`)  
  - **Create an article**: `/admin/new`  
  - **Edit an article**: `/admin/articles/<title>/edit`  
  - **Delete an article**: `/admin/articles/<title>/delete`  

## Project Structure
```bash
PersonalBlog/
│── articles/              # Stores articles in JSON format
│── static/                # CSS styles
│── templates/             # HTML templates
│── LICENSE
│── README.md
│── server.py              # Main Flask server
```

## Author
anton3029941  
See license in LICENSE

