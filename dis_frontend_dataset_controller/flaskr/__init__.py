import os
from typing import TypedDict

from flask import Flask, render_template


class PageConfigDict(TypedDict):
    title: str
    header: dict
    description: str
    absoluteUrl: str
    meta: dict
    footer: dict


def build_page_config() -> PageConfigDict:
    return {
        "title": "Frontend Dataset Controller",
        "header": {
            "mastheadLogoAltText": "Alt text for ONS logo",
            "mastheadLogoUrl": "/",
            "mastheadLogo": {},
            "titleLogo": "large",
        },
        "description": "Frontend dataset controller app",
        "absoluteUrl": "/",
        "meta": {"canonicalUrl": "/"},
        "footer": {
            "oglLink": {
                "pre": "All content is available under the",
                "link": "Open Government Licence v3.0",
                "url": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
                "post": ", except where otherwise stated",
            },
            "footerLogo": {
                "logos": {
                    "logo1": {"logoImage": '<img src="logo.svg" class="custom-logo" alt="logo">'},
                    "logo2": {
                        "logoUrl": "#0",
                        "logoImage": '<img src="a-logo.svg">',
                    },
                },
            },
        },
    }


def create_app() -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route("/hello")
    def hello() -> str:
        return render_template("hello.html", pageconfig=build_page_config())

    return app
