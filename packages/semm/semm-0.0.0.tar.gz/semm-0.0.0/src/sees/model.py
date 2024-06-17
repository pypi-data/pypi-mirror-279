import numpy as np

class Model:
    def __iter__(self):
        return iter((self.nodes, self.cells))

    @property
    def nodes(self):
        pass

    @property
    def cells(self):
        pass

    def filt_cells(self, filt=None):
        pass

    def iter_cells(self, filt=None):
        pass



class PlaneModel:
    pass

class FrameModel:
#   nodes
#   elements
#   sections
#   prototypes


    def __getitem__(self, key):
        return self._data[key]

    def __init__(self, sam:dict, shift = None, rot=None):
        """
        Process OpenSees JSON output and return dict with the form:

            {<elem tag>: {"crd": [<coordinates>], ...}}
        """
        try:
            sam = sam["StructuralAnalysisModel"]
        except KeyError:
            pass

        ndm = 3
        R = np.eye(ndm) if rot is None else rot

        geom = sam.get("geometry", sam.get("assembly"))

        if shift is None:
            shift = np.zeros(ndm)
        else:
            shift = np.asarray(shift)

        try:
            #coord = np.array([R@n.pop("crd") for n in geom["nodes"]], dtype=float) + shift
            coord = np.array([R@n["crd"] for n in geom["nodes"]], dtype=float) + shift
        except:
            coord = np.array([R@[*n["crd"], 0.0] for n in geom["nodes"]], dtype=float) + shift

        nodes = {
                n["name"]: {**n, "crd": coord[i], "idx": i}
                    for i,n in enumerate(geom["nodes"])
        }

        ndm = len(next(iter(nodes.values()))["crd"])


        try:
            trsfm = {t["name"]: t for t in sam["properties"]["crdTransformations"]}
        except KeyError:
            trsfm = {}

        elems =  {
          e["name"]: dict(
            **e,
            crd=np.array([nodes[n]["crd"] for n in e["nodes"]], dtype=float),
            trsfm=trsfm[e["crdTransformation"]]
                if "crdTransformation" in e and e["crdTransformation"] in trsfm
                else dict(yvec=R@e["yvec"] if "yvec" in e else None)
          ) for e in geom["elements"]
        }

        try:
            sections = {s["name"]: s for s in sam["properties"]["sections"]}
        except:
            sections = {}

        output = dict(nodes=nodes,
                      assembly=elems,
                      coord=coord,
                      sam=sam,
                      sections=sections,
                      ndm=ndm)

        if "prototypes" in sam:
            output.update({"prototypes": sam["prototypes"]})

        self._data = output

