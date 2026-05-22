from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QFrame
)

import pandas as pd

import data.app_state as app_state

from services.analise_service import analisar_desempenho


class ImportPage(QWidget):

    def __init__(self, dashboard_page):
        super().__init__()

        self.dashboard_page = dashboard_page

        layout = QVBoxLayout(self)

        # TÍTULO
        titulo = QLabel("Importação de Dados")

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        descricao = QLabel(
            "Importe arquivos Excel para análise pedagógica"
        )

        # BOTÃO IMPORTAR
        self.botao_importar = QPushButton(
            "📥 Selecionar Planilha Excel"
        )

        self.botao_importar.clicked.connect(
            self.importar_excel
        )

        # TABELA
        self.tabela = QTableWidget()

        # ÁREA DE RESULTADOS
        self.resultado_box = QFrame()
        self.resultado_box.setObjectName("card")

        resultado_layout = QVBoxLayout(self.resultado_box)

        resultado_titulo = QLabel(
            "Diagnóstico Pedagógico"
        )

        resultado_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.resultado_label = QLabel(
            "Nenhuma análise realizada."
        )

        self.resultado_label.setWordWrap(True)

        resultado_layout.addWidget(resultado_titulo)
        resultado_layout.addWidget(self.resultado_label)

        # ADICIONAR COMPONENTES
        layout.addWidget(titulo)
        layout.addWidget(descricao)

        layout.addSpacing(20)

        layout.addWidget(self.botao_importar)

        layout.addSpacing(20)

        layout.addWidget(self.tabela)

        layout.addSpacing(20)

        layout.addWidget(self.resultado_box)

    def importar_excel(self):

        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if caminho_arquivo:

            # LER EXCEL
            df = pd.read_excel(caminho_arquivo)

            # REMOVER LINHAS VAZIAS
            df = df.dropna(how="all")

            # RESETAR ÍNDICE
            df = df.reset_index(drop=True)

            # SALVAR GLOBALMENTE
            app_state.dados_importados = df

            # CONFIGURAR TABELA
            self.tabela.setRowCount(df.shape[0])
            self.tabela.setColumnCount(df.shape[1])

            self.tabela.setHorizontalHeaderLabels(
                [str(col) for col in df.columns]
            )

            # PREENCHER TABELA
            for linha in range(df.shape[0]):

                for coluna in range(df.shape[1]):

                    valor = str(df.iat[linha, coluna])

                    self.tabela.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(valor)
                    )

            # REALIZAR ANÁLISE
            resultados = analisar_desempenho(df)

            # TEXO RESULTADOS
            if resultados:

                texto = "\n\n".join(resultados)

            else:

                texto = """
✅ Nenhum alerta pedagógico encontrado.

As turmas apresentam desempenho equilibrado.
"""

            # MOSTRAR RESULTADO
            self.resultado_label.setText(texto)

            # ATUALIZAR DASHBOARD
            self.dashboard_page.atualizar_dashboard()