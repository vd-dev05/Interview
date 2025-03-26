#  Sử dụng dictionary grouping
import json
def merge_orders_dict(orders):
    merged = {}
    for order in orders:
        addr = order["address"]
        if addr not in merged:
            merged[addr] = {
                "order_ids": [order["order_id"]],
                "address": addr,
                "products": order["products"][:]  # copy danh sách sản phẩm
            }
        else:
            merged[addr]["order_ids"].append(order["order_id"])
            merged[addr]["products"].extend(order["products"])
    return list(merged.values())

# Test case ví dụ cho cách 1:
orders_same = [
    {"order_id": "ORD001", "address": "Address A", "products": ["Apple", "Banana"]},
    {"order_id": "ORD002", "address": "Address A", "products": ["Orange"]}
]
print("Merged orders (dictionary grouping):", json.dumps(merge_orders_dict(orders_same), indent=4, ensure_ascii=False))
[
    {
        "order_ids": [
            "ORD001",
            "ORD002"
        ],
        "address": "Address A",
        "products": [
            "Apple",
            "Banana",
            "Orange"
        ]
    }
]

# Sử dụng sắp xếp và duyệt tuần tự
def merge_orders_sort(orders):
    # Sắp xếp các đơn hàng theo địa chỉ
    orders_sorted = sorted(orders, key=lambda x: x["address"])
    merged = []
    current = None
    for order in orders_sorted:
        if current is None or current["address"] != order["address"]:
            if current is not None:
                merged.append(current)
            current = {
                "order_ids": [order["order_id"]],
                "address": order["address"],
                "products": order["products"][:]  # copy danh sách sản phẩm
            }
        else:
            current["order_ids"].append(order["order_id"])
            current["products"].extend(order["products"])
    if current:
        merged.append(current)
    return merged

# Test case ví dụ cho cách 2:
orders_mixed = [
    {"order_id": "ORD005", "address": "Address A", "products": ["Apple"]},
    {"order_id": "ORD006", "address": "Address B", "products": ["Banana"]},
    {"order_id": "ORD007", "address": "Address A", "products": ["Cherry"]},
    {"order_id": "ORD008", "address": "Address C", "products": ["Date"]},
    {"order_id": "ORD009", "address": "Address B", "products": ["Elderberry"]}
]

print("Merged orders (sort & group):", json.dumps(merge_orders_sort(orders_mixed), indent=4, ensure_ascii=False))
# output :
[
    {
        "order_ids": [
            "ORD005",
            "ORD007"
        ],
        "address": "Address A",
        "products": [
            "Apple",
            "Cherry"
        ]
    },
    {
        "order_ids": [
            "ORD006",
            "ORD009"
        ],
        "address": "Address B",
        "products": [
            "Banana",
            "Elderberry"
        ]
    },
    {
        "order_ids": [
            "ORD008"
        ],
        "address": "Address C",
        "products": [
            "Date"
        ]
    }
]
