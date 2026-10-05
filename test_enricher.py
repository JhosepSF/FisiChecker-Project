import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FisiChecker.settings')
django.setup()

from bs4 import BeautifulSoup
from audits.wcag.context import build_context
from audits.checks.criteria.registry import list_available_codes, get_check
from audits.wcag.enricher import enrich_all_criteria

html = """<!DOCTYPE html>
<html lang="es">
<head>
  <title>Portal de Prueba - Accesibilidad</title>
</head>
<body>
  <h1>Título Principal del Sitio</h1>
  <h2>Sección de Contenido</h2>
  <p>Texto de prueba con un <a href="#main">Ir al contenido</a> y otro enlace a <a href="https://ejemplo.com">haz clic aquí</a>.</p>
  
  <!-- Imágenes -->
  <img src="foto.jpg" alt="Persona usando computadora">
  <img src="decorativa.png" alt="">
  <img src="sin_alt.png">

  <!-- Formularios -->
  <form>
    <label for="nom">Nombre:</label>
    <input id="nom" name="name" autocomplete="name">
    <input id="clave" name="password" type="password">
    <button type="submit">Enviar formulario</button>
    <button></button>
  </form>

  <!-- IDs Duplicados -->
  <div id="elemento-duplicado">Uno</div>
  <span id="elemento-duplicado">Dos</span>
</body>
</html>"""

soup = BeautifulSoup(html, "html.parser")
ctx = build_context(soup)
codes = list_available_codes()
raw_outcomes = [get_check(c)(ctx) for c in codes]
enriched = enrich_all_criteria(soup, raw_outcomes, url="https://test.com")

print(f"Total criterios evaluados: {len(enriched)}")

# 1.1.1
c111 = next(o for o in enriched if o.code == "1.1.1")
print(f"\n[1.1.1] Veredicto: {c111.verdict} | Score: {c111.score_0_2}")
print(f"  Evidencias: {c111.details.get('evidences')}")
print(f"  Errores: {c111.details.get('errors')}")

# 2.4.4
c244 = next(o for o in enriched if o.code == "2.4.4")
print(f"\n[2.4.4] Veredicto: {c244.verdict} | Score: {c244.score_0_2}")
print(f"  Evidencias: {c244.details.get('evidences')}")
print(f"  Errores: {c244.details.get('errors')}")

# 3.1.1
c311 = next(o for o in enriched if o.code == "3.1.1")
print(f"\n[3.1.1] Veredicto: {c311.verdict} | Score: {c311.score_0_2}")
print(f"  Evidencias: {c311.details.get('evidences')}")

# 4.1.1
c411 = next(o for o in enriched if o.code == "4.1.1")
print(f"\n[4.1.1] Veredicto: {c411.verdict} | Score: {c411.score_0_2}")
print(f"  Errores: {c411.details.get('errors')}")

# 4.1.2
c412 = next(o for o in enriched if o.code == "4.1.2")
print(f"\n[4.1.2] Veredicto: {c412.verdict} | Score: {c412.score_0_2}")
print(f"  Errores: {c412.details.get('errors')}")

# 1.2.2 (Video no presente)
c122 = next(o for o in enriched if o.code == "1.2.2")
print(f"\n[1.2.2] Veredicto (sin videos): {c122.verdict} | Score: {c122.score_0_2}")
print(f"  Evidencias: {c122.details.get('evidences')}")
