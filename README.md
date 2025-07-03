# 📁 SecureFileShare (SFS)

SecureFileShare (SFS) is a centralized file-sharing backend system built using Django REST Framework. This system allows two user roles — **Operational Users** (OPS) and **Client Users** — to interact with the system based on their responsibilities. Operational users can upload specific types of documents, while clients can securely access them through encrypted links.

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Setup Instructions](#-setup-instructions)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Demo](#-demo)
- [License](#-license)
- [Author](#-author)
- [Requirements](#-requirements)

---

## 🚀 Features

### 🔐 Operational User (OPS)
- Signup and email verification
- Secure login using JWT
- Upload `.pptx`, `.docx`, `.xlsx` files

### 👤 Client User
- Signup and email verification
- Secure login using JWT
- View list of uploaded files
- Download files through unique, encrypted links

---

## 🧱 Tech Stack

- **Backend**: Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: SQLite 3
- **File Security**: Encrypted download links using `cryptography`

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd SecureFileShare
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

---

## 📌 API Endpoints

| Method | Endpoint                             | Description                                      |
|--------|--------------------------------------|--------------------------------------------------|
| POST   | `/register/`                         | Register a new user                              |
| GET    | `/verify-email/`                     | Verify email via token                           |
| POST   | `/login/`                            | Obtain JWT access/refresh tokens                 |
| POST   | `/file-upload/`                      | Upload file (OPS only)                           |
| GET    | `/generate-link/<int:file_id>/`      | Generate encrypted download link (OPS only)      |
| GET    | `/download-file/<str:encrypted_id>/` | Download file via encrypted link (Client only)   |
| GET    | `/list-files/`                       | List files uploaded (Client only)                |
| GET    | `/admin/`                            | Django admin panel (admin only)                  |

---

## 🧪 Testing

- All endpoints tested using **Postman**
- ✅ Postman collection included in the repository

---

## 📸 Demo

### 1. Client Signup, Ops Signup 
**POST** `/register/`  
➡ Creates a new client user  
![client_signup](https://github.com/user-attachments/assets/739d5e05-811c-4d49-9ff6-0630677e0056)
![Opssignup](https://github.com/user-attachments/assets/daf1ad72-3334-4e6f-aa67-bb5209420386)



---

### 2. Email Verification  
**GET** `/verify-email/`  
➡ Activates the client account  
![clientverify](https://github.com/user-attachments/assets/45d06bfe-faa0-4972-8ba2-cc34faef38cd)


---

### 3. Client Login, Ops Login
**POST** `/login/`  
➡ Returns JWT token for authentication  
![clientlogin](https://github.com/user-attachments/assets/6bd4f8b0-99db-4edd-8ac2-640de71c7e61)
![opslogin](https://github.com/user-attachments/assets/ae1a3b2c-b8f5-44e8-a573-9b247eaa7fa3)


---

###  4. Upload File (Ops only)  
**POST** `/file-upload/`  
➡ Auth: Ops JWT required  
![uploadfile](https://github.com/user-attachments/assets/3799b8e3-2728-4f14-abb2-3662746f600a)


---

### 5. List Uploaded Files (Client only)  
**GET** `/list-files/`  
➡ Lists file names and metadata  
![listfile](https://github.com/user-attachments/assets/e994a008-c437-471f-a25d-478caeb79c60)

---

### 6. Generate Download Link
**POST** `/generate-link/<int:file_id>/`  
➡ Auth: Client JWT required  
➡ Body: `{ "filename": "sample.pptx" }`  
![genratelink](https://github.com/user-attachments/assets/a63052a2-a550-47d2-8d57-b2a98c9ced9e)

---

### 7. Download File  
**GET** `/download-file/<str:encrypted_id>/`  
➡ Secure one-time file access  
![downloadfile](https://github.com/user-attachments/assets/d6b04189-1b03-4a28-b48d-8ad6bbb5105c)

## Postman Collection

You can import the complete Postman Collection from this link:

🔗 [Secure File Sharing API Collection (JSON)](https://github.com/prashantgupta2385/Assignment-EZ/blob/main/postman/SecureFileSharingAPI%20Collection.postman_collection.json)


![Screenshot for 200 Ok ](https://github.com/user-attachments/assets/41369a63-8e53-402e-b4cd-79808487095d)
![](https://github.com/user-attachments/assets/71e00aca-5940-4635-bb6a-65d6ccb63bdb)




---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software as per the license terms.

---

## 👨‍💻 Author

**Prashant Gupta**  
- [LinkedIn](https://www.linkedin.com/in/prashant-gupta-6b0443257/)  
- [GitHub](https://github.com/prashantgupta2385)

---

## 📦 Requirements

Dependencies used in this project (`requirements.txt`):
