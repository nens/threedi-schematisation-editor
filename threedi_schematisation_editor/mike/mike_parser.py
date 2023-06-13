# Copyright (C) 2023 by Lutra Consulting
import os.path
import re
from collections import OrderedDict, defaultdict, namedtuple
from functools import cached_property
from operator import attrgetter

from threedi_schematisation_editor.mike.utils import interpolate_chainage_point


class MikeComponent:
    """MIKE11 component base class."""

    NAME = None

    def __init__(self, parser, filepath=None):
        self.parser = parser
        self.filepath = filepath
        self.search_pattern = re.compile(rf"{self.NAME} = \|(?P<relative_path>[^|]+)\|", re.M) if self.NAME else None
        self.data = OrderedDict()

    def parse_component_data(self):
        """Method for parsing component data."""
        pass

    @property
    def is_available(self):
        """Check if component file is available."""
        if self.filepath and os.path.exists(self.filepath):
            return True
        else:
            return False

    def discover_component_path(self, text_to_search):
        """Discover component data file paths."""
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
    """MIKE11 network component class."""

    NAME = "nwk"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = {}
        self.chainage_points = {}
        self.node_replacements = {}
        self.branches = {}
        self.extra_branch_points = defaultdict(set)
        self.branch_split_points = defaultdict(set)
        self.point_cls = namedtuple("point", ["id", "x", "y", "m"])
        self.branch_cls = namedtuple(
            "branch",
            [
                "name",
                "topo_id",
                "upstream_chainage",
                "downstream_chainage",
                "upstream_connection",
                "downstream_connection",
                "points",
                "is_link",
            ],
        )

    def _parse_projection(self, nwk_txt):
        """Parse projection information."""
        data_area_txt = self.parser.extract_sections(nwk_txt, "DATA_AREA")[0]
        projection_prefix = "projection = "
        projection_definition = data_area_txt.split(projection_prefix)[-1]
        self.parser.projection = projection_definition.strip("'")

    def _parse_points(self, nwk_txt):
        """Parse network points."""
        points_txt = self.parser.extract_sections(nwk_txt, "POINTS")[0]
        point_prefix = "point = "
        point_rows = [row.strip().replace(point_prefix, "") for row in points_txt.split("\n") if "=" in row]
        for point_row in point_rows:
            pid_str, x_str, y_str, user_defined_str, chainage_str = [i.strip() for i in point_row.split(",")][:-1]
            pid, x, y, m = (
                int(pid_str),
                float(x_str),
                float(y_str),
                float(chainage_str),
            )
            point = self.point_cls(pid, x, y, m)
            self.points[point.id] = point

    def _parse_branches(self, nwk_txt):
        """Parse branches data."""
        branch_txt_list = self.parser.extract_sections(nwk_txt, "branch")
        for branch_txt in branch_txt_list:
            branch_rows = [row.split("=")[-1].strip().replace("'", "") for row in branch_txt.split("\n") if "=" in row]
            definition_txt, connections_txt, points_txt = branch_rows[:3]
            name, topo_id, up_chainage_str, down_chainage_str, definition_leftovers = [
                i.strip().upper() for i in definition_txt.split(",", 4)
            ]
            up_link_name, up_link_chainage_str, down_link_name, down_link_chainage_str = [
                i.strip().upper() for i in connections_txt.split(",")
            ]
            up_chainage, down_chainage = float(up_chainage_str), float(down_chainage_str)
            up_link_chainage, down_link_chainage = float(up_link_chainage_str), float(down_link_chainage_str)
            upstream_connection = (up_link_name, up_link_chainage)
            downstream_connection = (down_link_name, down_link_chainage)
            points = []
            for pid_txt in points_txt.split(","):
                pid = int(pid_txt)
                point = self.points[pid]
                points.append(point)
                self.chainage_points[name, point.m] = pid
            branch = self.branch_cls(
                name,
                topo_id,
                up_chainage,
                down_chainage,
                upstream_connection,
                downstream_connection,
                tuple(points),
                False,
            )
            self.branches[name] = branch

    def generate_chainage_point(self, branch, chainage):
        """Create branch chainage point."""
        chainage_point_geom = interpolate_chainage_point(branch, chainage)
        new_point_id = max(self.points.keys()) + 1 if self.points else 1
        x, y, m = chainage_point_geom.GetX(), chainage_point_geom.GetY(), chainage
        new_point = self.point_cls(new_point_id, x, y, m)
        return new_point

    def _add_connections_as_branches(self):
        """Add branch connections as additional branches."""
        connection_branches = {}
        for branch in self.branches.values():
            up_link_name, up_link_chainage = branch.upstream_connection
            down_link_name, down_link_chainage = branch.downstream_connection
            if up_link_name:
                from_branch = self.branches[up_link_name]
                to_branch = branch
                to_point = to_branch.points[0]
                try:
                    from_pid = self.chainage_points[up_link_name, up_link_chainage]
                    from_point = self.points[from_pid]
                except KeyError:
                    from_point = self.generate_chainage_point(from_branch, up_link_chainage)
                    self.points[from_point.id] = from_point
                    self.chainage_points[up_link_name, up_link_chainage] = from_point.id
                    self.extra_branch_points[up_link_name].add(from_point)
                upstream_replacement_point = self.point_cls(-from_point.id, from_point.x, from_point.y, float("-inf"))
                self.points[upstream_replacement_point.id] = upstream_replacement_point
                self.node_replacements[to_point.id] = upstream_replacement_point.id
                if from_point != from_branch.points[-1]:
                    self.branch_split_points[up_link_name].add(from_point)
                up_link_points = (from_point, to_point)
                up_link_branch_name = f"{from_branch.name}_{to_branch.name}"
                up_link_branch_topo_id = f"{from_branch.topo_id}_{to_branch.topo_id}"
                up_link_branch = self.branch_cls(
                    up_link_branch_name, up_link_branch_topo_id, 0.0, 0.0, None, None, up_link_points, True
                )
                connection_branches[up_link_branch_name] = up_link_branch
            if down_link_name:
                from_branch = branch
                to_branch = self.branches[down_link_name]
                from_point = branch.points[-1]
                try:
                    to_pid = self.chainage_points[down_link_name, down_link_chainage]
                    to_point = self.points[to_pid]
                except KeyError:
                    to_point = self.generate_chainage_point(to_branch, down_link_chainage)
                    self.points[to_point.id] = to_point
                    self.chainage_points[down_link_name, down_link_chainage] = to_point.id
                    self.extra_branch_points[down_link_name].add(to_point)
                downstream_replacement_point = self.point_cls(-to_point.id, to_point.x, to_point.y, float("inf"))
                self.points[downstream_replacement_point.id] = downstream_replacement_point
                self.node_replacements[from_point.id] = downstream_replacement_point.id
                if to_point != to_branch.points[0]:
                    self.branch_split_points[down_link_name].add(to_point)
                down_link_points = (from_point, to_point)
                down_link_branch_name = f"{from_branch.name}_{to_branch.name}"
                down_link_branch_topo_id = f"{from_branch.topo_id}_{to_branch.topo_id}"
                down_link_branch = self.branch_cls(
                    down_link_branch_name, down_link_branch_topo_id, 0.0, 0.0, None, None, down_link_points, True
                )
                connection_branches[down_link_branch_name] = down_link_branch
        self.branches.update(connection_branches)

    def parse_component_data(self):
        """Parse full component data."""
        if not self.is_available:
            return
        with open(self.filepath) as nwk_file:
            nwk_txt = nwk_file.read()
            self._parse_projection(nwk_txt)
            self._parse_points(nwk_txt)
            self._parse_branches(nwk_txt)
            self._add_connections_as_branches()


class XSComponent(MikeComponent):
    """MIKE11 cross-sections component class."""

    NAME = "xs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rawdata_filepath = None
        self.cross_section_data = defaultdict(list)
        self.xs_cls = namedtuple("cross_section", ["name", "topo_id", "chainage", "resistance_type", "profile"])

    @property
    def is_available(self):
        """Check if component file is available."""
        if super().is_available:
            return self.rawdata_filepath and os.path.exists(self.rawdata_filepath)
        else:
            return False

    @cached_property
    def levee_banks_markers(self):
        """Return cross-section levee banks markers."""
        return {"<#1>", "<#4>"}

    @cached_property
    def lowest_point_marker(self):
        """Return cross-section lowest point marker."""
        return "<#2>"

    def _discover_rawdata_path(self):
        """Discover path of the cross-sections raw data file."""
        if self.filepath:
            rawdata_filepath = self.filepath.rsplit(".", 1)[0] + ".txt"
            if os.path.exists(rawdata_filepath):
                self.rawdata_filepath = rawdata_filepath

    @staticmethod
    def segmentize_xs_rawdata(single_xs_rawdata):
        """Split cross-section raw data sections."""
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
        """Parse full component data."""
        if not self.is_available:
            return
        with open(self.rawdata_filepath) as xs_file:
            for xs_txt_raw in xs_file.read().split("*******************************"):
                xs_txt = xs_txt_raw.strip()
                if not xs_txt:
                    continue
                rawdata_segments = self.segmentize_xs_rawdata(xs_txt)
                topo_id, name, chainage_str = [row.strip() for row in rawdata_segments["CHANNEL"].split("\n")]
                chainage = float(chainage_str)
                resistance_numbers = [number.strip() for number in rawdata_segments["RESISTANCE NUMBERS"].split()]
                resistance_type = int(resistance_numbers[1])
                profile_lines = (row.strip() for row in rawdata_segments["PROFILE"].split("\n")[1:])
                profile = []
                for line in profile_lines:
                    line_values = [val.strip() for val in line.split()][:4]
                    profile.append(line_values)
                xs = self.xs_cls(name, topo_id, chainage, resistance_type, profile)
                self.cross_section_data[name].append(xs)

    def discover_component_path(self, text_to_search):
        """Discover component data file paths."""
        super().discover_component_path(text_to_search)
        self._discover_rawdata_path()


class BNDComponent(MikeComponent):
    NAME = "bnd"


class RRComponent(MikeComponent):
    NAME = "rr"


class HDComponent(MikeComponent):
    """MIKE11 HD component class."""

    NAME = "hd"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_conditions = defaultdict(list)
        self.bed_resistance = defaultdict(list)
        self.initial_conditions_cls = namedtuple("initial_conditions", ["river_name", "chainage", "h", "q"])
        self.bed_resistance_cls = namedtuple("bed_resistance", ["river_name", "chainage", "resistance"])

    def _parse_init_list(self, hd_txt):
        """Parse initial conditions data."""
        init_txt = self.parser.extract_sections(hd_txt, "InitList")[0]
        init_rows = [row.split("=")[-1].strip().replace("'", "") for row in init_txt.split("\n") if "=" in row]
        for init_row in init_rows:
            river_name, chainage_str, h_str, q_str = [i.strip() for i in init_row.split(",")]
            river_name = river_name.upper()
            chainage = float(chainage_str)
            h = float(h_str)
            q = float(q_str)
            initial_conditions = self.initial_conditions_cls(river_name, chainage, h, q)
            self.initial_conditions[river_name].append(initial_conditions)
        for river_initial_conditions in self.initial_conditions.values():
            river_initial_conditions.sort(key=attrgetter("chainage"))

    def _parse_bed_list(self, hd_txt):
        """Parse bed resistance data."""
        bed_txt = self.parser.extract_sections(hd_txt, "BedList")[0]
        bed_rows = [row.split("=")[-1].strip().replace("'", "") for row in bed_txt.split("\n") if "=" in row]
        for bed_row in bed_rows:
            river_name, chainage_str, resistance_str = [i.strip() for i in bed_row.split(",")][:3]
            river_name = river_name.upper()
            chainage = float(chainage_str)
            resistance = float(resistance_str)
            bed_resistance = self.bed_resistance_cls(river_name, chainage, resistance)
            self.bed_resistance[river_name].append(bed_resistance)
        for river_bed_resistance in self.bed_resistance.values():
            river_bed_resistance.sort(key=attrgetter("chainage"))

    def parse_component_data(self):
        """Parse full component data."""
        if not self.is_available:
            return
        with open(self.filepath) as hd_file:
            hd_txt = hd_file.read()
            self._parse_init_list(hd_txt)
            self._parse_bed_list(hd_txt)


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
    """Main MIKE11 components parsing class."""

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
        """Split and extract component data section."""
        section_pattern = re.compile(rf"\[{split_token}\].+?EndSect  // {split_token}", re.M | re.S)
        match_list = re.findall(section_pattern, text)
        return match_list

    @property
    def sim11_dir(self):
        """Return simulation filepath."""
        return os.path.dirname(self.sim11_filepath)

    def detect_components(self):
        """Detect all available components filepaths."""
        with open(self.sim11_filepath) as sim11_file:
            sim11_text = sim11_file.read()
            inputs_text = self.extract_sections(sim11_text, "Input")[0]
            for component_cls in self.COMPONENT_CLASSES:
                component = component_cls(self)
                component.discover_component_path(inputs_text)
                if component.is_available:
                    self.components[component_cls] = component
