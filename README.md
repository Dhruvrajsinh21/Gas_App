# Gas Utility Company Service Management

This Django application provides consumer services for gas utilities. It allows customers to submit service requests, track their status, and view account information. Due to **high request volume**, **Celery-Redis** is used for scaling and managing tasks efficiently. Customer support representatives can also manage service requests and assist customers.

---

## Features

- **Sign up/Login**: The application opens to the login or signup page. Users must create an account or log in before they can interact with the service request system.
- **Create Service Request**: After logging in, users can create a service request for issues like installation, maintenance, etc.
- **Track Service Request**: Users can track the status of their service requests, including their submission time and resolution time.
- **Admin Panel**: Admins or customer support representatives can manage service requests and update their statuses.
- **Celery Integration**:Celery is used for asynchronous task processing, such as updating the service request statuses in the background. To ensure that Celery works, make sure the Redis server is running 
  before starting the Celery worker.
  
  ![image](https://github.com/user-attachments/assets/00985504-5572-49bc-8feb-83d637726b5b)
  
---

Photos of Django Application:

![image](https://github.com/user-attachments/assets/94b3eea4-9db3-4e78-9e58-8a3ed6130220)
![image](https://github.com/user-attachments/assets/c8eb6c3b-a771-4a92-89f1-83ccd84d99a6)
![image](https://github.com/user-attachments/assets/5bd9da29-f6e1-4ce3-9583-66c1c3d0bd64)
![image](https://github.com/user-attachments/assets/3de17f5d-7057-4d4b-86a1-d26e382d23af)
![image](https://github.com/user-attachments/assets/000180b7-565c-418b-b00e-d8937d31e416)
##CeleryWorking
![image](https://github.com/user-attachments/assets/5b40b8f6-9918-497a-bf19-af5ec0893e5e)

## General requirements:

- **Python 3.x**
- **Django 5.x**
- **Celery**
- **Redis** (used as the Celery broker)

---

## Installation

Follow these steps to set up the project in your local environment.

### Step 1: Clone the repository

```bash
git clone <repository_url>
cd Gas_App
```

### Step 2: Create a Virtual Environment
Create a virtual environment to isolate the project's dependencies:

``` bash
python -m venv venv
```

Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages using requirements.txt:

```bash
pip install -r requirements.txt
cd gasapp
```

### Step 4: Install Redis
Since Celery requires a message broker, we use Redis in this project.

Windows: Follow the instructions at Redis Windows.
Mac: You can install Redis using Homebrew:

Start the Redis server:

``` bash
docker run --name redis -p 6379:6379 -d redis:alpine
# For running this command you should have docker desktop install.
```

### Step 5: Apply Migrations
Apply the necessary migrations to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Run the Django Development Server
Start the Django development server:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to access the application.

### Step 7: Run Celery Worker
To process tasks asynchronously with Celery, start the Celery worker in a new terminal window:

```bash
celery -A gasapp worker --loglevel=info --pool=solo
```

Directory Structure
The structure of the project is as follows:

```graphql
Gas_App/
    manage.py                    
    gasapp/                       
        apis/                     
            __init__.py
            views.py              
            serializers.py        
            tasks.py              # Celery tasks for background processing
            .....
        gasapp/                    
            __init__.py
            settings.py           
            urls.py               
            .....
        templates/                
            signup.html           
            home.html
            login.html
            ...         
        static/                  
```
