import re

class EzJS:
    def __init__(self):
        self.pattern = re.compile(r'\$(\w+)\[([^\]]+)\]', re.DOTALL)

    def ezjs_to_js(self, text):
        def replace_tag(match):
            tag = match.group(1)
            content = match.group(2).strip()
            return f'{tag}({content});'
        
        return self.pattern.sub(replace_tag, text)

    def convert(self, code):
        return self.ezjs_to_js(code)
