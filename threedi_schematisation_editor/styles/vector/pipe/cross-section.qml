<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" readOnly="0" minScale="0" labelsEnabled="1" simplifyAlgorithm="0" simplifyMaxScale="1" simplifyLocal="1" simplifyDrawingTol="1" simplifyDrawingHints="1" maxScale="0" version="3.22.10-Białowieża" styleCategories="AllStyleCategories" symbologyReferenceScale="-1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal mode="0" fixedDuration="0" limitMode="0" endField="" startExpression="" endExpression="" accumulate="0" durationField="" durationUnit="min" enabled="0" startField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" forceraster="0" symbollevels="0" referencescale="-1" attr="sewerage_type" type="categorizedSymbol">
    <categories>
      <category value="0" render="true" symbol="0" label="Combined sewer"/>
      <category value="1" render="true" symbol="1" label="Storm drain"/>
      <category value="2" render="true" symbol="2" label="Sanitary sewer"/>
      <category value="3" render="true" symbol="3" label="Transport"/>
      <category value="" render="true" symbol="4" label="Other"/>
    </categories>
    <symbols>
      <symbol clip_to_extent="1" name="0" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="255,170,0,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,170,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="1" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="85,170,255,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="2" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="255,0,0,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
		</layer>
      </symbol>
      <symbol clip_to_extent="1" name="3" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="153,153,153,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="153,153,153,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="4" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="0,0,0,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" name="0" alpha="1" force_rhr="0" type="line">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" class="SimpleLine" enabled="1" locked="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="0" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="255,170,0,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.4" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,170,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="trim_distance_end"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
          <prop v="MM" k="trim_distance_end_unit"/>
          <prop v="0" k="trim_distance_start"/>
          <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
          <prop v="MM" k="trim_distance_start_unit"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="try( coalesce( scale_linear(cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table), 0.1, 1, 0.1, 3), 1),	1)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontUnderline="0" fontItalic="0" fontSize="7" forcedItalic="0" previewBkgrdColor="255,255,255,255" fontStrikeout="0" isExpression="1" textColor="0,0,0,255" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontKerning="1" fontWordSpacing="0" fieldName="cross_section_label(cross_section_shape, cross_section_width, cross_section_height, cross_section_table, 'mm', True)" namedStyle="Regular" fontWeight="50" forcedBold="0" allowHtml="0" capitalization="0" useSubstitutions="0" fontFamily="MS Gothic" fontLetterSpacing="0" legendString="Aa" fontSizeUnit="Point" multilineHeightUnit="Percentage" textOpacity="1" blendMode="0" textOrientation="horizontal" multilineHeight="1">
        <families/>
        <text-buffer bufferNoFill="0" bufferBlendMode="0" bufferSize="0.69999999999999996" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferDraw="1" bufferSizeUnits="MM" bufferOpacity="1"/>
        <text-mask maskSize="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskedSymbolLayers="" maskOpacity="1" maskType="0" maskEnabled="0" maskSizeUnits="MM"/>
        <background shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeType="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeRadiiX="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeRadiiUnit="MM" shapeSizeY="0" shapeJoinStyle="64" shapeBlendMode="0" shapeOffsetY="0" shapeOffsetX="0" shapeRadiiY="0" shapeSizeX="0" shapeRotation="0" shapeBorderWidth="0" shapeSVGFile="" shapeRotationType="0" shapeOffsetUnit="MM" shapeSizeUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255">
          <symbol type="marker" frame_rate="10" is_animated="0" name="markerSymbol" alpha="1" clip_to_extent="1" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer pass="0" locked="0" enabled="1" class="SimpleMarker">
              <Option type="Map">
                <Option value="0" type="QString" name="angle"/>
                <Option value="square" type="QString" name="cap_style"/>
                <Option value="133,182,111,255" type="QString" name="color"/>
                <Option value="1" type="QString" name="horizontal_anchor_point"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="circle" type="QString" name="name"/>
                <Option value="0,0" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="MM" type="QString" name="offset_unit"/>
                <Option value="35,35,35,255" type="QString" name="outline_color"/>
                <Option value="solid" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="diameter" type="QString" name="scale_method"/>
                <Option value="2" type="QString" name="size"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                <Option value="MM" type="QString" name="size_unit"/>
                <Option value="1" type="QString" name="vertical_anchor_point"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol type="fill" frame_rate="10" is_animated="0" name="fillSymbol" alpha="1" clip_to_extent="1" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
            <layer pass="0" locked="0" enabled="1" class="SimpleFill">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale"/>
                <Option value="255,255,255,255" type="QString" name="color"/>
                <Option value="bevel" type="QString" name="joinstyle"/>
                <Option value="0,0" type="QString" name="offset"/>
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                <Option value="MM" type="QString" name="offset_unit"/>
                <Option value="128,128,128,255" type="QString" name="outline_color"/>
                <Option value="no" type="QString" name="outline_style"/>
                <Option value="0" type="QString" name="outline_width"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="solid" type="QString" name="style"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowDraw="0" shadowOffsetAngle="135" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetUnit="MM" shadowUnder="0" shadowOffsetGlobal="1"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format wrapChar="" multilineAlign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" autoWrapLength="0" rightDirectionSymbol=">" formatNumbers="0" decimals="3" plussign="0" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0"/>
      <placement predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" lineAnchorClipping="0" lineAnchorType="0" offsetType="0" fitInPolygonOnly="0" offsetUnits="MapUnit" polygonPlacementFlags="2" geometryGenerator="" allowDegraded="0" lineAnchorPercent="0.5" overrunDistance="0" layerType="LineGeometry" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorTextPoint="CenterOfText" distUnits="MM" preserveRotation="1" geometryGeneratorType="PointGeometry" maxCurvedCharAngleOut="-25" xOffset="0" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" repeatDistance="0" quadOffset="4" priority="5" overlapHandling="PreventOverlap" placement="2" maxCurvedCharAngleIn="25" centroidWhole="0" overrunDistanceUnit="MM" placementFlags="9" geometryGeneratorEnabled="0" repeatDistanceUnits="MM" yOffset="0" dist="0" rotationUnit="AngleDegrees" centroidInside="0"/>
      <rendering upsidedownLabels="0" labelPerPart="0" minFeatureSize="0" obstacle="1" scaleMax="5000" drawLabels="1" maxNumLabels="2000" scaleMin="0" zIndex="0" mergeLines="0" limitNumLabels="0" obstacleType="0" unplacedVisibility="0" fontMaxPixelSize="10000" fontLimitPixelSize="0" fontMinPixelSize="3" obstacleFactor="1" scaleVisibility="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="Color">
              <Option value="false" type="bool" name="active"/>
              <Option value="case &#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end" type="QString" name="expression"/>
              <Option value="3" type="int" name="type"/>
            </Option>
          </Option>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
          <Option value="0" type="int" name="blendMode"/>
          <Option type="Map" name="ddProperties">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
          <Option value="false" type="bool" name="drawToAllParts"/>
          <Option value="0" type="QString" name="enabled"/>
          <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
          <Option value="&lt;symbol type=&quot;line&quot; frame_rate=&quot;10&quot; is_animated=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer pass=&quot;0&quot; locked=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;align_dash_pattern&quot;/>&lt;Option value=&quot;square&quot; type=&quot;QString&quot; name=&quot;capstyle&quot;/>&lt;Option value=&quot;5;2&quot; type=&quot;QString&quot; name=&quot;customdash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;customdash_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;customdash_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;draw_inside_polygon&quot;/>&lt;Option value=&quot;bevel&quot; type=&quot;QString&quot; name=&quot;joinstyle&quot;/>&lt;Option value=&quot;60,60,60,255&quot; type=&quot;QString&quot; name=&quot;line_color&quot;/>&lt;Option value=&quot;solid&quot; type=&quot;QString&quot; name=&quot;line_style&quot;/>&lt;Option value=&quot;0.3&quot; type=&quot;QString&quot; name=&quot;line_width&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;line_width_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;ring_filter&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;use_custom_dash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;width_map_unit_scale&quot;/>&lt;/Option>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
          <Option value="0" type="double" name="minLength"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
          <Option value="MM" type="QString" name="minLengthUnit"/>
          <Option value="0" type="double" name="offsetFromAnchor"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
          <Option value="0" type="double" name="offsetFromLabel"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <Option type="Map">
      <Option name="embeddedWidgets/count" value="0" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory minimumSize="0" spacing="5" width="15" rotationOffset="270" backgroundAlpha="255" penColor="#000000" enabled="0" spacingUnitScale="3x:0,0,0,0,0,0" minScaleDenominator="0" lineSizeType="MM" diagramOrientation="Up" scaleBasedVisibility="0" height="15" sizeType="MM" direction="0" penWidth="0" maxScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" showAxis="1" spacingUnit="MM" opacity="1" labelPlacementMethod="XHeight" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" barWidth="5">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" colorOpacity="1" label=""/>
      <axisSymbol>
        <symbol clip_to_extent="1" name="" alpha="1" force_rhr="0" type="line">
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer pass="0" class="SimpleLine" enabled="1" locked="0">
            <Option type="Map">
              <Option name="align_dash_pattern" value="0" type="QString"/>
              <Option name="capstyle" value="square" type="QString"/>
              <Option name="customdash" value="5;2" type="QString"/>
              <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="customdash_unit" value="MM" type="QString"/>
              <Option name="dash_pattern_offset" value="0" type="QString"/>
              <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
              <Option name="draw_inside_polygon" value="0" type="QString"/>
              <Option name="joinstyle" value="bevel" type="QString"/>
              <Option name="line_color" value="35,35,35,255" type="QString"/>
              <Option name="line_style" value="solid" type="QString"/>
              <Option name="line_width" value="0.26" type="QString"/>
              <Option name="line_width_unit" value="MM" type="QString"/>
              <Option name="offset" value="0" type="QString"/>
              <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offset_unit" value="MM" type="QString"/>
              <Option name="ring_filter" value="0" type="QString"/>
              <Option name="trim_distance_end" value="0" type="QString"/>
              <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_end_unit" value="MM" type="QString"/>
              <Option name="trim_distance_start" value="0" type="QString"/>
              <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_start_unit" value="MM" type="QString"/>
              <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
              <Option name="use_custom_dash" value="0" type="QString"/>
              <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            </Option>
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="trim_distance_end"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_end_map_unit_scale"/>
            <prop v="MM" k="trim_distance_end_unit"/>
            <prop v="0" k="trim_distance_start"/>
            <prop v="3x:0,0,0,0,0,0" k="trim_distance_start_map_unit_scale"/>
            <prop v="MM" k="trim_distance_start_unit"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" zIndex="0" obstacle="0" linePlacementFlags="18" showAll="1" placement="2" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Embedded" value="0" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Isolated" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Connected" value="2" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Broad crested" value="3" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Short crested" value="4" type="int"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dist_calc_points">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="-1.7976931348623157e+308" type="double"/>
            <Option name="Precision" value="4" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="invert_level_start_point">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="-1.7976931348623157e+308" type="double"/>
            <Option name="Precision" value="3" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="invert_level_end_point">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="-1.7976931348623157e+308" type="double"/>
            <Option name="Precision" value="3" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="friction_value">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="0" type="double"/>
            <Option name="Precision" value="4" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Chezy" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Manning" value="2" type="int"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="material">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="Concrete" value="0" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Pvc" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Gres" value="2" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Cast iron" value="3" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Brickwork" value="4" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Hpe" value="5" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Hdpe" value="6" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Plate iron" value="7" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Steel" value="8" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Stoneware" value="9" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Sheet iron" value="10" type="int"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="pipe_quality">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="sewerage_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="Mixed" value="0" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Rain water" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Dry weather flow" value="2" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Transport" value="3" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Spillway" value="4" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Zinker" value="5" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Storage" value="6" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Storage tank" value="7" type="int"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="Lowest visibility" value="0" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Low visibility" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Medium low visibility" value="2" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Medium visibility" value="3" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="High visibility" value="4" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Highest visibility" value="5" type="int"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="profile_num">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="original_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="connection_node_start_id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="connection_node_end_id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Closed rectangle" value="0" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Open rectangle" value="1" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Circle" value="2" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Egg" value="3" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated rectangle" value="5" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated trapezium" value="6" type="int"/>
              </Option>
              <Option type="Map">
                <Option name="YZ" type="int" value="7"/>
              </Option>
              <Option type="Map">
                <Option name="Inverted egg" type="int" value="8"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_width">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="-1.7976931348623157e+308" type="double"/>
            <Option name="Precision" value="3" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_height">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="1.7976931348623157e+308" type="double"/>
            <Option name="Min" value="-1.7976931348623157e+308" type="double"/>
            <Option name="Precision" value="3" type="int"/>
            <Option name="Step" value="1" type="double"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_table">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="code" index="2"/>
    <alias name="" field="display_name" index="3"/>
    <alias name="" field="calculation_type" index="4"/>
    <alias name="" field="dist_calc_points" index="5"/>
    <alias name="" field="invert_level_start_point" index="6"/>
    <alias name="" field="invert_level_end_point" index="7"/>
    <alias name="" field="friction_value" index="8"/>
    <alias name="" field="friction_type" index="9"/>
    <alias name="" field="material" index="10"/>
    <alias name="" field="pipe_quality" index="11"/>
    <alias name="" field="sewerage_type" index="12"/>
    <alias name="" field="zoom_category" index="13"/>
    <alias name="" field="profile_num" index="14"/>
    <alias name="" field="original_length" index="15"/>
    <alias name="" field="connection_node_start_id" index="16"/>
    <alias name="" field="connection_node_end_id" index="17"/>
    <alias name="" field="cross_section_shape" index="18"/>
    <alias name="" field="cross_section_width" index="19"/>
    <alias name="" field="cross_section_height" index="20"/>
    <alias name="" field="cross_section_table" index="21"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" field="fid" expression=""/>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="code" expression=""/>
    <default applyOnUpdate="0" field="display_name" expression=""/>
    <default applyOnUpdate="0" field="calculation_type" expression=""/>
    <default applyOnUpdate="0" field="dist_calc_points" expression=""/>
    <default applyOnUpdate="0" field="invert_level_start_point" expression=""/>
    <default applyOnUpdate="0" field="invert_level_end_point" expression=""/>
    <default applyOnUpdate="0" field="friction_value" expression=""/>
    <default applyOnUpdate="0" field="friction_type" expression=""/>
    <default applyOnUpdate="0" field="material" expression=""/>
    <default applyOnUpdate="0" field="pipe_quality" expression=""/>
    <default applyOnUpdate="0" field="sewerage_type" expression=""/>
    <default applyOnUpdate="0" field="zoom_category" expression=""/>
    <default applyOnUpdate="0" field="profile_num" expression=""/>
    <default applyOnUpdate="0" field="original_length" expression=""/>
    <default applyOnUpdate="0" field="connection_node_start_id" expression=""/>
    <default applyOnUpdate="0" field="connection_node_end_id" expression=""/>
    <default applyOnUpdate="0" field="cross_section_shape" expression=""/>
    <default applyOnUpdate="0" field="cross_section_width" expression=""/>
    <default applyOnUpdate="0" field="cross_section_height" expression=""/>
    <default applyOnUpdate="0" field="cross_section_table" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="1" field="fid" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="0" field="id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="code" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="display_name" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="calculation_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="dist_calc_points" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="invert_level_start_point" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="invert_level_end_point" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="friction_value" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="friction_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="material" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="pipe_quality" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="sewerage_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="zoom_category" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="profile_num" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="original_length" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="connection_node_start_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="connection_node_end_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="cross_section_shape" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="cross_section_width" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="cross_section_height" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="cross_section_table" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="display_name" desc="" exp=""/>
    <constraint field="calculation_type" desc="" exp=""/>
    <constraint field="dist_calc_points" desc="" exp=""/>
    <constraint field="invert_level_start_point" desc="" exp=""/>
    <constraint field="invert_level_end_point" desc="" exp=""/>
    <constraint field="friction_value" desc="" exp=""/>
    <constraint field="friction_type" desc="" exp=""/>
    <constraint field="material" desc="" exp=""/>
    <constraint field="pipe_quality" desc="" exp=""/>
    <constraint field="sewerage_type" desc="" exp=""/>
    <constraint field="zoom_category" desc="" exp=""/>
    <constraint field="profile_num" desc="" exp=""/>
    <constraint field="original_length" desc="" exp=""/>
    <constraint field="connection_node_start_id" desc="" exp=""/>
    <constraint field="connection_node_end_id" desc="" exp=""/>
    <constraint field="cross_section_shape" desc="" exp=""/>
    <constraint field="cross_section_width" desc="" exp=""/>
    <constraint field="cross_section_height" desc="" exp=""/>
    <constraint field="cross_section_table" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column hidden="1" name="fid" width="-1" type="field"/>
      <column hidden="0" name="id" width="-1" type="field"/>
      <column hidden="0" name="code" width="-1" type="field"/>
      <column hidden="0" name="display_name" width="-1" type="field"/>
      <column hidden="0" name="calculation_type" width="-1" type="field"/>
      <column hidden="0" name="dist_calc_points" width="-1" type="field"/>
      <column hidden="0" name="invert_level_start_point" width="-1" type="field"/>
      <column hidden="0" name="invert_level_end_point" width="-1" type="field"/>
      <column hidden="0" name="friction_value" width="-1" type="field"/>
      <column hidden="0" name="friction_type" width="-1" type="field"/>
      <column hidden="0" name="material" width="-1" type="field"/>
      <column hidden="0" name="pipe_quality" width="-1" type="field"/>
      <column hidden="0" name="sewerage_type" width="-1" type="field"/>
      <column hidden="0" name="zoom_category" width="-1" type="field"/>
      <column hidden="0" name="profile_num" width="-1" type="field"/>
      <column hidden="0" name="original_length" width="-1" type="field"/>
      <column hidden="0" name="connection_node_start_id" width="-1" type="field"/>
      <column hidden="0" name="connection_node_end_id" width="-1" type="field"/>
      <column hidden="0" name="cross_section_shape" width="-1" type="field"/>
      <column hidden="0" name="cross_section_width" width="-1" type="field"/>
      <column hidden="0" name="cross_section_height" width="-1" type="field"/>
      <column hidden="0" name="cross_section_table" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:\Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\python39/python/plugins\threedi_schematisation_editor\forms\ui\pipe.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_schematisation_editor.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Pipe view" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="0">
      <attributeEditorContainer name="General" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="1">
        <attributeEditorField name="id" showLabel="1" index="1"/>
        <attributeEditorField name="display_name" showLabel="1" index="3"/>
        <attributeEditorField name="code" showLabel="1" index="2"/>
        <attributeEditorField name="calculation_type" showLabel="1" index="4"/>
        <attributeEditorField name="dist_calc_points" showLabel="1" index="5"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="1">
        <attributeEditorField name="invert_level_start_point" showLabel="1" index="6"/>
        <attributeEditorField name="invert_level_end_point" showLabel="1" index="7"/>
        <attributeEditorField name="friction_value" showLabel="1" index="8"/>
        <attributeEditorField name="friction_type" showLabel="1" index="9"/>
        <attributeEditorField name="material" showLabel="1" index="10"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section definition" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="1">
        <attributeEditorField name="cross_section_shape" showLabel="1" index="18"/>
        <attributeEditorField name="cross_section_width" showLabel="1" index="19"/>
        <attributeEditorField name="cross_section_height" showLabel="1" index="20"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="1">
        <attributeEditorField name="sewerage_type" showLabel="1" index="12"/>
        <attributeEditorField name="zoom_category" showLabel="1" index="13"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Connection nodes" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1" columnCount="1" groupBox="1">
        <attributeEditorField name="connection_node_start_id" showLabel="1" index="16"/>
        <attributeEditorField name="connection_node_end_id" showLabel="1" index="17"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="0" name="connection_node_end_id"/>
    <field editable="0" name="connection_node_start_id"/>
    <field editable="1" name="cross_section_height"/>
    <field editable="1" name="cross_section_shape"/>
    <field editable="1" name="cross_section_table"/>
    <field editable="1" name="cross_section_width"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="invert_level_end_point"/>
    <field editable="1" name="invert_level_start_point"/>
    <field editable="1" name="material"/>
    <field editable="1" name="original_length"/>
    <field editable="1" name="pipe_quality"/>
    <field editable="1" name="profile_num"/>
    <field editable="1" name="sewerage_type"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="calculation_type" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="cross_section_height" labelOnTop="0"/>
    <field name="cross_section_shape" labelOnTop="0"/>
    <field name="cross_section_table" labelOnTop="0"/>
    <field name="cross_section_width" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dist_calc_points" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="invert_level_end_point" labelOnTop="0"/>
    <field name="invert_level_start_point" labelOnTop="0"/>
    <field name="material" labelOnTop="0"/>
    <field name="original_length" labelOnTop="0"/>
    <field name="pipe_quality" labelOnTop="0"/>
    <field name="profile_num" labelOnTop="0"/>
    <field name="sewerage_type" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="calculation_type" reuseLastValue="0"/>
    <field name="code" reuseLastValue="0"/>
    <field name="connection_node_end_id" reuseLastValue="0"/>
    <field name="connection_node_start_id" reuseLastValue="0"/>
    <field name="cross_section_height" reuseLastValue="0"/>
    <field name="cross_section_shape" reuseLastValue="0"/>
    <field name="cross_section_table" reuseLastValue="0"/>
    <field name="cross_section_width" reuseLastValue="0"/>
    <field name="display_name" reuseLastValue="0"/>
    <field name="dist_calc_points" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
    <field name="friction_type" reuseLastValue="0"/>
    <field name="friction_value" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="invert_level_end_point" reuseLastValue="0"/>
    <field name="invert_level_start_point" reuseLastValue="0"/>
    <field name="material" reuseLastValue="0"/>
    <field name="original_length" reuseLastValue="0"/>
    <field name="pipe_quality" reuseLastValue="0"/>
    <field name="profile_num" reuseLastValue="0"/>
    <field name="sewerage_type" reuseLastValue="0"/>
    <field name="zoom_category" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>