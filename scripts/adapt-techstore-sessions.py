#!/usr/bin/env python3
"""Adapt ecom course HTML sessions to TechStore-Proyecto (ProyectoMS2026)."""
from pathlib import Path
import re

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sesiones"

# Order matters: longer / more specific patterns first
REPLACEMENTS = [
    ("infra/config/config-repo", "infra/config-repo"),
    ("infra/config-server-repo", "infra/config-repo"),  # fix prior bad replace
    ("catalogo-ms", "catalogo"),
    ("producto-ms", "producto"),
    ("pedido-ms", "pedido"),
    ("pago-ms", "pago"),
    ("carrito-ms", "carrito"),
    ("auth-ms", "auth"),
    ("CATALOGO-MS", "CATALOGO"),
    ("PRODUCTO-MS", "PRODUCTO"),
    ("lb://catalogo-ms", "lb://catalogo"),
    ("lb://producto-ms", "lb://producto"),
    ("lb://pedido-ms", "lb://pedido"),
    ("lb://pago-ms", "lb://pago"),
    ("lb://carrito-ms", "lb://carrito"),
    ("lb://auth-ms", "lb://auth"),
    ("ecom-gateway", "gateway"),
    ("ecom-config", "config-server"),
    ("ecom-prod-net", "ms-net"),
    ("ecom-s01", "TechStore-s01"),
    ("ecom-s02", "TechStore-s02"),
    ("ecom-s03", "TechStore-s03"),
    ("ecom-s04", "TechStore-s04"),
    ("ecom-s05", "TechStore-s05"),
    ("ecom-s06", "TechStore-s06"),
    ("ecom-s07", "TechStore-s07"),
    ("ecom-s08", "TechStore-s08"),
    ("ecom-s09", "TechStore-s09"),
    ("ecom-s10", "TechStore-s10"),
    ("ecom-s11", "TechStore-s11"),
    ("ecom-s12", "TechStore-s12"),
    ("ecom-s13", "TechStore-s13"),
    ("ecom-s14", "TechStore-s14"),
    ("ecom-s15", "TechStore-s15"),
    ("ecom-s16", "TechStore-s16"),
    ("http://localhost:18080", "http://localhost:7091"),
    ("localhost:18080", "localhost:7091"),
    ("http://localhost:28082", "http://localhost:7092"),
    ("localhost:28082", "localhost:7092"),
    ("http://localhost:28080", "http://localhost:7092"),
    ("localhost:28080", "localhost:7092"),
    ("http://localhost:18761", "http://localhost:7081"),
    ("localhost:18761", "localhost:7081"),
    ("http://localhost:28761", "http://localhost:7082"),
    ("localhost:28761", "localhost:7082"),
    ("http://localhost:18888", "http://localhost:7071"),
    ("localhost:18888", "localhost:7071"),
    (":8761 interno", ":7081 interno"),
    (":8761/eureka", ":7081/eureka"),
    (":8888 interno", ":7071 interno"),
    ("config-server:8888", "config-server:7071"),
    ("gateway&lt;br/&gt;8080 interno", "gateway&lt;br/&gt;7091 interno"),
    ("catalogo&lt;br/&gt;8080 interno", "catalogo&lt;br/&gt;8082 interno"),
    ("producto&lt;br/&gt;8080 interno", "producto&lt;br/&gt;9092 interno"),
    ('Eureka["eureka', 'Eureka["registry-server'),
    ('Eureka&lt;br/&gt;localhost:7081"', 'registry-server&lt;br/&gt;localhost:7081"'),
    ('Gateway&lt;br/&gt;localhost:7091"', 'Gateway&lt;br/&gt;7091"'),
    ("#22-arquitectura-del-producto-en-ecom", "#22-arquitectura-del-producto-en-techstore"),
    ("id=\"22-arquitectura-del-producto-en-ecom\"", "id=\"22-arquitectura-del-producto-en-techstore\""),
    ("http://eureka:8761/eureka", "http://registry-server:7081/eureka"),
    ("http://eureka:8761", "http://registry-server:7081"),
    ("http://config-server:8888", "http://config-server:7071"),
    ("http://gateway:8080", "http://gateway:7091"),
    ("infra/eureka", "infra/registry-server"),
    ("cd infra/config\n", "cd infra/config-server\n"),
    ("cd infra/config\r\n", "cd infra/config-server\r\n"),
    ("compose-dev.yml", "docker-compose-dev.yml"),
    ("infra/compose.yml", "infra/docker-compose.yml"),
    ("docker compose up -d --build config eureka", "docker compose up -d --build config-server registry-server"),
    ("docker compose up -d --build config eureka gateway", "docker compose up -d --build config-server registry-server gateway"),
    ("config + eureka + gateway", "config-server + registry-server + gateway"),
    ("config + eureka", "config-server + registry-server"),
    ('alt="ecom logo"', 'alt="TechStore logo"'),
    ("Artifact Id: ecom-gateway", "Artifact Id: gateway"),
    ("spring.application.name: ecom-gateway", "spring.application.name: gateway"),
    ("catálogo-ms", "catalogo"),
    ("https://github.com/261dist/ecom.git", "https://github.com/AliciaVizcarraRamos/PROYECTO-FINAL-TechStore.git"),
    ("Arquitectura del producto en ecom", "Arquitectura del producto en TechStore"),
    ("#22-arquitectura-del-producto-en-ecom", "#22-arquitectura-del-producto-en-techstore"),
    ("en <code>ecom</code>", "en TechStore-Proyecto"),
    ("monorepo <code>ecom</code>", "monorepo <code>ProyectoMS2026</code> (TechStore)"),
    ("S04_Equipo##_ApellidoNombre", "S04_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S05_Equipo##_ApellidoNombre", "S05_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S06_Equipo##_ApellidoNombre", "S06_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S07_Equipo##_ApellidoNombre", "S07_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S08_Equipo##_ApellidoNombre", "S08_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S09_Equipo##_ApellidoNombre", "S09_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S10_Equipo##_ApellidoNombre", "S10_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S11_Equipo##_ApellidoNombre", "S11_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S12_Equipo##_ApellidoNombre", "S12_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S13_Equipo##_ApellidoNombre", "S13_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S14_Equipo##_ApellidoNombre", "S14_Equipo07_TechStore-g2_ApellidoNombre"),
    ("S15_Equipo##_ApellidoNombre", "S15_Equipo07_TechStore-g2_ApellidoNombre"),
    ("ecom_catálogo_db", "db_catalogo"),
    ("ecom_producto_db", "db_producto"),
    ("ecom_auth_db", "db_auth"),
    ("ecom_orden_db", "db_pedido"),
    ("ecom_pago_db", "db_pago"),
    ("ecom_carrito_db", "db_carrito"),
    ("Arquitectura ecom v2026", "Arquitectura TechStore-Proyecto"),
    ("#21-arquitectura-ecom-v2026", "#21-arquitectura-techstore"),
    ("id=\"21-arquitectura-ecom-v2026\"", "id=\"21-arquitectura-techstore\""),
    ("D 18761", "D 7081"),
    ("P 28761", "P 7082"),
    ("D 18080", "D 7091"),
    ("P 28082", "P 7092"),
    ("jdbc:postgresql://localhost:15431/ecom_auth_db", "jdbc:mysql://localhost:3341/db_auth"),
    ("Artifact Id: ecom-auth", "Artifact Id: auth"),
    ("ecom-kafka-dev", "kafka"),
    ("ecom-kafka-prod-net", "ms-net"),
    (" + ecom-kafka-prod-net", ""),
    ("ecom-ng", "techstore-proyecto"),
    ("clients/ecom-ng", "techstore-proyecto"),
    ("techstore-app", "techstore-proyecto"),
    ("frontend/techstore-app", "techstore-proyecto"),
    ('username: ecom\n', 'username: root\n'),
    ('password: ecom\n', 'password: root\n'),
    ("S16_Equipo##_ApellidoNombre", "S16_Equipo07_TechStore-g2_ApellidoNombre"),
    ("orden-ms", "pedido"),
    ("services/orden-ms", "services/pedido"),
    ("com.upeu.ordenms", "com.upeu.pedido"),
    ("orden-eventos", "pedido-eventos"),
    ("orden_db", "db_pedido"),
    ("OrdenDB", "PedidoDB"),
    ('Orden["pedido', 'Pedido["pedido'),
    ("Gateway --&gt; Orden", "Gateway --&gt; Pedido"),
    ("Orden --&gt;", "Pedido --&gt;"),
    ("    Orden[", "    Pedido["),
    ("implementar-persistencia-inicial-en-pedido-ms", "implementar-persistencia-inicial-en-pedido"),
    ("implementar-productor-en-pedido-ms", "implementar-productor-en-pedido"),
    ("consumir-resultado-de-pago-en-pedido-ms", "consumir-resultado-de-pago-en-pedido"),
    ("jdbc:postgresql://localhost:15431/db_auth", "jdbc:mysql://localhost:3341/db_auth"),
    ("jdbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}", "jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}"),
    ("org.postgresql.Driver", "com.mysql.cj.jdbc.Driver"),
    ('<span class="l l-Scalar l-Scalar-Plain">ecom</span>', '<span class="l l-Scalar l-Scalar-Plain">root</span>'),
    ('orden-ms&lt;br/&gt;puerto dinamico', 'pedido&lt;br/&gt;9101'),
    ('orden-ms&lt;br/&gt;8080 interno', 'pedido&lt;br/&gt;9102 interno'),
    ('Microservicios&lt;br/&gt;puerto dinamico', 'MS TechStore&lt;br/&gt;9081-9121'),
    ('Microservicios: puerto dinamico', 'Microservicios: 9081-9121 (DEV)'),
    ('(Keycloak u otro)', 'JWT'),
    ('AuthDB["auth_db&lt;br/&gt;D 15431&lt;br/&gt;P 25431"]', 'AuthDB["db_auth&lt;br/&gt;D 3341&lt;br/&gt;P 3341"]'),
    ('CatalogoDB["catálogo_db&lt;br/&gt;D 15432&lt;br/&gt;P 25432"]', 'CatalogoDB["db_catalogo&lt;br/&gt;D 3381"]'),
    ('ProductoDB["producto_db&lt;br/&gt;D 15433&lt;br/&gt;P 25433"]', 'ProductoDB["db_producto&lt;br/&gt;D 3391"]'),
    ('PedidoDB["db_pedido&lt;br/&gt;D 15434&lt;br/&gt;P 25434"]', 'PedidoDB["db_pedido&lt;br/&gt;D 3401"]'),
    ('PagoDB["pago_db&lt;br/&gt;D 15435&lt;br/&gt;P 25435"]', 'PagoDB["db_pago&lt;br/&gt;D 3411"]'),
    ('Config["Config&lt;br/&gt;D 18888&lt;br/&gt;P 28888"]', 'Config["config-server&lt;br/&gt;D 7071&lt;br/&gt;P 7072"]'),
    ('catalogo&lt;br/&gt;dinamico', 'catalogo&lt;br/&gt;9081 / 8082'),
    ('producto&lt;br/&gt;dinamico', 'producto&lt;br/&gt;9091 / 9092'),
    ('pedido&lt;br/&gt;dinamico', 'pedido&lt;br/&gt;9101 / 9102'),
    ('pago&lt;br/&gt;dinamico', 'pago&lt;br/&gt;9111 / 9112'),
    ('auth&lt;br/&gt;dinamico', 'auth&lt;br/&gt;8041 / 8042'),
]

MERMAID_CLASS_OLD = re.compile(
    r"classDef done fill:#e8f5e9,stroke:#2e7d32,color:#111;?\s*"
    r"classDef today fill:#ffe08a,stroke:#9a6b00,stroke-width:2px,color:#111;?",
    re.MULTILINE,
)
MERMAID_CLASS_NEW = """classDef done fill:#e8eaf6,stroke:#5c6bc0,color:#111
    classDef today fill:#ede7f6,stroke:#7b1fa2,stroke-width:2px,color:#111
    classDef planned fill:#e3f2fd,stroke:#1565c0,color:#111"""


def adapt_content(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = MERMAID_CLASS_OLD.sub(MERMAID_CLASS_NEW, text)
    # Fix docker service names in compose snippets (standalone words)
    text = re.sub(r"\bcontainer_name:\s*ecom-gateway\b", "container_name: gateway", text)
    text = re.sub(r'ports:\s*\n\s*-\s*"28082:8080"', 'ports:\n      - "7092:7091"', text)
    text = re.sub(r'EXPOSE\s+8080', "EXPOSE 7091", text)
    return text


def main():
    updated = 0
    for html in sorted(SESSIONS_DIR.glob("s*/index.html")):
        original = html.read_text(encoding="utf-8")
        adapted = adapt_content(original)
        if adapted != original:
            html.write_text(adapted, encoding="utf-8")
            updated += 1
            print(f"Updated: {html.relative_to(SESSIONS_DIR.parent)}")
    print(f"Done. {updated} files modified.")


if __name__ == "__main__":
    main()
