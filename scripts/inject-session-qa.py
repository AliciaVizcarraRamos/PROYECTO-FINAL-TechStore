#!/usr/bin/env python3
"""Inject TechStore Q&A answers into session HTML (section 5.3 and selected 1.4)."""
from pathlib import Path
import re

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sesiones"

# session folder -> HTML for 5.3 (replaces entire <ol>...</ol> after 5.3 heading)
QA_53 = {
    "s01-arquitectura-base": """
<ol>
<li><p><strong>¿Por qué separar el sistema en microservicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Cada dominio (catálogo, producto, pedido, pago, carrito, auth) evoluciona y despliega de forma independiente. Un fallo o cambio en <code>pago</code> no obliga a recompilar todo el monorepo <code>ProyectoMS2026</code>.</p></li>
<li><p><strong>¿Qué ventaja tiene Docker en desarrollo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> MySQL por servicio en puertos fijos (<code>3381</code>, <code>3391</code>, etc.) sin instalar seis BDs en el host; la red <code>ms-net</code> unifica infra en PROD local.</p></li>
<li><p><strong>¿Cómo se nombra un microservicio en TechStore?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Carpeta y <code>artifactId</code> = nombre del servicio (<code>catalogo</code>, no <code>catalogo-ms</code>); coincide con <code>spring.application.name</code> y archivos en <code>config-repo</code>.</p></li>
</ol>""",
    "s02-configuracion-centralizada": """
<ol>
<li><p><strong>¿Qué problema resuelve la configuración centralizada?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Evita hardcodear puertos y JDBC en seis JARs; un cambio en <code>infra/config-repo</code> actualiza DEV (<code>7071</code>) y PROD (<code>7072</code>) para todos los perfiles.</p></li>
<li><p><strong>¿Qué diferencia hay entre Config Server y Config repo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Config repo son los YAML en disco; Config Server los expone por HTTP con <code>/{application}/{profile}</code> (ej. <code>/producto/dev</code>).</p></li>
<li><p><strong>¿Qué debe coincidir entre nombre de app y archivos?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>spring.application.name: producto</code> = archivo <code>producto-dev.yml</code> = segmento URL <code>/producto/dev</code>.</p></li>
</ol>""",
    "s06-feign-circuit-breaker": """
<ol>
<li><p><strong>¿Por qué un microservicio no debe leer la BD de otro?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Rompe el bounded context: <code>producto</code> no accede a <code>db_catalogo</code>; consulta <code>catalogo</code> vía Feign (<code>CatalogoClient</code>) y API REST. Igual patrón: <code>pedido</code>→<code>producto</code>, <code>pedido</code>→<code>pago</code>, <code>carrito</code>→<code>producto</code>.</p></li>
<li><p><strong>¿Qué pasa si el servicio llamado no responde?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Feign lanza excepción; el servicio llamador debe devolver error controlado (4xx/5xx con mensaje) sin caer todo el sistema. Opcional: circuit breaker en S06+.</p></li>
<li><p><strong>¿Qué evidencia demuestra comunicación entre servicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Logs en <code>producto</code> con llamada a <code>catalogo</code>; <code>GET http://localhost:7091/api/v1/productos/{id}/detalle</code> que enriquece categoría; traceId en ambos servicios.</p></li>
<li><p><strong>¿Cómo ayuda el correlation id?</strong></p>
<p><strong>Respuesta (TechStore):</strong> El Gateway propaga <code>traceId</code>; en logs de <code>producto</code> y <code>catalogo</code> aparece el mismo id para seguir una petición end-to-end.</p></li>
</ol>""",
    "s07-seguridad-jwt": """
<ol>
<li><p><strong>¿Qué diferencia hay entre autenticación y autorización?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Autenticación (<code>auth</code>, <code>/auth/login</code>) verifica identidad y emite JWT. Autorización decide si el token puede acceder a <code>/api/v1/productos</code> o rutas admin.</p></li>
<li><p><strong>¿Qué contiene un token?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Claims: usuario, roles, <code>iss: auth</code>, expiración; firmado con secreto compartido configurado en Gateway y microservicios vía <code>config-repo</code>.</p></li>
<li><p><strong>¿Por qué una ruta responde 401?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Sin header <code>Authorization: Bearer</code>, token expirado, firma inválida o ruta protegida sin login previo en <code>7091/auth/login</code>.</p></li>
<li><p><strong>¿Dónde validar acceso: Gateway, servicio o ambos?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Gateway filtra rutas públicas/protegidas; cada MS (<code>producto</code>, <code>pedido</code>, etc.) valida JWT en recursos sensibles — defensa en profundidad.</p></li>
</ol>""",
    "s08-angular-cors-jwt": """
<ol>
<li><p><strong>¿Por qué CORS es necesario con Angular?</strong></p>
<p><strong>Respuesta (TechStore):</strong> El frontend (<code>localhost:4200</code>) y el API (<code>localhost:7091</code>) son orígenes distintos; el navegador bloquea peticiones sin cabeceras CORS en Gateway.</p></li>
<li><p><strong>¿Cómo envía el token el cliente Angular?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Interceptor HTTP añade <code>Authorization: Bearer {token}</code> tras login contra <code>/auth/login</code> vía Gateway.</p></li>
<li><p><strong>¿Qué pasa si CORS está mal configurado?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Error en consola del navegador; las peticiones a <code>7091</code> fallan antes de llegar al backend aunque Postman funcione.</p></li>
</ol>""",
    "s09-kafka-eventos": """
<ol>
<li><p><strong>¿Cuándo usar mensajería asíncrona vs Feign?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Feign (S06) para consultas síncronas inmediatas; Kafka para eventos de dominio (ej. <code>pedido-creado</code>) donde <code>pago</code> o <code>carrito</code> reaccionan sin bloquear al emisor.</p></li>
<li><p><strong>¿Qué es un topic?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Canal de mensajes; productor (<code>pedido</code>) publica, consumidor (<code>pago</code>) se suscribe con grupo de consumidores.</p></li>
<li><p><strong>¿Cómo evidencias un evento publicado?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Logs del productor, consumer activo, mensaje en topic vía consola Kafka o herramienta de observabilidad.</p></li>
</ol>""",
    "s10-observabilidad": """
<ol>
<li><p><strong>¿Qué aporta Actuator en cada microservicio?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>/actuator/health</code>, métricas y prometheus en Gateway (<code>7091</code>) y en <code>catalogo</code>, <code>producto</code>, etc., para monitoreo unificado.</p></li>
<li><p><strong>¿Cómo correlacionas logs entre servicios?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>traceId</code> propagado desde Gateway (<code>TraceIdGlobalFilter</code>) visible en logs de todos los MS.</p></li>
<li><p><strong>¿Qué revisas si un servicio está lento?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Métricas de latencia, logs Feign, estado Eureka (<code>7081</code>) y health de MySQL del servicio.</p></li>
</ol>""",
    "s11-integracion-fullstack": """
<ol>
<li><p><strong>¿Por qué el frontend solo habla con Gateway?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Un solo origen API (<code>7091</code>), JWT y CORS centralizados; el cliente Angular no conoce los seis microservicios internos.</p></li>
<li><p><strong>¿Cómo se prueba el flujo completo?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Login → listar productos → carrito → pedido → pago, todo vía <code>7091</code> con token y datos en las BDs correspondientes.</p></li>
<li><p><strong>¿Qué evidencia integración real?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Capturas Angular + logs de <code>auth</code>, <code>producto</code>, <code>carrito</code>, <code>pedido</code>, <code>pago</code> con mismo <code>traceId</code>.</p></li>
</ol>""",
    "s13-validacion-integral": """
<ol>
<li><p><strong>¿Qué valida una prueba end-to-end en TechStore?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Flujo de negocio completo: UI o scripts contra Gateway, datos consistentes en BDs, eventos Kafka si aplica, y JWT válido en cadena.</p></li>
<li><p><strong>¿Qué orden de arranque respetas?</strong></p>
<p><strong>Respuesta (TechStore):</strong> <code>config-server</code> → <code>registry-server</code> → <code>gateway</code> → BDs → microservicios (<code>auth</code>, <code>catalogo</code>, <code>producto</code>, <code>pedido</code>, <code>pago</code>, <code>carrito</code>).</p></li>
</ol>""",
    "s14-cierre-tecnico": """
<ol>
<li><p><strong>¿Qué debe quedar documentado al cerrar U2?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Puertos, rutas Gateway, Feign entre MS, JWT, Kafka topics, observabilidad y enlaces GitHub Pages del equipo.</p></li>
<li><p><strong>¿Cómo demuestras deuda técnica resuelta?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Issues cerrados, PRs mergeados en rama del equipo y evidencia en documentación S06–S14.</p></li>
</ol>""",
}

MS_FEIGN_BLOCK = """
<h4 id="351-comunicacion-feign-techstore">3.5.1 Comunicación Feign entre microservicios TechStore</h4>
<p>En TechStore la práctica guiada detalla <code>producto</code> → <code>catalogo</code>. El mismo patrón aplica al resto:</p>
<table>
<thead><tr><th>Origen</th><th>Cliente Feign</th><th>Destino</th><th>Uso</th></tr></thead>
<tbody>
<tr><td><code>producto</code></td><td><code>CatalogoClient</code></td><td><code>catalogo</code></td><td>Validar/enriquecer categoría</td></tr>
<tr><td><code>pedido</code></td><td><code>ProductoClient</code></td><td><code>producto</code></td><td>Validar productos del pedido</td></tr>
<tr><td><code>pedido</code></td><td><code>PagoClient</code></td><td><code>pago</code></td><td>Iniciar/confirmar pago</td></tr>
<tr><td><code>pago</code></td><td><code>PedidoClient</code></td><td><code>pedido</code></td><td>Actualizar estado pedido</td></tr>
<tr><td><code>carrito</code></td><td><code>ProductoClient</code></td><td><code>producto</code></td><td>Precio/stock de ítems</td></tr>
</tbody>
</table>
<p>Cada cliente usa <code>@FeignClient(name = "…")</code> con el mismo nombre que <code>spring.application.name</code> del destino en Eureka.</p>
"""

ALICIA_EVIDENCE = {
    "s06-feign-circuit-breaker": ("S06", "Comunicación Feign de producto hacia catalogo", "producto", "catalogo"),
    "s07-seguridad-jwt": ("S07", "Login JWT y rutas protegidas vía auth", "auth", "8041"),
    "s09-kafka-eventos": ("S09", "Publicación/consumo de eventos de pedido", "pedido", "9101"),
    "s10-observabilidad": ("S10", "Métricas y health de producto", "producto", "9091"),
    "s11-integracion-fullstack": ("S11", "Flujo Angular → Gateway → producto", "producto", "9091"),
}


def inject_53(html: str, folder: str) -> str:
    if folder not in QA_53 or "Respuesta (TechStore)" in html.split("53-preguntas-de-defensa")[-1][:2000]:
        return html
    pattern = r'(<h3 id="53-preguntas-de-defensa-y-reflexion">5\.3 Preguntas de defensa y reflexión</h3>\s*)<ol>.*?</ol>'
    replacement = r"\1" + QA_53[folder].strip()
    return re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)


def inject_feign_table(html: str, folder: str) -> str:
    if folder != "s06-feign-circuit-breaker" or "351-comunicacion-feign-techstore" in html:
        return html
    marker = "<h3 id=\"36-levantar-config-server-en-dev\">"
    if marker in html:
        return html.replace(marker, MS_FEIGN_BLOCK + "\n" + marker)
    return html


def inject_s05_diagram(html: str) -> str:
    old = """    DB1["ecom_catálogo_db"]
    DB2["ecom_producto_db"]

    Cliente --&gt; Gateway
    Gateway -. descubre servicios .-&gt; Eureka
    Catalogo -. registra instancia .-&gt; Eureka
    Producto -. registra instancia .-&gt; Eureka
    Gateway --&gt; Catalogo
    Gateway --&gt; Producto"""
    new = """    subgraph MS["Microservicios TechStore"]
        Catalogo["catalogo 9081"]
        Producto["producto 9091"]
        Auth["auth 8041"]
        Pedido["pedido 9101"]
        Pago["pago 9111"]
        Carrito["carrito 9121"]
    end
    Config["config-server 7071"]
    Eureka["registry-server 7081"]

    Cliente --&gt; Gateway
    Gateway -. descubre .-&gt; Eureka
    Gateway -. config .-&gt; Config
    MS -. registra .-&gt; Eureka
    MS -. config .-&gt; Config
    Gateway --&gt; MS

    classDef done fill:#e8eaf6,stroke:#5c6bc0,color:#111
    classDef today fill:#ede7f6,stroke:#7b1fa2,stroke-width:2px,color:#111
    class Catalogo,Producto,Auth,Pedido,Pago,Carrito,Config,Eureka done
    class Gateway today"""
    return html.replace(old, new) if old in html else html


def inject_s05_qa(html: str) -> str:
    old = """<ol>
<li>Qué evidencia demuestra que el sistema funciona integrado?</li>
<li>Qué parte del producto puedes defender individualmente?</li>
<li>Qué revisas cuando una ruta del Gateway falla?</li>
</ol>"""
    new = """<ol>
<li><p><strong>¿Qué evidencia demuestra integración?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Demo por <code>7091</code>: Config (<code>7071</code>), Eureka (<code>7081</code>), seis MS registrados, rutas CRUD y dos instancias de un servicio.</p></li>
<li><p><strong>¿Qué parte defiendes individualmente?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Ej. configuración de <code>producto</code> en S02–S04 con PDF y commits en GitHub del Equipo 07.</p></li>
<li><p><strong>¿Qué revisas si falla una ruta Gateway?</strong></p>
<p><strong>Respuesta (TechStore):</strong> Health Gateway/Eureka, registro del MS, predicate en <code>gateway-dev.yml</code>, <code>lb://nombre</code> correcto.</p></li>
</ol>"""
    return html.replace(old, new) if old in html and "Respuesta (TechStore)" not in html else html


def main():
    for folder, qa in QA_53.items():
        path = SESSIONS_DIR / folder / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = inject_53(text, folder)
        new = inject_feign_table(new, folder)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"QA 5.3: {folder}")

    s05 = SESSIONS_DIR / "s05-evaluacion-u1" / "index.html"
    if s05.exists():
        t = s05.read_text(encoding="utf-8")
        u = inject_s05_diagram(inject_s05_qa(t))
        if u != t:
            s05.write_text(u, encoding="utf-8")
            print("Updated s05-evaluacion-u1")


if __name__ == "__main__":
    main()
