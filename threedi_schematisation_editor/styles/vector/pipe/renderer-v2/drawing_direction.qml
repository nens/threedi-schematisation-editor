<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 type="RuleRenderer" enableorderby="0" referencescale="-1" forceraster="0" symbollevels="0">
    <rules key="{1c4a4e03-d442-4bb0-8ffc-82b9a703e08f}">
      <rule label="Combined sewer" symbol="0" key="{844e5e28-ad8f-43dc-ae9b-2eedeecde873}" filter="sewerage_type = 0" />
      <rule label="Storm drain" symbol="1" key="{3b41f70d-2dfe-4438-8b1a-3722a52ff82b}" filter="sewerage_type = 1" />
      <rule label="Sanitary sewer" symbol="2" key="{c8833167-878e-49b2-bd37-5019aeea2451}" filter="sewerage_type = 2" />
      <rule label="Transport" symbol="3" key="{d62bccfa-4138-43ba-ab6d-51eae9f5b079}" filter="sewerage_type = 3" />
      <rule label="Spillway" symbol="4" key="{3d909156-553e-4d45-8a2f-02337ffb74d5}" filter="sewerage_type = 4" />
      <rule label="Syphon" symbol="5" key="{a445abaf-878b-4b6b-8f1d-1314d1271d38}" filter="sewerage_type =5" />
      <rule label="Storage" symbol="6" key="{c6ba261b-8172-407e-bc72-8487b24a1cc4}" filter="sewerage_type = 6" />
      <rule label="Storage and settlement tank" symbol="7" key="{8eb66a66-0335-4672-a78d-1aac6c4702ff}" filter="sewerage_type = 7" />
      <rule label="Other" symbol="8" key="{aa320dac-96a8-41e4-af30-3e9153ceaeae}" filter="ELSE" />
    </rules>
    <symbols>
      <symbol type="line" force_rhr="0" name="0" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{cb3a09f5-f0d2-4f56-b942-87c2dfc1ac3e}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="255,170,0,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{1bd4ac27-0a67-4037-ad7a-73b7701a1bff}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
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
            <layer class="SimpleMarker" locked="0" pass="0" id="{4f2d6789-9766-48a1-9049-07521382d517}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,170,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
      <symbol type="line" force_rhr="0" name="1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{f842a4cb-b412-4e2d-a956-9c2ebc771924}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="85,170,255,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{fc876425-d9e4-4e19-bc07-b82830e11e27}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@1@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{63b2cc93-2c2c-4c91-bef6-5c8a295e1063}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="85,170,255,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
      <symbol type="line" force_rhr="0" name="2" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{386f6172-f80d-47fd-9ec2-a0b4c74b653c}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="255,0,0,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{0d2e4359-2c74-4bb4-85fe-5c1132e4679f}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@2@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{e645752f-a8bf-41f6-9b41-8ef4e362a7f8}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
      <symbol type="line" force_rhr="0" name="3" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{663fb02f-f330-4ef5-96a5-308f03ba2191}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="153,153,153,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{b1585a3f-4ee8-4501-95a0-edfe1209e837}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@3@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{fd51016f-8ab2-4fef-912d-2312617184f2}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="153,153,153,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
      <symbol type="line" force_rhr="0" name="4" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{7dfcd733-bc53-4d85-b738-c3eceb660616}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="85,170,255,255" />
            <Option type="QString" name="line_style" value="dot" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{f833c341-360e-4027-af80-45b349844b99}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@4@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{962b669f-977a-49ce-b4b9-2110e203cc97}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="85,170,255,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
      <symbol type="line" force_rhr="0" name="5" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{1c1563c3-0e34-428c-916b-382f76f14903}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="85,170,255,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{02f321a3-4e36-4ff5-9322-bef841e4eb13}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@5@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{f4cdac9e-35e5-4e45-b5d4-a1eca57e3268}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="85,170,255,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="left_half_triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="85,170,255,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="3.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                  </Option>
                  <Option type="QString" name="type" value="collection" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{0da681a0-51e8-4512-9fa9-cc108c13d1db}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@5@2" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{086c70fc-002b-4bea-bf15-1dda73afb9a5}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="85,170,255,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="semi_circle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="35,35,35,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="1.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option name="properties" />
                  <Option type="QString" name="type" value="collection" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="6" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{fb9cd4e0-7e42-41fc-b984-42b3b3d53ca8}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="189,189,189,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="2" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{30ccf23c-9c7a-41b1-8061-e91155022aeb}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@6@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{975864f0-8311-4f0b-8f97-6abeac6710bf}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="arrowhead" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="35,35,35,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.4" />
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
                  <Option name="properties" />
                  <Option type="QString" name="type" value="collection" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="7" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{3d01f469-1245-49d5-91f9-0055272ae1fb}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="92,92,92,255" />
            <Option type="QString" name="line_style" value="solid" />
            <Option type="QString" name="line_width" value="2" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{a88c0dc1-8667-4a4e-9e5a-2c5305898d26}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@7@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{1660843d-edd0-40a7-8717-f387e26b4aa7}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="arrowhead" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,255,255,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.4" />
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
                  <Option name="properties" />
                  <Option type="QString" name="type" value="collection" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="8" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{8d1d8f99-3003-4906-a98a-3cbbd5af7996}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0" />
            <Option type="QString" name="capstyle" value="square" />
            <Option type="QString" name="customdash" value="0" />
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="customdash_unit" value="MM" />
            <Option type="QString" name="dash_pattern_offset" value="0" />
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="dash_pattern_offset_unit" value="MM" />
            <Option type="QString" name="draw_inside_polygon" value="0" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="line_color" value="0,0,0,255" />
            <Option type="QString" name="line_style" value="dot" />
            <Option type="QString" name="line_width" value="0.4" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{d6173210-e691-4f76-9685-61aa107d57a2}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="10" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@8@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{35ee55a3-1951-40e8-b90c-8a4d7202d72f}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="90" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="0,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="255,170,0,255" />
                <Option type="QString" name="outline_style" value="no" />
                <Option type="QString" name="outline_width" value="0.6" />
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="outline_width_unit" value="MM" />
                <Option type="QString" name="scale_method" value="diameter" />
                <Option type="QString" name="size" value="2.4" />
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="size_unit" value="MM" />
                <Option type="QString" name="vertical_anchor_point" value="1" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value="" />
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false" />
                      <Option type="QString" name="expression" value="" />
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
  </renderer-v2>
  </qgis>