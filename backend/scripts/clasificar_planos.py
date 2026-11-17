import glob

from app.engine.clasificador import clasificar_pdf

for ruta in sorted(glob.glob("../planos/*.pdf")):
    for pagina in clasificar_pdf(ruta):
        vistas = sorted(v.value for v in pagina.vistas)
        print(f"{pagina.archivo} | pág. {pagina.pagina} | {vistas}")