from ...tools import calculate_expression


def calculate_node(state: dict):
    parsed = state.get("parsed_data", {})
    items = parsed.get("items", [])
    discount = parsed.get("discount_percent", 0.0)

    try:
        for item in items:
            item["subtotal"] = calculate_expression(
                f"{item['quantity']}*{item['unit_price']}"
            )

        total_before = calculate_expression(
            "+".join(str(i["subtotal"]) for i in items) or "0"
        )
        total_after = calculate_expression(f"{total_before}*(1-{discount}/100)")

        parsed["total_before_discount"] = total_before
        parsed["total_after_discount"] = round(total_after, 2)

        return {"parsed_data": parsed}
    except Exception as e:
        return {"error": f"calculation_failed: {e}"}
