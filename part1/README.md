# HBnB Evolution – Technical Documentation (Part 1)

## 📌 Overview

This document provides a high-level overview of the architecture of the **HBnB Evolution** application.
The system is designed using a **three-layer architecture** to ensure separation of concerns, scalability, and maintainability.

---

## 🏗 Architecture

The application is divided into three main layers:

* **Presentation Layer** – Handles user interaction (API, services)
* **Business Logic Layer** – Contains core logic and models
* **Persistence Layer** – Manages data storage and retrieval

The interaction between layers is managed using the **Facade Pattern**, which provides a unified interface.

---

## 📊 Package Diagram

<img width="3612" height="3635" alt="image" src="https://github.com/user-attachments/assets/8ffa3ef2-5a3a-4a1e-9db6-5b1d479c957f" />


## 🔹 Layer Description

### 1. Presentation Layer

This layer is responsible for handling user interactions.

It includes:

* API endpoints
* Service classes

The Presentation Layer does not directly interact with the business models. Instead, it communicates through the Facade.

---

### 2. Business Logic Layer

This layer contains the core functionality of the application.

It includes the following models:

* **User**
* **Place**
* **Review**
* **Amenity**

These models define the business rules and logic of the system.

---

### 3. Persistence Layer

This layer is responsible for data management.

It includes:

* Repository (data access logic)
* Database

All data is stored and retrieved through this layer.

---

## 🔹 Facade Pattern

The **Facade** acts as an intermediary between the Presentation Layer and the Business Logic Layer.

Instead of interacting directly with multiple models, the Presentation Layer communicates only with the Facade.

### Benefits:

* Simplifies communication between layers
* Reduces coupling
* Improves maintainability

---

## 🔄 Data Flow

1. A user sends a request via the API
2. The request is handled by the Facade
3. The Facade interacts with the appropriate business model
4. The model communicates with the Repository
5. The Repository interacts with the Database
6. The response flows back to the user

---

## ✅ Conclusion

This architecture ensures:

* Clear separation of concerns
* Scalable design
* Easy maintenance and extension

The use of the Facade pattern simplifies interactions and enforces a clean structure for the application.
