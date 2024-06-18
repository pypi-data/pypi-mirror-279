import rdflib
import html

import pandas as pd
from itables import init_notebook_mode, show

init_notebook_mode()


def make_html(node, nsm=None, max_len=50):
    if isinstance(node, rdflib.Literal):
        if isinstance(node.toPython(), bytes):
            return "BLOB"
    out = esc = html.escape(node.n3(nsm))
    out = out[:max_len]
    if isinstance(node, rdflib.URIRef):
        out = f'<a href="{str(node)}" title="{str(node)}">{out}</a>'
    if '"' in esc:
        print(esc)
    out += f" <button onclick=\"filt('s', this, '{esc}')\">s</button>"
    out += f"<button onclick=\"filt('p', this, '{esc}')\">p</button>"
    out += f"<button onclick=\"filt('o', this, '{esc}')\">o</button>"
    return out


def table(g: rdflib.Graph, max_len=50):
    script = """
    <script>
    filt = (x, button, value) => {
        table = button.closest('table');
        table.querySelectorAll('input').forEach((input) => {
            input.value = '';
            input.dispatchEvent(new Event('change'));
        });
        input = table.querySelectorAll('input[placeholder="Search '+x+'"]')[0];
        input.value = value;
        input.dispatchEvent(new Event('change'));
    }
    reset = (element) => {
        table = element.parentElement.querySelector('table');
        table.querySelectorAll('input').forEach((input) => {
            input.value = '';
            input.dispatchEvent(new Event('change'));
        });
    }
    </script>
    <button style="position:absolute; z-index:999" onclick="reset(this)">Clear search</button>
    """
    df = pd.DataFrame(list(g), columns=["s", "p", "o"])
    df = df.applymap(make_html, nsm=g.namespace_manager, max_len=max_len)  # type: ignore
    return show(
        df,
        column_filters="header",
        layout={
            "topStart": None,
            "topEnd": None,
            "bottomStart": "pageLength",
            "top": "info",
        },
        tags=script,
    )
