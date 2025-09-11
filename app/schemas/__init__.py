# Import all schemas to make them easily accessible from a single point
from .user import UserRead, UserCreate, UserUpdate, UserInDB, UserSimple, Token
from .product import ProductRead, ProductCreate, ProductSimple
from .review import ReviewRead, ReviewCreate
from .order import OrderRead, OrderCreate
from .cart import CartRead, CartItemAdd

# Resolve forward references
ProductRead.model_rebuild()
ReviewRead.model_rebuild()