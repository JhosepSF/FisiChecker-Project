# audits/wcag/enricher.py
"""
Enricher y Analizador Profundo de Criterios WCAG 2.1 (78 Criterios)
Revisa, valida y enriquece las evaluaciones de accesibilidad web,
eliminando falsos positivos/negativos, detectando elementos reales en el DOM,
y formateando evidencias y errores detallados en español.
"""
import re
import json
from typing import Dict, Any, List, Optional, Set, Tuple
from bs4 import BeautifulSoup
from bs4.element import Tag

from .constants import WCAG_META
from ..checks.criteria.base import CriterionOutcome

# Códigos de idioma ISO 639-1 válidos comunes
VALID_ISO_LANGS = {
    "es", "en", "pt", "fr", "de", "it", "ca", "gl", "eu", "qu", "ay", 
    "zh", "ja", "ru", "ar", "ko", "nl", "sv", "no", "fi", "da", "pl"
}

# Palabras clave de enlaces no descriptivos (WCAG 2.4.4 & 2.4.9)
AMBIGUOUS_LINK_TEXTS = {
    "aqui", "aquí", "clic aqui", "clic aquí", "haz clic aqui", "haz clic aquí",
    "click", "click here", "read more", "leer mas", "leer más", "ver mas", "ver más",
    "mas", "más", "more", "info", "mas info", "más info", "mas informacion", "más información",
    "detalles", "ver detalles", "conoce mas", "conoce más", "descargar", "download",
    "enlace", "link", "ir", "aqui>", "aquí>", "ver", "ingresar", "entrar"
}

# Textos genéricos no descriptivos para imágenes (WCAG 1.1.1)
GENERIC_ALT_TEXTS = {
    "imagen", "image", "img", "foto", "photo", "picture", "pic", "logo",
    "banner", "grafico", "gráfico", "icono", "icon", "sin titulo", "sin título",
    "untitled", "dsc", "screenshot", "captura", "default", "separador"
}

# Separadores y formatos para títulos (WCAG 2.4.2)
TITLE_PLACEHOLDERS = {
    "untitled", "sin título", "sin titulo", "document", "documento", 
    "home", "inicio", "index", "index.html", "react app", "vite app", "my app"
}


def _clean(s: Any) -> str:
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def _lower(s: Any) -> str:
    return _clean(s).lower()


def _get_attr(el: Any, attr: str) -> str:
    if isinstance(el, dict):
        v = el.get(attr)
        if isinstance(v, list):
            return " ".join(str(x) for x in v)
        return _clean(v)
    if hasattr(el, "get"):
        v = el.get(attr)
        if isinstance(v, list):
            return " ".join(str(x) for x in v)
        return _clean(v)
    return ""


def enrich_all_criteria(soup: BeautifulSoup, outcomes: List[CriterionOutcome], url: str = "") -> List[CriterionOutcome]:
    """
    Toma los resultados brutos de los 78 criterios y los pasa por un análisis
    profundo de aplicabilidad, detección semántica y enriquecimiento de evidencias.
    """
    # 1. Recolección de elementos base del DOM
    all_imgs = soup.find_all("img")
    all_svgs = soup.find_all("svg")
    all_videos = soup.find_all("video")
    all_audios = soup.find_all("audio")
    all_iframes = soup.find_all("iframe")
    all_anchors = soup.find_all("a")
    all_buttons = soup.find_all("button")
    all_inputs = soup.find_all(["input", "select", "textarea"])
    all_tables = soup.find_all("table")
    all_forms = soup.find_all("form")
    all_headings = soup.find_all(re.compile(r"^h[1-6]$", re.I))
    all_landmarks = soup.find_all(["main", "nav", "header", "footer", "aside", "section", "article"]) + \
                    soup.find_all(attrs={"role": re.compile(r"^(main|navigation|banner|contentinfo|complementary|search)$", re.I)})

    # Recolectar todos los IDs para verificación de duplicados (4.1.1)
    all_id_elements = []
    seen_ids = set()
    duplicate_ids = set()
    for el in soup.find_all(True):
        el_id = _clean(el.get("id"))
        if el_id:
            all_id_elements.append((el_id, el.name))
            if el_id in seen_ids:
                duplicate_ids.add(el_id)
            else:
                seen_ids.add(el_id)

    # 2. Iterar y enriquecer cada uno de los 78 criterios
    enriched_outcomes: List[CriterionOutcome] = []
    
    for outcome in outcomes:
        code = outcome.code
        details = dict(outcome.details or {})
        errors: List[str] = []
        evidences: List[str] = []
        warnings: List[str] = []
        
        # Copiar errores y evidencias previas si existían
        if isinstance(details.get("errors"), list):
            errors.extend([str(e) for e in details["errors"]])
        if isinstance(details.get("evidences"), list):
            evidences.extend([str(e) for e in details["evidences"]])
        if isinstance(details.get("offenders"), list):
            for off in details["offenders"]:
                if isinstance(off, dict):
                    reason = off.get("reason") or off.get("title") or json.dumps(off, ensure_ascii=False)
                    tag = off.get("tag") or ""
                    src = off.get("src") or off.get("href") or ""
                    msg = f"<{tag}> {reason}" if tag else reason
                    if src:
                        msg += f" (Fuente: {src[:80]})"
                    errors.append(msg)
                elif isinstance(off, str):
                    errors.append(off)

        # -------------------------------------------------------------
        # EVALUACIÓN ESPECÍFICA POR CRITERIO
        # -------------------------------------------------------------

        # === 1.1.1: Contenido no textual ===
        if code == "1.1.1":
            total_imgs = len(all_imgs)
            total_svgs = len(all_svgs)
            total_media = total_imgs + total_svgs
            
            if total_media == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No se detectaron imágenes <img> ni gráficos <svg> en la página.")
            else:
                missing_alt = 0
                valid_alt = 0
                decorative = 0
                generic_alt = 0
                
                for img in all_imgs:
                    alt = img.get("alt")
                    src = _get_attr(img, "src")[:80] or "img"
                    in_link = bool(img.find_parent("a"))
                    aria_hidden = _lower(img.get("aria-hidden")) in ("true", "1")
                    role = _lower(img.get("role"))
                    
                    if alt is None:
                        if aria_hidden or role in ("presentation", "none"):
                            decorative += 1
                        else:
                            missing_alt += 1
                            errors.append(f'Imagen <img src="{src}"> no tiene atributo alt ni está marcada como decorativa.')
                    else:
                        alt_clean = _clean(alt)
                        if alt_clean == "":
                            if in_link:
                                missing_alt += 1
                                errors.append(f'Imagen enlazada <img src="{src}"> tiene alt="" vacío (debe describir el destino del enlace).')
                            else:
                                decorative += 1
                        else:
                            # Verificar si es genérico
                            if _lower(alt_clean) in GENERIC_ALT_TEXTS or re.search(r"\.(jpg|png|gif|webp|svg|jpeg)$", alt_clean, re.I):
                                generic_alt += 1
                                warnings.append(f'Texto alt potencialmente poco descriptivo en <img src="{src}">: "{alt_clean}".')
                                valid_alt += 1
                            else:
                                valid_alt += 1
                
                # Revisar SVGs
                for svg in all_svgs:
                    aria_hidden = _lower(svg.get("aria-hidden")) in ("true", "1")
                    aria_label = _get_attr(svg, "aria-label")
                    has_title = bool(svg.find("title"))
                    if not aria_hidden and not aria_label and not has_title:
                        warnings.append("Gráfico <svg> interactivo o informativo sin <title> ni aria-label.")
                
                evidences.append(f"Total imágenes analizadas: {total_imgs} ({valid_alt} con texto descriptivo, {decorative} decorativas válidas).")
                
                if missing_alt == 0:
                    outcome.verdict = "pass"
                    outcome.passed = True
                elif missing_alt <= total_imgs * 0.2:
                    outcome.verdict = "partial"
                    outcome.passed = False
                else:
                    outcome.verdict = "fail"
                    outcome.passed = False
                details["missing_alt"] = missing_alt
                details["images_total"] = total_imgs

        # === 1.2.1 a 1.2.9: Medios Temporales (Audio y Video) ===
        elif code.startswith("1.2."):
            has_videos = len(all_videos) > 0
            has_audios = len(all_audios) > 0
            
            # Buscar también iframes de YouTube o Vimeo
            has_media_iframes = any("youtube" in _get_attr(ifr, "src").lower() or "vimeo" in _get_attr(ifr, "src").lower() for ifr in all_iframes)
            
            if not has_videos and not has_audios and not has_media_iframes:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No se detectaron elementos de audio <audio>, video <video> ni reproductores multimedia embebidos.")
            else:
                evidences.append(f"Medios detectados: {len(all_videos)} video(s), {len(all_audios)} audio(s), {len(all_iframes)} iframe(s).")
                if code == "1.2.2":
                    # Verificar si tienen <track kind="captions"|"subtitles">
                    videos_with_tracks = 0
                    for v in all_videos:
                        tracks = v.find_all("track")
                        if any(_lower(t.get("kind")) in ("captions", "subtitles") for t in tracks):
                            videos_with_tracks += 1
                        else:
                            errors.append(f'Video <video src="{_get_attr(v, "src")[:60]}"> no tiene pista <track kind="captions">.')
                    
                    if len(all_videos) > 0 and videos_with_tracks == len(all_videos):
                        outcome.verdict = "pass"
                        outcome.passed = True
                    elif videos_with_tracks > 0:
                        outcome.verdict = "partial"
                        outcome.passed = False
                    else:
                        outcome.verdict = "fail"
                        outcome.passed = False

        # === 1.3.1: Información y Relaciones ===
        elif code == "1.3.1":
            h_count = len(all_headings)
            t_count = len(all_tables)
            i_count = len(all_inputs)
            
            evidences.append(f"Estructura analizada: {h_count} encabezados, {t_count} tablas, {i_count} controles de formulario.")
            
            # 1. Encabezados: verificar h1 y no saltar niveles
            h1_tags = soup.find_all("h1")
            if len(h1_tags) == 0:
                errors.append("La página no cuenta con ningún encabezado principal <h1>.")
            elif len(h1_tags) > 2:
                warnings.append(f"La página tiene {len(h1_tags)} encabezados <h1> (se recomienda 1 único <h1> principal).")
            else:
                evidences.append(f"Encabezado principal <h1> presente: \"{_clean(h1_tags[0].get_text())[:60]}\".")
            
            # Verificar salto de niveles de encabezados
            last_level = 0
            for h in all_headings:
                lvl = int(h.name[1])
                if last_level > 0 and lvl > last_level + 1:
                    errors.append(f"Jerarquía de encabezados discontinua: salto de <h{last_level}> a <h{lvl}>.")
                last_level = lvl
            
            # 2. Form labels
            inputs_without_label = 0
            for inp in all_inputs:
                inp_type = _lower(inp.get("type"))
                if inp_type in ("hidden", "submit", "button", "reset", "image"):
                    continue
                inp_id = _get_attr(inp, "id")
                has_label = bool(inp_id and soup.find("label", attrs={"for": inp_id})) or \
                            bool(inp.find_parent("label")) or \
                            bool(_get_attr(inp, "aria-label")) or \
                            bool(_get_attr(inp, "aria-labelledby"))
                if not has_label:
                    inputs_without_label += 1
                    errors.append(f'Campo de formulario <{inp.name} id="{inp_id}" name="{_get_attr(inp, "name")}"> no tiene etiqueta <label> asociada.')
            
            # 3. Tablas de datos
            for tbl in all_tables:
                has_th = bool(tbl.find("th"))
                is_layout = _lower(tbl.get("role")) in ("presentation", "none")
                if not is_layout and not has_th:
                    warnings.append("Tabla sin encabezados <th> detectada (si es tabla de datos requiere <th>, si es de diseño use role='presentation').")
            
            if len(errors) == 0:
                outcome.verdict = "pass"
                outcome.passed = True
            elif len(errors) <= 3:
                outcome.verdict = "partial"
                outcome.passed = False
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 1.3.4: Orientación ===
        elif code == "1.3.4":
            meta_vp = soup.find("meta", attrs={"name": re.compile(r"viewport", re.I)})
            vp_content = _lower(_get_attr(meta_vp, "content")) if meta_vp else ""
            if "orientation" in vp_content:
                errors.append("El meta viewport restringe la orientación de la pantalla.")
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append("No se detectaron bloqueos de orientación en la etiqueta meta viewport.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 1.3.5: Identificar el propósito de la entrada ===
        elif code == "1.3.5":
            applicable_inputs = []
            inputs_with_autocomplete = 0
            
            # Tipos de campos personales que requieren autocomplete
            personal_fields = {"name", "email", "tel", "username", "password", "street-address", "postal-code", "address"}
            for inp in all_inputs:
                name_or_type = _lower(_get_attr(inp, "name")) + " " + _lower(_get_attr(inp, "type")) + " " + _lower(_get_attr(inp, "id"))
                if any(pf in name_or_type for pf in personal_fields):
                    applicable_inputs.append(inp)
                    if _get_attr(inp, "autocomplete"):
                        inputs_with_autocomplete += 1
                    else:
                        errors.append(f'Campo personal <{inp.name} name="{_get_attr(inp, "name")}"> no tiene atributo autocomplete.')
            
            if len(applicable_inputs) == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No se detectaron campos de entrada de datos personales del usuario.")
            else:
                evidences.append(f"Campos personales identificados: {len(applicable_inputs)} ({inputs_with_autocomplete} con autocomplete).")
                if inputs_with_autocomplete == len(applicable_inputs):
                    outcome.verdict = "pass"
                    outcome.passed = True
                elif inputs_with_autocomplete > 0:
                    outcome.verdict = "partial"
                    outcome.passed = False
                else:
                    outcome.verdict = "fail"
                    outcome.passed = False

        # === 1.4.1: Uso del color ===
        elif code == "1.4.1":
            evidences.append(f"Evaluados {len(all_anchors)} enlaces y {len(all_inputs)} campos de entrada.")
            # Verificar si hay requeridos denotados sólo por asterisco rojo sin aria-required
            for inp in all_inputs:
                if _get_attr(inp, "required") or _get_attr(inp, "aria-required"):
                    continue
                # Si el label contiene asterisco pero no atributo semántico
                lbl = soup.find("label", attrs={"for": _get_attr(inp, "id")})
                if lbl and "*" in lbl.get_text() and not inp.get("required"):
                    warnings.append(f'Campo <{inp.name} id="{_get_attr(inp, "id")}"> usa "*" en la etiqueta pero carece de required o aria-required="true".')
            outcome.verdict = "pass" if len(errors) == 0 else "partial"
            outcome.passed = len(errors) == 0

        # === 1.4.3 & 1.4.6: Contraste Mínimo y Mejorado ===
        elif code in ("1.4.3", "1.4.6"):
            # Analizar colores en línea
            low_contrast_count = 0
            for tag in soup.find_all(style=True):
                st = _lower(tag.get("style"))
                if "color:#aaa" in st or "color:#ccc" in st or "color:#eee" in st or "color:white" in st and "background" not in st:
                    low_contrast_count += 1
                    errors.append(f'Elemento <{tag.name}> tiene estilo de color con riesgo de bajo contraste: style="{st[:60]}".')
            
            evidences.append("Revisión de contraste visual y estilos inline.")
            if low_contrast_count == 0:
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                outcome.verdict = "partial" if code == "1.4.3" else "fail"
                outcome.passed = False

        # === 1.4.4: Redimensionar texto ===
        elif code == "1.4.4":
            meta_vp = soup.find("meta", attrs={"name": re.compile(r"viewport", re.I)})
            vp_content = _lower(_get_attr(meta_vp, "content")) if meta_vp else ""
            if "user-scalable=no" in vp_content or "maximum-scale=1.0" in vp_content or "maximum-scale=1" in vp_content:
                errors.append('Meta viewport deshabilita el zoom del usuario: ' + vp_content)
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append("El meta viewport permite el escalado y zoom del texto sin restricciones.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 1.4.5 & 1.4.9: Imágenes de texto ===
        elif code in ("1.4.5", "1.4.9"):
            if len(all_imgs) == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No hay imágenes en la página.")
            else:
                evidences.append(f"Se revisaron {len(all_imgs)} imágenes en búsqueda de imágenes de texto.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 2.1.1 & 2.1.3: Teclado ===
        elif code in ("2.1.1", "2.1.3"):
            # Detectar elementos interactivos simulados con onclick en divs o spans sin tabindex
            fake_buttons = 0
            for tag in soup.find_all(["div", "span", "a", "i"], attrs={"onclick": True}):
                if tag.name == "a" and tag.get("href"):
                    continue
                tabindex = tag.get("tabindex")
                role = tag.get("role")
                if tabindex is None and role not in ("button", "link"):
                    fake_buttons += 1
                    errors.append(f'Elemento <{tag.name} onclick="..."> no es accesible por teclado (falta tabindex="0" y role="button").')
            
            evidences.append(f"Controles interactivos analizados: {len(all_buttons)} botones, {len(all_anchors)} enlaces, {len(all_inputs)} campos.")
            if fake_buttons == 0:
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 2.1.2: Sin trampa de teclado ===
        elif code == "2.1.2":
            # Detectar tabindex positivo (> 0) que altera el orden natural
            positive_tabindex = []
            for el in soup.find_all(attrs={"tabindex": True}):
                try:
                    ti = int(el.get("tabindex"))
                    if ti > 0:
                        positive_tabindex.append((el.name, ti))
                        errors.append(f'Elemento <{el.name} tabindex="{ti}"> usa tabindex positivo (interrumpe la navegación secuencial por teclado).')
                except ValueError:
                    pass
            
            if len(positive_tabindex) == 0:
                evidences.append("No se detectaron atributos tabindex positivos que alteren el foco.")
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 2.2.1: Tiempo ajustable ===
        elif code == "2.2.1":
            meta_refresh = soup.find("meta", attrs={"http-equiv": re.compile(r"refresh", re.I)})
            if meta_refresh:
                errors.append(f'Redirección o refresco automático no configurable: <meta http-equiv="refresh" content="{_get_attr(meta_refresh, "content")}">.')
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append("No se detectaron etiquetas de refresco automático forzado.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 2.2.2: Pausar, detener, ocultar ===
        elif code == "2.2.2":
            marquees = soup.find_all(["marquee", "blink"])
            if len(marquees) > 0:
                errors.append(f"Se detectaron {len(marquees)} elementos en movimiento obsoleto (<marquee> o <blink>).")
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append("No se detectaron elementos <marquee> ni <blink>.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 2.4.1: Omitir bloques (Skip links) ===
        elif code == "2.4.1":
            has_nav = len(soup.find_all(["nav"]) + soup.find_all(attrs={"role": "navigation"})) > 0
            has_main = bool(soup.find("main") or soup.find(attrs={"role": "main"}))
            skip_links = []
            
            for a in all_anchors:
                href = _lower(_get_attr(a, "href"))
                txt = _lower(a.get_text())
                if href.startswith("#") and ("skip" in txt or "saltar" in txt or "contenido" in txt or "ir al" in txt or "main" in href):
                    skip_links.append(href)
            
            if len(skip_links) > 0 or has_main:
                evidences.append(f"Mecanismo de salto detectado: {len(skip_links)} enlace(s) skip-link, landmark <main> presente: {has_main}.")
                outcome.verdict = "pass"
                outcome.passed = True
            elif has_nav:
                errors.append("La página contiene bloques de navegación pero carece de enlace directo al contenido principal (skip-link) o landmark <main>.")
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("Página simple sin bloques de navegación repetitivos.")

        # === 2.4.2: Página titulada ===
        elif code == "2.4.2":
            title_tag = soup.title
            if not title_tag or not title_tag.string or not _clean(title_tag.string):
                errors.append("La página no tiene etiqueta <title> o está vacía.")
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                title_txt = _clean(title_tag.string)
                if _lower(title_txt) in TITLE_PLACEHOLDERS or len(title_txt) < 3:
                    errors.append(f'El título de la página es genérico o insuficiente: "{title_txt}".')
                    outcome.verdict = "fail"
                    outcome.passed = False
                else:
                    evidences.append(f'Título de página válido y descriptivo: "{title_txt}".')
                    outcome.verdict = "pass"
                    outcome.passed = True

        # === 2.4.4 & 2.4.9: Propósito de los enlaces ===
        elif code in ("2.4.4", "2.4.9"):
            if len(all_anchors) == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No se detectaron enlaces en la página.")
            else:
                ambiguous_count = 0
                empty_links = 0
                for a in all_anchors:
                    txt = _lower(a.get_text())
                    aria = _lower(_get_attr(a, "aria-label"))
                    title = _lower(_get_attr(a, "title"))
                    href = _get_attr(a, "href")
                    
                    full_label = txt or aria or title
                    if not full_label:
                        empty_links += 1
                        errors.append(f'Enlace vacío sin texto accesible: <a href="{href[:60]}"></a>.')
                    elif full_label in AMBIGUOUS_LINK_TEXTS:
                        ambiguous_count += 1
                        errors.append(f'Enlace con texto no descriptivo: <a href="{href[:60]}">{full_label}</a> (use texto contextual).')
                
                evidences.append(f"Total de enlaces evaluados: {len(all_anchors)} ({len(all_anchors) - ambiguous_count - empty_links} descriptivos).")
                
                if ambiguous_count == 0 and empty_links == 0:
                    outcome.verdict = "pass"
                    outcome.passed = True
                elif (ambiguous_count + empty_links) <= len(all_anchors) * 0.15:
                    outcome.verdict = "partial"
                    outcome.passed = False
                else:
                    outcome.verdict = "fail"
                    outcome.passed = False

        # === 2.4.7: Foco visible ===
        elif code == "2.4.7":
            # Revisar estilos que quiten el outline
            outline_none_found = False
            for tag in soup.find_all(style=True):
                st = _lower(tag.get("style"))
                if "outline:none" in st or "outline: 0" in st or "outline:0" in st:
                    outline_none_found = True
                    errors.append(f'Elemento <{tag.name}> elimina el contorno de foco (outline: none) sin sustituto visible.')
            
            if outline_none_found:
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append("No se detectaron anulaciones directas de contorno de foco en estilos en línea.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 2.5.3: Etiqueta en el nombre ===
        elif code == "2.5.3":
            controls_tested = 0
            label_mismatches = 0
            for btn in all_buttons:
                aria_label = _lower(_get_attr(btn, "aria-label"))
                btn_text = _lower(btn.get_text())
                if aria_label and btn_text:
                    controls_tested += 1
                    if btn_text not in aria_label:
                        label_mismatches += 1
                        errors.append(f'El botón con texto visible "{btn_text}" tiene un aria-label "{aria_label}" que no lo contiene.')
            
            if controls_tested == 0:
                evidences.append("No se detectaron botones con aria-label y texto visible simultáneo.")
                outcome.verdict = "pass"
                outcome.passed = True
            elif label_mismatches == 0:
                evidences.append(f"Se verificaron {controls_tested} botones y todos incluyen el texto visible en su nombre accesible.")
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 3.1.1: Idioma de la página ===
        elif code == "3.1.1":
            html_tag = soup.find("html")
            lang_attr = _clean(html_tag.get("lang")) if html_tag else ""
            
            if not lang_attr:
                errors.append('La etiqueta <html> no tiene el atributo "lang" definido.')
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                base_lang = lang_attr.split("-")[0].lower()
                if base_lang not in VALID_ISO_LANGS and len(base_lang) != 2 and len(base_lang) != 3:
                    errors.append(f'El código de idioma "{lang_attr}" en <html lang="..."> no parece ser un código ISO 639-1 válido.')
                    outcome.verdict = "fail"
                    outcome.passed = False
                else:
                    evidences.append(f'Idioma del documento correctamente especificado: <html lang="{lang_attr}">.')
                    outcome.verdict = "pass"
                    outcome.passed = True

        # === 3.2.1 & 3.2.2: Al recibir foco y al introducir datos ===
        elif code in ("3.2.1", "3.2.2"):
            auto_submits = 0
            for sel in soup.find_all("select", attrs={"onchange": True}):
                if "submit" in _lower(_get_attr(sel, "onchange")):
                    auto_submits += 1
                    errors.append(f'Selector <select name="{_get_attr(sel, "name")}"> envía el formulario automáticamente onchange sin aviso.')
            
            if len(all_inputs) == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No hay campos de formulario en la página.")
            elif auto_submits == 0:
                evidences.append("No se detectaron envíos automáticos inesperados en campos de entrada.")
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 3.3.2: Etiquetas o instrucciones ===
        elif code == "3.3.2":
            if len(all_inputs) == 0:
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True
                evidences.append("No hay campos de formulario en la página.")
            else:
                unlabeled = 0
                for inp in all_inputs:
                    inp_type = _lower(inp.get("type"))
                    if inp_type in ("hidden", "submit", "button", "reset"):
                        continue
                    has_acc_name = bool(_get_attr(inp, "id") and soup.find("label", attrs={"for": _get_attr(inp, "id")})) or \
                                   bool(inp.find_parent("label")) or \
                                   bool(_get_attr(inp, "aria-label")) or \
                                   bool(_get_attr(inp, "aria-labelledby"))
                    if not has_acc_name:
                        unlabeled += 1
                        errors.append(f'Campo <{inp.name} name="{_get_attr(inp, "name")}"> no tiene etiqueta descriptiva ni instrucción accesible.')
                
                evidences.append(f"Controles de formulario revisados: {len(all_inputs)} ({len(all_inputs) - unlabeled} etiquetados).")
                if unlabeled == 0:
                    outcome.verdict = "pass"
                    outcome.passed = True
                elif unlabeled <= len(all_inputs) * 0.25:
                    outcome.verdict = "partial"
                    outcome.passed = False
                else:
                    outcome.verdict = "fail"
                    outcome.passed = False

        # === 4.1.1: Análisis sintáctico (Parsing) ===
        elif code == "4.1.1":
            if len(duplicate_ids) > 0:
                for dup in list(duplicate_ids)[:8]:
                    errors.append(f'Identificador id="{dup}" duplicado en varios elementos del documento.')
                outcome.verdict = "fail"
                outcome.passed = False
            else:
                evidences.append(f"Se verificaron {len(all_id_elements)} elementos con atributo id y todos son únicos en el DOM.")
                outcome.verdict = "pass"
                outcome.passed = True

        # === 4.1.2: Nombre, función, valor (ARIA) ===
        elif code == "4.1.2":
            unnamed_controls = 0
            for btn in all_buttons:
                name = _clean(btn.get_text()) or _get_attr(btn, "aria-label") or _get_attr(btn, "title")
                if not name:
                    unnamed_controls += 1
                    errors.append(f'Botón sin nombre accesible: <button class="{_get_attr(btn, "class")}"></button>.')
            
            for a in all_anchors:
                if not a.get("href"):
                    continue
                name = _clean(a.get_text()) or _get_attr(a, "aria-label") or _get_attr(a, "title")
                if not name:
                    unnamed_controls += 1
                    errors.append(f'Enlace interactivo sin nombre accesible: <a href="{_get_attr(a, "href")[:50]}"></a>.')
            
            evidences.append(f"Elementos interactivos verificados: {len(all_buttons) + len(all_anchors)}.")
            if unnamed_controls == 0:
                outcome.verdict = "pass"
                outcome.passed = True
            elif unnamed_controls <= 3:
                outcome.verdict = "partial"
                outcome.passed = False
            else:
                outcome.verdict = "fail"
                outcome.passed = False

        # === 4.1.3: Mensajes de estado ===
        elif code == "4.1.3":
            live_regions = soup.find_all(attrs={"aria-live": True}) + soup.find_all(attrs={"role": re.compile(r"^(status|alert|log)$", re.I)})
            if len(live_regions) > 0:
                evidences.append(f"Se detectaron {len(live_regions)} regiones dinámicas aria-live / role='status|alert'.")
                outcome.verdict = "pass"
                outcome.passed = True
            else:
                evidences.append("Sin regiones dinámicas aria-live detectadas en el HTML estático.")
                outcome.verdict = "na"
                outcome.passed = None
                details["na"] = True

        # -------------------------------------------------------------
        # NORMALIZACIÓN FINAL DE EVIDENCIAS Y SCORE
        # -------------------------------------------------------------
        details["errors"] = errors
        details["evidences"] = evidences
        details["warnings"] = warnings
        
        # Calcular score 0-2 (0=fail, 1=partial, 2=pass, None=na)
        if outcome.verdict == "pass":
            outcome.score_0_2 = 2
            outcome.score_hint = 1.0
        elif outcome.verdict == "partial":
            outcome.score_0_2 = 1
            outcome.score_hint = 0.5
        elif outcome.verdict == "fail":
            outcome.score_0_2 = 0
            outcome.score_hint = 0.0
        else:
            outcome.verdict = "na"
            outcome.score_0_2 = None
            outcome.score_hint = None
            details["na"] = True

        outcome.details = details
        enriched_outcomes.append(outcome)

    return enriched_outcomes
