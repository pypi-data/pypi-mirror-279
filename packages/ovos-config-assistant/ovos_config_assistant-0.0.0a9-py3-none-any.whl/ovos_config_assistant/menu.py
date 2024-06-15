import json
from os.path import dirname

from ovos_config import Configuration
from ovos_config.config import update_mycroft_config
from pywebio.input import actions, input_group, input, TEXT, NUMBER, textarea
from pywebio.output import popup, put_code, put_image, use_scope, put_text

from ovos_config_assistant.backend import backend_menu
from ovos_config_assistant.datasets import datasets_menu
from ovos_config_assistant.oauth import oauth_menu
from ovos_config_assistant.plugins import plugins_menu


def main_menu():
    with use_scope("logo", clear=True):
        from os.path import dirname
        img = open(f'{dirname(__file__)}/res/OCA.png', 'rb').read()
        put_image(img)

    opt = actions(label="What would you like to do?",
                  buttons=[{'label': 'Manage Datasets', 'value': "db"},
                           {'label': 'OAuth Applications', 'value': "oauth"},
                           {'label': 'Configure Backend', 'value': "backend"},
                           {'label': 'Configure Plugins', 'value': "plugins"},
                           {'label': 'Configure Secrets', 'value': "secrets"},
                           {'label': 'Configure Email', 'value': "smtp"}
                           ])
    if opt == "oauth":
        oauth_menu(back_handler=main_menu)
    elif opt == "db":
        datasets_menu(back_handler=main_menu)
    elif opt == "backend":
        backend_menu(back_handler=main_menu)
    elif opt == "plugins":
        plugins_menu(back_handler=main_menu)
    elif opt == "secrets":
        cfg = Configuration()
        api_cfg = cfg.get("microservices") or {}

        data = input_group('Secret Keys', [
            input("WolframAlpha key", value="TODO",
                  type=TEXT, name='wolfram'),
            input("OpenWeatherMap key", value="TODO",
                  type=TEXT, name='owm')
        ])
        api_cfg["wolfram_key"] = data["wolfram"]
        api_cfg["own_key"] = data["owm"]
        update_mycroft_config({"microservices": api_cfg}, bus=cfg.bus)
        popup("Secrets updated!")
    elif opt == "smtp":
        cfg = Configuration()
        api_cfg = cfg.get("microservices") or {}

        if "email" not in api_cfg:
            api_cfg["email"] = {}
        if "smtp" not in api_cfg["email"]:
            api_cfg["email"]["smtp"] = {}

        data = input_group('SMTP Configuration', [
            input("Username", value=api_cfg["email"]["smtp"].get("username", 'user'),
                  type=TEXT, name='username'),
            input("Password", value=api_cfg["email"]["smtp"].get("password", '***********'),
                  type=TEXT, name='password'),
            input("Host", value=api_cfg["email"]["smtp"].get("host", 'smtp.mailprovider.com'),
                  type=TEXT, name='host'),
            input("Port", value=api_cfg["email"]["smtp"].get("port", '465'),
                  type=NUMBER, name='port')
        ])

        api_cfg["email"]["smtp"]["username"] = data["username"]
        api_cfg["email"]["smtp"]["password"] = data["password"]
        api_cfg["email"]["smtp"]["host"] = data["host"]
        api_cfg["email"]["smtp"]["port"] = data["port"]
        with popup(f"SMTP configuration for: {data['host']}"):
            put_code(json.dumps(data, ensure_ascii=True, indent=2), "json")

        update_mycroft_config({"microservices": api_cfg}, bus=cfg.bus)


def prompt_admin_key():
    admin_key = textarea("insert your admin_key, this should have been set in your ovos configuration file",
                         placeholder="SuperSecretPassword1!",
                         required=True)
    if Configuration()["admin_key"] != admin_key:
        popup("INVALID ADMIN KEY!")
        prompt_admin_key()


def start():
    with use_scope("logo", clear=True):
        img = open(f'{dirname(__file__)}/res/OCA.png', 'rb').read()
        put_image(img)
    cfg = Configuration()
    # cfg["admin_key"] = "123"
    if not cfg.get("admin_key"):
        put_text("This OpenVoiceOS instance does not have the admin interface exposed")
        return
    prompt_admin_key()
    main_menu()
