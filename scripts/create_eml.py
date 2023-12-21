import sys
sys.path.append(".")
from email.message import Message
import argparse
from pylib.ioutils import base64encode_urlsafe
from jinja2 import Environment, select_autoescape, FileSystemLoader, Template, StrictUndefined
import os
import html2eml

class EmlTemplate:

    def __init__(self):
        self.template: Template = None

    def load_html_template(self, template_name):  # Load Html
        search_path = os.path.dirname(template_name)
        template_name = os.path.basename(template_name)
        env = Environment(
            loader=FileSystemLoader(search_path),
            autoescape=select_autoescape(['html', 'xml']),
            undefined=StrictUndefined
        )
        self.template = env.get_template(template_name)
        return self

    def render(self, *args, **kwargs):
        self.html = self.template.render(*args, **kwargs)
        return self

    def set_headers(self, from_addr, to_addr, subject):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        return self

    def build(self) -> Message:
        msg = html2eml.from_html(self.html, subject=self.subject,
                                 to=self.to_addr, from_=self.from_addr)
        return msg


parser = argparse.ArgumentParser(description='Generate EML file with HTML templates.')
parser.add_argument('--from-addr', help="Define the address from which the email is sent.")
parser.add_argument('--to-list', help="A file define a list of email addresses to which emails are sent.")
parser.add_argument('--subject', help="Subject of the email.")
parser.add_argument('--tmp', help="Email template file in html format.")
parser.add_argument('--domain', help="Domain of the email server.")
parser.add_argument('-o', '--out', help="Output directory of the eml files.")
args = parser.parse_args()

if __name__ == '__main__':
    from_addr = args.from_addr
    subject = args.subject
    domain = args.domain
    templatefile = args.tmp
    out = args.out
    to_list_file = args.to_list
    to_list = []
    with open(to_list_file, 'r') as f:
        to_list = [line.strip() for line in f if line.strip()]
        to_list = set(to_list)
    for i, to_addr in enumerate(to_list):
        b64 = base64encode_urlsafe(to_addr)
        cancel = f"{domain}/newsletter/unsub?em={b64}"
        print(f"[{i + 1}/{len(to_list)}]: {to_addr} <{b64}>")
        t = EmlTemplate()\
            .load_html_template(templatefile)\
            .render(cancel=cancel)\
            .set_headers(from_addr=from_addr,
                         to_addr=to_addr, subject=subject).build()

        with open(os.path.join(out, f"{to_addr}.eml"), 'w', encoding="utf-8") as f:
            f.write(t.as_string())

