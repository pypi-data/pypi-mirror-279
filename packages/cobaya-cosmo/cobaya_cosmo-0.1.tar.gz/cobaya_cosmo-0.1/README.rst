

External packages
-----------------

This Python packages also lists a number of likelihoods, theory codes and wrappers written by other researchers and hosted somewhere else. Listing them here allows for the Cobaya installer to install them when mentioned just by name. You can see the current list at [LINK]

If you want your package to be featured here, please send a pull request [LINK] and include the following information:

- The name of your likelihood in the Cobaya input file. Please follow, where applicable, the following structure: `[observable_in_lower_case].[survey]_[release]_[dataset_or_likelihood]`, e.g. `cmb.planck_2018_highell_plikHM`, `sn.....`, etc. If it's not clear how to adapt this to your case, let us know in the PR/ISSUE and we can find a compromise. If you already have code containing a different class name, tell it to us (we'll add a "class: [name]" to the dict and a pip reference).

- A 1-sentence description of it.

- A link to one or more papers that describe it (if more than one is requested to be cited, this is not the place; see [LINK])

- How can people install your likelihood. If you follow [SOME RULES], we will make it so it's automatically installed by `cobaya-installed` when requested by name. 

- The current version number of the code

Though in principle all reasonable requests are accepted immediately, some level of documentation, tests, etc may be requested.


FAQ
---

I have updated my likelihood/wrapper/... and want Cobaya to reflect that. How do I do that?

--> Open a PR and mention the new version.
