cmb = {
    # Planck #############################################################################
    "planck_PR4_lollipop.lowlE": {
        "class": "planck_2020_lollipop.lowlE",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/lollipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_lollipop",
            "min_version": "4.1.1",
        },
    },
    "planck_PR4_lollipop.lowlB": {
        "class": "planck_2020_lollipop.lowlB",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/lollipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_lollipop",
            "min_version": "4.1.1",
        },
    },
    "planck_PR4_lollipop.lowlEB": {
        "class": "planck_2020_lollipop.lowlEB",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/lollipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_lollipop",
            "min_version": "4.1.1",
        },
    },
    "planck_PR4_hillipop.TT": {
        "class": "planck_2020_hillipop.TT",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/hillipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_hillipop",
            "min_version": "4.2.2",
        },
    },
    "planck_PR4_hillipop.TE": {
        "class": "planck_2020_hillipop.TE",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/hillipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_hillipop",
            "min_version": "4.2.2",
        },
    },
    "planck_PR4_hillipop.EE": {
        "class": "planck_2020_hillipop.EE",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/hillipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_hillipop",
            "min_version": "4.2.2",
        },
    },
    "planck_PR4_hillipop.TTTEEE": {
        "class": "planck_2020_hillipop.TTTEEE",
        "desc": "sth...",
        "url": "https://github.com/planck-npipe/hillipop",
        "biburl": "http...",
        "package_install": {
            "pip": "planck_2020_hillipop",
            "min_version": "4.2.2",
        },
    },
    "planck_PR4_lensing": {
        "class": "planckpr4lensing",
        "desc": "Planck PR4 (NPIPE) lensing likelihoods, by J. Carron, M. Mirmelstein and A. Lewis, together with the Planck PR4 ISW-lensing likelihoods by J. Carron, G. Fabbian and A. Lewis",
        "url": "https://github.com/carronj/planck_PR4_lensing",
        "biburl": ["https://arxiv.org/abs/2007.04997", "https://arxiv.org/abs/2005.05290"],
        "package_install": {
            "github_repository": "carronj/planck_PR4_lensing",
            "min_version": "1.0.2",
        },
    },
    "planck_2018_highl_plik_mflike": {
        "class": "plikmflike.PlikMFLike",
        "desc": "",


#        Reimplementation

#        Planck PR4 (NPIPE) lensing likelihoods, by J. Carron, M. Mirmelstein and A. Lewis, together with the Planck PR4 ISW-lensing likelihoods by J. Carron, G. Fabbian and A. Lewis


#        ",
        "url": "https://github.com/simonsobs/LAT_MFLike/tree/mflike-plik",
        "biburl": ["...???????"],
        "package_install": {
            "pip": "git+https://github.com/simonsobs/LAT_MFLike@mflike-plik",
#            "github_repository": "simonsobs/LAT_MFLike",
#            "release_name": "mflike-plik",
#            "min_version": "1.0.2",
        },
    },
    
    # ACT ################################################################################
    "act_dr4_lite": {
        "class": "pyactlike.ACTPol_lite_DR4",
        "desc": "Atacama Cosmology Telescope DR4 CMB power spectrum likelihood, already marginalized over SZ and foreground emission; based on the WMAP and ACT team's likelihood software.",
        "url": "https://github.com/ACTCollaboration/pyactlike",
        "biburl": ["https://arxiv.org/abs/2007.07288", "https://arxiv.org/abs/2007.07289"],
        "package_install": {
            "github_repository": "ACTCollaboration/pyactlike",  # BRANCH cobaya_updates???
        },
    },
    "act_dr4_lite_for_planck_combination": {
        "class": "pyactlike.ACTPol_lite_DR4_for_combining_with_planck",
        "desc": "Atacama Cosmology Telescope DR4 CMB power spectrum likelihood, already marginalized over SZ and foreground emission, with a multipole cut to avoid correlations with Plank; based on the WMAP and ACT team's likelihood software.",
        "url": "https://github.com/ACTCollaboration/pyactlike",
        "biburl": ["https://arxiv.org/abs/2007.07288", "https://arxiv.org/abs/2007.07289"],
        "package_install": {
            "github_repository": "ACTCollaboration/pyactlike", # BRANCH cobaya_updates???
        },
    },
    "act_dr6_lenslike": {
        "class": "act_dr6_lenslike.ACTDR6LensLike",
        "desc": "...",
        "url": "https://github.com/ACTCollaboration/act_dr6_lenslike",
        "biburl": ["https://arxiv.org/abs/2304.05203", "https://arxiv.org/abs/2304.05202"],
        "package_install": {
            "pip": "act_dr6_lenslike",
            "min_version": "1.2.0",
        },
    },
    # SPT ################################################################################
    "sptpol_2017.TEEE": {
        "class": "sptpol_2017.TEEE",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/1707.09353",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt3g_2020.TEEE": {
        "class": "spt3g_2020.TEEE",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2101.01684",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt_hiell_2020.TT": {
        "class": "spt_hiell_2020.TT",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2002.06197",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt3g_2022.TT": {
        "class": "spt3g_2022.TT",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2212.05642",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt3g_2022.TE": {
        "class": "spt3g_2022.TE",
        "desc": "",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2212.05642",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt3g_2022.EE": {
        "class": "spt3g_2022.EE",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2212.05642",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    "spt3g_2022.TTTEEE": {
        "class": "spt3g_2022.TTTEEE",
        "desc": "...",
        "url": "https://github.com/xgarrido/spt_likelihoods",
        "biburl": "https://arxiv.org/abs/2212.05642",
        "package_install": {
            "github_repository": "xgarrido/spt_likelihoods",
        },
    },
    # WMAP ###############################################################################
    "wmap_v5": {
        "class": "wmaplike.WMAPLike",
        "desc": "WMAP likelihood implementation by H. Jense of the WMAP v5 likelihood, retaining only data in temperature and high-l polarization.",
        "url": "https://github.com/HTJense/pyWMAP",
        "biburl": "https://arxiv.org/pdf/1212.5225",
        "package_install": {
            "github_repository": "HTJense/pyWMAP",
            "min_version": "0.1.1",
        },
    },
    # MOCK/FUTURE ########################################################################
    # SUSPENDIDA POR AHORA, HASTA QUE CONTESTEN AL ISSUE
    "mock_hdlike": {
        "class": "hdlike.hdlike.HDLike",
        "desc": "Mock CMB-HD likelihood including lensed and delensed TT/TE/EE/BB CMB + lensing spectra from multipoles 30 to 20,000.",
        "url": "https://github.com/CMB-HD/hdlike",
        "biburl": "https://arxiv.org/abs/2309.03021",
        "package_install": {
            "github_repository": "CMB-HD/hdlike",
        },
    },
    "mock_cmb_SO": {
        "class": "cobaya_mock_cmb.MockSO",
        "desc": "Mock Simons Observatory likelihood following Sailer, Schaan and Ferraro 2020, based on MontePython's 'Likelihood_mock_cmb' (config by J. Muñoz).",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
   "mock_cmb_SO.baseline": {
        "class": "cobaya_mock_cmb.MockSOBaseline",
        "desc": "Mock Simons Observatory likelihood with TT, EE 'deproj0' noise curves (baseline sensitivity), based on MontePython's 'Likelihood_mock_cmb'.",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
   "mock_cmb_SO.goal": {
        "class": "cobaya_mock_cmb.MockSOGoal",
        "desc": "Mock Simons Observatory likelihood with TT, EE 'deproj0' noise curves (goal sensitivity), based on MontePython's 'Likelihood_mock_cmb'.",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
   "mock_cmb_CMBS4": {
        "class": "cobaya_mock_cmb.MockCMBS4",
        "desc": "Mock CMB-S4 likelihood following the science book, based on MontePython's 'Likelihood_mock_cmb' (config by J. Muñoz).",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
   "mock_cmb_CMBS4.sens0": {
        "class": "cobaya_mock_cmb.MockCMBS4sens0",
        "desc": "Mock CMB-S4 likelihood with TT, EE 'deproj0' noise curves, based on MontePython's 'Likelihood_mock_cmb'.",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
   "mock_cmb_Planck": {
        "class": "cobaya_mock_cmb.MockCMBS4sens0",
        "desc": "Mock Planck likelihood following Munoz et al 2016 with f_sky=0.2 (fraction independent of SO and CMB-S4), based on MontePython's 'Likelihood_mock_cmb'.",
        "url": "https://github.com/misharash/cobaya_mock_cmb",
        "biburl": "https://arxiv.org/abs/2108.02747",
        "package_install": {
            "github_repository": "misharash/cobaya_mock_cmb",
        },
    },
}



# MISSING:
# - https://github.com/nataliehogg/tdcosmo_ext
# - the 2 examples in the bottom
