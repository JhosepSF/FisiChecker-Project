/**
 * FisiChecker - Panel & Audit Client Script
 */

// ========= WCAG Metadata en Español & Explicaciones =========
const WCAG_META_ES = {
  // P1 – Perceptible
  "1.1.1": { title: "Contenido no textual", level: "A", principle: "Perceptible", explain: "Revisa que las imágenes y elementos no textuales tengan alternativa de texto adecuada o rol decorativo para lectores de pantalla." },
  "1.2.1": { title: "Solo audio y solo vídeo (pregrabado)", level: "A", principle: "Perceptible", explain: "Verifica alternativas para contenido solo de audio o vídeo pregrabado." },
  "1.2.2": { title: "Subtítulos (pregrabado)", level: "A", principle: "Perceptible", explain: "Verifica que los videos pregrabados con audio incluyan subtítulos sincronizados." },
  "1.2.3": { title: "Audiodescripción o alternativa multimedia", level: "A", principle: "Perceptible", explain: "Verifica que exista audiodescripción o alternativa textual completa para contenido multimedia." },
  "1.2.4": { title: "Subtítulos (en directo)", level: "AA", principle: "Perceptible", explain: "Revisa subtítulos para transmisiones en directo." },
  "1.2.5": { title: "Audiodescripción (pregrabado)", level: "AA", principle: "Perceptible", explain: "Verifica audiodescripción en vídeos pregrabados." },
  "1.2.6": { title: "Lengua de señas (pregrabado)", level: "AAA", principle: "Perceptible", explain: "Verifica interpretación en lengua de señas para audio pregrabado." },
  "1.2.7": { title: "Audiodescripción extendida", level: "AAA", principle: "Perceptible", explain: "Verifica audiodescripción extendida cuando las pausas normales son insuficientes." },
  "1.2.8": { title: "Alternativa para medios (pregrabado)", level: "AAA", principle: "Perceptible", explain: "Revisa transcripción descriptiva completa para vídeos." },
  "1.2.9": { title: "Solo audio (en directo)", level: "AAA", principle: "Perceptible", explain: "Verifica alternativas para transmisiones en directo de solo audio." },
  "1.3.1": { title: "Información y relaciones", level: "A", principle: "Perceptible", explain: "Verifica el uso correcto de encabezados (h1-h6), listas, tablas estructuradas y etiquetas semánticas." },
  "1.3.2": { title: "Secuencia significativa", level: "A", principle: "Perceptible", explain: "Verifica que el orden en el DOM coincida con el orden de lectura y comprensión lógica." },
  "1.3.3": { title: "Características sensoriales", level: "A", principle: "Perceptible", explain: "Revisa que las instrucciones no dependan exclusivamente de forma, tamaño, ubicación o sonido." },
  "1.3.4": { title: "Orientación", level: "AA", principle: "Perceptible", explain: "Verifica que el contenido no restrinja la visualización a una única orientación (vertical/horizontal)." },
  "1.3.5": { title: "Identificar el propósito de la entrada", level: "AA", principle: "Perceptible", explain: "Comprueba el uso de autocompletado estándar (autocomplete) en campos de formularios personales." },
  "1.3.6": { title: "Identificar el propósito", level: "AAA", principle: "Perceptible", explain: "Verifica el uso de landmarks e iconos con significado identificable por software." },
  "1.4.1": { title: "Uso del color", level: "A", principle: "Perceptible", explain: "Comprueba que el color no sea el único medio visual para transmitir información o acciones." },
  "1.4.2": { title: "Control de audio", level: "A", principle: "Perceptible", explain: "Verifica que el audio automático que dura más de 3 segundos se pueda pausar o detener." },
  "1.4.3": { title: "Contraste (mínimo)", level: "AA", principle: "Perceptible", explain: "Verifica que el texto estándar tenga una relación de contraste mínima de 4.5:1 (3:1 para texto grande)." },
  "1.4.4": { title: "Redimensionar texto", level: "AA", principle: "Perceptible", explain: "Comprueba que el texto pueda aumentarse hasta un 200% sin pérdida de contenido ni funcionalidad." },
  "1.4.5": { title: "Imágenes de texto", level: "AA", principle: "Perceptible", explain: "Verifica que se utilice texto real en lugar de imágenes de texto siempre que sea posible." },
  "1.4.6": { title: "Contraste (mejorado)", level: "AAA", principle: "Perceptible", explain: "Verifica una relación de contraste mejorada de al menos 7:1 para texto estándar." },
  "1.4.7": { title: "Audio de fondo bajo o inexistente", level: "AAA", principle: "Perceptible", explain: "Verifica que el audio de fondo no interfiera con el diálogo." },
  "1.4.8": { title: "Presentación visual", level: "AAA", principle: "Perceptible", explain: "Verifica personalización visual de bloques de texto (ancho, justificación, espaciado)." },
  "1.4.9": { title: "Imágenes de texto (sin excepción)", level: "AAA", principle: "Perceptible", explain: "Verifica que no se usen imágenes de texto excepto cuando sea esencial." },
  "1.4.10": { title: "Reflow (Diseño adaptable)", level: "AA", principle: "Perceptible", explain: "Comprueba que la página no requiera desplazamiento en dos dimensiones a 320px de ancho." },
  "1.4.11": { title: "Contraste no textual", level: "AA", principle: "Perceptible", explain: "Verifica que los componentes de la interfaz e iconos clave tengan un contraste de 3:1 con el fondo." },
  "1.4.12": { title: "Espaciado de texto", level: "AA", principle: "Perceptible", explain: "Comprueba que no se trunque contenido al ajustar interlineado y espaciado de letras/palabras." },
  "1.4.13": { title: "Contenido al pasar el cursor o al enfocar", level: "AA", principle: "Perceptible", explain: "Verifica que tooltips y menús desplegables sean descartables y permanentes mientras el cursor está encima." },

  // P2 – Operable
  "2.1.1": { title: "Teclado", level: "A", principle: "Operable", explain: "Verifica que todas las funciones interactivas sean accesibles y operables mediante el teclado." },
  "2.1.2": { title: "Sin trampa de teclado", level: "A", principle: "Operable", explain: "Comprueba que el foco del teclado no quede atrapado en ningún componente." },
  "2.1.3": { title: "Teclado (sin excepción)", level: "AAA", principle: "Operable", explain: "Verifica acceso completo por teclado sin excepciones de pulsaciones cronometradas." },
  "2.1.4": { title: "Atajos de teclas de un carácter", level: "A", principle: "Operable", explain: "Verifica que los atajos de teclado de un solo carácter puedan desactivarse o reconfigurarse." },
  "2.2.1": { title: "Tiempo ajustable", level: "A", principle: "Operable", explain: "Comprueba que los límites de tiempo puedan apagarse, ajustarse o extenderse por el usuario." },
  "2.2.2": { title: "Pausar, detener, ocultar", level: "A", principle: "Operable", explain: "Verifica que animaciones y carruseles automáticos cuenten con botón para pausar o detener." },
  "2.2.3": { title: "Sin temporización", level: "AAA", principle: "Operable", explain: "Verifica que la página no tenga límite de tiempo para completar tareas." },
  "2.2.4": { title: "Interrupciones", level: "AAA", principle: "Operable", explain: "Verifica que las alertas o interrupciones puedan posponerse o suprimirse." },
  "2.2.5": { title: "Reautenticación", level: "AAA", principle: "Operable", explain: "Permite continuar sin pérdida de datos tras expirar una sesión." },
  "2.2.6": { title: "Exclusiones de temporización", level: "AAA", principle: "Operable", explain: "Advierte a los usuarios sobre la duración de la inactividad que causará pérdida de datos." },
  "2.3.1": { title: "Tres destellos o por debajo del umbral", level: "A", principle: "Operable", explain: "Verifica que ningún elemento parpadee más de tres veces por segundo para evitar convulsiones." },
  "2.3.2": { title: "Tres destellos", level: "AAA", principle: "Operable", explain: "Verifica ausencia total de elementos con más de 3 destellos por segundo." },
  "2.3.3": { title: "Animación por interacción", level: "AAA", principle: "Operable", explain: "Verifica que la animación causada por interacción pueda desactivarse (prefers-reduced-motion)." },
  "2.4.1": { title: "Omitir bloques (Skip links)", level: "A", principle: "Operable", explain: "Verifica la existencia de un enlace visible al inicio para saltar directamente al contenido principal." },
  "2.4.2": { title: "Página titulada", level: "A", principle: "Operable", explain: "Comprueba que la página tenga una etiqueta <title> descriptiva y no vacía." },
  "2.4.3": { title: "Orden del foco", level: "A", principle: "Operable", explain: "Verifica que el orden de navegación por tabulador sea secuencial y coherente." },
  "2.4.4": { title: "Propósito de los enlaces (en contexto)", level: "A", principle: "Operable", explain: "Comprueba que los enlaces tengan textos descriptivos claros (evitando 'clic aquí' o enlaces vacíos)." },
  "2.4.5": { title: "Múltiples maneras", level: "AA", principle: "Operable", explain: "Verifica que existan varios métodos para localizar páginas (buscador, menú, mapa de sitio)." },
  "2.4.6": { title: "Encabezados y etiquetas", level: "AA", principle: "Operable", explain: "Comprueba que los encabezados y etiquetas describan con claridad el tema o propósito del campo." },
  "2.4.7": { title: "Foco visible", level: "AA", principle: "Operable", explain: "Verifica que el indicador de foco del teclado sea claramente visible en elementos interactivos." },
  "2.4.8": { title: "Ubicación", level: "AAA", principle: "Operable", explain: "Verifica que existan migas de pan (breadcrumbs) o indicadores de ubicación actual." },
  "2.4.9": { title: "Propósito de los enlaces (solo enlace)", level: "AAA", principle: "Operable", explain: "Verifica que el texto de cada enlace por sí solo identifique su destino." },
  "2.4.10": { title: "Encabezados de sección", level: "AAA", principle: "Operable", explain: "Verifica el uso de encabezados para estructurar las secciones de contenido." },
  "2.5.1": { title: "Gestos del puntero", level: "A", principle: "Operable", explain: "Verifica que las funciones que usan gestos complejos puedan ejecutarse con un solo toque o clic." },
  "2.5.2": { title: "Cancelación del puntero", level: "A", principle: "Operable", explain: "Verifica que las acciones se ejecuten al soltar el clic/toque (up-event) para permitir cancelación." },
  "2.5.3": { title: "Etiqueta en el nombre", level: "A", principle: "Operable", explain: "Comprueba que el nombre accesible contenga el texto visible en botones y controles." },
  "2.5.4": { title: "Activación por movimiento", level: "A", principle: "Operable", explain: "Verifica que funciones activadas por sacudir/inclinar el dispositivo cuenten con alternativa por interfaz." },
  "2.5.5": { title: "Tamaño del objetivo (Target size)", level: "AAA", principle: "Operable", explain: "Verifica que los botones y áreas táctiles tengan al menos 44x44 píxeles." },
  "2.5.6": { title: "Mecanismos de entrada simultáneos", level: "AAA", principle: "Operable", explain: "Permite cambiar libremente entre ratón, pantalla táctil y teclado." },

  // P3 – Comprensible
  "3.1.1": { title: "Idioma de la página", level: "A", principle: "Comprensible", explain: "Comprueba que la etiqueta <html lang='...'> esté presente y tenga un código de idioma válido." },
  "3.1.2": { title: "Idioma de las partes", level: "AA", principle: "Comprensible", explain: "Verifica el atributo lang en pasajes o frases en idiomas diferentes al principal." },
  "3.1.3": { title: "Palabras inusuales", level: "AAA", principle: "Comprensible", explain: "Verifica definiciones o glosarios para modismos o jerga técnica." },
  "3.1.4": { title: "Abreviaturas", level: "AAA", principle: "Comprensible", explain: "Verifica el uso de <abbr> o explicación de siglas y abreviaturas." },
  "3.1.5": { title: "Nivel de lectura", level: "AAA", principle: "Comprensible", explain: "Verifica versión simplificada cuando el texto requiere educación avanzada." },
  "3.1.6": { title: "Pronunciación", level: "AAA", principle: "Comprensible", explain: "Proporciona pronunciación cuando el significado depende de ella." },
  "3.2.1": { title: "Al recibir el foco", level: "A", principle: "Comprensible", explain: "Verifica que recibir el foco no provoque un cambio inesperado de contexto (envío de formulario o popups)." },
  "3.2.2": { title: "Al introducir datos", level: "A", principle: "Comprensible", explain: "Comprueba que cambiar un valor en un selector o checkbox no cambie el contexto automáticamente sin avisar." },
  "3.2.3": { title: "Navegación consistente", level: "AA", principle: "Comprensible", explain: "Verifica que los menús y cabeceras aparezcan en el mismo orden en todas las páginas." },
  "3.2.4": { title: "Identificación consistente", level: "AA", principle: "Comprensible", explain: "Verifica que iconos y funciones idénticas tengan la misma etiqueta en todo el sitio." },
  "3.2.5": { title: "Cambio a petición", level: "AAA", principle: "Comprensible", explain: "Verifica que los cambios de contexto solo ocurran por solicitud explícita del usuario." },
  "3.3.1": { title: "Identificación de errores", level: "A", principle: "Comprensible", explain: "Comprueba que los errores en formularios se identifiquen y describan en texto claro al usuario." },
  "3.3.2": { title: "Etiquetas o instrucciones", level: "A", principle: "Comprensible", explain: "Verifica que todos los campos de formulario cuenten con <label> o instrucciones visibles." },
  "3.3.3": { title: "Sugerencia ante errores", level: "AA", principle: "Comprensible", explain: "Comprueba que el sistema sugiera cómo corregir errores de entrada cuando sea posible." },
  "3.3.4": { title: "Prevención de errores (financieros/legales)", level: "AA", principle: "Comprensible", explain: "Verifica confirmación o posibilidad de revertir envíos con consecuencias legales o de datos." },
  "3.3.5": { title: "Ayuda", level: "AAA", principle: "Comprensible", explain: "Proporciona ayuda contextual disponible en formularios." },
  "3.3.6": { title: "Prevención de errores (todos)", level: "AAA", principle: "Comprensible", explain: "Verifica confirmación previa o revisión antes de cualquier envío de datos." },

  // P4 – Robusto
  "4.1.1": { title: "Análisis sintáctico (Parsing)", level: "A", principle: "Robusto", explain: "Verifica que el HTML no tenga IDs duplicados, etiquetas mal anidadas o errores graves de sintaxis." },
  "4.1.2": { title: "Nombre, función, valor (ARIA)", level: "A", principle: "Robusto", explain: "Comprueba que botones, enlaces e inputs personalizados tengan roles y nombres accesibles válidos." },
  "4.1.3": { title: "Mensajes de estado", level: "AA", principle: "Robusto", explain: "Verifica el uso de aria-live / role='status' para notificar cambios dinámicos a lectores de pantalla." }
};

const VERDICT_LABELS = {
  pass: "CUMPLE",
  fail: "NO CUMPLE",
  partial: "PARCIAL",
  na: "N/A"
};

// ========= Estado global de filtros y auditoría =========
let currentAuditData = null;
let activeFilterPrinciple = "ALL";
let activeFilterLevel = "ALL";
let activeFilterVerdict = "ALL";
let activeSearchQuery = "";

// ========= Inicialización =========
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupAuditForm();
  setupFilters();
  setupModals();
});

// ========= Manejo del Tema Claro / Oscuro =========
function initTheme() {
  const getSystem = () => window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  const saved = localStorage.getItem("theme") || getSystem();
  setTheme(saved);

  const themeBtn = document.getElementById("theme-toggle-btn");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme || "light";
      const next = current === "dark" ? "light" : "dark";
      setTheme(next);
    });
  }
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("theme", theme);
  const themeBtn = document.getElementById("theme-toggle-btn");
  if (themeBtn) {
    themeBtn.textContent = theme === "dark" ? "☀️ Claro" : "🌙 Oscuro";
  }
}

// ========= Helpers de URL =========
function normalizeUrl(u) {
  if (!u) return "";
  const trimmed = u.trim();
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  return `https://${trimmed}`;
}

function isValidUrl(u) {
  try {
    new URL(normalizeUrl(u));
    return true;
  } catch {
    return false;
  }
}

function setExampleUrl(url) {
  const input = document.getElementById("audit-url-input");
  if (input) {
    input.value = url;
    input.focus();
  }
}

// ========= Formulario de Auditoría Unificado =========
function setupAuditForm() {
  const form = document.getElementById("audit-form");
  const input = document.getElementById("audit-url-input");
  const btn = document.getElementById("audit-submit-btn");

  if (!form || !btn) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const rawVal = input.value.trim();
    if (!rawVal) {
      alert("Por favor ingresa una URL válida.");
      input.focus();
      return;
    }

    const cleanUrl = normalizeUrl(rawVal);
    if (!isValidUrl(cleanUrl)) {
      alert("La URL ingresada no es válida.");
      input.focus();
      return;
    }

    input.value = cleanUrl;
    await executeAudit(cleanUrl);
  });
}

// ========= Función Ejecutora de Auditoría =========
async function executeAudit(url) {
  const btn = document.getElementById("audit-submit-btn");
  const input = document.getElementById("audit-url-input");
  const resultsCard = document.getElementById("audit-results-card");
  const errorAlert = document.getElementById("audit-error-alert");

  if (errorAlert) errorAlert.style.display = "none";
  
  // Estado de carga
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> Auditando sitio...`;
  if (input) input.disabled = true;

  try {
    const csrfToken = getCookie("csrftoken");
    const response = await fetch("/api/audit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken || "",
      },
      credentials: "include",
      body: JSON.stringify({ url: url }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({ detail: "Error del servidor." }));
      throw new Error(errData.detail || `Error HTTP ${response.status}`);
    }

    const data = await response.json();
    currentAuditData = normalizeAuditData(data);
    
    // Renderizar resultados en pantalla
    renderAuditResults(currentAuditData);
    if (resultsCard) {
      resultsCard.style.display = "block";
      resultsCard.scrollIntoView({ behavior: "smooth" });
    }

    // Actualizar fila en historial si existe
    addOrUpdateRecentRow(data);

  } catch (err) {
    console.error("Error al ejecutar auditoría:", err);
    if (errorAlert) {
      errorAlert.textContent = `❌ Error: ${err.message}`;
      errorAlert.style.display = "block";
    } else {
      alert(`Error al auditar: ${err.message}`);
    }
  } finally {
    btn.disabled = false;
    btn.innerHTML = `🔍 Auditar`;
    if (input) input.disabled = false;
  }
}

// ========= Normalización de datos del Backend =========
function normalizeAuditData(audit) {
  const criteriaMap = {};

  // Extraer de results y de criterion_results
  for (const [code, r] of Object.entries(audit.results || {})) {
    criteriaMap[code] = {
      code,
      details: r.details || {},
      passed: r.passed === true,
      verdict: r.passed ? "pass" : "fail"
    };
  }

  const crList = audit.criterion_results || [];
  for (const cr of crList) {
    const code = cr.code;
    const meta = WCAG_META_ES[code] || { title: cr.title || "Criterio", level: cr.level || "A", principle: cr.principle || "Perceptible" };
    criteriaMap[code] = {
      code,
      title: cr.title || meta.title,
      level: cr.level || meta.level,
      principle: cr.principle || meta.principle,
      verdict: (cr.verdict || "na").toLowerCase(),
      passed: cr.verdict === "pass",
      score_hint: cr.score_hint ?? null,
      details: (typeof cr.details === "object" && cr.details !== null) ? cr.details : {},
      explain: WCAG_META_ES[code]?.explain || ""
    };
  }

  // Asegurar metadata en todos los códigos
  for (const [code, item] of Object.entries(criteriaMap)) {
    const meta = WCAG_META_ES[code] || {};
    item.title = item.title || meta.title || "Criterio";
    item.level = item.level || meta.level || "A";
    item.principle = item.principle || meta.principle || "Perceptible";
    item.explain = item.explain || meta.explain || "";
  }

  return {
    id: audit.id,
    url: audit.url,
    title: audit.page_title || audit.url,
    score: audit.score,
    fetched_at: audit.fetched_at,
    status_code: audit.status_code,
    elapsed_ms: audit.elapsed_ms,
    criteria: Object.values(criteriaMap)
  };
}

// ========= Renderizado de Resultados =========
function renderAuditResults(audit) {
  // Score general
  const scoreVal = audit.score != null ? Math.round(audit.score * 100) : 0;
  const scoreFill = document.getElementById("result-score-fill");
  const scoreLabel = document.getElementById("result-score-label");
  if (scoreFill) scoreFill.style.width = `${scoreVal}%`;
  if (scoreLabel) scoreLabel.textContent = `${scoreVal}%`;

  // URL y Título
  const resUrl = document.getElementById("result-url");
  const resTitle = document.getElementById("result-title");
  const resMeta = document.getElementById("result-meta-info");

  if (resUrl) {
    resUrl.textContent = audit.url;
    resUrl.href = audit.url;
  }
  if (resTitle) resTitle.textContent = audit.title || audit.url;
  if (resMeta) {
    resMeta.textContent = `Auditado el ${formatDate(audit.fetched_at)} • Tiempo: ${audit.elapsed_ms || 0} ms • Estado: ${audit.status_code || 200}`;
  }

  // Conteo de Veredictos
  let passCount = 0, failCount = 0, partialCount = 0, naCount = 0;
  audit.criteria.forEach(c => {
    if (c.verdict === "pass") passCount++;
    else if (c.verdict === "fail") failCount++;
    else if (c.verdict === "partial") partialCount++;
    else naCount++;
  });

  const elPass = document.getElementById("count-pass");
  const elFail = document.getElementById("count-fail");
  const elPartial = document.getElementById("count-partial");
  const elNA = document.getElementById("count-na");

  if (elPass) elPass.textContent = passCount;
  if (elFail) elFail.textContent = failCount;
  if (elPartial) elPartial.textContent = partialCount;
  if (elNA) elNA.textContent = naCount;

  // Renderizar lista filtrada
  renderFilteredCriteria();
}

// ========= Renderizar Lista Filtrada de Criterios =========
function renderFilteredCriteria() {
  if (!currentAuditData) return;

  const container = document.getElementById("criteria-list-container");
  if (!container) return;

  const filtered = currentAuditData.criteria.filter(c => {
    // Filtro Principio
    if (activeFilterPrinciple !== "ALL" && c.principle.toLowerCase() !== activeFilterPrinciple.toLowerCase()) {
      return false;
    }
    // Filtro Nivel
    if (activeFilterLevel !== "ALL" && c.level.toUpperCase() !== activeFilterLevel.toUpperCase()) {
      return false;
    }
    // Filtro Veredicto
    if (activeFilterVerdict !== "ALL" && c.verdict.toLowerCase() !== activeFilterVerdict.toLowerCase()) {
      return false;
    }
    // Filtro Búsqueda
    if (activeSearchQuery) {
      const q = activeSearchQuery.toLowerCase();
      const matchCode = c.code.toLowerCase().includes(q);
      const matchTitle = c.title.toLowerCase().includes(q);
      if (!matchCode && !matchTitle) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="alert warn compact" style="text-align:center; padding: 24px;">
        🔍 No se encontraron criterios con los filtros seleccionados.
      </div>
    `;
    return;
  }

  let html = "";
  filtered.forEach(c => {
    const verdictClass = `verdict-${c.verdict}`;
    const verdictLabel = VERDICT_LABELS[c.verdict] || c.verdict.toUpperCase();
    const detailsJson = JSON.stringify(c.details, null, 2);
    const hasDetails = Object.keys(c.details || {}).length > 0;

    // Detectados / Evidencias
    let detectedInfo = "";
    if (c.details?.errors && Array.isArray(c.details.errors) && c.details.errors.length > 0) {
      detectedInfo += `<div class="callout warn"><div class="callout-title">⚠️ Errores Detectados:</div><ul>${c.details.errors.map(e => `<li>${escapeHtml(typeof e === 'object' ? JSON.stringify(e) : String(e))}</li>`).join('')}</ul></div>`;
    }
    if (c.details?.evidences && Array.isArray(c.details.evidences) && c.details.evidences.length > 0) {
      detectedInfo += `<div class="callout info"><div class="callout-title">🔍 Elementos Evaluados:</div><ul>${c.details.evidences.slice(0, 10).map(ev => `<li>${escapeHtml(typeof ev === 'object' ? JSON.stringify(ev) : String(ev))}</li>`).join('')}</ul></div>`;
    }

    html += `
      <details class="criterion" id="criterion-${c.code.replace(/\./g, '-')}">
        <summary class="criterion-summary">
          <span class="criterion-code">${c.code}</span>
          <span class="criterion-title">${escapeHtml(c.title)}</span>
          <span class="principle">${escapeHtml(c.principle)}</span>
          <span class="level level-${c.level}">${c.level}</span>
          <span class="verdict ${verdictClass}">${verdictLabel}</span>
        </summary>
        <div class="criterion-body">
          ${c.explain ? `
            <div class="callout info">
              <div class="callout-title">📘 ¿Qué evalúa este criterio?</div>
              <div>${escapeHtml(c.explain)}</div>
            </div>
          ` : ""}
          
          ${detectedInfo}

          ${hasDetails ? `
            <details style="margin-top: 10px;">
              <summary style="font-size: 13px; font-weight: 600; cursor: pointer; color: var(--c-muted);">
                Ver detalles técnicos (JSON)
              </summary>
              <pre class="json" style="margin-top: 8px;"><code>${escapeHtml(detailsJson)}</code></pre>
            </details>
          ` : ""}
        </div>
      </details>
    `;
  });

  container.innerHTML = html;
}

// ========= Configuración de Filtros =========
function setupFilters() {
  // Filtros de Principio
  document.querySelectorAll("[data-filter-principle]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-filter-principle]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilterPrinciple = btn.getAttribute("data-filter-principle");
      renderFilteredCriteria();
    });
  });

  // Filtros de Nivel
  document.querySelectorAll("[data-filter-level]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-filter-level]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilterLevel = btn.getAttribute("data-filter-level");
      renderFilteredCriteria();
    });
  });

  // Filtros de Veredicto
  document.querySelectorAll("[data-filter-verdict]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-filter-verdict]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilterVerdict = btn.getAttribute("data-filter-verdict");
      renderFilteredCriteria();
    });
  });

  // Buscador
  const searchInput = document.getElementById("criteria-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      activeSearchQuery = e.target.value.trim();
      renderFilteredCriteria();
    });
  }
}

// ========= Modales & Eliminación =========
let pendingDeleteId = null;

function setupModals() {
  const modal = document.getElementById("delete-modal");
  const cancelBtn = document.getElementById("delete-cancel-btn");
  const confirmBtn = document.getElementById("delete-confirm-btn");

  if (!modal) return;

  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      modal.style.display = "none";
      pendingDeleteId = null;
    });
  }

  if (confirmBtn) {
    confirmBtn.addEventListener("click", async () => {
      if (!pendingDeleteId) return;
      confirmBtn.disabled = true;
      confirmBtn.textContent = "Borrando...";

      try {
        const csrfToken = getCookie("csrftoken");
        const res = await fetch(`/api/audits/${pendingDeleteId}/delete/`, {
          method: "DELETE",
          headers: { "X-CSRFToken": csrfToken || "" },
          credentials: "include"
        });

        if (res.ok) {
          const row = document.getElementById(`audit-row-${pendingDeleteId}`);
          if (row) row.remove();
          modal.style.display = "none";
        } else {
          alert("No se pudo eliminar la auditoría.");
        }
      } catch (e) {
        alert("Error de conexión al eliminar.");
      } finally {
        confirmBtn.disabled = false;
        confirmBtn.textContent = "Eliminar";
        modal.style.display = "none";
        pendingDeleteId = null;
      }
    });
  }
}

function promptDeleteAudit(id) {
  pendingDeleteId = id;
  const modal = document.getElementById("delete-modal");
  if (modal) modal.style.display = "flex";
}

// ========= Actualizar Historial Reciente =========
function addOrUpdateRecentRow(audit) {
  const tbody = document.getElementById("recent-audits-tbody");
  if (!tbody) return;

  const existingRow = document.getElementById(`audit-row-${audit.id}`);
  const scorePct = audit.score != null ? `${Math.round(audit.score * 100)}%` : "—";
  const dateStr = formatDate(audit.fetched_at);

  const rowHtml = `
    <td><strong>#${audit.id}</strong></td>
    <td style="max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
      <a href="${escapeHtml(audit.url)}" target="_blank" rel="noopener noreferrer" style="color: var(--c-brand); font-weight: 600; text-decoration: none;">
        ${escapeHtml(audit.url)}
      </a>
      <div style="font-size: 12px; color: var(--c-muted);">${escapeHtml(audit.page_title || '')}</div>
    </td>
    <td><span class="badge badge-ok">${scorePct}</span></td>
    <td style="font-size: 13px; color: var(--c-muted);">${dateStr}</td>
    <td>
      <div class="row gap-sm">
        <a href="/audits/${audit.id}/" class="audit-btn sm secondary" title="Ver reporte completo">Ver Detalle</a>
        <button type="button" class="chip chip-bad" onclick="promptDeleteAudit(${audit.id})" title="Eliminar">🗑️</button>
      </div>
    </td>
  `;

  if (existingRow) {
    existingRow.innerHTML = rowHtml;
  } else {
    const newTr = document.createElement("tr");
    newTr.id = `audit-row-${audit.id}`;
    newTr.innerHTML = rowHtml;
    tbody.insertBefore(newTr, tbody.firstChild);
  }
}

// ========= Utilidades =========
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatDate(dStr) {
  if (!dStr) return "";
  const d = new Date(dStr);
  if (isNaN(d.getTime())) return dStr;
  return d.toLocaleString("es-ES", {
    year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit"
  });
}
