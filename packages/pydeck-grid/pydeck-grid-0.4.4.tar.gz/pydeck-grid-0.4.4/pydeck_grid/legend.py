import jinja2
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, Normalize
from .colormap import GridColormap


class Colorbar:
    def __init__(self, colormap, vmin=0, vmax=1.0, labels=None, units=None):
        self.colormap = colormap
        if isinstance(colormap, GridColormap):
            self.colormap = colormap
        elif colormap is not None:
            self.colormap = GridColormap(colormap, vmin, vmax)
        self.labels = labels
        self.units = units

    def to_html(
        self,
        width=200,
        height=50,
        labelcolor="white",
        style={},
    ):
        if self.colormap is None:
            return "<div></div>"
        grads = self.labels or self.colormap["domain"]
        labelwidth = int(width / (len(grads) + int(self.units is not None)))
        gradient = [grads[0], grads[0], grads[0]] if self.units else [grads[0]]
        if len(self.colormap["scale"]) == len(self.colormap["domain"]):
            lscm = LinearSegmentedColormap.from_list(
                "colormap", zip(self.colormap["scale"], self.colormap["domain"])
            )
            norm = lambda x: x
        else:
            lscm = ListedColormap(self.colormap["scale"])
            norm = Normalize(
                vmin=self.colormap["domain"][0], vmax=self.colormap["domain"][-1]
            )
        for i, l in enumerate(grads):
            i0 = i if i < len(grads) - 1 else i - 1
            gradient = gradient + [l, 0.5 * (l + grads[i0 + 1])]
        colorString = []
        for g in gradient:
            rgb = [int(255 * c) for c in lscm(norm(g))]
            colorString.append(f"rgb({rgb[0]},{rgb[1]},{rgb[2]})")
        ticks = ([self.units] if self.units else []) + grads
        labelsize = min(int(width / 2 / len(grads)), int(height / 1.5))
        divstyle = {
            "width": f"{width}px",
            "height": f"{height}px",
            "border-radius": "5px",
            "background": f"linear-gradient(to right, {','.join(colorString)})",
            "font-size": f"{labelsize}px",
            "display": "flex",
            "align-items": "center",
            "font-family": "sans-serif",
        }
        divstyle.update(style)
        stylestr = ";".join([f"{k}:{v}" for k, v in divstyle.items()])
        colorbar_template = jinja2.Template(
            """<div style=" {{ stylestr }} ">
            {% for tick in ticks %}
            <span
            style="
                width: {{ labelwidth }}px;
                text-align: center;
                vertical-align: middle;
                display: inline-block;
                color: {{ labelcolor }}"
            >
            {{ tick }}
            </span>
            {% endfor %}
        </div>
        """
        )
        html_str = colorbar_template.render(
            colorString=colorString,
            width=width,
            height=height,
            ticks=ticks,
            labelsize=labelsize,
            labelwidth=labelwidth,
            labelcolor=labelcolor,
            stylestr=stylestr,
        )
        return html_str
