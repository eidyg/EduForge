import fitz
import os
from mcp.server.fastmcp import FastMCP
from docx import Document
from openpyxl import load_workbook

mcp = FastMCP("eduforge-plan-pedagogico")

def leer_pdf(ruta: str) -> str:
    """Lee un archivo PDF y devuelve todo su texto"""
    documento = fitz.open(ruta)
    texto = ""
    for pagina in documento:
        texto += pagina.get_text()
    documento.close()
    return texto

def leer_plan_anual(ruta: str) -> str:
    """Lee el plan anual en formato .docx o .xlsx"""
    extension = os.path.splitext(ruta)[1].lower()

    if extension == ".docx":
        documento = Document(ruta)
        texto = ""
        for parrafo in documento.paragraphs:
            texto += parrafo.text + "\n"
        return texto

    elif extension == ".xlsx":
        wb = load_workbook(ruta)
        texto = ""
        for hoja in wb.worksheets:
            for fila in hoja.iter_rows():
                for celda in fila:
                    if celda.value:
                        texto += str(celda.value) + " "
                texto += "\n"
        return texto

    else:
        return "Formato no soportado. Usá .docx o .xlsx"
if __name__ == "__main__":
    texto = leer_plan_anual("C:\\Users\\Eidy G\\Documents\\A2026\\PLANES MEP\\Cronogramas Anuales Configuracion y Soporte 2026.xlsx")
    print(texto[:500])