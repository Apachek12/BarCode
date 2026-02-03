import os
import requests
from urllib.parse import urlparse

# --- CONFIGURACIÓN ---
ARCHIVO_URLS = "urlsPDF.txt"
CARPETA_DESTINO = "PDFs" # Aquí se guardará todo

def descargar_pdfs():
    print("--- 1. ANALIZANDO EL ARCHIVO DE ENLACES ---")
    
    urls_para_descargar = set() # Usamos un set para evitar duplicados automáticamente

    try:
        with open(ARCHIVO_URLS, 'r', encoding='utf-8', errors='ignore') as f:
            lineas = f.readlines()
            
        for linea in lineas:
            # Tu archivo a veces tiene varias URLs separadas por comas
            partes = linea.split(',')
            for parte in partes:
                url_limpia = parte.strip()
                # Filtramos solo si es un PDF válido y empieza por http
                if url_limpia.lower().endswith('.pdf') and url_limpia.startswith('http'):
                    urls_para_descargar.add(url_limpia)
                    
    except FileNotFoundError:
        print(f"❌ No encuentro el archivo '{ARCHIVO_URLS}'")
        return

    total = len(urls_para_descargar)
    print(f"✅ Encontrados {total} PDFs únicos. Empezando descarga...\n")

    # --- 2. DESCARGA ---
    for i, url in enumerate(urls_para_descargar):
        try:
            # Analizamos la URL para sacar la estructura de carpetas
            # Ejemplo: https://web.com/media/folder/doc.pdf  -->  ruta: /media/folder/doc.pdf
            parsed_url = urlparse(url)
            ruta_en_servidor = parsed_url.path 
            
            # Quitamos la primera barra '/' para que os.path.join funcione bien
            if ruta_en_servidor.startswith('/'):
                ruta_en_servidor = ruta_en_servidor[1:]
            
            # Ruta completa en tu PC: "PDFs_Para_Github/media/folder/doc.pdf"
            ruta_destino_completa = os.path.join(CARPETA_DESTINO, ruta_en_servidor)
            
            # Obtenemos solo la carpeta (sin el archivo) para crearla si no existe
            carpeta_solo = os.path.dirname(ruta_destino_completa)
            
            if not os.path.exists(carpeta_solo):
                os.makedirs(carpeta_solo) # Crea todas las subcarpetas necesarias

            # Si el archivo ya existe, nos lo saltamos para ahorrar tiempo
            if not os.path.exists(ruta_destino_completa):
                print(f"⬇️ [{i+1}/{total}] Descargando: {os.path.basename(ruta_destino_completa)}")
                
                # Descarga con timeout de 20s por si un PDF es muy pesado
                response = requests.get(url, timeout=20)
                
                if response.status_code == 200:
                    with open(ruta_destino_completa, 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"   ❌ Error {response.status_code} en la web")
            else:
                print(f"⏩ [{i+1}/{total}] Ya existe: {os.path.basename(ruta_destino_completa)}")
                
        except Exception as e:
            print(f"   ❌ Error descargando {url}: {e}")

    print(f"\n🎉 ¡PROCESO TERMINADO!")
    print(f"Tus archivos están en la carpeta: {CARPETA_DESTINO}")
    print("Ahora puedes subir esa carpeta completa a GitHub.")

if __name__ == "__main__":
    descargar_pdfs()