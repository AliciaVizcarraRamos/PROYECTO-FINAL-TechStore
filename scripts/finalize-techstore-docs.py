#!/usr/bin/env python3
"""Final gaps: S01 Alicia, S02 1.4, S12/S16 Q&A, Equipo 07 blocks, index kafka ports."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/AliciaVizcarraRamos/PROYECTO-FINAL-TechStore"
DOCS = "http://127.0.0.1:8002"

S02_QA = """
<p>Preguntas para los estudiantes:</p>
<ol>
<li><p><strong>¿Por qué no duplicar YAML en cada microservicio?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Con seis MS, un cambio de puerto o JDBC repetido en seis JARs genera errores. <code>infra/config-repo</code> + Config Server (<code>7071</code>) es la única fuente de verdad.</p></li>
<li><p><strong>¿Qué debe coincidir entre nombre y archivo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>spring.application.name: producto</code> = <code>producto-dev.yml</code> = URL <code>/producto/dev</code>.</p></li>
<li><p><strong>¿Cómo verificas que Config Server entrega datos?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>curl http://localhost:7071/producto/dev</code> y logs del MS al arrancar con <code>Located environment</code>.</p></li>
</ol>
"""

S12_QA = """<ol>
<li><p><strong>¿Cómo se protege el sistema?</strong></p>
<p><strong>Respuesta (TechStore):</strong> JWT vía <code>auth</code> (<code>8041</code>), login en <code>7091/auth/login</code>, rutas protegidas en Gateway y validación en MS (<code>pedido</code>, <code>pago</code>, etc.).</p></li>
<li><p><strong>¿Qué flujo demuestra comunicación entre servicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>GET /api/v1/productos/{id}/detalle</code> — <code>producto</code> consulta <code>catalogo</code> por Feign; <code>pedido</code> valida <code>producto</code>.</p></li>
<li><p><strong>¿Qué evidencia muestra mensajería asíncrona?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>pedido</code> publica en <code>pedido-eventos</code>, <code>pago</code> consume; logs + Kafka UI en <code>28085</code>.</p></li>
<li><p><strong>¿Cómo se diagnostica un fallo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Eureka <code>7081</code> → health MS → Config <code>7071</code> → logs con <code>traceId</code> → <code>referencias/troubleshooting</code>.</p></li>
<li><p><strong>¿Cuál fue tu aporte individual?</strong></p>
<p><strong>Respuesta (TechStore — Equipo 07):</strong> Ej. documentación y pruebas de <code>producto</code>/Gateway en S06–S11; PDFs y commits en PROYECTO-FINAL-TechStore.</p></li>
</ol>"""

S12_DIAGRAM = """<pre class="mermaid"><code>flowchart LR
    Front["techstore-proyecto&lt;br/&gt;4200"]
    Gateway["gateway&lt;br/&gt;7091"]
    Auth["auth 8041"]
    Catalogo["catalogo 9081"]
    Producto["producto 9091"]
    Pedido["pedido 9101"]
    Pago["pago 9111"]
    Carrito["carrito 9121"]
    Broker["Kafka 29092"]
    Obs["Actuator / Prometheus"]

    Front --&gt; Gateway
    Gateway --&gt; Auth
    Gateway --&gt; Producto
    Gateway --&gt; Pedido
    Gateway --&gt; Pago
    Gateway --&gt; Carrito
    Gateway --&gt; Catalogo
    Producto --&gt;|"Feign"| Catalogo
    Pedido --&gt;|"pedido-eventos"| Broker
    Broker --&gt; Pago
    Gateway -. traceId .-&gt; Obs
    classDef infra fill:#e8eaf6,stroke:#5c6bc0,color:#111
    classDef ms fill:#ede7f6,stroke:#7b1fa2,color:#111
    classDef gw fill:#c5cae9,stroke:#3949ab,stroke-width:2px,color:#111
    class Gateway gw
    class Auth,Catalogo,Producto,Pedido,Pago,Carrito ms
    class Broker,Obs infra
</code></pre>"""

S16_QA = """<ol>
<li><p><strong>¿Qué competencia estás demostrando?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Ej. operar y defender un MS del monorepo (<code>producto</code>, Gateway, Config) o el flujo E2E del equipo 07.</p></li>
<li><p><strong>¿Qué comando ejecutaste y por qué?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Ej. <code>curl http://localhost:7091/actuator/health</code> para verificar Gateway antes de demo; <code>curl http://localhost:7071/producto/dev</code> para validar config.</p></li>
<li><p><strong>¿Qué evidencia confirma el resultado?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Salida JSON <code>UP</code>, captura Eureka con 6 MS, PDF S04–S14, commits en GitHub.</p></li>
<li><p><strong>¿Cómo corregirías el fallo presentado?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Revisar orden arranque (Config → Eureka → Gateway → MS), <code>defaultZone</code>, predicate Gateway, MySQL del dominio.</p></li>
<li><p><strong>¿Qué aprendiste respecto a tu aporte?</strong></p>
<p><strong>Respuesta (TechStore):</strong> El valor de un punto único de acceso, config centralizada y evidencia reproducible en documentación GitHub Pages.</p></li>
</ol>"""

EQUIPO_07_BLOCK = f"""<p>Ejemplo Equipo 07 — TechStore-g2:</p>
<ul>
<li>Equipo: 07 — TechStore-g2</li>
<li>Proyecto: TechStore-Proyecto (<code>ProyectoMS2026</code>)</li>
<li>Link de GitHub: <a href="{GITHUB}">PROYECTO-FINAL-TechStore</a></li>
<li>Link de documentación: <a href="{DOCS}">{DOCS}</a> (GitHub Pages local)</li>
<li>Rama integrada evaluada: <code>main</code> (o rama del equipo)</li>
<li>Evidencia de integración: PRs mergeados, sistema integrado en demo</li>
<li>Integrantes: Alicia Vizcarra Ramos (y equipo)</li>
<li>Productos de sesión integrados: S01–S05 (U1) / S06–S11 (U2) según unidad</li>
<li>Anexos individuales: PDFs <code>S##_Equipo07_TechStore-g2_*.pdf</code></li>
</ul>"""


def patch(path: Path, old: str, new: str) -> bool:
    t = path.read_text(encoding="utf-8")
    if old not in t:
        return False
    path.write_text(t.replace(old, new, 1), encoding="utf-8")
    return True


def fix_search_index():
    search = ROOT / "search" / "search_index.json"
    if not search.exists():
        return
    t = search.read_text(encoding="utf-8")
    replacements = [
        ("18080", "7091"), ("18888", "7071"), ("18761", "7081"),
        ("15431", "3341"), ("orden-ms", "pedido"), ("ecom_auth_db", "db_auth"),
        ("41092", "29092"), ("41085", "28085"),
    ]
    u = t
    for old, new in replacements:
        u = u.replace(old, new)
    if u != t:
        search.write_text(u, encoding="utf-8")
        print("Fixed: search/search_index.json")


def fix_kafka_ports():
    """Kafka DEV real: broker 29092, UI 28085 (no 41092/41085)."""
    for p in ROOT.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        u = t.replace("41092", "29092").replace("41085", "28085")
        if u != t:
            p.write_text(u, encoding="utf-8")
            print(f"Fixed kafka ports: {p.relative_to(ROOT)}")


def fix_s01_nav_mysql():
    """Anclas de navegación S01: postgresql → mysql."""
    s01 = ROOT / "sesiones/s01-arquitectura-base/index.html"
    if not s01.exists():
        return
    t = s01.read_text(encoding="utf-8")
    u = t.replace("postgresql-dev", "mysql-dev").replace("postgresql-y-flyway", "mysql-y-flyway")
    if u != t:
        s01.write_text(u, encoding="utf-8")
        print("Fixed S01 nav anchors (mysql)")


def fix_docker_compose_paths():
    """Corrige reemplazos masivos que rompieron docker-compose-dev.yml."""
    sesiones = ROOT / "sesiones"
    fixes = [
        ("docker-docker-docker-docker-docker-docker-docker-compose-dev.yml", "docker-compose-dev.yml"),
        ("docker-docker-docker-docker-docker-docker-compose-dev.yml", "docker-compose-dev.yml"),
    ]
    for p in sesiones.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        u = t
        for old, new in fixes:
            u = u.replace(old, new)
        if u != t:
            p.write_text(u, encoding="utf-8")
            print(f"Fixed docker-compose paths: {p.relative_to(ROOT)}")


def main():
    fix_docker_compose_paths()
    fix_kafka_ports()
    fix_s01_nav_mysql()
    fix_search_index()
    s01 = ROOT / "sesiones/s01-arquitectura-base/index.html"
    patch(s01, "S01_Equipo07_TechStore-g2_GarciaLuis.pdf", "S01_Equipo07_TechStore-g2_Vizcarra.pdf")
    patch(s01, "docker compose -f docker-docker-docker-docker-docker-docker-docker-compose-dev.yml up -d",
          "docker compose -f services/producto/docker-compose-dev.yml up -d")
    patch(s01, """<h4 id="411-datos-del-estudiante">4.1.1 Datos del estudiante</h4>
<ul>
<li>Nombre:</li>
<li>Equipo: 07 — TechStore-g2</li>
<li>Proyecto: TechStore-Proyecto (<code>ProyectoMS2026</code>)</li>
<li>Sesión: S01 — Construcción de un servicio base para un sistema distribuido</li>
<li>Rol o aporte realizado:</li>
<li>Microservicio trabajado (S1: <code>catalogo</code>; autónomo sugerido: <code>producto</code>):</li>
<li>Link de GitHub del monorepo:</li>
</ul>""", f"""<h4 id="411-datos-del-estudiante">4.1.1 Datos del estudiante</h4>
<p>Ejemplo Equipo 07 — TechStore-g2:</p>
<ul>
<li>Nombre: Alicia Vizcarra Ramos</li>
<li>Equipo: 07 — TechStore-g2</li>
<li>Proyecto: TechStore-Proyecto (<code>ProyectoMS2026</code>)</li>
<li>Sesión: S01 — Construcción de un servicio base para un sistema distribuido</li>
<li>Rol o aporte realizado: Microservicio base <code>catalogo</code> (9081, MySQL 3381); patrón replicado en <code>producto</code></li>
<li>Microservicio trabajado: <code>catalogo</code> (S1) / <code>producto</code> (autónomo)</li>
<li>Link de GitHub: <a href="{GITHUB}">PROYECTO-FINAL-TechStore</a></li>
</ul>""")

    s02 = ROOT / "sesiones/s02-configuracion-centralizada/index.html"
    patch(s02, """</code></pre></div>
<h3 id="15-ubicacion-en-el-curso">1.5 Ubicación en el curso</h3>
<ul>
<li>Unidad: U1 - Sistema distribuido base orientado a producción.</li>
<li>Producto de unidad: sistema distribuido base funcional, configurable y preparado para múltiples instancias.</li>
<li>Avance del producto en esta sesión: configuración externa por ambiente mediante Config Server.</li>
</ul>
<p>Roadmap para elaborar el producto de la unidad:</p>""",
          f"""</code></pre></div>
{S02_QA}
<h3 id="15-ubicacion-en-el-curso">1.5 Ubicación en el curso</h3>
<ul>
<li>Unidad: U1 - Sistema distribuido base orientado a producción.</li>
<li>Producto de unidad: sistema distribuido base funcional, configurable y preparado para múltiples instancias.</li>
<li>Avance del producto en esta sesión: configuración externa por ambiente mediante Config Server.</li>
</ul>
<p>Roadmap para elaborar el producto de la unidad:</p>""")

    s12 = ROOT / "sesiones/s12-evaluacion-u2/index.html"
    patch(s12, """<ol>
<li>Cómo se protege el sistema?</li>
<li>Qué flujo demuestra comunicación entre servicios?</li>
<li>Qué evidencia muestra mensajería asíncrona?</li>
<li>Cómo se diagnostica un fallo?</li>
<li>Cuál fue tu aporte individual?</li>
</ol>""", S12_QA)
    old_d = """<pre class="mermaid"><code>flowchart LR
    Front["techstore-proyecto"]
    Gateway["Gateway"]
    Auth["auth"]
    Producto["producto"]
    Catalogo["catalogo"]
    Pedido["pedido"]
    Pago["pago"]
    Broker["Kafka"]
    Obs["Observabilidad"]

    Front --&gt; Gateway
    Gateway --&gt; Auth
    Gateway --&gt; Producto
    Gateway --&gt; Pedido
    Producto --&gt; Catalogo
    Pedido --&gt; Broker
    Broker --&gt; Pago
    Pago --&gt; Broker
    Gateway -. logs/metrics .-&gt; Obs</code></pre>"""
    patch(s12, old_d, S12_DIAGRAM)
    patch(s12, """<h4 id="311-datos-del-equipo">3.1.1 Datos del equipo</h4>
<ul>
<li>Equipo:</li>
<li>Sesión: S12 - Evaluación U2</li>
<li>Proyecto:</li>
<li>Link de GitHub:</li>
<li>Link de documentación:</li>
<li>Rama integrada evaluada:</li>
<li>Evidencia de integración o merge:</li>
<li>Integrantes:</li>
<li>Productos de sesión integrados por el equipo:</li>
<li>Anexos individuales incluidos:</li>
</ul>""", f"""<h4 id="311-datos-del-equipo">3.1.1 Datos del equipo</h4>
{EQUIPO_07_BLOCK.replace('S01–S05 (U1) / S06–S11 (U2)', 'S06–S11')}""")
    patch(s12, "S12_Equipo##_U2_Docs.pdf", "S12_Equipo07_TechStore-g2_U2_Docs.pdf")
    patch(s12, "U2_Equipo##_Presentación.pdf", "U2_Equipo07_TechStore-g2_Presentacion.pdf")

    s05 = ROOT / "sesiones/s05-evaluacion-u1/index.html"
    patch(s05, """<h4 id="311-datos-del-equipo">3.1.1 Datos del equipo</h4>
<ul>
<li>Equipo:</li>
<li>Sesión: S05 - Evaluación U1</li>
<li>Proyecto:</li>
<li>Link de GitHub:</li>
<li>Link de documentación:</li>
<li>Rama integrada evaluada:</li>
<li>Evidencia de integración o merge:</li>
<li>Integrantes:</li>
<li>Productos de sesión integrados por el equipo:</li>
<li>Anexos individuales incluidos:</li>
</ul>""", f"""<h4 id="311-datos-del-equipo">3.1.1 Datos del equipo</h4>
{EQUIPO_07_BLOCK.replace('S06–S11', 'S01–S04')}""")
    patch(s05, "S05_Equipo##_U1_Docs.pdf", "S05_Equipo07_TechStore-g2_U1_Docs.pdf")
    patch(s05, "U1_Equipo##_Presentación.pdf", "U1_Equipo07_TechStore-g2_Presentacion.pdf")

    s16 = ROOT / "sesiones/s16-evaluacion-final/index.html"
    patch(s16, """<ol>
<li>Qué competencia estas demostrando?</li>
<li>Qué comando ejecutaste y por qué?</li>
<li>Qué evidencia confirma el resultado?</li>
<li>Cómo corregirias el fallo presentado?</li>
<li>Qué aprendiste respecto a tu aporte en el sistema?</li>
</ol>""", S16_QA)
    patch(s16, "<code>clients/techstore-proyecto</code>", "<code>techstore-proyecto</code>")
    patch(s16, """<h4 id="311-datos-del-estudiante">3.1.1 Datos del estudiante</h4>
<ul>
<li>Nombre:</li>
<li>Equipo:</li>
<li>Sesión: S16 - Evaluación final de competencias pendientes</li>
<li>Proyecto:</li>
<li>Competencia pendiente:</li>
<li>Consigna asignada:</li>
<li>Link de GitHub:</li>
<li>Link de documentación:</li>
<li>Rama, commit o pull request de la corrección:</li>
</ul>""", f"""<h4 id="311-datos-del-estudiante">3.1.1 Datos del estudiante</h4>
<p>Ejemplo Equipo 07 — TechStore-g2:</p>
<ul>
<li>Nombre: Alicia Vizcarra Ramos</li>
<li>Equipo: 07 — TechStore-g2</li>
<li>Sesión: S16 - Evaluación final de competencias pendientes</li>
<li>Proyecto: TechStore-Proyecto (<code>ProyectoMS2026</code>)</li>
<li>Competencia pendiente: Demo E2E Gateway + verificación Config Server</li>
<li>Consigna asignada: <code>curl http://localhost:7091/actuator/health</code> y flujo login JWT</li>
<li>Link de GitHub: <a href="{GITHUB}">PROYECTO-FINAL-TechStore</a></li>
<li>Link de documentación: <a href="{DOCS}">{DOCS}</a></li>
<li>Rama/commit: <code>main</code> — commits documentación S01–S15</li>
</ul>""")
    patch(s16, "S15_Equipo##_U3_Docs.pdf", "S15_Equipo07_TechStore-g2_U3_Docs.pdf")

    s15 = ROOT / "sesiones/s15-defensa-tecnica/index.html"
    if "Equipo: 07" not in s15.read_text(encoding="utf-8"):
        patch(s15, """<li>Equipo:</li>
<li>Sesión: S15""", """<li>Equipo: 07 — TechStore-g2</li>
<li>Sesión: S15""")

    idx = ROOT / "index.html"
    t = idx.read_text(encoding="utf-8")
    u = t.replace("41092", "29092").replace("41085", "28085")
    if u != t:
        idx.write_text(u, encoding="utf-8")
        print("Updated index.html kafka ports")

    for name in ["s01-arquitectura-base", "s02-configuracion-centralizada", "s05-evaluacion-u1",
                 "s12-evaluacion-u2", "s16-evaluacion-final", "s15-defensa-tecnica"]:
        print(f"Patched: {name}")


if __name__ == "__main__":
    main()
