import asyncio
import datetime
import os
import platform
import threading
from typing import TypedDict

from flask import Flask, render_template

from dis_python_healthcheck.models import Version
from dis_python_healthcheck import HealthCheck, ExternalAPIHealthCheck, Version


class PageConfigDict(TypedDict):
    title: str
    header: dict
    description: str
    absoluteUrl: str
    meta: dict
    footer: dict

class PanelLinkDict(TypedDict):
    text: str
    url: str
    ariaLabel: str

class PanelDict(TypedDict):
    panelText: str
    panelType: str
    panelLink: PanelLinkDict

class DescriptionListDict(TypedDict):
    termCol: str
    descriptionCol: str
    itemsList: list[ItemDict]

class ItemDict(TypedDict):
    term: str
    descriptions: list[DescriptionDict]

class DescriptionDict(TypedDict):
    description: str

class OnsHeroDict(TypedDict):
    variants: str
    detailsColumns: str
    officialStatisticsBadge: bool
    officialStatisticsBadgeUrl: str
    informationPanel: PanelDict
    topic: str
    title: str
    text: str
    descriptionList: DescriptionListDict


def build_hero_banner() -> OnsHeroDict:
    return {
        "variants": "grey",
        "detailsColumns": "12",
        "officialStatisticsBadge": "true",
        "officialStatisticsBadgeUrl": "https://uksa.statisticsauthority.gov.uk/about-the-authority/uk-statistical-system/types-of-official-statistics/",
        "informationPanel":{
            "panelText": "Latest release",
            "panelType": "ons-green",
            "panelLink": {
                "text": "View previous releases",
                "url": "#0",
                "ariaLabel": "View previous release of Retail sales rise amid summer discounts and sporting events"
            }
        },
        "topic": "Dataset",
        "title": "Dataset title goes here",
        "text":  "Dataset description goes here",
        "censusLogo": "false",
        "descriptionList": {
            "termCol": "5",
            "descriptionCol": "7",
            "itemsList": [
                {
                    "term": "Released:",
                    "descriptions": [
                        {
                            "description": "16 August 2024"
                        }
                    ]
                },
                {
                    "term": "Last Updated:",
                    "descriptions": [
                        {
                            "description": "20 September 2024"
                        }
                    ]
                },
                {
                    "term": "Version:",
                    "descriptions": [
                        {
                            "description": "1"
                        }
                    ]
                }
            ]
        }
    }

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
    app.config.from_pyfile(os.path.join(app.root_path, "../config.py"))
    build_time = datetime.datetime.fromtimestamp(
        int(os.environ["BUILD_TIME"]),
        tz=datetime.timezone.utc,
    )

    build_info = Version(language="python",language_version=platform.python_version(),version=os.environ["VERSION"],build_time=build_time.isoformat(),
                    git_commit=os.environ["GIT_COMMIT"]
                )

    registry = HealthCheck(build_info)
    api_check = ExternalAPIHealthCheck(
        app.config['DATASET_API_URL'] + "/health",
        "Dataset-API"
    )
    registry.register(
        "Dataset-API",
        app.config['DATASET_API_URL'] + "/health",
        api_check.check,
        timeout=5.0,
        critical=False
    )

    def start_registry() -> None:
        asyncio.run(registry.start())

    t = threading.Thread(target=start_registry, daemon=True)
    t.start()

    # a simple page that says hello
    @app.route("/hello")
    def hello() -> str:
        return render_template("hello.html", pageconfig=build_page_config(), herobanner=build_hero_banner())


    @app.route("/health")
    async def health() -> str:
        result = await registry.run_all_checks()
        status_code = 200 if result['status'] == 'OK' else 503
        return result, status_code
    
    return app
