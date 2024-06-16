import re
from flask import Flask, render_template_string

class EzHTML:
    def __init__(self):
        self.pattern = re.compile(r'\$(\w+)\[([^\]]+)\]', re.DOTALL)

    def ezhtml_to_html(self, text):
        def replace_tag(match):
            tag = match.group(1)
            content = match.group(2).strip()
            # แปลง \n เป็น <br> ในกรณีของ <div>
            if tag == 'div':
                content = content.replace('\n', '<br>\n')
            return f'<{tag}>{content}</{tag}>'
        
        return self.pattern.sub(replace_tag, text)

    def run_flask(self, example_code):
        app = Flask(__name__)

        @app.route('/')
        def index():
            try:
                html_output = self.ezhtml_to_html(example_code)
                return render_template_string(html_output)
            except Exception as e:
                return f"Error: {e}", 500

        app.run(debug=True)
