# main.py

import io
from fastapi import FastAPI, Response, Query, HTTPException
from fastapi.responses import StreamingResponse
import qrcode
from PIL.Image import Image

# Crea la aplicación FastAPI
app = FastAPI(
    title="API de Códigos QR",
    description="Una API sencilla para generar códigos QR personalizados.",
    version="1.0.0",
)

@app.get("/generate-qr", 
         tags=["Generador QR"],
         summary="Genera un código QR a partir de un texto.",
         description="Este endpoint genera una imagen de código QR en formato PNG a partir de los datos proporcionados.")
def generate_qr_code(
    # Parámetros de la petición (Query Parameters)
    data: str = Query(..., description="El texto o URL a codificar en el QR."),
    box_size: int = Query(10, ge=1, le=100, description="Tamaño de cada 'caja' del QR."),
    border: int = Query(4, ge=0, le=50, description="Grosor del borde del QR."),
    fill_color: str = Query("black", description="Color del código QR (nombre o hexadecimal)."),
    back_color: str = Query("white", description="Color del fondo (nombre o hexadecimal).")
):
    """
    Genera un código QR con personalización y lo devuelve como una imagen PNG.
    """
    if not data:
        raise HTTPException(status_code=400, detail="El parámetro 'data' no puede estar vacío.")

    try:
        # Configuración del generador de QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )

        # Añadir los datos
        qr.add_data(data)
        qr.make(fit=True)

        # Crear la imagen del QR con los colores personalizados
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Guardar la imagen en un buffer de memoria en lugar de un archivo
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0) # Mover el cursor al inicio del buffer

        # Devolver la imagen como una respuesta HTTP
        # media_type="image/png" le dice al navegador que esto es una imagen
        return Response(content=buffer.getvalue(), media_type="image/png")

    except Exception as e:
        # Manejo de errores genéricos
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al generar el QR: {str(e)}")