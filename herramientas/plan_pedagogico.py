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

def generar_con_ia(prompt: str) -> str:
    """Llama a Claude para generar contenido — modo simulado por ahora"""
    respuesta_simulada = f"""
ESTRATEGIAS DEL DOCENTE (D/):
- Presenta los conceptos mediante técnica expositiva dialogada, 
  usando ejemplos del sector turístico y agrícola de Guanacaste.
- Modela el análisis mediante casos reales de empresas guanacastecas.
- Facilita discusión grupal conectando el tema con la experiencia 
  laboral del grupo nocturno.
- Promueve la reflexión usando analogías con actividades cotidianas 
  de la zona costera.

ESTRATEGIAS DEL ESTUDIANTE (E/):
- Construye mapa conceptual sobre los temas abordados.
- Analiza casos prácticos relacionados con su entorno laboral.
- Participa en discusión grupal aportando experiencias propias.

EVIDENCIAS:
Conocimiento: Mapa conceptual sobre los temas de la unidad.
Desempeño: Exposición grupal con ejemplos de Guanacaste.
Producto: Cuadro comparativo elaborado en clase.
"""
    return respuesta_simulada

@mcp.tool()
def generar_plan_pedagogico(
    ruta_programa: str,
    ruta_plan_anual: str,
    subarea: str,
    nivel: str,
    modalidad: str,
    nombre_docente: str,
    nombre_institucion: str,
    caracteristicas_grupo: str
) -> str:
    """Genera un plan de práctica pedagógica MEP completo"""
    texto_programa = leer_pdf(ruta_programa)
    texto_plan_anual = leer_plan_anual(ruta_plan_anual)
    prompt = f"""
Sos un docente experto en educación técnica costarricense.
Generá estrategias de mediación pedagógica para un plan de 
práctica pedagógica del MEP con estas características:

Subárea: {subarea}
Nivel: {nivel}
Modalidad: {modalidad}
Institución: {nombre_institucion}
Docente: {nombre_docente}
Características del grupo: {caracteristicas_grupo}

Contenido del programa de estudio:
{texto_programa[:3000]}

Plan anual:
{texto_plan_anual[:1000]}

Generá:
1. Estrategias del DOCENTE (D/) — mínimo 4, contextualizadas 
   para Guanacaste, fomentando la Guanacastequidad
2. Estrategias del ESTUDIANTE (E/) — basadas en indicadores de logro
3. Evidencias — Conocimiento, Desempeño y Producto
"""
    return generar_con_ia(prompt)

if __name__ == "__main__":
    mcp.run()