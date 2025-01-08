from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFrame,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QSplineSeries,
    QValueAxis,
    QDateTimeAxis,
)
from PySide6.QtGui import QPainter
from datetime import datetime
from collections import defaultdict

from src.style_config import Theme


class ChartTab(QWidget):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        colors = Theme.get_theme_colors()
        layout = QVBoxLayout(self)
        layout.setSpacing(5)

        # Control and Chart Card combined
        control_chart_card = QFrame(self)
        control_chart_card.setStyleSheet(
            f"QFrame {{ background-color: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 2px; }}"
        )
        control_chart_layout = QVBoxLayout(control_chart_card)

        # Control Layout
        control_layout = QHBoxLayout()

        # Year Selection
        year_widget = QFrame()
        year_widget.setStyleSheet("border: none;")
        year_layout = QVBoxLayout(year_widget)

        year_label = QLabel("Select Year")
        year_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 13px;")

        self.year_combo = QComboBox()
        current_year = datetime.now().year
        years = range(current_year - 5, current_year + 1)
        self.year_combo.addItems([str(year) for year in years])
        self.year_combo.setCurrentText(str(current_year))
        self.year_combo.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
                min-width: 100px;
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {colors['background']};
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {colors['text_primary']};
                margin-right: 5px;
            }}
            """
        )
        self.year_combo.currentTextChanged.connect(self.update_chart)

        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)
        control_layout.addWidget(year_widget)
        control_layout.addStretch()

        control_chart_layout.addLayout(control_layout)

        # Chart Container
        chart_layout = QVBoxLayout()

        # Setup Chart
        self.chart_view = self.setup_chart()
        chart_layout.addWidget(self.chart_view)

        control_chart_layout.addLayout(chart_layout)

        layout.addWidget(control_chart_card)

        self.update_chart()

    def setup_chart(self):
        colors = Theme.get_theme_colors()
        chart_theme = Theme.get_chart_theme()
        # Create Chart
        chart = QChart()
        chart.setBackgroundBrush(Qt.transparent)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(False)
        chart.setTheme(chart_theme)

        # Create Axes
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("MMM")
        self.axis_x.setLabelsColor(colors["text_primary"])
        self.axis_x.setGridLineColor(colors["border"])

        self.axis_y = QValueAxis()
        self.axis_y.setLabelsColor(colors["text_primary"])
        self.axis_y.setGridLineColor(colors["border"])
        self.axis_y.setLabelFormat("Rp%',.0f")

        chart.addAxis(self.axis_x, Qt.AlignBottom)
        chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Create Chart View
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(
            f"QChartView {{ background-color: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 2px; }}"
        )

        return chart_view

    def update_chart(self):
        colors = Theme.get_theme_colors()
        selected_year = int(self.year_combo.currentText())

        # Get transactions for the selected year
        start_date = datetime(selected_year, 1, 1)
        end_date = datetime(selected_year, 12, 31)
        transactions = self.transaction_manager.get_transactions_by_date_range(
            start_date, end_date
        )

        # Group transactions by month
        monthly_profits = defaultdict(float)
        monthly_revenue = defaultdict(float)

        for transaction in transactions:
            month = transaction.date.month
            monthly_profits[month] += float(transaction.profit)
            monthly_revenue[month] += float(transaction.total)

        # Create series
        profit_series = QSplineSeries()
        profit_series.setName("Monthly Profit")

        revenue_series = QSplineSeries()
        revenue_series.setName("Monthly Revenue")

        # Initialize min and max values
        min_value = float("inf")
        max_value = float("-inf")

        for month in range(1, 13):
            date = datetime(selected_year, month, 15)
            timestamp = int(datetime.timestamp(date) * 1000)
            profit_value = monthly_profits.get(month, 0)
            revenue_value = monthly_revenue.get(month, 0)

            profit_series.append(timestamp, profit_value)
            revenue_series.append(timestamp, revenue_value)

            min_value = min(min_value, profit_value, revenue_value)
            max_value = max(max_value, profit_value, revenue_value)

        # Ensure minimum value is non-negative
        min_value = min(min_value, 0)

        # Update chart
        chart = self.chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(profit_series)
        chart.addSeries(revenue_series)

        # Update axes
        start_date = datetime(selected_year, 1, 1)
        end_date = datetime(selected_year, 12, 31)

        self.axis_x.setRange(start_date, end_date)
        self.axis_y.setRange(min_value, max_value * 1.1)

        profit_series.attachAxis(self.axis_x)
        profit_series.attachAxis(self.axis_y)
        revenue_series.attachAxis(self.axis_x)
        revenue_series.attachAxis(self.axis_y)

        chart.setTitle(f"Monthly Sales Profit and Revenue - {selected_year}")
        # Customize Y-axis appearance
        self.axis_y.setLabelsColor(colors["text_primary"])

        self.axis_y.setGridLineColor(colors["border"])
        self.axis_y.setTickCount(11)
        self.axis_y.setMinorTickCount(4)

        # print("Transactions:", transactions)
        # print("Monthly Profits:", dict(monthly_profits))
        # print("Monthly Revenue:", dict(monthly_revenue))
        # print(f"Min Value: {min_value}, Max Value: {max_value}")
