from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
    QTableWidget,
    QTableWidgetItem
)

import data.app_state as app_state


class AcompanhamentoPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # ==========================================
        # TÍTULO
        # ==========================================

        titulo = QLabel("Acompanhamento Pedagógico")

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        subtitulo = QLabel(
            "Monitoramento detalhado por turma"
        )

        self.layout.addWidget(titulo)

        self.layout.addWidget(subtitulo)

        self.layout.addSpacing(20)

        # ==========================================
        # FILTRO
        # ==========================================

        self.filtro_turma = QComboBox()

        self.filtro_turma.currentTextChanged.connect(
            self.atualizar_dados
        )

        self.layout.addWidget(self.filtro_turma)

        # ==========================================
        # TABELA
        # ==========================================

        tabela_box = QFrame()

        tabela_box.setObjectName("card")

        tabela_layout = QVBoxLayout(tabela_box)

        tabela_titulo = QLabel(
            "Desempenho da Turma"
        )

        tabela_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.tabela = QTableWidget()

        tabela_layout.addWidget(tabela_titulo)

        tabela_layout.addWidget(self.tabela)

        self.layout.addWidget(tabela_box)

    # ==========================================
    # CARREGAR FILTROS
    # ==========================================

    def carregar_filtros(self):

        df = app_state.dados_importados

        if df is None:
            return

        self.filtro_turma.clear()

        turmas = sorted(df["Turma"].unique())

        self.filtro_turma.addItems(turmas)

    # ==========================================
    # ATUALIZAR DADOS
    # ==========================================

    def atualizar_dados(self):

        df = app_state.dados_importados

        if df is None:
            return

        turma = self.filtro_turma.currentText()

        if turma == "":
            return

        dados_turma = df[df["Turma"] == turma]

        self.tabela.setRowCount(
            dados_turma.shape[0]
        )

        self.tabela.setColumnCount(
            dados_turma.shape[1]
        )

        self.tabela.setHorizontalHeaderLabels(
            dados_turma.columns
        )

        for linha in range(dados_turma.shape[0]):

            for coluna in range(
                dados_turma.shape[1]
            ):

                valor = str(
                    dados_turma.iat[linha, coluna]
                )

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )