### molab is a python package for setting up and configuring Morpheus training labs ###

# Original Imports
from .deploy import *
from .destroy import *
from .configure import *
from .courses import *

# v6.0 Imports
from .labs import newClass, existingClass, newLab, existingLab, awsEnv
from .tools import gen_instance_names, extract_json_content