from models.component import Component
from schemas.components import ComponentsSchemas
from sqlalchemy.orm import Session

def create_components(data: ComponentsSchemas, db: Session):
    new_component = Component(name=data.name,
                              quantity=data.quantity,
                              price=data.price,
                            )
    try:
        db.add(new_component)
        db.commit()
        db.refresh(new_component)
    except Exception as e:
        print(e)

    return new_component


def get_components(id: int, db: Session):
    try:
        component = db.query(Component).filter(Component.id == id).first()
    except Exception as e:
        component = []
        print(e)

    return component


def update_components(data: ComponentsSchemas, db: Session, id: int):
    try:
        component = db.query(Component).filter(Component.id == id).first()
        component.name = data.name
        component.quantity = data.quantity
        component.price = data.price

        db.add(component)
        db.commit()
        db.refresh(component)
    except Exception as e:
        component = []
        print(e)

    return component


def remove_components(id: int, db: Session):
    component = db.query(Component).filter(Component.id == id).delete()
    try:
        db.commit()
    except Exception as e:
        print(e)

    return component
