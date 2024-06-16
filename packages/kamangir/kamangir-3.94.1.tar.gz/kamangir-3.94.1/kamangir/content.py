import abcli
import articraft
import blue_geo
import blue_stability
import hubblescope
import ferfereh
import gizai
import notebooks_and_scripts
import openai_commands
import roofAI
import vancouver_watching

content = {
    "cols": 3,
    "items": {
        "blue-geo": {
            "module": blue_geo,
        },
        "notebooks-and-scripts": {
            "module": notebooks_and_scripts,
        },
        "vancouver-watching": {
            "module": vancouver_watching,
        },
        "giza": {
            "module": gizai,
        },
        "roofAI": {
            "module": roofAI,
        },
        "openai-commands": {
            "module": openai_commands,
        },
        "hubble": {
            "module": hubblescope,
        },
        "blue-stability": {
            "module": blue_stability,
        },
        "aiart": {
            "module": articraft,
        },
        "awesome-bash-cli": {
            "module": abcli,
        },
        "ferfereh": {
            "module": ferfereh,
        },
        "Kanata": {
            "legacy": True,
            "image": "https://kamangir-public.s3.ca-central-1.amazonaws.com/Canadians_v11.gif",
            "description": "a multi-screen video feed that is comprised of a matrix of animated faces that slide to the right.",
        },
        "dec82": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/dec82-6.jpg",
            "description": "A wearable Raspberry Pi + Grove / Qwiic + Camera.",
        },
        "blue-rvr": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-rvr/raw/master/abcli/assets/marquee.jpeg",
            "description": "a bash cli for Sphero RVR SDK - runs deep learning vision models on a Raspberry Pi using Python and TensorFlow.",
        },
        "blue-bracket": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/marquee.jpg",
            "description": "a parametric 3d-printed bracket to build hardware for machine vision & ai on raspberry pi and jetson nano on the edge.",
        },
        "blue-sbc": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/blue3-1.jpg",
            "description": "python + bash bootstrap for edge computing on single board computers.",
        },
        "template": {
            "module": abcli,
        },
    },
}
