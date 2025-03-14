<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 type="singleSymbol" enableorderby="0" referencescale="-1" forceraster="0" symbollevels="0">
    <symbols>
      <symbol type="line" force_rhr="0" name="0" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{dd168761-4db6-458d-ae94-450d054a83b3}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="5;2" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="5,77,209,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.66" />
            <Option type="QString" name="line_width_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="trim_distance_end" value="0" />
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="trim_distance_end_unit" value="MM" />
            <Option type="QString" name="trim_distance_start" value="0" />
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="trim_distance_start_unit" value="MM" />
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0" />
            <Option type="QString" name="use_custom_dash" value="0" />
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 0.66,0.3)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{57e8991c-c8b0-44eb-839a-dac20139272b}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="50" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="RenderMetersInMapUnits" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MM" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="bool" name="place_on_every_part" value="true" />
            <Option type="QString" name="placements" value="Interval" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="1" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="@map_scale&lt;10000" />
                  <Option type="int" name="type" value="3" />
                </Option>
                <Option type="Map" name="interval">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;calculation_point_distance&quot;" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@0@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{98885453-2205-4073-adfb-2160fc0848bf}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="5,77,209,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="circle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="35,35,35,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 2,1)" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                  </Option>
                  <Option type="QString" name="type" value="collection" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation />
    <sizescale />
  </renderer-v2>
  </qgis>