# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>

import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_BASE_DIR = os.path.join(os.getcwd(), "aac_init_output_working_dir")

DEFAULT_USER_OPTIONS = [
    "Wipe and boot APIC/switch to particular version(APIC + Switch)",
    "APIC initial setup(Single Pod)",
    "Init ACI Fabric via NaC(Network as Code)"
]


DEFAULT_DATA_PATH = "00-global_policy.yml"
DATA_PATH = "nac_data"

TEMPLATE_DIR = [
    [os.path.join(BASE_DIR, "templates", "01-fabric_bootstrap", "apic"),
    os.path.join(BASE_DIR, "templates", "01-fabric_bootstrap", "aci_switch")],
    os.path.join(BASE_DIR, "templates", "02-apic_setup"),
    os.path.join(BASE_DIR, "templates", "03-nac_tasks"),
]

OUTPUT_DIR = [
    os.path.join(OUTPUT_BASE_DIR, "01-fabric_bootstrap"),
    os.path.join(OUTPUT_BASE_DIR, "02-apic_setup"),
    os.path.join(OUTPUT_BASE_DIR, "03-nac_tasks"),
]

os.environ["aac_init_option_1"] = OUTPUT_DIR[0]
os.environ["aac_init_option_2"] = OUTPUT_DIR[1]


STEP_1_YAML_LIST = []
STEP_2_YAML_LIST = []

YAML_NAME = [
    ['playbook_apic_bootstrap.yaml', 'playbook_aci_switch_bootstrap.yaml'],
    'playbook_apic_setup.yaml'
]

ANSIBLE_STEP = [
    'apic_bootstrap',
    'aci_switch_bootstrap',
    'apic_setup',
    'aac_validate',
    'aac_deploy',
    'aac_test'
]
