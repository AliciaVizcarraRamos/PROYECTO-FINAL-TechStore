#!/usr/bin/env python3
"""Complete TechStore session docs: 1.4 Q&A, section 4 evidence, diagram ports."""
from pathlib import Path
import re

SESSIONS = Path(__file__).resolve().parent.parent / "sesiones"
GITHUB = "https://github.com/AliciaVizcarraRamos/PROYECTO-FINAL-TechStore"

# 1.4 questions injected after motivation paragraph (before 1.5)
QA_14 = {
    "s07-seguridad-jwt": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Por qué no basta con proteger solo el Gateway?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Un cliente interno o un atacante podría llamar directamente a <code>9091</code> (<code>producto</code>) saltándose <code>7091</code>. Cada MS sensible valida JWT — defensa en profundidad en los seis servicios.</p></li>
<li><p><strong>¿Qué servicio emite el token en TechStore?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>auth</code> en <code>8041</code> (DEV); el cliente hace <code>POST /auth/login</code> vía Gateway y recibe JWT con roles.</p></li>
<li><p><strong>¿Cómo evidencias un 401?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Llamar <code>GET http://localhost:7091/api/v1/pedidos</code> sin header <code>Authorization: Bearer</code> y capturar respuesta 401 en Postman o logs del Gateway.</p></li>
</ol>""",
    "s08-angular-cors-jwt": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Cuándo usar Kafka en lugar de Feign?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Feign (S06) para consultas inmediatas; Kafka cuando <code>pedido</code> publica <code>pedido-creado</code> y <code>pago</code> o inventario reaccionan sin bloquear la respuesta al usuario.</p></li>
<li><p><strong>¿Qué microservicios publican eventos en TechStore?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Típicamente <code>pedido</code> (creación/estado), <code>pago</code> (confirmación) y consumidores en <code>carrito</code> o notificaciones — cada uno con su BD MySQL.</p></li>
<li><p><strong>¿Cómo evidencias un mensaje publicado?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Log del productor en <code>pedido</code> (<code>9101</code>), consumer activo en <code>pago</code> (<code>9111</code>) y verificación en consola Kafka del topic.</p></li>
</ol>""",
    "s09-kafka-eventos": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Por qué no hay una transacción global en microservicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Cada MS tiene su MySQL (<code>db_pedido</code>, <code>db_pago</code>, etc.). Un checkout actualiza pedido, pago y carrito en pasos; la consistencia se logra con saga/eventos, no con 2PC.</p></li>
<li><p><strong>¿Qué pasa si pago falla después de crear el pedido?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Se compensa: evento de fallo, estado <code>CANCELADO</code> en <code>pedido</code> o reintento idempotente en <code>pago</code> — documentado en logs y BD.</p></li>
<li><p><strong>¿Cómo demuestras consistencia eventual?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Tras checkout, verificar filas coherentes en <code>db_pedido</code> y <code>db_pago</code> tras unos segundos, con mismo <code>pedidoId</code> en ambas.</p></li>
</ol>""",
    "s10-observabilidad": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Qué endpoint revisas primero si un MS no responde?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>/actuator/health</code> del servicio (ej. <code>http://localhost:9091/actuator/health</code> para <code>producto</code>) y registro en Eureka <code>7081</code>.</p></li>
<li><p><strong>¿Cómo sigues una petición entre seis microservicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>traceId</code> propagado desde Gateway; buscar el mismo id en logs de <code>auth</code>, <code>producto</code>, <code>carrito</code>, <code>pedido</code>, <code>pago</code>.</p></li>
<li><p><strong>¿Qué métricas expone el Gateway?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Prometheus en <code>7091/actuator/prometheus</code>, health, y latencia de rutas hacia <code>lb://*</code>.</p></li>
</ol>""",
    "s11-integracion-fullstack": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Por qué Angular no llama a cada microservicio?</strong></p>
<p><strong>Respuesta (TechStore):</strong> El frontend <code>techstore-proyecto</code> usa proxy/API base hacia <code>7091</code> únicamente; CORS y JWT se centralizan en Gateway.</p></li>
<li><p><strong>¿Cómo envía el token la SPA?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>auth.interceptor.ts</code> añade <code>Authorization: Bearer</code> tras login en <code>/auth/login</code>.</p></li>
<li><p><strong>¿Qué flujo demuestra integración real?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Login → catálogo → carrito → checkout → pago Mercado Pago, con datos en las BDs y mismo <code>traceId</code> en backend.</p></li>
</ol>""",
    "s13-validacion-integral": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Qué orden de arranque usa TechStore?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>config-server</code> (<code>7071</code>) → <code>registry-server</code> (<code>7081</code>) → <code>gateway</code> (<code>7091</code>) → MySQL → <code>auth</code>, <code>catalogo</code>, <code>producto</code>, <code>pedido</code>, <code>pago</code>, <code>carrito</code>.</p></li>
<li><p><strong>¿Qué valida una prueba E2E?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Flujo de negocio completo vía <code>7091</code> o UI Angular, JWT válido, datos en BDs y eventos Kafka si aplica.</p></li>
<li><p><strong>¿Cómo documentas un fallo reproducible?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Pasos, curl o captura UI, logs con <code>traceId</code>, health de servicios y estado en Eureka.</p></li>
</ol>""",
    "s14-cierre-tecnico": """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Qué debe quedar en la documentación del equipo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Puertos DEV/PROD, rutas Gateway, Feign, JWT, Kafka, observabilidad y enlace a GitHub Pages (<code>techstore-gh-pages</code>).</p></li>
<li><p><strong>¿Cómo demuestras que el producto es desplegable?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>docker compose</code> en <code>infra/</code>, perfiles <code>prod</code> en <code>config-repo</code> y health <code>UP</code> en los seis MS.</p></li>
<li><p><strong>¿Qué revisas antes de la defensa (S15)?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Demo reproducible, PDFs S06–S14, commits en rama del equipo y diagramas actualizados con paleta azul/morado.</p></li>
</ol>""",
}

# Section 4 Alicia evidence blocks (replace empty 4.1.1 + 4.1.2)
EVIDENCE = {
    "s06-feign-circuit-breaker": {
        "code": "S06",
        "title": "S06 - Comunicación síncrona resiliente entre servicios",
        "rol": "Implementación y prueba de Feign de producto hacia catalogo; documentación de patrón replicado en pedido→producto/pago y carrito→producto.",
        "ms": "producto",
        "tasks": [
            "Verificar <code>CatalogoClient</code> en <code>producto</code> con <code>@FeignClient(name = \"catalogo\")</code>.",
            "Caso exitoso: <code>GET http://localhost:7091/api/v1/productos/{id}/detalle</code> enriquece categoría desde <code>catalogo</code> (<code>9081</code>).",
            "Caso error: detener <code>catalogo</code> y verificar respuesta controlada desde <code>producto</code> (503/404 de negocio).",
            "Replicar patrón documentado para <code>pedido</code>→<code>producto</code>, <code>pedido</code>→<code>pago</code>, <code>carrito</code>→<code>producto</code>.",
            "Capturar logs con mismo <code>traceId</code> en ambos servicios.",
        ],
        "curl": [
            ("Detalle producto vía Gateway", "curl http://localhost:7091/api/v1/productos/1/detalle"),
            ("Health producto", "curl http://localhost:9091/actuator/health"),
            ("Health catalogo", "curl http://localhost:9081/actuator/health"),
        ],
    },
    "s07-seguridad-jwt": {
        "code": "S07",
        "title": "S07 - Seguridad distribuida y control de acceso",
        "rol": "Flujo login JWT vía auth; prueba de rutas protegidas y errores 401/403 en Gateway y microservicios.",
        "ms": "auth",
        "tasks": [
            "Login: <code>POST http://localhost:7091/auth/login</code> con credenciales de prueba.",
            "Consumir ruta protegida con <code>Authorization: Bearer {token}</code> (ej. pedidos o admin).",
            "Probar sin token y documentar 401.",
            "Explicar claims (usuario, roles, exp) del JWT emitido por <code>auth</code> (<code>8041</code>).",
            "Verificar validación en al menos un MS además del Gateway (ej. <code>pedido</code> <code>9101</code>).",
        ],
        "curl": [
            ("Login", 'curl -X POST http://localhost:7091/auth/login -H "Content-Type: application/json" -d "{\\"username\\":\\"admin\\",\\"password\\":\\"...\\"}"'),
            ("Sin token (401)", "curl -i http://localhost:7091/api/v1/pedidos"),
        ],
    },
    "s08-angular-cors-jwt": {
        "code": "S08",
        "title": "S08 - Mensajería asíncrona entre servicios",
        "rol": "Configuración Kafka y evento pedido-creado desde pedido con consumidor en pago.",
        "ms": "pedido",
        "tasks": [
            "Levantar Kafka en red <code>ms-net</code> (o perfil local documentado).",
            "Publicar evento al crear pedido desde <code>pedido</code> (<code>9101</code>).",
            "Consumir en <code>pago</code> (<code>9111</code>) y actualizar estado.",
            "Evidenciar logs productor y consumidor con mismo <code>pedidoId</code>.",
            "Comparar con llamada Feign síncrona (S06): cuándo usar cada enfoque.",
        ],
        "curl": [
            ("Crear pedido vía Gateway", 'curl -X POST http://localhost:7091/api/v1/pedidos -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d "{...}"'),
            ("Health pedido", "curl http://localhost:9101/actuator/health"),
        ],
    },
    "s09-kafka-eventos": {
        "code": "S09",
        "title": "S09 - Consistencia distribuida en procesos de negocio",
        "rol": "Saga de checkout: pedido + pago + compensación documentada en TechStore.",
        "ms": "pedido",
        "tasks": [
            "Describir pasos del checkout sin transacción global.",
            "Verificar estado coherente en <code>db_pedido</code> y <code>db_pago</code> tras pago exitoso.",
            "Simular fallo de pago y documentar compensación (cancelar pedido o reintento).",
            "Relacionar eventos Kafka (S08) con consistencia eventual.",
            "Evidenciar idempotencia en confirmación de pago.",
        ],
        "curl": [
            ("Estado pedido", "curl http://localhost:7091/api/v1/pedidos/1 -H \"Authorization: Bearer {token}\""),
            ("Health pago", "curl http://localhost:9111/actuator/health"),
        ],
    },
    "s10-observabilidad": {
        "code": "S10",
        "title": "S10 - Observabilidad y diagnóstico de sistemas distribuidos",
        "rol": "Health, métricas Prometheus y traceId en producto y Gateway.",
        "ms": "producto",
        "tasks": [
            "Verificar <code>/actuator/health</code> en los seis MS y Gateway.",
            "Consultar <code>/actuator/prometheus</code> en Gateway (<code>7091</code>).",
            "Seguir <code>traceId</code> en logs de una petición a <code>producto</code>.",
            "Documentar diagnóstico si <code>producto</code> está DOWN en Eureka.",
            "Tabla resumen: puerto, health URL y MS para catalogo, auth, producto, pedido, pago, carrito.",
        ],
        "curl": [
            ("Prometheus Gateway", "curl http://localhost:7091/actuator/prometheus"),
            ("Health producto", "curl http://localhost:9091/actuator/health"),
        ],
    },
    "s11-integracion-fullstack": {
        "code": "S11",
        "title": "S11 - Integración con cliente frontend",
        "rol": "Angular techstore-proyecto contra Gateway; interceptor JWT y flujo tienda.",
        "ms": "techstore-proyecto",
        "tasks": [
            "Levantar <code>ng serve</code> en <code>techstore-proyecto</code> (puerto <code>4200</code>).",
            "Verificar proxy/API hacia <code>7091</code> en <code>environment.ts</code>.",
            "Login, listar productos, agregar al carrito y checkout con token.",
            "Capturar consola navegador sin errores CORS.",
            "Correlacionar acción UI con logs backend (<code>traceId</code>).",
        ],
        "curl": [
            ("API vía Gateway (como Angular)", "curl http://localhost:7091/api/v1/productos"),
        ],
    },
    "s13-validacion-integral": {
        "code": "S13",
        "title": "S13 - Validación end-to-end del producto del curso",
        "rol": "Checklist E2E del equipo: infra + 6 MS + frontend + flujo compra.",
        "ms": "todos",
        "tasks": [
            "Checklist arranque: Config, Eureka, Gateway, BDs, 6 MS UP en <code>7081</code>.",
            "Flujo: login → productos → carrito → pedido → pago.",
            "Verificar datos en MySQL de cada dominio.",
            "Documentar un fallo y su resolución con evidencia.",
            "Exportar PDF S13 con capturas y comandos reproducibles.",
        ],
        "curl": [
            ("Eureka apps", "curl http://localhost:7081/eureka/apps"),
            ("Gateway health", "curl http://localhost:7091/actuator/health"),
        ],
    },
    "s14-cierre-tecnico": {
        "code": "S14",
        "title": "S14 - Revisión técnica y estabilización del producto",
        "rol": "Consolidación documentación GitHub Pages, docker PROD y deuda técnica cerrada.",
        "ms": "infra",
        "tasks": [
            "Revisar <code>infra/docker-compose.yml</code> y perfiles <code>*-prod.yml</code>.",
            "Actualizar diagramas S06–S11 en documentación del equipo.",
            "Listar issues/PRs cerrados en repositorio del equipo.",
            "Verificar demo PROD local (<code>7092</code>, <code>7082</code>).",
            "Preparar guion de defensa técnica (S15).",
        ],
        "curl": [
            ("PROD Gateway", "curl http://localhost:7092/actuator/health"),
            ("PROD Eureka", "curl http://localhost:7082/"),
        ],
    },
}

PORT_REPLACEMENTS = [
    ('producto&lt;br/&gt;puerto dinamico', 'producto&lt;br/&gt;9091'),
    ('catalogo&lt;br/&gt;puerto dinamico', 'catalogo&lt;br/&gt;9081'),
    ('auth&lt;br/&gt;puerto dinamico', 'auth&lt;br/&gt;8041'),
    ('pedido&lt;br/&gt;puerto dinamico', 'pedido&lt;br/&gt;9101'),
    ('pago&lt;br/&gt;puerto dinamico', 'pago&lt;br/&gt;9111'),
    ('carrito&lt;br/&gt;puerto dinamico', 'carrito&lt;br/&gt;9121'),
    ('pedido&lt;br/&gt;puerto dinamico', 'pedido&lt;br/&gt;9101'),
    ('Pedido["pedido&lt;br/&gt;puerto dinamico"]', 'Pedido["pedido&lt;br/&gt;9101"]'),
    ('Catalogo["catalogo&lt;br/&gt;puerto dinamico"]', 'Catalogo["catalogo&lt;br/&gt;9081"]'),
    ('Auth["auth&lt;br/&gt;puerto dinamico"]', 'Auth["auth&lt;br/&gt;8041"]'),
    ('catálogo_db', 'db_catalogo'),
    ('producto_db', 'db_producto'),
    ('registry-server&lt;br/&gt;8761 interno', 'registry-server&lt;br/&gt;7081 interno'),
    ('http://registry-server:7081/eureka', 'http://registry-server:8761/eureka'),
    ('http://catalogo:8080', 'http://catalogo:8082'),
]

MERMAID_STYLES = """
    classDef infra fill:#e8eaf6,stroke:#5c6bc0,color:#111
    classDef ms fill:#ede7f6,stroke:#7b1fa2,color:#111
    classDef gw fill:#c5cae9,stroke:#3949ab,stroke-width:2px,color:#111
    classDef db fill:#e3f2fd,stroke:#1976d2,color:#111"""


def fix_ports(text: str) -> str:
    for old, new in PORT_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def inject_14(text: str, folder: str) -> str:
    if folder not in QA_14:
        return text
    section = text.split('id="14-motivacion-de-la-sesion"', 1)
    if len(section) < 2:
        return text
    chunk = section[1].split('id="15-ubicacion-en-el-curso"', 1)[0]
    if "Preguntas para los estudiantes" in chunk:
        return text
    block = QA_14[folder].strip()
    pattern = r'(<h3 id="14-motivacion-de-la-sesion">1\.4 Motivacion de la sesión</h3>\s*<p>.*?</p>)\s*(<h3 id="15-ubicacion-en-el-curso">)'
    return re.sub(pattern, r"\1\n" + block + r"\n\2", text, count=1, flags=re.DOTALL)


def build_evidence_html(ev: dict) -> str:
    tasks = "\n".join(f"<li>{t}</li>" for t in ev["tasks"])
    curls = ""
    if ev.get("curl"):
        parts = []
        for i, (label, cmd) in enumerate(ev["curl"], 1):
            parts.append(f"<p><strong>{i}. {label}</strong></p>\n<div class=\"highlight\"><pre><span></span><code>{cmd}\n</code></pre></div>")
        curls = "\n<h4 id=\"413-evidencia-tecnica\">4.1.3 Evidencia técnica</h4>\n" + "\n".join(parts)
    return f"""<p>Repositorio del equipo: <a href="{GITHUB}">{GITHUB}</a>. Monorepo local: <code>ProyectoMS2026</code>.</p>
<div class="highlight"><pre><span></span><code>{ev['code']}_Equipo07_TechStore-g2_ApellidoNombre.pdf
</code></pre></div>
<p>Ejemplo Equipo 07 — TechStore-g2:</p>
<div class="highlight"><pre><span></span><code>{ev['code']}_Equipo07_TechStore-g2_Vizcarra.pdf
</code></pre></div>
<h4 id="411-datos-del-estudiante">4.1.1 Datos del estudiante</h4>
<p>Ejemplo de referencia (Equipo 07 — TechStore-g2):</p>
<ul>
<li>Nombre: Alicia Vizcarra Ramos</li>
<li>Equipo: 07 — TechStore-g2</li>
<li>Proyecto: TechStore-Proyecto (<code>ProyectoMS2026</code>)</li>
<li>Sesión: {ev['title']}</li>
<li>Rol o aporte realizado: {ev['rol']}</li>
<li>Microservicio trabajado en autónomo: <code>{ev['ms']}</code></li>
<li>Link de GitHub: <a href="{GITHUB}">PROYECTO-FINAL-TechStore</a></li>
</ul>
<h4 id="412-trabajo-autonomo-realizado">4.1.2 Trabajo autónomo realizado</h4>
<ol>
{tasks}
</ol>
{curls}"""


def inject_evidence(text: str, folder: str) -> str:
    if folder not in EVIDENCE or "Alicia Vizcarra Ramos" in text:
        return text
    ev_html = build_evidence_html(EVIDENCE[folder])
    # Replace from 4.1 header through end of 4.1.2 ol (before 4.2 or 42-criterios)
    pattern = (
        r'(<h3 id="41-plantilla-de-evidencia-individual">4\.1 Plantilla de evidencia individual</h3>\s*)'
        r'(?:<p>.*?</p>\s*)*'
        r'(?:<div class="highlight">.*?</div>\s*)*'
        r'<h4 id="411-datos-del-estudiante">4\.1\.1 Datos del estudiante</h4>\s*'
        r'<ul>.*?</ul>\s*'
        r'<h4 id="412-trabajo-autonomo-realizado">4\.1\.2 Trabajo autónomo realizado</h4>\s*'
        r'<ol>.*?</ol>'
    )
    replacement = r"\1" + ev_html
    new = re.sub(pattern, replacement, text, count=1, flags=re.DOTALL)
    if new == text:
        return text
    # Update 5.2 pdf name
    new = new.replace(
        f"{EVIDENCE[folder]['code']}_Equipo07_TechStore-g2_ApellidoNombre.pdf",
        f"{EVIDENCE[folder]['code']}_Equipo07_TechStore-g2_Vizcarra.pdf",
        1,
    )
    return new


def add_mermaid_styles(text: str) -> str:
    """Append classDef to flowcharts in S06-S14 that lack styling."""
    def enhance_block(m):
        block = m.group(1)
        if "classDef" in block:
            return m.group(0)
        # assign classes heuristically
        extra = MERMAID_STYLES + "\n    class Gateway gw\n    class Producto,Catalogo,Auth,Pedido,Pago,Carrito ms\n    class Eureka,Config infra"
        if "ProductoDB" in block or "CatalogoDB" in block:
            extra += "\n    class ProductoDB,CatalogoDB db"
        return f'<pre class="mermaid"><code>{block.rstrip()}{extra}\n</code></pre>'

    return re.sub(
        r'<pre class="mermaid"><code>(flowchart[\s\S]*?)</code></pre>',
        enhance_block,
        text,
    )


def main():
    folders = list(QA_14.keys()) + list(EVIDENCE.keys())
    folders = sorted(set(folders))
    for folder in folders:
        path = SESSIONS / folder / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = fix_ports(text)
        new = inject_14(new, folder)
        new = inject_evidence(new, folder)
        if folder.startswith("s06") or folder.startswith("s07") or folder.startswith("s08") or folder.startswith("s09") or folder.startswith("s10") or folder.startswith("s11") or folder.startswith("s13") or folder.startswith("s14"):
            new = add_mermaid_styles(new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"Updated: {folder}")


if __name__ == "__main__":
    main()
