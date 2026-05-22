from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout
)

from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import data.app_state as app_state


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(25, 25, 25, 25)

        self.layout.setSpacing(20)

        # =========================================
        # TÍTULO
        # =========================================

        titulo = QLabel("Resumo Geral")

        titulo.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        titulo.setAlignment(Qt.AlignCenter)

        subtitulo = QLabel(
            "Painel de diagnóstico pedagógico"
        )

        subtitulo.setStyleSheet("""
         font-size: 16px;
            color: #cfcfe8;
        """)

        subtitulo.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(titulo)

        self.layout.addWidget(subtitulo)

        self.layout.addSpacing(25)

        # =====================================
        # CARDS
        # =====================================

        cards_layout = QGridLayout()

        self.card_turmas = self.criar_card(
            "Turmas",
            "0"
        )

        self.card_alertas = self.criar_card(
            "Alertas",
            "0"
        )

        self.card_conteudos = self.criar_card(
            "Conteúdos",
            "0"
        )

        self.card_media = self.criar_card(
            "Média Geral",
            "0"
        )

        cards_layout.addWidget(self.card_turmas, 0, 0)

        cards_layout.addWidget(self.card_alertas, 0, 1)

        cards_layout.addWidget(self.card_conteudos, 0, 2)

        cards_layout.addWidget(self.card_media, 0, 3)

        self.layout.addLayout(cards_layout)

        self.layout.addSpacing(20)

        # =====================================
        # GRÁFICO
        # =====================================

        grafico_box = QFrame()

        grafico_box.setObjectName("card")

        grafico_layout = QVBoxLayout(grafico_box)

        grafico_titulo = QLabel(
            "Desempenho por Turma"
        )
        grafico_titulo.setAlignment(Qt.AlignCenter)

        grafico_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.figure = Figure(
            figsize=(10, 5)
        )

        self.canvas = FigureCanvas(self.figure)

        grafico_layout.addWidget(grafico_titulo)

        grafico_layout.addWidget(self.canvas)

        self.layout.addWidget(grafico_box)

        self.layout.addSpacing(20)

        # =====================================
        # INSIGHTS
        # =====================================

        self.insights_box = QFrame()

        self.insights_box.setObjectName("card")

        insights_layout = QVBoxLayout(
            self.insights_box
        )

        insights_titulo = QLabel(
            "Insights Pedagógicos"
        )
        insights_titulo.setAlignment(Qt.AlignCenter)

        insights_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.insights_label = QLabel(
            "Nenhuma análise disponível."
        )

        self.insights_label.setWordWrap(True)

        insights_layout.addWidget(insights_titulo)

        insights_layout.addWidget(
            self.insights_label
        )

        self.layout.addWidget(self.insights_box)

    # =====================================
    # CARD
    # =====================================

    def criar_card(self, titulo, valor):

        card = QFrame()

        card.setObjectName("card")

        card.setFixedHeight(180)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(15)

        layout.setAlignment(Qt.AlignCenter)

        titulo_label = QLabel(titulo)

        titulo_label.setStyleSheet("""
            font-size: 18px;
        """)

        valor_label = QLabel(valor)

        valor_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
        """)

        layout.addWidget(titulo_label)

        layout.addStretch()

        layout.addWidget(valor_label)

        card.valor_label = valor_label

        return card

    # =====================================
    # DASHBOARD
    # =====================================

    def atualizar_dashboard(self):

        df = app_state.dados_importados

        if df is None:
            return

        # =====================================
        # INDICADORES
        # =====================================

        total_turmas = df["Turma"].nunique()

        total_conteudos = df["Conteúdo"].nunique()

        media_geral = df["Média"].mean()

        alertas = df[df["Média"] < 5].shape[0]

        # =====================================
        # CARDS
        # =====================================

        self.card_turmas.valor_label.setText(
            str(total_turmas)
        )

        self.card_alertas.valor_label.setText(
            str(alertas)
        )

        self.card_conteudos.valor_label.setText(
            str(total_conteudos)
        )

        self.card_media.valor_label.setText(
            f"{media_geral:.1f}"
        )

        # =====================================
        # GRÁFICO
        # =====================================

        medias = (
            df.groupby("Turma")["Média"]
            .mean()
            .sort_values()
        )

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        barras = ax.bar(
            medias.index,
            medias.values
        )

        # CORES

        for barra, valor in zip(
            barras,
            medias.values
        ):

            if valor < 5:
                barra.set_color("#ff4d4d")

            elif valor < 6:
                barra.set_color("#ffc107")

            else:
                barra.set_color("#28a745")

        # LINHA MÉDIA

        ax.axhline(
            media_geral,
            linestyle="--"
        )

        ax.set_title(
            "Média por Turma",
            color="white"
        )

        ax.set_facecolor("#1e1e2f")

        self.figure.patch.set_facecolor(
            "#2b2b40"
        )

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        self.canvas.draw()

        # =====================================
        # INSIGHTS
        # =====================================

        pior_turma = medias.idxmin()

        melhor_turma = medias.idxmax()

        pior_media = medias.min()

        melhor_media = medias.max()

        conteudo_critico = (
            df.groupby("Conteúdo")["Média"]
            .mean()
            .idxmin()
        )

        insights = f"""
⚠️ Turma mais crítica: {pior_turma}
(Média: {pior_media:.1f})

🏆 Melhor turma: {melhor_turma}
(Média: {melhor_media:.1f})

📚 Conteúdo mais crítico:
{conteudo_critico}

📊 Média geral da escola:
{media_geral:.1f}
"""

        self.insights_label.setText(
            insights
        )