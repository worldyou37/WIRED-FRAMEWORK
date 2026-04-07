from fpdf import FPDF
import datetime
import os

class IntelligenceReporter(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Courier", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"CLASSIFIED // WIRED INTELLIGENCE PROTOCOL // {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} // TRACE_ID: {os.getpid()}", 0, 0, "C")

    def generate_intel_report(self, target, data_blocks):
        self.add_page()
        
        # Título Principal
        self.set_font("Courier", "B", 20)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, f"INTEL REPORT: {target}", 0, 1, "L")
        self.line(10, 32, 200, 32)
        self.ln(10)

        # Largura útil da página (Margens padrão: 10mm esquerda + 10mm direita = 190mm livres)
        effective_width = self.w - 20 

        for block in data_blocks:
            # Subtítulos de Seção
            self.set_fill_color(230, 230, 230)
            self.set_font("Courier", "B", 11)
            self.cell(0, 8, f" > {block['title'].upper()}", 1, 1, "L", fill=True)
            self.ln(3)

            # Conteúdo da Seção
            self.set_font("Courier", "", 9)
            content = block['content']
            
            if isinstance(content, list):
                for item in content:
                    # Usamos multi_cell com a largura efetiva para evitar estouro
                    self.multi_cell(effective_width, 5, f"[-] {str(item)}", border=0)
            elif isinstance(content, dict):
                for k, v in content.items():
                    # Trata dicionários aninhados (como os serviços do scanner)
                    text = f"[{k}]: {str(v)}"
                    # Limpeza de strings para evitar caracteres que o FPDF não gosta
                    text = text.encode('ascii', 'ignore').decode('ascii')
                    self.multi_cell(effective_width, 5, text, border=0)
                    self.ln(1)
            else:
                self.multi_cell(effective_width, 5, str(content), border=0)
            
            self.ln(5)

        # Salvamento
        folder = "relatorios"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = f"{target.replace('.', '-')}.pdf"
        filepath = os.path.join(folder, filename)
        
        try:
            self.output(filepath)
            return filepath
        except Exception as e:
            return f"Erro ao gerar arquivo: {e}"