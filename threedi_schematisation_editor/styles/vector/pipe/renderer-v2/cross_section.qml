<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 type="categorizedSymbol" enableorderby="0" attr="sewerage_type" referencescale="-1" forceraster="0" symbollevels="0">
    <categories>
      <category type="string" render="true" value="0" label="Combined sewer" symbol="0" uuid="0" />
      <category type="string" render="true" value="1" label="Storm drain" symbol="1" uuid="1" />
      <category type="string" render="true" value="2" label="Sanitary sewer" symbol="2" uuid="2" />
      <category type="string" render="true" value="3" label="Transport" symbol="3" uuid="3" />
      <category type="string" render="true" value="" label="Other" symbol="4" uuid="4" />
    </categories>
    <symbols>
      <symbol type="line" force_rhr="0" name="0" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{f3e49aaf-fff5-4a3d-92c8-02426d579636}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
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
        <layer class="SimpleLine" locked="0" pass="0" id="{28d29ca6-9d31-4ea1-8682-45f0c46d1977}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
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
        <layer class="SimpleLine" locked="0" pass="0" id="{d0820680-4862-4cd5-ad28-c188cb7f54a9}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
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
        <layer class="SimpleLine" locked="0" pass="0" id="{bb2174e8-b214-4a06-a25b-754398edf0a7}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
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
        <layer class="SimpleLine" locked="0" pass="0" id="{98b4d3ed-de2a-4305-a495-1eafa1df485c}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol type="line" force_rhr="0" name="0" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{5e2aca7e-df1e-4184-9931-208a1dcfff91}" enabled="1">
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
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),&#09;1)" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation />
    <sizescale />
  </renderer-v2>
  </qgis>