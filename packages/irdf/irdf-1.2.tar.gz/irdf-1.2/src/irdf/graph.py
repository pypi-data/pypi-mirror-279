import collections
import typing

import rdflib
import requests
import ipycytoscape


def make_node(n, g, lang=None, p_filter=(), labels=()):
    labels = dict(labels)
    n3 = n.n3(g.namespace_manager)
    data = {"id": hex(abs(hash(n)))}
    if not n3.startswith("<"):
        data["label"] = labels.get(n, n3)
    else:
        n3 = str(n)

    tt = f'<b><a style="color:white" href="{n}">{n3}</a></b>'
    tt += '<ul style="color:white">'
    for p, o in g[n]:
        if isinstance(o, rdflib.Literal):
            if p_filter and not any(f in str(p) for f in p_filter):
                continue
            if lang and getattr(o, "language", None) and o.language != lang:
                continue
            p_n3, o_str = p.n3(g.namespace_manager), str(o.toPython())
            p_str = labels.get(p, p_n3)
            if len(o_str) > 50:
                o_str = o_str[:50] + "..."
            tt += "<li>"
            tt += f'<a style="color:white" href="{p}">{p_str}</a> '
            tt += o_str
            tt += "</li>"
    data["tooltip"] = tt + "</ul>"

    if any(ext in n.lower() for ext in [".jpg", ".svg", ".png"]):
        data["image"] = requests.get(n, stream=True).url
    return {"data": data}


def make_graph_obj(g, p_filter=None, lang="en", label_path=None, max_edge_count=4):
    label_path = label_path or "rdfs:label"
    labels = {
        b["s"]: str(b["l"])
        for b in g.query("select * where { ?s " + label_path + " ?l }").bindings
        if lang and getattr(b["l"], "language", None) and b["l"].language == lang
    }
    nodes, edges = set(), []
    p_count = collections.Counter(g.predicates())
    for s, p, o in g:
        if p_filter and not any(f in str(p) for f in p_filter):
            continue
        if isinstance(o, rdflib.URIRef):
            if p_count[p]:
                nodes.add(s)
                nodes.add(o)
                data = {
                    "source": hex(abs(hash(s))),
                    "target": hex(abs(hash(o))),
                    "label": labels.get(p, p.n3(g.namespace_manager)),
                }
                if p_count[p] > max_edge_count:
                    data["label"] += f" (+ {p_count[p]-1})"
                    p_count[p] = 0
                edges.append({"data": data})

    nodes = [
        make_node(n, g, lang=lang, p_filter=p_filter, labels=labels) for n in nodes
    ]
    return {"nodes": nodes, "edges": edges}


def make_widget(data):
    cytoscapeobj = ipycytoscape.CytoscapeWidget()
    cytoscapeobj.graph.add_graph_from_json(data, directed=True)
    cytoscapeobj.set_style(
        cytoscapeobj.get_style()
        + [
            {
                "selector": "node",
                "css": {
                    "content": "data(label)",
                    "font-size": "8pt",
                    "text-outline-width": 1,
                    "text-wrap": "wrap",
                    "text-valign": "center",
                    "color": "white",
                },
            },
            {
                "selector": "node[image]",
                "css": {
                    "width": 80,
                    "height": 80,
                    "background-fit": "contain",
                    "background-image": "data(image)",
                    "background-color": "white",
                    "border-width": "1px",
                },
            },
            {
                "selector": "edge",
                "css": {
                    "content": "data(label)",
                    "text-valign": "center",
                    "color": "white",
                    "font-size": "8pt",
                    "text-outline-width": 1,
                },
            },
        ]
    )
    return cytoscapeobj


def graph(
    g: rdflib.Graph,
    p_filter: typing.Collection[str] = (),
    lang: typing.Optional[str] = "en",
    label_path: typing.Optional[str] = None,
    max_edge_count: int = 4,
):
    data = make_graph_obj(
        g, p_filter=p_filter, label_path=label_path, max_edge_count=max_edge_count
    )
    return make_widget(data)
