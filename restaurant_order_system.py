"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import os
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create an order; return False if it exists or has no dishes."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": 15.0 * items_count,
        "is_settled": False,
    }
    message = f"Created order for {table_id} with {items_count} dishes"
    order_log.append(message)
    return True


def void_table_order(table_id):
    """Remove an order if it exists; do nothing otherwise."""
    orders.pop(table_id, None)


def check_table_status(table_id):
    """Return True if the table exists and its bill is still unsettled."""
    if table_id not in orders:
        return False
    return not orders[table_id]["is_settled"]


def calculate_discounted_bill(table_id, discount_rate):
    """Return the bill after applying a discount rate between 0 and 1."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_bill = orders[table_id]["bill"]
    return base_bill * (1 - discount_rate)


def generate_ticket_hash(table_id):
    """Return a SHA-256 hex digest identifying the table's ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Return a cryptographically secure 4-digit POS PIN."""
    return secrets.randbelow(9000) + 1000


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write all orders to a file for the kitchen printer."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(orders))
    print(f"Ticket sent to kitchen printer: {filename}")


def get_pending_summary(order_book):
    """Count orders that are not yet settled."""
    return sum(1 for d in order_book.values() if not d["is_settled"])


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = os.environ.get("POS_TERMINAL_KEY")
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 0.10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS key configured:", pos_terminal_key is not None)


if __name__ == "__main__":
    main()