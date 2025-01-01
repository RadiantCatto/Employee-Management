# API Documentation for Employee Management

This collection contains a set of APIs that provide functionality and data related to **Employees**, **WorkSchedules**, and **Users**. Below are detailed descriptions for key endpoints, along with their request/response formats.

## 📂 Project Setup

### 🔧 Local Environment Setup

- **Django REST API**:  
  Set up a Django REST API project on your local machine and explore the Django environment.

- **Version Control**:  
  Use **Git** and **Sourcetree** for managing version control.

- **Postman**:  
  Utilize **Postman** for API testing and documentation.

## 📂 **Repository Structure**

```
Employee-Management/
|
|-- mysite/                  # Django project directory
|   |-- Name/                # Project name directory
|   |-- Employees/           # Employee-related functionality
|   |-- Users/               # User-related functionality
|   |-- env/                 # Virtual environment
|   |-- mysite/              # Settings and project configuration
|   |-- manage.py            # Django manage script
|   |-- requirements.txt     # Project dependencies
|   |-- tut.txt              # Project documentation/tutorials

```

## 📚 API Endpoints

### 1. **Users Management**

#### 🚀 Create a User Record

**POST** [Create a User].

This API request is used to create a new user record with the provided parameters.

**Request Parameters:**

| Field Name    | Data Type | Is Required | Description                | Sample Value     |
|---------------|-----------|-------------|----------------------------|------------------|
| UserType      | String    | Yes         | The type of user.          | "Employees"      |
| employee_id   | Integer   | Yes         | The ID of the employee.    | 10005            |
| useraccess    | String    | Yes         | The username of the user.  | "TestEmployee"   |
| passphrase    | String    | Yes         | The passphrase of the user.| "My_pass2763"    |

**Response Parameters:**

| Field Name    | Data Type | Description                | Sample Value        |
|---------------|-----------|----------------------------|---------------------|
| UserType      | String    | Type of user               | "Employees"         |
| employee_id   | Integer   | ID of the employee         | 1                   |
| salt          | String    | Salt value for passphrase  | "bd8e59af47aa..."   |
| useraccess    | String    | User access information    | "TestUser"          |
| passphrase    | String    | Encrypted passphrase       | "c82343d33baf..."   |

### 2. **Update User Record**

**PATCH** [Update User Record]

This API endpoint allows you to update a user record with the `UserType` and `useraccess` fields.

#### Request Parameters:

| Field Name    | Data Type | Is Required | Description                | Sample Value     |
|---------------|-----------|-------------|----------------------------|------------------|
| UserType      | String    | Yes         | Type of the user           | "Administrator"  |
| useraccess    | String    | Yes         | Access level of the user   | "UserTestAdmin"  |

#### Response Parameters:

| Field Name    | Data Type | Is Required | Description                | Sample Value      |
|---------------|-----------|-------------|----------------------------|-------------------|
| UserType      | String    | Yes         | Type of the user           | "Administrator"    |
| employee_id   | Integer   | Yes         | ID of the associated employee | 2               |
| useraccess    | String    | Yes         | Access level of the user   | "UserTestAdmin"    |

## 🔐 Authorization

This folder utilizes **Bearer Tokens** for authorization. Please make sure to include a valid token in the request headers.

## 📜 API Documentation via Postman

All endpoints are documented via **Postman**, which can be accessed [here](https://documenter.getpostman.com/view/26443770/2s93kxckys#intro).

## 🚀 Project Enhancements

Feel free to contribute to this project by following these guidelines:

1. Fork the repository and create a new branch.
2. Implement changes or additions.
3. Submit a pull request with a clear description of the changes.

## 💬 Support & Contributions

For any issues or contributions, please open an issue in this repository or contact the project maintainers.



