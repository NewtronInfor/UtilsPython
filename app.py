import streamlit as st
from PIL import Image
import io
import zipfile

def reducir_calidad(imagen, calidad):
    """
    Reduce la calidad de una imagen y la devuelve como un objeto BytesIO.
    
    :param imagen: Imagen de Pillow.
    :param calidad: Nivel de calidad de la imagen (1 a 100).
    :return: Objeto BytesIO de la imagen con calidad reducida.
    """
    buffer = io.BytesIO()
    imagen.save(buffer, format="JPEG", quality=calidad, optimize=True)
    buffer.seek(0)
    return buffer

def convertir_formato(imagen, formato):
    """
    Convierte el formato de una imagen y la devuelve como un objeto BytesIO.
    
    :param imagen: Imagen de Pillow.
    :param formato: Formato al que se convertirá la imagen (por ejemplo, 'PNG', 'JPEG').
    :return: Objeto BytesIO de la imagen en el nuevo formato.
    """
    if formato == "PNG" and imagen.mode in ["CMYK", "P"]:
        imagen = imagen.convert("RGB")
    
    buffer = io.BytesIO()
    imagen.save(buffer, format=formato)
    buffer.seek(0)
    return buffer

st.title("Herramientas de Procesamiento de Imágenes")

opcion = st.sidebar.selectbox("Selecciona una opción", ["Reducir Calidad", "Convertir Formato"])

if opcion == "Reducir Calidad":
    st.subheader("Reductor de Calidad de Imágenes")
    
    uploaded_files = st.file_uploader("Sube imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        calidad = st.slider("Selecciona la calidad de la imagen", min_value=1, max_value=100, value=10)
        
        archivos_zip = []
        
        for uploaded_file in uploaded_files:
            imagen = Image.open(uploaded_file)
            imagen_reducida = reducir_calidad(imagen, calidad)
            
            archivo_reducido = io.BytesIO(imagen_reducida.getvalue())
            archivo_reducido.name = f"{uploaded_file.name}"
            archivos_zip.append((archivo_reducido.name, archivo_reducido))
            
            st.image(imagen, caption=f"Imagen Original: {uploaded_file.name}", use_column_width=True)
            st.image(imagen_reducida, caption=f"Imagen con Calidad Reducida: {uploaded_file.name}", use_column_width=True)
        
        if archivos_zip:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for nombre, archivo in archivos_zip:
                    archivo.seek(0)  # Asegúrate de leer desde el inicio del archivo BytesIO
                    zip_file.writestr(nombre, archivo.read())
            
            zip_buffer.seek(0)
            
            st.download_button(
                label="Descargar Todas las Imágenes Reducidas en ZIP",
                data=zip_buffer,
                file_name="imagenes_reducidas.zip",
                mime="application/zip"
            )
    
elif opcion == "Convertir Formato":
    st.subheader("Conversión de Formato de Imágenes")
    
    uploaded_files = st.file_uploader("Sube imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        formato_destino = st.selectbox("Selecciona el formato al que convertir", ["PNG", "JPEG"])
        
        archivos_zip = []
        
        for uploaded_file in uploaded_files:
            imagen = Image.open(uploaded_file)
            imagen_convertida = convertir_formato(imagen, formato_destino)
            
            archivo_convertido = io.BytesIO(imagen_convertida.getvalue())
            archivo_convertido.name = f"{uploaded_file.name.rsplit('.', 1)[0]}.{formato_destino.lower()}"
            archivos_zip.append((archivo_convertido.name, archivo_convertido))
            
            st.image(imagen, caption=f"Imagen Original: {uploaded_file.name}", use_column_width=True)
            st.image(imagen_convertida, caption=f"Imagen Convertida a {formato_destino}: {uploaded_file.name.rsplit('.', 1)[0]}.{formato_destino.lower()}", use_column_width=True)
        
        if archivos_zip:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for nombre, archivo in archivos_zip:
                    archivo.seek(0)  # Asegúrate de leer desde el inicio del archivo BytesIO
                    zip_file.writestr(nombre, archivo.read())
            
            zip_buffer.seek(0)
            
            st.download_button(
                label="Descargar Todas las Imágenes Convertidas en ZIP",
                data=zip_buffer,
                file_name="imagenes_convertidas.zip",
                mime="application/zip"
            )
