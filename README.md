# 🧬 Pydantic Validation & Schema Guide

A comprehensive guide and reference implementation for **Pydantic (v2)**, Python's most popular data validation and parsing library. Pydantic leverages standard Python type hints to enforce schema validation at runtime, providing clean error handling, type coercion, and schema serialization.

The exercises and sample classes are implemented in the interactive Jupyter notebook [pydantic.ipynb](pydantic/pydantic.ipynb).

---

## 📂 Project Structure

```text
langgraph/
├── pydantic/
│   └── pydantic.ipynb            # Interactive Notebook & Code Examples
├── pyproject.toml                # Project Config and Dependencies
└── README.md                     # This documentation file
```

---

## 🧠 Core Pydantic Concepts

### 1. Pydantic `BaseModel` vs. Standard Python `@dataclass`
Python’s standard `@dataclass` allows you to annotate field types, but it **does not enforce them** at runtime. If you pass an invalid type, standard dataclasses will accept it without throwing an error.

* **Standard Dataclass**:
  ```python
  from dataclasses import dataclass

  @dataclass
  class Person:
      name: str
      age: int
      city: str

  # ❌ accepts a string "three" for the integer age!
  person = Person(name="Nitish", age="three", city="Bangalore")
  print(person) # Person(name='Nitish', age='three', city='Bangalore')
  ```
  See implementation in [pydantic.ipynb#L50](pydantic/pydantic.ipynb#L50).

* **Pydantic `BaseModel`**:
  Pydantic models inherit from `BaseModel`. They perform strict runtime validation and raise a `ValidationError` when data types do not conform.
  ```python
  from pydantic import BaseModel

  class Person1(BaseModel):
      name: str
      age: int
      city: str

  # ❌ Throws ValidationError: Input should be a valid integer
  person = Person1(name="Nitish", age="three", city="Bangalore")
  ```
  See implementation in [pydantic.ipynb#L93](pydantic/pydantic.ipynb#L93).

---

## 🧱 Key Features & Code Walkthrough

### 2. Models with Optional Fields
Fields can be marked as optional by providing default values or utilizing Python's `Optional` union type.
* **Required vs Optional**: If a field has no default value, it is *required*. If it has a default value (e.g., `= None` or `= True`), it is *optional*.
* **Type Coercion**: Pydantic will still validate the type of optional fields if a value is provided (e.g., converting an integer `60000` to float `60000.0`).
```python
from typing import Optional

class Employee(BaseModel):
    id: int                          # Required
    name: str                        # Required
    department: str                  # Required
    salary: Optional[float] = None   # Optional (Defaults to None)
    is_active: Optional[bool] = True # Optional (Defaults to True)
```
See implementation in [pydantic.ipynb#L157](pydantic/pydantic.ipynb#L157).

### 3. Collection Fields & Item Validation
Pydantic validates the contents of collection types like `List`, `Dict`, or `Set`. If any item inside a list violates the type rule, the entire model validation fails.
```python
from pydantic import BaseModel
from typing import List

class ClassRoom(BaseModel):
    room_number: str
    students: List[str]  # All items in this list MUST be strings
    capacity: int
```
See implementation in [pydantic.ipynb#L214](pydantic/pydantic.ipynb#L214).

### 4. Nested Models
Models can be nested inside one another to construct complex hierarchical data structures. Pydantic automatically parses dictionaries into nested models:
```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Customer(BaseModel):
    customer_id: int
    name: str
    address: Address # Nested BaseModel
```
See implementation in [pydantic.ipynb#L294](pydantic/pydantic.ipynb#L294) and [pydantic.ipynb#L299](pydantic/pydantic.ipynb#L299).

---

## 🛠️ Advanced Field Customization (`Field`)

Pydantic's `Field` function is used to add metadata, validation constraints, and default factories to model fields:

### 5. Constraints and Numeric Range Validation
You can enforce numeric constraints like `ge` (greater than or equal to), `le` (less than or equal to), or string length constraints like `min_length` and `max_length`:
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=2, max_length=50) # Length bounds
    price: float = Field(ge=0, le=1000)            # 0 <= price <= 1000
    quantity: int = Field(ge=0)                    # Non-negative integer
```
See implementation in [pydantic.ipynb#L344](pydantic/pydantic.ipynb#L344).

### 6. Descriptions and Default Factories
* **description**: Document fields directly in code (useful for generating OpenAPI docs or instructing LLMs in Structured Tool Output).
* **default_factory**: Used to generate dynamic default values (like current timestamps, UUIDs, or default lists/dictionaries).
```python
class User(BaseModel):
    username: str = Field(..., description="Unique username for the user")
    age: int = Field(default=18, description="User age, defaults to 18")
    email: str = Field(
        default_factory=lambda: "user@example.com", 
        description="Default email address"
    )
```
See implementation in [pydantic.ipynb#L372](pydantic/pydantic.ipynb#L372).

---

## ⚡ Setup & Requirements

1. **Prerequisites**: Make sure Pydantic v2 is installed:
   ```bash
   pip install pydantic
   ```
2. **Interactive Play**: Run the cells in [pydantic.ipynb](pydantic/pydantic.ipynb) to see runtime errors, validation traces, and model schemas in action.
