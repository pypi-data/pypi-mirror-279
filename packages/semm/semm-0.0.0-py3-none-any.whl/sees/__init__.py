import os
import sys
try:
    import orjson as json
except ImportError:
    import json

import yaml
import numpy as np
Array = np.ndarray
FLOAT = np.float32

from .config import Config, apply_config
from .frame import SkeletalRenderer


Frame, Patch, Plane, Solid = range(4)

# Data shaping / Misc.
#----------------------------------------------------

# The following functions are used for reshaping data
# and carrying out other miscellaneous operations.

class RenderError(Exception): pass


def read_displacements(res_file):

    if not isinstance(res_file, str):
        return yaml.load(res_file, Loader=yaml.Loader)

    from urllib.parse import urlparse
    res_path = urlparse(res_file)
    if "json" in res_path[2]:
        with open(res_path[2], "r") as f:
            res = json.loads(f.read())
    else:
        with open(res_path[2], "r") as f:
            res = yaml.load(f, Loader=yaml.Loader)
    if res_path[4]: # query parameters passed
        res = res[int(res_path[4].split("=")[-1])]

    return res


def read_model(filename:str, shift=None)->dict:

    if isinstance(filename, str) and filename.endswith(".tcl"):
        import opensees.tcl
        with open(filename, "r") as f:
            interp = opensees.tcl.exec(f.read(), silent=True, analysis=False)
        return interp.serialize()

    try:
        with open(filename,"r") as f:
            sam = json.loads(f.read())

    except TypeError:
        sam = json.loads(filename.read())

    return sam


def render(sam_file, res_file=None, noshow=False, ndf=6, **opts):
    # Configuration is determined by successively layering
    # from sources with the following priorities:
    #      defaults < file configs < kwds 


    config = Config()

    if sam_file is None:
        raise RenderError("ERROR -- expected required argument <sam-file>")

    # Read and clean model
    if hasattr(sam_file, "asdict"):
        model = sam_file.asdict()
    elif not isinstance(sam_file, dict):
        model = read_model(sam_file)
    elif isinstance(sam_file, tuple):
        pass
    else:
        model = sam_file

    if "RendererConfiguration" in model:
        apply_config(model["RendererConfiguration"], config)

    apply_config(opts, config)



    renderer = SkeletalRenderer(model, ndf=ndf, **config)


    #
    # Read and clean displacements 
    # TODO: 
    # - remove `cases` var, 
    # - change add_displacements from being a generator
    # rename `name` parameter
    if res_file is not None:
        cases = renderer.add_displacements(res_file, scale=config["scale"],
                                           name=config["mode_num"])
        list(cases)

    elif config["displ"] is not None:
        cases = [renderer.add_point_displacements(config["displ"], scale=config["scale"])]

    if "Displacements" in model:
        cases.extend(renderer.add_displacements(model["Displacements"],scale=config["scale"],
                                                name=config["mode_num"]))


    # write plot to file if file name provided
    if config["write_file"]:
        renderer.draw()
        renderer.write(config["write_file"])

    else:
        renderer.draw()
        if not noshow:
            renderer.canvas.show()
        # renderer.repl()

    return renderer

