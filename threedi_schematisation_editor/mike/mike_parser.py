# Copyright (C) 2023 by Lutra Consulting
import os.path
import re
from collections import OrderedDict, defaultdict, namedtuple


class MikeComponent:
    NAME = None

    def __init__(self, parser, filepath=None):
        self.parser = parser
        self.filepath = filepath
        self.search_pattern = re.compile(rf"{self.NAME} = \|(?P<relative_path>[^|]+)\|", re.M) if self.NAME else None
        self.data = OrderedDict()

    def parse_component_data(self):
        pass

    @property
    def is_available(self):
        if self.filepath and os.path.exists(self.filepath):
            return True
        else:
            return False

    def discover_component_path(self, text_to_search):
        if self.search_pattern is None:
            return
        match = re.search(self.search_pattern, text_to_search)
        if not match:
            return
        match_dict = match.groupdict()
        relative_path = match_dict["relative_path"]
        absolute_path = os.path.abspath(os.path.join(self.parser.sim11_dir, relative_path))
        self.filepath = absolute_path


class NWKComponent(MikeComponent):
    NAME = "nwk"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = {}
        self.branches = {}

    def _parse_projection(self, nwk_txt):
        data_area_txt = self.parser.extract_sections(nwk_txt, "DATA_AREA")[0]
        projection_prefix = "projection = "
        projection_definition = data_area_txt.split(projection_prefix)[-1]
        self.parser.projection = projection_definition.strip("'")

    def _parse_points(self, nwk_txt):
        points_txt = self.parser.extract_sections(nwk_txt, "POINTS")[0]
        point_prefix = "point = "
        point_cls = namedtuple("Point", ["id", "x", "y", "user_defined", "chainage"])
        point_rows = [row.strip().replace(point_prefix, "") for row in points_txt.split("\n") if "=" in row]
        for point_row in point_rows:
            pid_str, x_str, y_str, user_defined_str, chainage_str = point_row.split(",")[:-1]
            pid, x, y, user_defined, chainage = (
                int(pid_str),
                float(x_str),
                float(y_str),
                bool(int(user_defined_str)),
                float(chainage_str),
            )
            point = point_cls(pid, x, y, user_defined, chainage)
            self.points[point.id] = point

    def _parse_branches(self, nwk_txt):
        branch_txt_list = self.parser.extract_sections(nwk_txt, "branch")
        branch_cls = namedtuple("branch", ["river_name", "topo_id", "points"])
        for branch_txt in branch_txt_list:
            branch_rows = [row.split("=")[-1].strip().replace("'", "") for row in branch_txt.split("\n") if "=" in row]
            definition_txt, connections_txt, points_txt = branch_rows
            topo_id, river_name, definition_leftovers = [i.strip() for i in definition_txt.split(",", 2)]
            point_ids = [int(pid_txt) for pid_txt in points_txt.split(",")]
            points = [self.points[pid] for pid in point_ids]
            branch = branch_cls(river_name, topo_id, points)
            self.branches[topo_id] = branch

    def parse_component_data(self):
        if not self.is_available:
            return
        with open(self.filepath) as nwk_file:
            nwk_txt = nwk_file.read()
            self._parse_projection(nwk_txt)
            self._parse_points(nwk_txt)
            self._parse_branches(nwk_txt)


class XSComponent(MikeComponent):
    NAME = "xs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rawdata_filepath = None
        self.cross_section_data = defaultdict(list)

    @property
    def is_available(self):
        if super().is_available:
            return self.rawdata_filepath and os.path.exists(self.rawdata_filepath)
        else:
            return False

    def _discover_rawdata_path(self):
        if self.filepath:
            rawdata_filepath = self.filepath.rsplit(".", 1)[0] + ".txt"
            if os.path.exists(rawdata_filepath):
                self.rawdata_filepath = rawdata_filepath

    @staticmethod
    def segmentize_xs_rawdata(single_xs_rawdata):
        rawdata_segments = OrderedDict()
        current_segment_identifier = "CHANNEL"
        rawdata_identifiers = [
            "COORDINATES",
            "FLOW DIRECTION",
            "PROTECT DATA",
            "DATUM",
            "CLOSED SECTION",
            "RADIUS TYPE",
            "DIVIDE X-Section",
            "SECTION ID",
            "INTERPOLATED",
            "ANGLE",
            "RESISTANCE NUMBERS",
            "PROFILE",
            "LEVEL PARAMS",
            "H-LEVELS",
        ]
        unprocessed_rawdata_text = single_xs_rawdata
        for segment_identifier in rawdata_identifiers:
            try:
                current_rawdata_segment, unprocessed_rawdata_text = unprocessed_rawdata_text.split(segment_identifier)
            except ValueError:
                continue
            rawdata_segments[current_segment_identifier] = current_rawdata_segment.strip()
            current_segment_identifier = segment_identifier
        return rawdata_segments

    def parse_component_data(self):
        if not self.is_available:
            return
        xs_cls = namedtuple("cross_section", ["river_name", "topo_id", "chainage", "profile"])
        with open(self.rawdata_filepath) as xs_file:
            for xs_txt_raw in xs_file.read().split("*******************************"):
                xs_txt = xs_txt_raw.strip()
                if not xs_txt:
                    continue
                rawdata_segments = self.segmentize_xs_rawdata(xs_txt)
                river_name, topo_id, chainage = [row.strip() for row in rawdata_segments["CHANNEL"].split("\n")]
                profile_lines = (row.strip() for row in rawdata_segments["PROFILE"].split("\n")[1:])
                profile = []
                for line in profile_lines:
                    line_values = [val.strip() for val in line.split()]
                    profile.append(line_values)
                xs = xs_cls(river_name, topo_id, chainage, profile)
                self.cross_section_data[topo_id].append(xs)

    def discover_component_path(self, text_to_search):
        super().discover_component_path(text_to_search)
        self._discover_rawdata_path()


class BNDComponent(MikeComponent):
    NAME = "bnd"


class RRComponent(MikeComponent):
    NAME = "rr"


class HDComponent(MikeComponent):
    NAME = "hd"


class ADComponent(MikeComponent):
    NAME = "ad"


class WQComponent(MikeComponent):
    NAME = "wq"


class STComponent(MikeComponent):
    NAME = "st"


class FFComponent(MikeComponent):
    NAME = "ff"


class RHDComponent(MikeComponent):
    NAME = "rhd"


class RRRComponent(MikeComponent):
    NAME = "rrr"


class DAComponent(MikeComponent):
    NAME = "da"


class ICEComponent(MikeComponent):
    NAME = "ice"


class MikeParser:
    COMPONENT_CLASSES = (
        NWKComponent,
        XSComponent,
        BNDComponent,
        RRComponent,
        HDComponent,
        ADComponent,
        WQComponent,
        STComponent,
        FFComponent,
        RHDComponent,
        RRRComponent,
        DAComponent,
        ICEComponent,
    )

    def __init__(self, sim11_filepath):
        self.sim11_filepath = sim11_filepath
        self.components = OrderedDict()
        self.projection = ""

    @staticmethod
    def extract_sections(text, split_token):
        section_pattern = re.compile(rf"\[{split_token}\].+?EndSect  // {split_token}", re.M | re.S)
        match_list = re.findall(section_pattern, text)
        return match_list

    @property
    def sim11_dir(self):
        return os.path.dirname(self.sim11_filepath)

    def detect_components(self):
        with open(self.sim11_filepath) as sim11_file:
            sim11_text = sim11_file.read()
            inputs_text = self.extract_sections(sim11_text, "Input")[0]
            for component_cls in self.COMPONENT_CLASSES:
                component = component_cls(self)
                component.discover_component_path(inputs_text)
                if component.is_available:
                    self.components[component_cls] = component
