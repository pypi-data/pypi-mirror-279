"""
This file generates and prints the contents of an rst sphinx file containing the list
of external likelihoods.
"""
from cobaya_cosmo.external import external_list


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
