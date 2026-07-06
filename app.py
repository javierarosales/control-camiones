import streamlit as st
from PIL import Image
from fpdf import FPDF
import datetime
import os

# Configuración de la página web
st.set_page_config(page_title="Control de Camiones", page_icon="🚛", layout="centered")

st.title("🚛 Control de Entrada y Salida de Camiones")
st.subheader("Versión Simplificada - Registro y Evidencia")
st.write("---")

# --- FORMULARIO DE ENTRADA DE DATOS ---
col1, col2 = st.columns(2)

with col1:
    tipo_registro = st.selectbox("Tipo de Registro", ["Entrada", "Salida"])
    localidad = st.selectbox("Localidad / Sucursal", ["MAYORISTA Dyl TALCA", "Santiago", "Concepción", "Antofagasta"])
    patente = st.text_input("Patente del Camión", placeholder="AA-BB-12 o AABB12").upper()

with col2:
    fecha = st.date_input("Fecha", datetime.date.today())
    proveedor = st.text_input("Proveedor / Empresa", placeholder="Ej: Transportes Express")
    n_guia = st.text_input("N° Guía / Factura", placeholder="Ej: 73250")

# Control Logístico Simplificado
st.markdown("### Control Logístico")
estado_mercaderia = st.selectbox("Estado de Mercadería", ["SIN OBSERVACIÓN", "CON MERMA", "DAÑADO", "FALTANTE"])
observaciones = st.text_area("Observaciones", placeholder="Escribe aquí cualquier detalle relevante...")

# Carga de Imagen / Evidencia
st.markdown("### Evidencia Fotográfica")
foto = st.file_uploader("Cargar imagen del camión o carga", type=["jpg", "jpeg", "png"])

if foto:
    st.image(foto, caption="Vista previa de la imagen cargada", use_container_width=True)

st.write("---")

# --- GENERACIÓN DEL PDF Y GUARDADO ---
if st.button("💾 Guardar Registro y Generar PDF", type="primary"):
    # Validación: campos obligatorios
    if not patente or not proveedor:
        st.error("❌ Por favor, completa al menos la Patente y el Proveedor.")
    else:
        # 1. Crear carpetas automáticamente si no existen
        if not os.path.exists("imagenes_camiones"):
            os.makedirs("imagenes_camiones")
        if not os.path.exists("registros_pdf"):
            os.makedirs("registros_pdf")

        # 2. Guardar la imagen localmente si el usuario subió una
        ruta_imagen = ""
        if foto is not None:
            img = Image.open(foto)
            # Guardamos la foto con un nombre limpio: PATENTE_FECHA_TIPO.png
            ruta_imagen = f"imagenes_camiones/{patente}_{fecha}_{tipo_registro.lower()}.png"
            img.save(ruta_imagen)

        # 3. Crear el documento PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        
        # Título en el PDF
        pdf.cell(190, 10, f"Control de {tipo_registro} - Camiones", ln=True, align="C")
        pdf.ln(10)
        
        # Tabla o cuadrícula con los datos del camión
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(95, 10, f"Localidad: {localidad}", border=1)
        pdf.cell(95, 10, f"Fecha: {fecha}", border=1, ln=True)
        
        pdf.cell(95, 10, f"Patente: {patente}", border=1)
        pdf.cell(95, 10, f"Proveedor: {proveedor}", border=1, ln=True)
        
        pdf.cell(190, 10, f"N° Guía / Factura: {n_guia}", border=1, ln=True)
        pdf.cell(190, 10, f"Estado Mercadería: {estado_mercaderia}", border=1, ln=True)
        
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(190, 10, "Observaciones:", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(190, 10, observaciones if observaciones else "Sin observaciones.", border=1)
        
        # Insertar la foto en el PDF si existe
        if ruta_imagen:
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(190, 10, "Evidencia Fotográfica:", ln=True)
            # Coloca la imagen debajo del texto de forma automática
            pdf.image(ruta_imagen, x=10, y=pdf.get_y() + 5, w=100)
        
        # Guardar el archivo PDF final en el disco duro
        nombre_pdf = f"registros_pdf/Registro_{patente}_{fecha}_{tipo_registro.lower()}.pdf"
        pdf.output(nombre_pdf)
        
        st.success(f"✅ ¡Registro guardado con éxito!")
        st.info(f"📄 Archivo guardado como: `{nombre_pdf}`")
        
        # Permitir descargar el PDF directamente desde la pantalla web
        with open(nombre_pdf, "rb") as f:
            st.download_button(
                label="📥 Descargar PDF Ahora",
                data=f,
                file_name=os.path.basename(nombre_pdf),
                mime="application/pdf"
            )