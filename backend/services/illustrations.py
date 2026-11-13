"""Hand-drawn SVG illustrations (320x240 canvas) for the Home & Kitchen products.

Each entry is the inner SVG markup for one product, keyed by product name.
"""

def _shadow(cx=160, cy=196, rx=80):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="9" fill="#000" opacity=".14"/>'


HOME_KITCHEN = {
    "Steel Water Bottle": _shadow(160, 200, 40) + """
<rect x="138" y="66" width="44" height="130" rx="14" fill="#8fa3b8"/>
<rect x="146" y="72" width="8" height="118" rx="4" fill="#fff" opacity=".35"/>
<rect x="132" y="116" width="56" height="26" fill="#2f6bff"/>
<rect x="146" y="40" width="28" height="30" rx="6" fill="#2b3340"/>
<path d="M174 48 q22 0 22 18 v10" fill="none" stroke="#2b3340" stroke-width="6" stroke-linecap="round"/>""",

    "Non-stick Cookware Set": _shadow() + """
<rect x="62" y="104" width="96" height="76" rx="8" fill="#2d3440"/>
<rect x="52" y="116" width="14" height="10" rx="3" fill="#161a21"/><rect x="154" y="116" width="14" height="10" rx="3" fill="#161a21"/>
<ellipse cx="110" cy="102" rx="52" ry="12" fill="#c7ced8"/>
<circle cx="110" cy="94" r="6" fill="#161a21"/>
<ellipse cx="226" cy="156" rx="52" ry="22" fill="#2d3440"/>
<ellipse cx="226" cy="152" rx="44" ry="16" fill="#4a5362"/>
<rect x="268" y="148" width="46" height="9" rx="4" fill="#161a21"/>""",

    "Digital Air Fryer": _shadow() + """
<rect x="100" y="52" width="120" height="140" rx="26" fill="#2a2f3a"/>
<rect x="116" y="68" width="88" height="26" rx="8" fill="#0f1319"/>
<text x="160" y="87" font-size="16" font-family="monospace" fill="#46f0a0" text-anchor="middle">180°</text>
<circle cx="136" cy="116" r="8" fill="#586173"/><circle cx="184" cy="116" r="8" fill="#586173"/>
<rect x="116" y="136" width="88" height="40" rx="10" fill="#3a4150"/>
<rect x="140" y="148" width="40" height="8" rx="4" fill="#8892a3"/>""",

    "Memory Foam Pillow": _shadow(160, 178, 90) + """
<rect x="64" y="80" width="192" height="92" rx="44" fill="#f6f3ff"/>
<rect x="64" y="80" width="192" height="92" rx="44" fill="none" stroke="#b9a8f5" stroke-width="3"/>
<rect x="80" y="94" width="160" height="64" rx="32" fill="none" stroke="#b9a8f5" stroke-width="2" stroke-dasharray="6 6"/>
<path d="M92 112 q68 -18 136 0" fill="none" stroke="#fff" stroke-width="6" opacity=".7" stroke-linecap="round"/>""",

    "LED Desk Lamp": """
<path d="M160 60 L214 110 L90 38 Z" fill="#fff6c2" opacity=".55"/>
<ellipse cx="108" cy="196" rx="54" ry="9" fill="#000" opacity=".14"/>
<rect x="72" y="182" width="72" height="12" rx="6" fill="#2b3340"/>
<path d="M108 182 L134 112 L184 74" fill="none" stroke="#3b4556" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="134" cy="112" r="7" fill="#586173"/>
<path d="M172 64 l44 22 l-12 22 l-44 -22 z" fill="#2f6bff"/>
<ellipse cx="205" cy="100" rx="14" ry="6" transform="rotate(27 205 100)" fill="#fff3a6"/>""",

    "Cotton Bedsheet Set": _shadow(160, 196, 110) + """
<rect x="58" y="136" width="204" height="52" rx="10" fill="#e8eefc"/>
<rect x="58" y="136" width="204" height="18" rx="9" fill="#5b86f0"/>
<rect x="50" y="88" width="14" height="100" rx="5" fill="#8b5e3c"/><rect x="256" y="112" width="14" height="76" rx="5" fill="#8b5e3c"/>
<rect x="76" y="108" width="68" height="34" rx="14" fill="#fff"/><rect x="152" y="108" width="68" height="34" rx="14" fill="#fff"/>
<path d="M76 168 h184 M76 178 h184" stroke="#c4d2f7" stroke-width="3"/>""",

    "Electric Kettle 1.5L": _shadow(160, 196, 70) + """
<path d="M112 188 L122 96 H206 L216 188 Z" fill="#e9edf3"/>
<path d="M122 96 q42 -50 84 0 z" fill="#c9d1dc"/>
<rect x="152" y="60" width="16" height="14" rx="5" fill="#2b3340"/>
<path d="M122 112 L92 84 L84 90 L116 130 Z" fill="#e9edf3"/>
<path d="M216 112 q38 4 30 44 q-4 16 -26 18" fill="none" stroke="#2b3340" stroke-width="9" stroke-linecap="round"/>
<rect x="132" y="130" width="12" height="46" rx="6" fill="#4aa8ff" opacity=".7"/>
<rect x="104" y="184" width="120" height="12" rx="6" fill="#2b3340"/>""",

    "Chef Knife Set": _shadow(160, 198, 70) + """
<rect x="106" y="116" width="108" height="78" rx="8" fill="#9a6a43"/>
<rect x="106" y="116" width="108" height="14" rx="6" fill="#b98558"/>
<g fill="#2b3340"><rect x="122" y="56" width="14" height="62" rx="6"/><rect x="153" y="46" width="14" height="72" rx="6"/><rect x="184" y="62" width="14" height="56" rx="6"/></g>
<g fill="#cfd6e0"><rect x="124" y="108" width="10" height="12"/><rect x="155" y="108" width="10" height="12"/><rect x="186" y="108" width="10" height="12"/></g>""",

    "Stackable Storage Bins": _shadow(160, 200, 90) + """
<rect x="86" y="62" width="148" height="40" rx="8" fill="#5b86f0"/>
<rect x="76" y="106" width="168" height="40" rx="8" fill="#7ea0f6"/>
<rect x="66" y="150" width="188" height="42" rx="8" fill="#a9c0fa"/>
<g fill="#fff" opacity=".75"><rect x="136" y="76" width="48" height="9" rx="4"/><rect x="136" y="120" width="48" height="9" rx="4"/><rect x="136" y="165" width="48" height="9" rx="4"/></g>""",

    "Aroma Diffuser": _shadow(160, 198, 50) + """
<path d="M126 192 q-12 -64 8 -100 h52 q20 36 8 100 z" fill="#f1e6d6"/>
<path d="M134 92 h52 v14 h-52 z" fill="#8b5e3c"/>
<ellipse cx="160" cy="92" rx="26" ry="6" fill="#6b4529"/>
<path d="M150 80 q-16 -16 0 -30 q14 -14 0 -28 M172 80 q16 -18 0 -34 q-12 -12 2 -26" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".85"/>
<circle cx="160" cy="140" r="10" fill="#f0b86e" opacity=".8"/>""",

    "Mixer Grinder 750W": _shadow(160, 198, 70) + """
<rect x="102" y="140" width="116" height="52" rx="12" fill="#2b3340"/>
<circle cx="130" cy="166" r="9" fill="#aab4c3"/><circle cx="160" cy="166" r="9" fill="#aab4c3"/><circle cx="190" cy="166" r="9" fill="#aab4c3"/>
<path d="M120 140 L128 66 H192 L200 140 Z" fill="#d8e6f7" opacity=".9"/>
<path d="M120 140 L124 112 H196 L200 140 Z" fill="#e8943a" opacity=".85"/>
<rect x="122" y="52" width="76" height="14" rx="6" fill="#2b3340"/>
<path d="M200 80 q28 4 24 34" fill="none" stroke="#2b3340" stroke-width="8" stroke-linecap="round"/>""",

    "Robot Vacuum Cleaner": """
<ellipse cx="160" cy="176" rx="96" ry="14" fill="#000" opacity=".14"/>
<ellipse cx="160" cy="130" rx="96" ry="52" fill="#d9dfe8"/>
<ellipse cx="160" cy="118" rx="96" ry="52" fill="#2b3340"/>
<ellipse cx="160" cy="116" rx="82" ry="42" fill="#3a4354"/>
<circle cx="160" cy="112" r="20" fill="#1c212b"/><circle cx="160" cy="112" r="8" fill="#46c7ff"/>
<rect x="104" y="96" width="30" height="6" rx="3" fill="#8892a3" transform="rotate(-18 104 96)"/>
<circle cx="236" cy="124" r="5" fill="#46f0a0"/>
<path d="M236 150 l14 10 M236 150 l-6 14" stroke="#e8943a" stroke-width="4" stroke-linecap="round"/>""",
}
