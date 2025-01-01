from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFrame,
    QLabel,
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QPainter
from datetime import datetime, timedelta
from collections import defaultdict
import calendar


class ChartTab(QWidget):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Control Card
        control_card = QFrame(self)
        control_card.setStyleSheet(
            "QFrame { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 8px; padding: 15px; }"
        )
        control_layout = QHBoxLayout(control_card)

        # Year Selection
        year_widget = QFrame()
        year_widget.setStyleSheet("border: none;")
        year_layout = QVBoxLayout(year_widget)

        year_label = QLabel("Select Year")
        year_label.setStyleSheet("color: #888888; font-size: 13px;")

        self.year_combo = QComboBox()
        current_year = datetime.now().year
        years = range(current_year - 5, current_year + 1)
        self.year_combo.addItems([str(year) for year in years])
        self.year_combo.setCurrentText(str(current_year))
        self.year_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                color: white;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #3c3c3c;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            """
        )
        self.year_combo.currentTextChanged.connect(self.update_chart)

        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)
        control_layout.addWidget(year_widget)
        control_layout.addStretch()

        # Chart Container
        chart_container = QFrame(self)
        chart_container.setStyleSheet(
            "QFrame { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 8px; padding: 15px; }"
        )
        chart_layout = QVBoxLayout(chart_container)

        # Create Chart
        self.chart_view = self.setup_chart()
        chart_layout.addWidget(self.chart_view)

        # Add to main layout
        layout.addWidget(control_card)
        layout.addWidget(chart_container, 1)  # 1 is stretch factor

        # Initial chart update
        self.update_chart()

    def setup_chart(self):
        # Create Chart
        chart = QChart()
        chart.setBackgroundBrush(Qt.transparent)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(False)
        chart.setTheme(QChart.ChartThemeDark)

        # Create Axes
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("MMM")
        self.axis_x.setLabelsColor("#ffffff")
        self.axis_x.setGridLineColor("#3c3c3c")

        self.axis_y = QValueAxis()
        self.axis_y.setLabelsColor("#ffffff")
        self.axis_y.setGridLineColor("#3c3c3c")
        self.axis_y.setLabelFormat("Rp%',.0f")

        chart.addAxis(self.axis_x, Qt.AlignBottom)
        chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Create Chart View
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def update_chart(self):
        selected_year = int(self.year_combo.currentText())

        # Get transactions for the selected year
        start_date = datetime(selected_year, 1, 1)
        end_date = datetime(selected_year, 12, 31)
        transactions = self.transaction_manager.get_transactions_by_date_range(
            start_date, end_date
        )

        # Group transactions by month
        monthly_profits = defaultdict(float)
        for transaction in transactions:
            month = transaction.date.month
            monthly_profits[month] += float(transaction.total)

        # Create series
        series = QLineSeries()
        series.setName("Monthly Profit")

        # Add data points for all months (including 0 for months without transactions)
        min_value = float("inf")
        max_value = float("-inf")

        for month in range(1, 13):
            date = datetime(selected_year, month, 15)  # middle of month
            timestamp = int(datetime.timestamp(date) * 1000)  # convert to milliseconds
            value = monthly_profits.get(month, 0)

            series.append(timestamp, value)

            min_value = min(min_value, value)
            max_value = max(max_value, value)

        # Update chart
        chart = self.chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        # Update axes
        start_date = datetime(selected_year, 1, 1)
        end_date = datetime(selected_year, 12, 31)

        self.axis_x.setRange(start_date, end_date)
        self.axis_y.setRange(0, max_value * 1.1)  # Add 10% padding

        series.attachAxis(self.axis_x)
        series.attachAxis(self.axis_y)

        # Set chart title
        chart.setTitle(f"Monthly Sales Profit - {selected_year}")
