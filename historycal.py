from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton

class HistoryWindow(QWidget):
    def __init__(self, historylist=None):
        super().__init__()
        self.setWindowTitle("История")
        self.setGeometry(100, 100, 300, 400)

        # Основной макет
        layout = QVBoxLayout()

        # Список для отображения истории
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        # Кнопка закрытия
        self.close_b = QPushButton("Закрыть")
        self.close_b.clicked.connect(self.close)
        layout.addWidget(self.close_b)

        self.setLayout(layout)

        # Если передан список истории, обновляем его
        if historylist is not None and isinstance(historylist, list):
            self.update_history(historylist)

    def update_history(self, historylist):
        """Обновляет список истории."""
        if isinstance(historylist, list) and all(isinstance(item, str) for item in historylist):
            self.history_list.clear()
            self.history_list.addItems(historylist)
        else:
            raise ValueError("historylist должен быть списком строк!")

