#!/usr/bin/env python3
"""Adapt referencias, silabo, guia, search_index to TechStore-Proyecto."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    ("alt=\"ecom logo\"", 'alt="TechStore logo"'),
    ("http://localhost:18888", "http://localhost:7071"),
    ("http://localhost:28888", "http://localhost:7072"),
    ("http://localhost:18761", "http://localhost:7081"),
    ("http://localhost:28761", "http://localhost:7082"),
    ("http://localhost:18080", "http://localhost:7091"),
    ("http://localhost:28082", "http://localhost:7092"),
    ("localhost:18080", "localhost:7091"),
    ("localhost:28082", "localhost:7092"),
    ("puerto <code>18888</code>", "puerto <code>7071</code>"),
    ("puerto <code>18761</code>", "puerto <code>7081</code>"),
    ("ecom_auth_db", "db_auth"),
    ("ecom_catalogo_db", "db_catalogo"),
    ("ecom_producto_db", "db_producto"),
    ("ecom_orden_db", "db_pedido"),
    ("ecom_pago_db", "db_pago"),
    ("ecom_carrito_db", "db_carrito"),
    ("auth-ms", "auth"),
    ("catálogo-ms", "catalogo"),
    ("producto-ms", "producto"),
    ("orden-ms", "pedido"),
    ("pago-ms", "pago"),
    ("carrito-ms", "carrito"),
    ("ecom-postgres-catalogo-dev", "mysql-catalogo-dev"),
    ("ecom-kafka-dev", "kafka"),
    ("ecom-kafka-prod", "kafka"),
    ("orden-eventos", "pedido-eventos"),
    ("<code>ecom</code> / <code>ecom</code>", "<code>root</code> / <code>root</code>"),
    ("Credenciales: <code>ecom</code>", "Credenciales: <code>root</code>"),
    ("psql", "mysql"),
    (" -U ecom ", " -uroot "),
    ("-U ecom ", "-uroot "),
    ("infra/config</code> este", "infra/config-server</code> esté"),
    ("proyecto <code>ecom</code>", "proyecto <code>TechStore-Proyecto</code> (<code>ProyectoMS2026</code>)"),
    ("Arquitectura del producto en ecom", "Arquitectura del producto en TechStore-Proyecto"),
    ("<code>auth-ms</code>", "<code>auth</code>"),
    ("<code>pago-ms</code>", "<code>pago</code>"),
    ("http://localhost:41085", "http://localhost:28085"),
    ("http://localhost:18888/producto-ms/dev", "http://localhost:7071/producto/dev"),
    ("http://localhost:28888/producto-ms/prod", "http://localhost:7072/producto/prod"),
    ("`ecom`", "`TechStore-Proyecto`"),
]

PUERTOS_BODY = """
<h2 id="microservicios-dev">Microservicios DEV (Maven en host)</h2>
<table>
<thead><tr><th>Servicio</th><th style="text-align: right;">Puerto</th><th>Swagger / health</th></tr></thead>
<tbody>
<tr><td><code>catalogo</code></td><td style="text-align: right;">9081</td><td><code>http://localhost:9081/swagger-ui.html</code></td></tr>
<tr><td><code>auth</code></td><td style="text-align: right;">8041</td><td><code>http://localhost:8041/actuator/health</code></td></tr>
<tr><td><code>producto</code></td><td style="text-align: right;">9091</td><td><code>http://localhost:9091/swagger-ui.html</code></td></tr>
<tr><td><code>pedido</code></td><td style="text-align: right;">9101</td><td><code>http://localhost:9101/swagger-ui.html</code></td></tr>
<tr><td><code>pago</code></td><td style="text-align: right;">9111</td><td><code>http://localhost:9111/swagger-ui.html</code></td></tr>
<tr><td><code>carrito</code></td><td style="text-align: right;">9121</td><td><code>http://localhost:9121/swagger-ui.html</code></td></tr>
<tr><td><code>techstore-proyecto</code> (Angular)</td><td style="text-align: right;">4200</td><td><code>http://localhost:4200</code></td></tr>
</tbody>
</table>
<h2 id="mysql-dev">MySQL DEV (Docker por servicio)</h2>
<table>
<thead><tr><th>Servicio</th><th style="text-align: right;">Puerto host</th><th>Base de datos</th><th>Contenedor compose</th></tr></thead>
<tbody>
<tr><td><code>auth</code></td><td style="text-align: right;">3341</td><td><code>db_auth</code></td><td><code>mysql-auth-dev</code> en <code>services/auth</code></td></tr>
<tr><td><code>catalogo</code></td><td style="text-align: right;">3381</td><td><code>db_catalogo</code></td><td><code>mysql-catalogo-dev</code></td></tr>
<tr><td><code>producto</code></td><td style="text-align: right;">3391</td><td><code>db_producto</code></td><td><code>mysql-producto-dev</code></td></tr>
<tr><td><code>pedido</code></td><td style="text-align: right;">3401</td><td><code>db_pedido</code></td><td><code>mysql-pedido-dev</code></td></tr>
<tr><td><code>pago</code></td><td style="text-align: right;">3411</td><td><code>db_pago</code></td><td><code>mysql-pago-dev</code></td></tr>
<tr><td><code>carrito</code></td><td style="text-align: right;">3421</td><td><code>db_carrito</code></td><td><code>mysql-carrito-dev</code></td></tr>
</tbody>
</table>
<p>Credenciales: <code>root</code> / <code>root</code>.</p>
<p>Ejemplo MySQL en contenedor:</p>
<div class="highlight"><pre><span></span><code>docker exec -it mysql-catalogo-dev mysql -uroot -proot db_catalogo
</code></pre></div>
<h2 id="kafka">Kafka (PROD local)</h2>
<table>
<thead><tr><th>Componente</th><th>URL / puerto</th></tr></thead>
<tbody>
<tr><td>Broker (host)</td><td><code>localhost:29092</code></td></tr>
<tr><td>Kafka UI</td><td><code>http://localhost:28085</code></td></tr>
<tr><td>Bootstrap dentro de <code>ms-net</code></td><td><code>kafka:9092</code></td></tr>
</tbody>
</table>
<h2 id="config-por-servicio">Config por servicio</h2>
<p>DEV:</p>
<div class="highlight"><pre><span></span><code>http://localhost:7071/producto/dev
http://localhost:7071/gateway/dev
</code></pre></div>
<p>PROD:</p>
<div class="highlight"><pre><span></span><code>http://localhost:7072/producto/prod
http://localhost:7072/gateway/prod
</code></pre></div>
"""

MYSQL_BLOCK_OLD = re.compile(
    r'<h2 id="postgresql-dev">.*?</h2>\s*<div class="highlight"><pre><span></span><code>http://localhost:7072/producto/prod\s*\nhttp://localhost:7072/gateway/prod\s*\n</code></pre></div>',
    re.DOTALL,
)


def apply_replacements(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # Fix nav anchors postgresql -> mysql
    text = text.replace('id="postgresql-dev"', 'id="mysql-dev"')
    text = text.replace('id="postgresql-prod"', 'id="mysql-prod"')
    text = text.replace('#postgresql-dev', '#mysql-dev')
    text = text.replace('#postgresql-prod', '#mysql-prod')
    text = text.replace('PostgreSQL DEV', 'MySQL DEV')
    text = text.replace('PostgreSQL PROD', 'MySQL PROD (Docker)')
    text = text.replace('postgresql-dentro-del-contenedor', 'mysql-dentro-del-contenedor')
    text = text.replace('PostgreSQL dentro del contenedor', 'MySQL dentro del contenedor')
    # Port numbers in old mysql tables
    text = re.sub(r'<td style="text-align: right;">15431</td>', '<td style="text-align: right;">3341</td>', text)
    text = re.sub(r'<td style="text-align: right;">15432</td>', '<td style="text-align: right;">3381</td>', text)
    text = re.sub(r'<td style="text-align: right;">15433</td>', '<td style="text-align: right;">3391</td>', text)
    text = re.sub(r'<td style="text-align: right;">15434</td>', '<td style="text-align: right;">3401</td>', text)
    text = re.sub(r'<td style="text-align: right;">15435</td>', '<td style="text-align: right;">3411</td>', text)
    text = re.sub(r'<td style="text-align: right;">25431</td>', '<td style="text-align: right;">3341</td>', text)
    text = re.sub(r'<td style="text-align: right;">25432</td>', '<td style="text-align: right;">3381</td>', text)
    text = re.sub(r'<td style="text-align: right;">25433</td>', '<td style="text-align: right;">3391</td>', text)
    text = re.sub(r'<td style="text-align: right;">25434</td>', '<td style="text-align: right;">3401</td>', text)
    text = re.sub(r'<td style="text-align: right;">25435</td>', '<td style="text-align: right;">3411</td>', text)
    return text


def patch_puertos(text: str) -> str:
    # Replace from postgresql-dev/mysql-dev through config section
    pattern = r'(<h2 id="mysql-dev">|<h2 id="postgresql-dev">).*?(?=<h2 id="config-por-servicio">)'
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(pattern, PUERTOS_BODY.split("<h2 id=\"config-por-servicio\">")[0], text, count=1, flags=re.DOTALL)
    # Replace config block if still old
    text = text.replace(
        "<div class=\"highlight\"><pre><span></span><code>http://localhost:7071/producto-ms/dev\n</code></pre></div>",
        "<div class=\"highlight\"><pre><span></span><code>http://localhost:7071/producto/dev\nhttp://localhost:7071/gateway/dev\n</code></pre></div>",
    )
    return text


def patch_comandos_mysql_psql(text: str) -> str:
    old_psql_block = """<p>Dentro de <code>psql</code>:</p>
<div class="highlight"><pre><span></span><code><span class="err">\\</span><span class="n">dt</span>
<span class="err">\\</span><span class="n">d</span><span class="w"> </span><span class="n">categorias</span>
<span class="k">SELECT</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="k">FROM</span><span class="w"> </span><span class="n">categorias</span><span class="p">;</span>
<span class="err">\\</span><span class="n">q</span>
</code></pre></div>"""
    new_mysql = """<p>Dentro de MySQL:</p>
<div class="highlight"><pre><span></span><code>SHOW TABLES;
DESCRIBE categorias;
SELECT * FROM categorias;
EXIT;
</code></pre></div>"""
    return text.replace(old_psql_block, new_mysql)


def main():
    targets = list((ROOT / "referencias").rglob("index.html"))
    targets += [
        ROOT / "silabo" / "index.html",
        ROOT / "silabo_dist_2026_1" / "index.html",
        ROOT / "silabo_dist_2026_2" / "index.html",
        ROOT / "guia-curso" / "index.html",
        ROOT / "404.html",
    ]
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = apply_replacements(text)
        if "puertos-y-accesos" in text:
            new = patch_puertos(new)
        if "comandos-bash" in str(path) or "comandos-powershell" in str(path):
            new = patch_comandos_mysql_psql(new)
            new = new.replace(
                'docker<span class="w"> </span><span class="nb">exec</span><span class="w"> </span>-it<span class="w"> </span>mysql-catalogo-dev<span class="w"> </span>mysql<span class="w"> </span>-uroot<span class="w"> </span>ecom<span class="w"> </span>-d<span class="w"> </span>db_catalogo',
                'docker<span class="w"> </span><span class="nb">exec</span><span class="w"> </span>-it<span class="w"> </span>mysql-catalogo-dev<span class="w"> </span>mysql<span class="w"> </span>-uroot<span class="w"> </span>-proot<span class="w"> </span>db_catalogo',
            )
            new = new.replace(
                'mysql-catalogo-dev</span> <span class="n">mysql</span> <span class="n">-uroot</span> <span class="n">ecom</span> <span class="n">-d</span> <span class="n">db_catalogo</span>',
                'mysql-catalogo-dev</span> <span class="n">mysql</span> <span class="n">-uroot</span> <span class="n">-proot</span> <span class="n">db_catalogo</span>',
            )
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"Updated: {path.relative_to(ROOT)}")

    search = ROOT / "search" / "search_index.json"
    if search.exists():
        t = search.read_text(encoding="utf-8")
        u = apply_replacements(t)
        u = u.replace("ecom", "TechStore-Proyecto")
        u = u.replace("TechStore-Proyecto-postgres", "TechStore-Proyecto")
        u = u.replace("TechStore-Proyecto_auth_db", "db_auth")
        if u != t:
            search.write_text(u, encoding="utf-8")
            print("Updated: search/search_index.json")


if __name__ == "__main__":
    main()
