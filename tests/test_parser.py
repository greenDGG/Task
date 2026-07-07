from parser import extract_task_number, extract_youtube_url

text = """🔠🔠🔠🔠🔠    2️⃣1️⃣
1. Abra la búsqueda de YouTube.

https://www.youtube.com/watch?v=pl16EsLpXxg


2. Puedes darle me gusta al video, tomar una captura de pantalla y enviarla al grupo.
3. El tiempo de trabajo es de 20 minutos.
4. Si tiene alguna pregunta en el trabajo, comuníquese con el personal de recepción.
5. Puede obtener 400 comisiones completando tareas que deben completarse continuamente y puede obtener 200 comisiones omitiendo tareas .
6. La siguiente tarea es a las  1️⃣8️⃣🔣0️⃣0️⃣"""

task_num = extract_task_number(text)
url = extract_youtube_url(text)

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== RESULTADOS ===")
print(f"Numero de tarea: {task_num}")
print(f"URL de YouTube: {url}")
print(f"\nEsperado: task=21, url=https://www.youtube.com/watch?v=pl16EsLpXxg")
