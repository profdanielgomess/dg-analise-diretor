from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame
)

import data.app_state as app_state


class AnalisesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(25, 25, 25, 25)

        self.layout.setSpacing(20)

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel("🧠 IA Pedagógica")

        titulo.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        subtitulo = QLabel(
            "Análise inteligente do desempenho escolar"
        )

        self.layout.addWidget(titulo)

        self.layout.addWidget(subtitulo)

        self.layout.addSpacing(20)

        # =====================================
        # BOX IA
        # =====================================

        self.box = QFrame()

        self.box.setObjectName("card")

        box_layout = QVBoxLayout(self.box)

        titulo_box = QLabel(
            "Relatório Inteligente"
        )

        titulo_box.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        self.relatorio = QLabel(
            "Nenhuma análise disponível."
        )

        self.relatorio.setWordWrap(True)

        self.relatorio.setStyleSheet("""
            font-size: 16px;
            line-height: 1.8;
        """)

        box_layout.addWidget(titulo_box)

        box_layout.addWidget(self.relatorio)

        self.layout.addWidget(self.box)

    # =====================================
    # IA PEDAGÓGICA
    # =====================================

    def atualizar_analise(self):

        df = app_state.dados_importados

        if df is None:
            self.relatorio.setText(
                "Importe uma planilha primeiro."
            )
            return

        # =====================================
        # MÉDIAS
        # =====================================

        medias_turma = (
            df.groupby("Turma")["Média"]
            .mean()
            .sort_values()
        )

        pior_turma = medias_turma.idxmin()

        melhor_turma = medias_turma.idxmax()

        pior_media = medias_turma.min()

        melhor_media = medias_turma.max()

        media_geral = df["Média"].mean()

        conteudo_critico = (
            df.groupby("Conteúdo")["Média"]
            .mean()
            .idxmin()
        )

        total_alertas = (
            df[df["Média"] < 5]
            .shape[0]
        )

        # =====================================
        # CLASSIFICAÇÃO
        # =====================================

        if media_geral < 5:
            classificacao = "CRÍTICA"

        elif media_geral < 6:
            classificacao = "MODERADA"

        else:
            classificacao = "POSITIVA"

        # =====================================
        # RELATÓRIO
        # =====================================

        texto = f"""
🧠 RELATÓRIO PEDAGÓGICO AUTOMÁTICO

━━━━━━━━━━━━━━━━━━

📊 Média geral da escola:
{media_geral:.1f}

📚 Conteúdo mais crítico:
{conteudo_critico}

⚠️ Total de alertas pedagógicos:
{total_alertas}

━━━━━━━━━━━━━━━━━━

🏆 Melhor turma:
{melhor_turma}
(Média: {melhor_media:.1f})

🚨 Turma mais crítica:
{pior_turma}
(Média: {pior_media:.1f})

━━━━━━━━━━━━━━━━━━

📈 Classificação geral:
{classificacao}

━━━━━━━━━━━━━━━━━━

💡 Recomendações da IA:

• Intensificar reforço nas turmas críticas

• Aplicar revisão diagnóstica em:
{conteudo_critico}

• Criar monitoria pedagógica para:
{pior_turma}

• Manter estratégias aplicadas na turma:
{melhor_turma}

━━━━━━━━━━━━━━━━━━

🤖 Sistema DG Analytics
Análise Inteligente Educacional
"""

        self.relatorio.setText(texto)