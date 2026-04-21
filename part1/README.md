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

## 1.1 What this task means (simple explanation)

In this part, we are not writing code. We are drawing a “map” of the whole system.

This map shows:
- what parts the system is made of
- how these parts are grouped
- how they communicate with each other

Think of it like a building:

- Presentation Layer = user entry point (API)
- Business Logic Layer = system brain (rules and logic)
- Persistence Layer = storage system (database)

The Facade acts as a single entry point between layers and simplifies communication.

---

## 1.2 Layers of the system

### Presentation Layer
Handles user requests:
- API endpoints
- Services

It does not contain business rules.

---

### Business Logic Layer
Core system logic:
- User
- Place
- Review
- Amenity

Responsible for rules, validation, and relationships.

---

### Persistence Layer
Handles data storage:
- Repository
- Database

---

## 1.3 Facade Pattern

The Facade is the single interface between API and business logic.

Instead of:
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
