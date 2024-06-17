""" atlassible/src/aticli/main.py 

"""

import logging
import jsonloggeriso8601datetime as jlidt
jlidt.setConfig()
logger = logging.getLogger(__name__)

from dataclasses import dataclass
import json 
from typing import Annotated

import atlassible 
# import domible
from domible.builders import element_from_object
from domible.elements import Html, Body, BaseElement  
from domible.starterDocuments import basic_head_empty_body 
from domible.tools import open_in_browser, save_to_file 
import typer


app = typer.Typer()


@dataclass
class MainOptions:
    browser: bool
    output_html: str
    force: bool 
    html_dump: bool 
    json_dump: bool


@app.command()
def me(ctx: typer.Context):
    mo: MainOptions = ctx.obj
    logger.info(f"Me, Me, and, More Me!!   output_file is {mo.output_html}")
    me = atlassible.myself.get_me()
    if me:
        if mo.browser or mo.html_dump or mo.output_html:
            me_html: BaseElement = element_from_object(me)
            if mo.html_dump:
                print(me_html)
            if mo.browser or mo.output_html:
                title = "All About Me"
                html_doc: Html = basic_head_empty_body(title)
                body: Body = html_doc.get_body_element()
                body.add_content(me_html)
                if mo.browser:
                    open_in_browser(html_doc)
                if mo.output_html:
                    save_to_file(html_doc, mo.output_html, force=mo.force)
        if mo.json_dump:
            print(json.dumps(me, indent=4))
    else:
        logger.warning("Atlassian does not know about you.")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
         browser: Annotated[bool, typer.Option("-b", help="include if you want the results opened in a browser")] = False,
         output_html: Annotated[str, typer.Option("-o", help="name of file to write complete HTML document")] = None,
         force: Annotated[bool, typer.Option("-f", help="include if you want any existing files overwritten by output_file")] = False,
         json_dump: Annotated[bool, typer.Option("-j", help="include if you want objects printed to stdout as JSON")] = False,
         html_dump: Annotated[bool, typer.Option("-h", help="include if you want objects printed to stdout as HTML")] = False
         ) -> None:
    ctx.obj = MainOptions(browser, output_html, force, html_dump, json_dump)
    logger.info("that's it for main.")


## end of file
