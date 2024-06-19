"""
This file generates and prints the contents of an rst sphinx file containing the list
of external likelihoods.
"""
from inspect import cleandoc

from cobaya_cosmo.external import external_list


def generate_full_text():
    main_text = cleandoc(
        """
        List of external likelihoods
        ============================

        Here is a non-extensive list of external likelihoods, i.e. likelihoods not
        integrated in the Cobaya cosmo package, and generally not authored by the main
        Cobaya developers. 

        All this likelihoods can be used just by mentioning them in an input file, and can
        be installed with ``cobaya-install [name]`` or ``cobaya-install [input.yaml]``
        (otherwise please submit an issue [LINK]).

        You can have your likelihood listed here by submitting a PR/ISSUE in the Cobaya
        cosmo package [LINK].

        List of external likelihoods grouped by observable
        --------------------------------------------------

        .. raw:: html"""
    )
    indent = 4 * " "
    main_text += "\n\n" + indent + f"\n{indent}".join(generate_external_list().split("\n"))
    return main_text


def generate_external_list():
    html_str = "<ul>"
    for observable, likelihoods in external_list.__dict__.items():
        if observable.startswith("_"):
            continue
        html_str += f"<li><details>\n<summary>{observable}</summary><ul>\n"
        for likename, likedata in likelihoods.items():
            html_str += f"\n<li><details>\n<summary><a href='{likedata['url']}'>"
            html_str += f"<b>{observable}.{likename}</b></a></summary>\n"
            html_str += f"{likedata['desc']} "
            if isinstance(likedata["biburl"], str):
                likedata["biburl"] = [likedata["biburl"]]
            html_str += ",".join(
                [
                    f"<a href='{url}'>[{i + 1}]</a>"
                    for i, url in enumerate(likedata["biburl"])
                ]
            )
            html_str += "\n</details></li>"
        html_str += "\n</ul></details></li>"
    html_str += "</ul>"
    return html_str
