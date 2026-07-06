import streamlit as st
from PIL import Image
from fpdf import FPDF
import datetime
import os

# Configuración de la página web
st.set_page_config(page_title="Control de Camiones - Mayorista DyL", page_icon="🚛", layout="centered")

# --- ENCABEZADO FORMAL CON LOGO ---
col_logo, col_titulo = st.columns([1, 3])

with col_logo:
    # Intenta cargar el logo si está en la misma carpeta
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("🚛")

with col_titulo:
    st.markdown("<h1 style='color: #0b3c5d; margin-bottom: 0;'>Control de Camiones</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555; font-size: 14px; margin-top: 5px;'>Registro de Entrada/Salida y Respaldo Fotográfico</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 0; border: 1px solid #0b3c5d;'>", unsafe_allow_html=True)

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

st.markdown("### 📋 Control Logístico")
estado_mercaderia = st.selectbox("Estado de Mercadería", ["SIN OBSERVACIÓN", "CON MERMA", "DAÑADO", "FALTANTE"])
observaciones = st.text_area("Observaciones", placeholder="Escribe aquí cualquier detalle relevante...")

# --- CARGA DE MÚLTIPLES IMÁGENES ---
st.markdown("### 📸 Evidencia Fotográfica (Múltiples Fotos)")
fotos = st.file_uploader("Puedes arrastrar o seleccionar varias imágenes a la vez", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if fotos:
    st.write(f"📷 Imágenes cargadas: {len(fotos)}")
    # Muestra las imágenes en una cuadrícula limpia de 3 columnas en pantalla
    columnas_fotos = st.columns(3)
    for i, foto in enumerate(fotos):
        with columnas_fotos[i % 3]:
            st.image(foto, caption=f"Evidencia {i+1}", use_container_width=True)

st.markdown("<hr style='border: 0.5px solid #ccc;'>", unsafe_allow_html=True)

# --- GENERACIÓN DEL PDF Y GUARDADO ---
if st.button("💾 Guardar Registro y Generar PDF", type="primary"):
    if not patente or not proveedor:
        st.error("❌ Por favor, completa al menos la Patente y el Proveedor.")
    else:
        # Asegurar directorios
        if not os.path.exists("imagenes_camiones"): os.makedirs("imagenes_camiones")
        if not os.path.exists("registros_pdf"): os.makedirs("registros_pdf")

        # Guardar las imágenes localmente y guardar sus rutas
        rutas_imagenes = []
        for idx, foto in enumerate(fotos):
            img = Image.open(foto)
            # Asegurar formato RGB para evitar errores de PDF
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            ruta_img = f"imagenes_camiones/{patente}_{fecha}_{tipo_registro.lower()}_foto{idx+1}.jpg"
            img.save(ruta_img, "JPEG")
            rutas_imagenes.append(ruta_img)

        # Crear el PDF Estructurado y Formal
        pdf = FPDF()
        pdf.add_page()
        
        # Margen decorativo superior (Azul Corporativo)
        pdf.set_fill_color(11, 60, 93)
        pdf.rect(0, 0, 210, 8, "F")
        pdf.ln(5)
        
        # Agregar Logo al PDF si existe
        if os.path.exists("logo.png"):
            pdf.image("logo.png", x=10, y=15, w=25)
            pdf.set_x(40)
            y_inicial = 18
        else:
            pdf.set_x(10)
            y_inicial = 15
            
        # Encabezado del documento
        pdf.set_y(y_inicial)
        pdf.set_x(40 if os.path.exists("logo.png") else 10)
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(11, 60, 93)
        pdf.cell(150, 8, f"COMPROBANTE DE LOGÍSTICA - {tipo_registro.upper()}", ln=True)
        
        pdf.set_x(40 if os.path.exists("logo.png") else 10)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(150, 5, f"Mayorista DyL - Reporte generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        
        pdf.ln(12)
        pdf.set_text_color(0, 0, 0)
        
        # Tabla de Datos Formales
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(190, 8, " DATOS GENERALES DEL REGISTRO", ln=True, border=1, fill=True)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(45, 8, "Localidad / Sucursal:", border=1)
        pdf.cell(145, 8, f" {localidad}", border=1, ln=True)
        
        pdf.cell(45, 8, "Fecha de Registro:", border=1)
        pdf.cell(50, 8, f" {fecha}", border=1)
        pdf.cell(45, 8, "Patente Vehículo:", border=1)
        pdf.cell(50, 8, f" {patente}", border=1, ln=True)
        
        pdf.cell(45, 8, "Proveedor / Empresa:", border=1)
        pdf.cell(50, 8, f" {proveedor}", border=1)
        pdf.cell(45, 8, "N° Guía / Factura:", border=1)
        pdf.cell(50, 8, f" {n_guia}", border=1, ln=True)
        
        pdf.cell(45, 8, "Estado Mercadería:", border=1)
        pdf.cell(145, 8, f" {estado_mercaderia}", border=1, ln=True)
        
        pdf.ln(4)
        
        # Sección de Observaciones
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(190, 8, " OBSERVACIONES Y COMENTARIOS", ln=True, border=1, fill=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(190, 7, observaciones if observaciones else "Sin observaciones o incidencias particulares registradas.", border=1)
        
        # Sección de Fotos Ordenadas de a 2 por fila
        if rutas_imagenes:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(190, 8, " RESPALDO Y EVIDENCIA FOTOGRÁFICA", ln=True, border=1, fill=True)
            pdf.ln(4)
            
            # Algoritmo para acomodar las fotos ordenadamente en cuadrícula dentro del PDF
            ancho_foto = 90
            alto_foto = 65
            x_inicial = 10
            spacing = 10
            
            for i, ruta_img in enumerate(rutas_imagenes):
                # Si nos pasamos del alto de la página actual, creamos una nueva hoja
                if pdf.get_y() + alto_foto > 270:
                    pdf.add_page()
                    pdf.ln(5)
                
                # Calcular posiciones X e Y para hacer 2 columnas de fotos
                fila = i // 2
                columna = i % 2
                
                pos_x = x_inicial + (columna * (ancho_foto + spacing))
                
                # Ajustar la Y para la segunda fila de fotos en adelante
                if columna == 0 and i > 0:
                    pdf.ln(alto_foto + 5)
                    
                actual_y = pdf.get_y()
                pdf.image(ruta_img, x=pos_x, y=actual_y, w=ancho_foto, h=alto_foto)
                
            # Dejar espacio al final de las fotos
            pdf.set_y(pdf.get_y() + alto_foto + 10)

        # Guardar archivo PDF final en el servidor público
        nombre_pdf = f"registros_pdf/Registro_{patente}_{fecha}_{tipo_registro.lower()}.pdf"
        pdf.output(nombre_pdf)
        
        st.success(f"✅ ¡Registro y evidencias guardadas con éxito!")
        
        # Botón elegante para descargar
        with open(nombre_pdf, "rb") as f:
            st.download_button(
                label="📥 Descargar Reporte PDF Formal",
                data=f,
                file_name=os.path.basename(nombre_pdf),
                mime="application/pdf"
            )
