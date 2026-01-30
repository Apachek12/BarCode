import requests
import os
import time

# CONFIGURACIÓN
ARCHIVO_URLS = 'urls.txt'  # Tu archivo único con los 26.000 enlaces
CARPETA_RAIZ = '.'         # Se guardan aquí mismo

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def descargar_unico():
    if not os.path.exists(ARCHIVO_URLS):
        print(f"ERROR: No encuentro el archivo {ARCHIVO_URLS}")
        return

    print(f"--- LEYENDO {ARCHIVO_URLS} ---")
    with open(ARCHIVO_URLS, 'r') as f:
        # Leemos y limpiamos líneas vacías de golpe
        urls = [line.strip() for line in f if line.strip()]

    print(f"Detectadas {len(urls)} imágenes. Iniciando descarga...")

    total_ok = 0
    total_error = 0

    for i, url in enumerate(urls):
        try:
            # 1. Definir ruta (ej: z/e/foto.jpg)
            if '/product/' in url:
                ruta_relativa = url.split('/product/')[-1]
            else:
                ruta_relativa = os.path.basename(url)

            ruta_completa = os.path.join(CARPETA_RAIZ, ruta_relativa)
            dir_destino = os.path.dirname(ruta_completa)

            # 2. SALTAR SI YA EXISTE (Vital para 26k archivos)
            if os.path.exists(ruta_completa) and os.path.getsize(ruta_completa) > 0:
                # Si ya la tienes, pasamos a la siguiente sin decir nada para ir rápido
                continue

            # 3. Crear carpetas
            if not os.path.exists(dir_destino):
                os.makedirs(dir_destino)

            # 4. Descargar
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                with open(ruta_completa, 'wb') as f:
                    f.write(response.content)
                print(f"[{i+1}/{len(urls)}] OK: {ruta_relativa}")
                total_ok += 1
            else:
                print(f"[{i+1}/{len(urls)}] ERROR {response.status_code}: {url}")
                total_error += 1

        except Exception as e:
            print(f"[{i+1}/{len(urls)}] FALLO: {e}")
            total_error += 1

    print(f"\n=== FINALIZADO ===")
    print(f"Descargadas nuevas: {total_ok}")
    print(f"Errores: {total_error}")
    print("Recuerda ejecutar: git add . / git commit -m 'fin' / git push origin main")

if __name__ == "__main__":
    descargar_unico()