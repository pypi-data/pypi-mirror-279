import os
from functools import reduce
import abcli
from abcli import file
from abcli.plugins import markdown
from kamangir import NAME, VERSION
from kamangir.content import content
from kamangir.logger import logger


def update(filename: str = ""):
    if not filename:
        filename = os.path.join(file.path(__file__), "../README.md")

    logger.info(f"{NAME}.update: {filename}")

    success, home_md = file.load_text(
        os.path.join(file.path(__file__), "./assets/home.md"),
    )
    if not success:
        return success

    items = [
        "[![image]({})]({}) {}".format(
            item["image"],
            f"https://github.com/kamangir/{name}",
            item["description"],
        )
        for name, item in content["items"].items()
        if name != "template"
    ]
    logger.info(
        "{} item(s) loaded: {}".format(
            len(content["items"]),
            ", ".join(list(content["items"].keys())),
        )
    )

    table = markdown.generate_table(items, content["cols"])

    home_md = reduce(
        lambda x, y: x + y,
        [
            (
                table
                if "--table--" in line
                else (
                    [
                        "---",
                        "built by [`{}`]({}), based on [`{}-{}`]({}).".format(
                            abcli.fullname(),
                            "https://github.com/kamangir/awesome-bash-cli",
                            NAME,
                            VERSION,
                            "https://github.com/kamangir/kamangir",
                        ),
                    ]
                    if "--signature--" in line
                    else [line]
                )
            )
            for line in home_md
        ],
        [],
    )

    return file.save_text(filename, home_md)
