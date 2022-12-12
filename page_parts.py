import re


def anything_but(s):
    """
    Constructs a regular expression that matches anything except for the given substring.
    Assumes s does not contain any special regex characters.
    """
    parts = []
    for i in range(len(s)):
        sofar = s[:i]
        bad = s[i]
        parts.append(f"{sofar}[^{bad}]")
    end = f".{{,{len(s)-1}}}" if len(s) > 1 else ""
    return f"(?:(?:{'|'.join(parts)})*{end})"


def tag_regex(tag, exact_start=False, exact_end=False):
    """
    Constructs a regular expression that matches the contents of html elements of the given tag.
    exact_start/exact_end determine whether the start/end should be anchored.
    """
    return f"(?s){'^'*exact_start}<{tag}(?: [^>]*)?>({anything_but('</'+tag+'>')})</{tag}>{'$'*exact_end}"


class PageParts:
    def __init__(self, page: str, parts=None):
        if parts is None:
            parts = [(page, 0, len(page))]

        self.page = page
        self.parts = set(parts)

    def __add__(self, other):
        if not isinstance(other, PageParts):
            return NotImplemented

        assert self.page == other.page
        return PageParts(self.page, self.parts | other.parts)

    def __contains__(self, other):
        if not isinstance(other, PageParts):
            return NotImplemented

        assert self.page == other.page

        for _op, ost, oend in other.parts_with_offsets():
            for _sp, sst, send in self.parts_with_offsets():
                if sst <= ost and oend <= send:
                    break
            else:
                return False
        return True

    def __iter__(self):
        for p, _, _ in self.parts_with_offsets():
            yield p

    def parts_with_offsets(self):
        return sorted(list(self.parts), key=lambda p: p[1])

    def subparts(self):
        for p in self.parts_with_offsets():
            yield PageParts(self.page, {p})

    def last(self):
        return self.parts_with_offsets()[-1][0]

    def last_part(self):
        return PageParts(self.page, [self.parts_with_offsets()[-1]])

    def __len__(self):
        return len(self.parts)

    def map(self, f):
        parts = {(f(p), i, j) for (p, i, j) in self.parts}
        return PageParts(self.page, parts)

    def filter(self, f):
        parts = {(p, i, j) for (p, i, j) in self.parts if f(p)}
        return PageParts(self.page, parts)

    def search(self, pat):
        parts = set()

        pat = re.compile(pat)

        for part, st, _end in self.parts:
            for m in re.finditer(pat, part):
                for i, gr in enumerate(m.groups()):
                    parts.add((gr, st+m.start(i), st+m.end(i)))

        return PageParts(self.page, parts)

    def tags(self, tag, exact_start=False, exact_end=False, strip=True):
        pat = tag_regex(tag, exact_start, exact_end)
        res = self.search(pat)
        if strip:
            res = res.map(lambda p: p.strip())
        return res

    def remove_tag_content(self, tag, exact_start=False, exact_end=False):
        pat = tag_regex(tag, exact_start, exact_end)
        pat = re.compile(pat)
        return self.map(lambda p: re.sub(pat, "", p))

    def remove_tag(self, tag):
        pat = re.compile(f"</?{tag}>")
        return self.map(lambda p: re.sub(pat, "", p))

    def html_entities(self):
        return self.map(lambda p: p.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&"))

    def for_part(self, part):
        def f(p):
            find = p.find("--- Part Two ---")
            if find > -1:
                if str(part) == "1":
                    p = p[:find]
                else:
                    p = p[find:]
            return p

        return self.map(f)

    def possible_examples(self):
        return self.tags("pre").tags("code", True, True, False).remove_tag("em").html_entities()

    def possible_outputs(self, part=None, no_li=False):
        ps = self
        if part:
            ps = self.for_part(part)
        ps = ps.remove_tag_content("pre")
        if no_li:
            ps = ps.remove_tag_content("li")

        return ps.tags("code").tags("em", exact_end=True) + ps.tags("em").tags("code", exact_end=True)

    def possible_inline_examples(self, part):
        uls = self.for_part(part).tags("ul")
        if not uls:
            return
        outs = self.possible_outputs(part)
        if outs and outs.last_part() in uls:
            for li in uls.tags("li").subparts():
                codes = li.tags("code")
                if len(codes) >= 2:
                    codes = codes.filter(lambda p: ">" not in p and "<" not in p).html_entities()
                    o = li.possible_outputs().filter(lambda p: ">" not in p and "<" not in p).html_entities()
                    if o:
                        inp, out = list(codes)[0], o.last()
                        if len(inp) >= 5:
                            yield inp, out
