Вот полностью готовый, финальный **README.md** со всеми тремя задачами, исправленный и собранный в один документ (можно сразу сдавать):

---

````markdown
# HBnB Evolution – Technical Documentation

## Introduction

This document describes the architecture and design of the HBnB Evolution application, a simplified system similar to Airbnb.

The purpose of this documentation is to define how the system is structured before implementation. It explains:

- how the system is divided into layers
- how components communicate
- how requests are processed step by step

The system is based on a three-layer architecture and uses the Facade design pattern to simplify communication between components.

---

# 1. High-Level Architecture (Package Diagram)

## 1.1 Overview

This section describes the global structure of the application.

The system is divided into three layers:
- Presentation Layer
- Business Logic Layer
- Persistence Layer

A Facade is used as a single entry point between layers to simplify communication.

---

## 1.2 Layers Description

### Presentation Layer
Responsible for handling user requests.

Includes:
- API endpoints
- Services

This layer does not contain business logic. It only forwards requests to the Facade.

---

### Business Logic Layer
This is the core of the system.

Includes:
- User
- Place
- Review
- Amenity

Responsible for:
- applying business rules
- managing relationships between entities
- processing application logic

---

### Persistence Layer
Responsible for storing and retrieving data.

Includes:
- Repository
- Database

---

## 1.3 Facade Pattern

The Facade acts as a single interface between the API and the business logic.

Instead of multiple direct calls:
- API → User
- API → Place
- API → Review

We use:
- API → Facade → Business Logic

This improves:
- simplicity
- maintainability
- separation of concerns

---

## 1.4 Package Diagram

```mermaid
graph TD

subgraph Presentation Layer
    API
    Services
end

subgraph Business Logic Layer
    Facade
    User
    Place
    Review
    Amenity
end

subgraph Persistence Layer
    Repository
    Database
end

API --> Facade
Services --> Facade

Facade --> User
Facade --> Place
Facade --> Review
Facade --> Amenity

User --> Repository
Place --> Repository
Review --> Repository
Amenity --> Repository

Repository --> Database
````

---

## 1.5 Summary

* System is divided into 3 layers
* API does not access business logic directly
* Facade is the single entry point
* Data is stored in a separate persistence layer

---

# 2. Business Logic Layer (Class Diagram)

## 2.1 Overview

This layer defines the core entities of the system and their relationships.

Each entity includes:

* UUID as unique identifier
* creation timestamp
* update timestamp

---

## 2.2 Class Diagram

```mermaid
classDiagram

class User {
    +UUID id
    +string first_name
    +string last_name
    +string email
    +string password
    +bool is_admin
    +datetime created_at
    +datetime updated_at
}

class Place {
    +UUID id
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +datetime created_at
    +datetime updated_at
}

class Review {
    +UUID id
    +string text
    +int rating
    +datetime created_at
    +datetime updated_at
}

class Amenity {
    +UUID id
    +string name
    +string description
    +datetime created_at
    +datetime updated_at
}

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : has
Place "*" --> "*" Amenity : includes
```

---

## 2.3 Summary

* A User can own multiple Places
* A User can write multiple Reviews
* A Place can have multiple Reviews
* A Place can include multiple Amenities
* Amenities can be shared across Places

---

# 3. Sequence Diagrams (API Calls)

## 3.1 Overview

This section shows how requests move through the system step by step.

All requests follow the same flow:

1. User sends request to API
2. API forwards request to Facade
3. Facade calls Business Logic
4. Business Logic interacts with Persistence Layer
5. Database processes data
6. Response is returned to user

---

## 3.2 User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant BusinessLogic
participant DB

User->>API: Register request
API->>Facade: Forward request
Facade->>BusinessLogic: Create user
BusinessLogic->>DB: Save user
DB-->>BusinessLogic: Confirmation
BusinessLogic-->>Facade: Success
Facade-->>API: Response
API-->>User: Registration successful
```

---

## 3.3 Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant BusinessLogic
participant DB

User->>API: Create place
API->>Facade: Forward request
Facade->>BusinessLogic: Create place
BusinessLogic->>DB: Save place
DB-->>BusinessLogic: Confirmation
BusinessLogic-->>Facade: Success
Facade-->>API: Response
API-->>User: Place created
```

---

## 3.4 Review Submission

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant BusinessLogic
participant DB

User->>API: Submit review
API->>Facade: Forward request
Facade->>BusinessLogic: Create review
BusinessLogic->>DB: Save review
DB-->>BusinessLogic: Confirmation
BusinessLogic-->>Facade: Success
Facade-->>API: Response
API-->>User: Review submitted
```

---

## 3.5 Fetch Places List

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant BusinessLogic
participant DB

User->>API: Request places list
API->>Facade: Forward request
Facade->>BusinessLogic: Get places
BusinessLogic->>DB: Fetch data
DB-->>BusinessLogic: Return data
BusinessLogic-->>Facade: Process result
Facade-->>API: Response
API-->>User: List of places
```

---

```


