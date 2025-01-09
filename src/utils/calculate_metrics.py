from collections import defaultdict
from decimal import Decimal


def calculate_metrics(self, transactions, products):
    self.transactions = transactions
    self.products = products
    if not transactions:
        return {}

    all_products = {str(p._id): p for p in products}

    stock_alerts = {"critical": [], "warning": []}

    for product in products:
        if product.stock <= 5:
            stock_alerts["critical"].append(
                {
                    "name": product.name,
                    "stock": product.stock,
                    "avg_daily_sales": 0,
                }
            )
        elif product.stock <= 10:
            stock_alerts["warning"].append(
                {
                    "name": product.name,
                    "stock": product.stock,
                    "avg_daily_sales": 0,
                }
            )

    sorted_transactions = sorted(transactions, key=lambda x: x.date)

    product_metrics = defaultdict(
        lambda: {
            "total_revenue": Decimal("0"),
            "total_profit": Decimal("0"),
            "quantity_sold": 0,
            "profit_margin": Decimal("0"),
            "stock_turnover": 0,
            "days_to_stockout": float("inf"),
        }
    )

    daily_metrics = defaultdict(
        lambda: {
            "sales": Decimal("0"),
            "profit": Decimal("0"),
            "transactions": 0,
            "products_sold": defaultdict(int),
        }
    )

    for trans in transactions:
        date_str = trans.date.strftime("%Y-%m-%d")
        prod_id = str(trans.product_id)

        daily_metrics[date_str]["sales"] += trans.total
        daily_metrics[date_str]["profit"] += trans.profit
        daily_metrics[date_str]["transactions"] += 1
        daily_metrics[date_str]["products_sold"][trans.product_name] += trans.quantity

        product_metrics[trans.product_name]["total_revenue"] += trans.total
        product_metrics[trans.product_name]["total_profit"] += trans.profit
        product_metrics[trans.product_name]["quantity_sold"] += trans.quantity

        if prod_id in all_products:
            current_stock = all_products[prod_id].stock
            total_sold = product_metrics[trans.product_name]["quantity_sold"]
            days = len(
                set(
                    dm
                    for dm in daily_metrics.keys()
                    if daily_metrics[dm]["products_sold"][trans.product_name] > 0
                )
            )

            if days > 0:
                avg_daily_sales = total_sold / days
                if avg_daily_sales > 0:
                    days_to_stockout = current_stock / avg_daily_sales
                    product_metrics[trans.product_name][
                        "days_to_stockout"
                    ] = days_to_stockout

                    for alert in stock_alerts["critical"]:
                        if alert["name"] == trans.product_name:
                            alert["avg_daily_sales"] = avg_daily_sales
                    for alert in stock_alerts["warning"]:
                        if alert["name"] == trans.product_name:
                            alert["avg_daily_sales"] = avg_daily_sales

    for prod_name, metrics in product_metrics.items():
        if metrics["total_revenue"] > 0:
            metrics["profit_margin"] = (
                metrics["total_profit"] / metrics["total_revenue"] * 100
            )

    if len(daily_metrics) >= 2:
        dates = sorted(daily_metrics.keys())
        first_week = sum(
            daily_metrics[d]["sales"] for d in dates[: min(7, len(dates) // 2)]
        )
        last_week = sum(
            daily_metrics[d]["sales"] for d in dates[-min(7, len(dates) // 2) :]
        )
        first_week_days = min(7, len(dates) // 2)
        last_week_days = min(7, len(dates) // 2)

        if first_week_days > 0 and first_week > 0:
            sales_trend = (
                ((last_week / last_week_days) - (first_week / first_week_days))
                / (first_week / first_week_days)
                * 100
            )
        else:
            sales_trend = 0
    else:
        sales_trend = 0

    sorted_by_profit = sorted(
        product_metrics.items(), key=lambda x: x[1]["total_profit"], reverse=True
    )
    sorted_by_revenue = sorted(
        product_metrics.items(), key=lambda x: x[1]["total_revenue"], reverse=True
    )

    return {
        "stock_alerts": stock_alerts,
        "product_metrics": dict(product_metrics),
        "daily_metrics": dict(daily_metrics),
        "sales_trend": sales_trend,
        "best_performing": {
            "by_profit": sorted_by_profit[:3],
            "by_revenue": sorted_by_revenue[:3],
        },
        "days_analyzed": len(daily_metrics),
    }
