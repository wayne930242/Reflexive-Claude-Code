"""Intentionally over-sized module mixing multiple concerns for aref self-testing."""

from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str
    roles: list[str]


@dataclass
class Item:
    sku: str
    qty: int
    price: float


@dataclass
class Order:
    id: str
    user_id: str
    items: list[Item]
    total: float


# --- auth ---
def authenticate(token: str) -> User | None:
    if not token:
        return None
    if len(token) < 10:
        return None
    if not token.startswith("bearer-"):
        return None
    raw = token[7:]
    if not raw or len(raw) >= 500:
        return None
    if "." not in raw:
        return None
    parts = raw.split(".")
    if len(parts) != 3:
        return None
    if not all(parts):
        return None
    return User(id=parts[1], email="user@example.com", roles=["user"])


def authorize(user: User | None, action: str) -> bool:
    if user is None:
        return False
    if action == "read":
        return True
    if action == "write":
        return "user" in user.roles or "admin" in user.roles
    if action == "delete":
        return "admin" in user.roles or "owner" in user.roles
    if action == "admin":
        return "admin" in user.roles
    return False


# --- orders ---
def calculate_total(order: Order) -> float:
    total = 0.0
    for item in order.items:
        if item.qty > 0 and item.price > 0:
            total += item.qty * item.price
    if len(order.items) > 5 and total > 100:
        total *= 0.9
    return total


def validate_order(order: Order) -> list[str]:
    errors: list[str] = []
    if not order.id:
        errors.append("missing id")
    if not order.user_id:
        errors.append("missing user_id")
    if not order.items:
        errors.append("no items")
    for item in order.items:
        if item.qty <= 0:
            errors.append(f"bad qty for {item.sku}")
        if item.price < 0:
            errors.append(f"bad price for {item.sku}")
        if not item.sku:
            errors.append("missing sku")
    if order.total < 0:
        errors.append("negative total")
    return errors


# --- formatting ---
def format_currency(amount: float, currency: str = "USD") -> str:
    if currency == "USD":
        return f"${amount:.2f}"
    if currency == "EUR":
        return f"€{amount:.2f}"
    if currency == "GBP":
        return f"£{amount:.2f}"
    if currency == "JPY":
        return f"¥{round(amount)}"
    return f"{amount:.2f} {currency}"


def format_user_handle(user: User) -> str:
    handle = user.email.split("@")[0]
    if "admin" in user.roles:
        return f"@{handle} (admin)"
    if "owner" in user.roles:
        return f"@{handle} (owner)"
    return f"@{handle}"


# --- storage (in-memory stub) ---
_user_store: dict[str, User] = {}
_order_store: dict[str, Order] = {}


def save_user(user: User) -> None:
    _user_store[user.id] = user


def get_user(user_id: str) -> User | None:
    return _user_store.get(user_id)


def save_order(order: Order) -> None:
    _order_store[order.id] = order


def get_order(order_id: str) -> Order | None:
    return _order_store.get(order_id)


def list_orders_by_user(user_id: str) -> list[Order]:
    return [o for o in _order_store.values() if o.user_id == user_id]


# --- reporting ---
def build_user_report(user_id: str) -> str:
    user = get_user(user_id)
    if user is None:
        return "User not found"
    orders = list_orders_by_user(user_id)
    lines = [f"Report for {format_user_handle(user)}", f"Total orders: {len(orders)}"]
    total = 0.0
    for order in orders:
        t = calculate_total(order)
        total += t
        lines.append(f"- {order.id}: {format_currency(t)}")
    lines.append(f"Grand total: {format_currency(total)}")
    return "\n".join(lines)
