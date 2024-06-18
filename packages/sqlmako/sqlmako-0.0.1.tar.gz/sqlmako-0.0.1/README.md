# SQLMako

SQLMako is a Python library that supercharges your SQLModel experience, infusing it with the intuitive queryset interface inspired by Django.

**Key Features:**

* **Django-Inspired QuerySets:** Unleash the power of familiar operations like `filter`, `exclude`, `order_by`, `get`, `all`, and more on your SQLModel models.
* **Enhanced Readability:** Craft SQL queries in a clean, expressive, and chainable style.
* **Seamless SQLModel Integration:** Works seamlessly with your existing SQLModel models, requiring no major refactoring.
* **Extensible:** Customize and extend the queryset functionality to fit your specific needs.

**Disclaimer:** SQLMako is currently in active development. We encourage your feedback and contributions as we work towards a stable release.

## Installation

```bash
pip install sqlmako
```

## Usage Examples

### Basic Querying

```python
from sqlmako import SQLMako, Field, Session, create_engine
from typing import Optional

class Hero(SQLMako, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    secret_name: str
    age: Optional[int] = Field(default=None)

def main():
    engine = create_engine("postgresql+psycopg2://user:password@host/database")

    with Session(engine) as session:
        SQLMako.metadata.create_all(engine)  # Create the table (only needed once)

        # Create instances
        hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
        session.add(hero_1)
        session.commit()

        # Filter and fetch
        hero = Hero.objects(session).get(name="Deadpond")
        print(hero)  # Output: Hero(id=1, name='Deadpond', secret_name='Dive Wilson', age=None)


if __name__ == "__main__":
    main()
```

**Advanced Queries:**

```python
# Filtering (Multiple Conditions)
heroes = Hero.objects(session).filter(age__gt=30, name__startswith="S")

# Ordering
heroes = Hero.objects(session).order_by(age="desc")

# ... and more! (Explore the full queryset API)
```

## Documentation

Coming Soon: Detailed documentation with comprehensive examples and API references.

## Contributing

We welcome contributions! Please check out the [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.