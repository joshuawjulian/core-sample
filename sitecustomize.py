# Auto-imported by Python's `site` at interpreter startup whenever the repo root is on
# PYTHONPATH (CI render step and devcontainer set it). It makes matplotlib's built-in
# mathtext parser TOLERANT, so figure labels written in full LaTeX (\tfrac, \boldsymbol\mu,
# \sqrt n, \le, \mathcal N, ...) never crash a render. Prose math is unaffected (that's
# real LaTeX in the PDF); this only touches what matplotlib draws inside plots.
#
# Strategy per label: (1) try as-is; (2) retry with mathtext-safe normalizations;
# (3) last resort, strip commands so it renders as plain text. It never raises.
try:
    import re as _re
    from matplotlib import mathtext as _mt

    _SUBS = [
        (_re.compile(r'\\le(?![a-zA-Z])'), r'\\leq'),
        (_re.compile(r'\\ge(?![a-zA-Z])'), r'\\geq'),
        (_re.compile(r'\\tfrac'), r'\\frac'),
        (_re.compile(r'\\dfrac'), r'\\frac'),
        (_re.compile(r'\\operatorname'), r'\\mathrm'),
        # font commands need a braced argument in mathtext; brace unbraced ones
        (_re.compile(r'\\(boldsymbol|bm|pmb|mathbf|mathbfit|mathcal|mathbb|mathrm|mathsf|mathfrak|mathit)(\\[A-Za-z]+)'), r'\\\1{\2}'),
        (_re.compile(r'\\(boldsymbol|bm|pmb|mathbf|mathbfit|mathcal|mathbb|mathrm|mathsf|mathfrak|mathit)\s+([A-Za-z0-9])'), r'\\\1{\2}'),
        (_re.compile(r'\\sqrt\s*([A-Za-z0-9]+)'), r'\\sqrt{\1}'),
        (_re.compile(r'\\frac\s*([A-Za-z0-9])\s*([A-Za-z0-9])'), r'\\frac{\1}{\2}'),
        (_re.compile(r'\\frac\s*([A-Za-z0-9])(?=[\\{])'), r'\\frac{\1}'),
    ]

    def _norm(s):
        for p, r in _SUBS:
            s = p.sub(r, s)
        return s

    def _dumb(s):  # last resort: render as plain-ish text, never raise
        return _re.sub(r'\\[A-Za-z]+', ' ', s).replace('{', ' ').replace('}', ' ').replace('\\', ' ')

    _orig = _mt.MathTextParser.parse

    def _safe(self, s, *a, **k):
        for candidate in (s, _norm(s), _dumb(s), ' '):
            try:
                return _orig(self, candidate, *a, **k)
            except Exception:
                continue
        return _orig(self, ' ', *a, **k)

    _mt.MathTextParser.parse = _safe
except Exception:
    pass
