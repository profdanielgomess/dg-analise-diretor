from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget
)

from ui.dashboard_page import DashboardPage
from ui.import_page import ImportPage
from ui.acompanhamento_page import AcompanhamentoPage
from ui.analises_page import AnalisesPage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("📚  DG Analytics")

        self.resize(1400, 850)

        # =====================================
        # LAYOUT PRINCIPAL
        # =====================================

        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        # =====================================
        # MENU
        # =====================================

        menu = QFrame()

        menu.setObjectName("menu")

        menu.setFixedWidth(260)

        menu_layout = QVBoxLayout(menu)

        titulo = QLabel("DG Analytics")

        titulo.setObjectName("titulo")

        menu_layout.addWidget(titulo)

        menu_layout.addSpacing(20)

        # =====================================
        # BOTÕES
        # =====================================

        self.dashboard_btn = QPushButton(
            "📊 Resumo Geral"
        )

        self.importar_btn = QPushButton(
            "📥 Importar Dados"
        )

        self.acompanhamento_btn = QPushButton(
            "📈 Acompanhamento"
        )

        self.analise_btn = QPushButton(
            "🧠 Análises"
        )

        menu_layout.addWidget(self.dashboard_btn)

        menu_layout.addWidget(self.importar_btn)

        menu_layout.addWidget(self.acompanhamento_btn)

        menu_layout.addWidget(self.analise_btn)

        menu_layout.addStretch()

        # =====================================
        # PÁGINAS
        # =====================================

        self.paginas = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.import_page = ImportPage(
            self.dashboard_page
        )

        self.acompanhamento_page = (
            AcompanhamentoPage()
        )

        self.analises_page = AnalisesPage()

        # =====================================
        # ADD PÁGINAS
        # =====================================

        self.paginas.addWidget(
            self.dashboard_page
        )

        self.paginas.addWidget(
            self.import_page
        )

        self.paginas.addWidget(
            self.acompanhamento_page
        )

        self.paginas.addWidget(
            self.analises_page
        )

        # =====================================
        # EVENTOS
        # =====================================

        self.dashboard_btn.clicked.connect(
            self.abrir_dashboard
        )

        self.importar_btn.clicked.connect(
            self.abrir_importacao
        )

        self.acompanhamento_btn.clicked.connect(
            self.abrir_acompanhamento
        )

        self.analise_btn.clicked.connect(
            self.abrir_analises
        )

        # =====================================
        # LAYOUT FINAL
        # =====================================

        main_layout.addWidget(menu)

        main_layout.addWidget(
            self.paginas,
            1
        )

        self.abrir_dashboard()

    # =====================================
    # DASHBOARD
    # =====================================

    def abrir_dashboard(self):

        self.dashboard_page.atualizar_dashboard()

        self.paginas.setCurrentIndex(0)

    # =====================================
    # IMPORTAÇÃO
    # =====================================

    def abrir_importacao(self):

        self.paginas.setCurrentIndex(1)

    # =====================================
    # ACOMPANHAMENTO
    # =====================================

    def abrir_acompanhamento(self):

        self.acompanhamento_page.carregar_filtros()

        self.acompanhamento_page.atualizar_dados()

        self.paginas.setCurrentIndex(2)

    # =====================================
    # IA PEDAGÓGICA
    # =====================================

    def abrir_analises(self):

        self.analises_page.atualizar_analise()

        self.paginas.setCurrentIndex(3)