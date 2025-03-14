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
        <layer class="SimpleLine" locked="0" pass="0" id="{5fb1042d-8124-4f5b-971b-35043efbe127}" enabled="1">
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
            <Option type="QString" name="line_color" value="227,26,28,255" />
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
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" locked="0" pass="0" id="{bc97792a-829c-4d7c-834f-cc90a69da0c1}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="5" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="RenderMetersInMapUnits" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="bool" name="place_on_every_part" value="true" />
            <Option type="QString" name="placements" value="FirstVertex" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="1" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="coalesce(discharge_coefficient_negative,0) = 0" />
                  <Option type="int" name="type" value="3" />
                </Option>
                <Option type="Map" name="offset">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="0.3333 * $length" />
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
            <layer class="SimpleMarker" locked="0" pass="0" id="{0beaa75a-bbee-47fb-a094-f8a84d74eef5}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="line" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="227,26,28,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.6" />
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
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="enabled">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{912c93e3-a801-42db-b33b-fa0452c212e7}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="5" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="RenderMetersInMapUnits" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="bool" name="place_on_every_part" value="true" />
            <Option type="QString" name="placements" value="FirstVertex" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="1" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="coalesce(discharge_coefficient_positive, 0) &gt; 0&#13;&#10;AND coalesce(discharge_coefficient_negative,0) = 0" />
                  <Option type="int" name="type" value="3" />
                </Option>
                <Option type="Map" name="offset">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="0.66 * $length" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@0@2" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{ea6a1ac7-4f45-45d4-b55e-b3bee9a813d7}" enabled="1">
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
                <Option type="QString" name="outline_color" value="227,26,28,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.6" />
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
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="enabled">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{f8b12124-c35a-404f-ba96-c65fb4322f45}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="5" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="RenderMetersInMapUnits" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="bool" name="place_on_every_part" value="true" />
            <Option type="QString" name="placements" value="FirstVertex" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="1" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="coalesce(discharge_coefficient_positive,0) = 0" />
                  <Option type="int" name="type" value="3" />
                </Option>
                <Option type="Map" name="offset">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="0.6667 * $length" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@0@3" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{75f72129-7d41-4333-a2b1-1a9434c3f305}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="180" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="line" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="227,26,28,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.6" />
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
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="enabled">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{9aafcb98-c280-4574-af0f-203ef30644b6}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="5" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="0" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="RenderMetersInMapUnits" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="bool" name="place_on_every_part" value="true" />
            <Option type="QString" name="placements" value="FirstVertex" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="1" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="coalesce(discharge_coefficient_negative,0) &gt; 0&#13;&#10;AND coalesce(discharge_coefficient_positive, 0) = 0" />
                  <Option type="int" name="type" value="3" />
                </Option>
                <Option type="Map" name="offset">
                  <Option type="bool" name="active" value="false" />
                  <Option type="int" name="type" value="1" />
                  <Option type="QString" name="val" value="" />
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="0.33 * $length" />
                  <Option type="int" name="type" value="3" />
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@0@4" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{9261729c-7987-44ec-8cd7-722adc8ff614}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="180" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="255,0,0,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="arrowhead" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="227,26,28,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0.6" />
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
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false" />
                      <Option type="int" name="type" value="1" />
                      <Option type="QString" name="val" value="" />
                    </Option>
                    <Option type="Map" name="enabled">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{9a46ca15-90b0-4d06-8440-66dab243968a}" enabled="1">
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
            <Option type="QString" name="placements" value="CentralPoint" />
            <Option type="QString" name="ring_filter" value="0" />
            <Option type="QString" name="rotate" value="0" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value="" />
              <Option name="properties" />
              <Option type="QString" name="type" value="collection" />
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@0@5" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{a1f43dfa-ade6-47bc-9acb-1674ac068ca6}" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0" />
                <Option type="QString" name="cap_style" value="square" />
                <Option type="QString" name="color" value="227,26,28,255" />
                <Option type="QString" name="horizontal_anchor_point" value="1" />
                <Option type="QString" name="joinstyle" value="bevel" />
                <Option type="QString" name="name" value="triangle" />
                <Option type="QString" name="offset" value="0,0" />
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
                <Option type="QString" name="offset_unit" value="MM" />
                <Option type="QString" name="outline_color" value="0,0,0,255" />
                <Option type="QString" name="outline_style" value="solid" />
                <Option type="QString" name="outline_width" value="0" />
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
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 3.4,2)" />
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