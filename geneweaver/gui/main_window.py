
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from geneweaver.system_info import get_gpu_info, get_system_metrics


class MetricCard(QFrame):
    def __init__(self, title, value="--", subtitle="Live system metric"):
        super().__init__()

        self.setObjectName("metricCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)

        title_label = QLabel(title)
        title_label.setObjectName("muted")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("metricValue")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("muted")

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(subtitle_label)

    def set_value(self, value):
        self.value_label.setText(value)


class GeneWeaverWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GeneWeaver | CRISPR Analysis")
        self.resize(1200, 760)
        self.setMinimumSize(950, 620)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #101722;
                color: #e8eef5;
                font-family: Segoe UI;
                font-size: 14px;
            }

            #sidebar {
                background-color: #172331;
                border-right: 1px solid #29394b;
            }

            #brand {
                color: #49d6df;
                font-size: 25px;
                font-weight: bold;
                padding: 12px;
            }

            QPushButton {
                background-color: transparent;
                color: #b8c7d8;
                border: none;
                text-align: left;
                padding: 13px 16px;
                border-radius: 7px;
            }

            QPushButton:hover {
                background-color: #26394b;
                color: white;
            }

            QPushButton:checked {
                background-color: #16475a;
                color: #60e0e5;
                font-weight: bold;
            }

            #pageTitle {
                font-size: 27px;
                font-weight: bold;
            }

            #muted {
                color: #91a4b8;
            }

            #metricCard, #contentCard {
                background-color: #192838;
                border: 1px solid #2b4053;
                border-radius: 12px;
            }

            #metricValue {
                color: #52d9df;
                font-size: 29px;
                font-weight: bold;
            }

            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
            }
        """)

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 15)

        brand = QLabel("GENEWEAVER")
        brand.setObjectName("brand")
        sidebar_layout.addWidget(brand)

        tagline = QLabel("CRISPR ANALYSIS ENGINE")
        tagline.setObjectName("muted")
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(30)

        self.stack = QStackedWidget()
        self.nav_buttons = []

        pages = [
            ("Overview", self.create_overview()),
            ("Sequence Analysis", self.create_placeholder(
                "Sequence Analysis",
                "FASTA input and sequence alignment workspace.",
                "FASTA parser and alignment engine will be connected here."
            )),
            ("Results", self.create_placeholder(
                "Analysis Results",
                "Review potential CRISPR off-target candidates.",
                "Result tables and scoring will appear here after implementation."
            )),
            ("Benchmarks", self.create_placeholder(
                "Performance Benchmarks",
                "Compare measured execution times across available backends.",
                "Benchmark results will appear here after implementation."
            )),
        ]

        for index, (name, page) in enumerate(pages):
            button = QPushButton(name)
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)
            self.stack.addWidget(page)

        sidebar_layout.addStretch()

        footer = QLabel("Development Build | v0.1")
        footer.setObjectName("muted")
        sidebar_layout.addWidget(footer)

        main_area = QWidget()
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(30, 25, 30, 25)

        main_layout.addWidget(self.stack)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(main_area, 1)

        self.change_page(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_metrics)
        self.timer.start(2000)

        self.refresh_metrics()

    def create_overview(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        title = QLabel("System Overview")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Monitor your system and access the GeneWeaver workspace."
        )
        description.setObjectName("muted")

        layout.addWidget(title)
        layout.addWidget(description)

        cards_layout = QHBoxLayout()

        self.cpu_card = MetricCard("CPU USAGE")
        self.ram_card = MetricCard("RAM USAGE")
        self.memory_card = MetricCard("MEMORY USED")

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.ram_card)
        cards_layout.addWidget(self.memory_card)

        layout.addLayout(cards_layout)

        system_card = QFrame()
        system_card.setObjectName("contentCard")
        system_layout = QVBoxLayout(system_card)

        system_heading = QLabel("Hardware Information")
        system_heading.setObjectName("sectionTitle")

        self.processor_label = QLabel("Processor: Detecting...")
        self.gpu_label = QLabel("GPU: Detecting...")

        self.processor_label.setWordWrap(True)
        self.gpu_label.setWordWrap(True)

        system_layout.addWidget(system_heading)
        system_layout.addWidget(self.processor_label)
        system_layout.addWidget(self.gpu_label)

        layout.addWidget(system_card)

        status_card = QFrame()
        status_card.setObjectName("contentCard")
        status_layout = QVBoxLayout(status_card)

        status_heading = QLabel("Development Status")
        status_heading.setObjectName("sectionTitle")

        status_text = QLabel(
            "Desktop interface: Running\n"
            "System monitoring: Active\n"
            "FASTA parser: Pending\n"
            "Alignment engine: Pending\n"
            "Off-target scoring: Pending"
        )

        status_layout.addWidget(status_heading)
        status_layout.addWidget(status_text)

        layout.addWidget(status_card)
        layout.addStretch()

        return page

    def create_placeholder(self, title_text, description, status):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel(title_text)
        title.setObjectName("pageTitle")

        description_label = QLabel(description)
        description_label.setObjectName("muted")

        card = QFrame()
        card.setObjectName("contentCard")

        card_layout = QVBoxLayout(card)

        status_label = QLabel(status)
        status_label.setWordWrap(True)

        card_layout.addWidget(status_label)

        layout.addWidget(title)
        layout.addWidget(description_label)
        layout.addSpacing(20)
        layout.addWidget(card)
        layout.addStretch()

        return page

    def change_page(self, index):
        self.stack.setCurrentIndex(index)

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

    def refresh_metrics(self):
        metrics = get_system_metrics()

        self.cpu_card.set_value(
            f"{metrics['cpu_percent']:.1f}%"
        )

        self.ram_card.set_value(
            f"{metrics['memory_percent']:.1f}%"
        )

        self.memory_card.set_value(
            f"{metrics['memory_used_gb']:.2f} GB"
        )

        self.processor_label.setText(
            f"Processor: {metrics['processor']}"
        )

        self.gpu_label.setText(
            "GPU: " + ", ".join(get_gpu_info())
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GeneWeaverWindow()
    window.show()

    sys.exit(app.exec())
