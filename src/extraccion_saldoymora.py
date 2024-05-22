import fitz
import os
import pandas as pd

def extraer_saldoymora(archivo_pdf):
    saldoymora = []

    carpeta_imagenes = "saldo y mora"
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    documento = fitz.open(archivo_pdf)

    for pagina_numero in range(len(documento)):
        pagina = documento.load_page(pagina_numero)
        
        x0 = 360
        x1 = 500
        y0 = 70
        y1 = 120
            
        area_saldoymora = fitz.Rect(x0, y0, x1, y1)
        texto_saldoymora = pagina.get_text("text", clip=area_saldoymora)
        saldoymora.append(texto_saldoymora)

        pix = pagina.get_pixmap(clip=area_saldoymora, dpi=300)  
        nombre_imagen = f"{os.path.splitext(os.path.basename(archivo_pdf))[0]}.png"
        ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
        pix.save(ruta_imagen)

    lista_info = []
    for info in saldoymora:
        info_lines = info.strip().splitlines()
        info_stripped = [line.strip() for line in info_lines if line.strip()]
        lista_info.extend(info_stripped)

    patrones_excluir = ['*' , 'b' , '_' , 'E' , 'F']

    lista_filtrada = []

    for elemento in lista_info:
        if any(elemento.startswith(patron) for patron in patrones_excluir):
            continue
        lista_filtrada.append(elemento)

    nombre_base = os.path.splitext(os.path.basename(archivo_pdf))[0]
    archivo_csv = f"{nombre_base}.csv"

    df_nuevo = pd.DataFrame({'saldoymora': lista_filtrada})

    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv, encoding='utf-8')
        df_actualizado = pd.concat([df_existente, df_nuevo], axis=1)
    else:
        df_actualizado = df_nuevo

    df_actualizado.to_csv(archivo_csv, index=False, encoding='utf-8')