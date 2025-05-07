<?xml version='1.0' encoding='utf-8'?>
<qgis>
  <renderer-v2 symbollevels="0" referencescale="-1" enableorderby="0" type="RuleRenderer" forceraster="0">
    <rules key="{1c4a4e03-d442-4bb0-8ffc-82b9a703e08f}">
      <rule symbol="0" label="Combined sewer" key="{844e5e28-ad8f-43dc-ae9b-2eedeecde873}" filter="sewerage_type = 0"/>
      <rule symbol="1" label="Storm drain" key="{3b41f70d-2dfe-4438-8b1a-3722a52ff82b}" filter="sewerage_type = 1"/>
      <rule symbol="2" label="Sanitary sewer" key="{c8833167-878e-49b2-bd37-5019aeea2451}" filter="sewerage_type = 2"/>
      <rule symbol="3" label="Transport" key="{d62bccfa-4138-43ba-ab6d-51eae9f5b079}" filter="sewerage_type = 3"/>
      <rule symbol="4" label="Spillway" key="{3d909156-553e-4d45-8a2f-02337ffb74d5}" filter="sewerage_type = 4"/>
      <rule symbol="5" label="Syphon" key="{a445abaf-878b-4b6b-8f1d-1314d1271d38}" filter="sewerage_type =5"/>
      <rule symbol="6" label="Storage" key="{c6ba261b-8172-407e-bc72-8487b24a1cc4}" filter="sewerage_type = 6"/>
      <rule symbol="7" label="Storage and settlement tank" key="{8eb66a66-0335-4672-a78d-1aac6c4702ff}" filter="sewerage_type = 7"/>
      <rule symbol="8" label="Infiltration drain" key="{b021f941-3672-49ad-9dd1-bb4c53793b56}" filter="sewerage_type = 8"/>
      <rule symbol="9" label="Slot/trench drain" key="{48c58665-9958-43ba-9dcf-3df827544aab}" filter="sewerage_type = 9"/>
      <rule symbol="10" label="Pressure sewer" key="{aa8e25bd-a2c0-469f-8067-f4648e7c2668}" filter="sewerage_type = 10"/>
      <rule symbol="11" label="Other" key="{fc49b29a-73ad-4a8d-b13c-790d69bd70a8}" filter="ELSE"/>
    </rules>
    <symbols>
      <symbol name="0" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="255,170,0,255,rgb:1,0.66666666666666663,0,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="255,170,0,255,rgb:1,0.66666666666666663,0,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="10" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="142,0,255,255,hsv:0.7593333333333333,1,1,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@10@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="142,0,255,255,hsv:0.7593333333333333,1,1,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="11" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="0,0,0,255,rgb:0,0,0,1" type="QString"/>
            <Option name="line_style" value="dot" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@11@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="0,0,0,255,rgb:0,0,0,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="2" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@2@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="3" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="153,153,153,255,rgb:0.59999999999999998,0.59999999999999998,0.59999999999999998,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@3@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="153,153,153,255,rgb:0.59999999999999998,0.59999999999999998,0.59999999999999998,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="4" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{186b2031-0712-472b-9614-911e00827838}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
            <Option name="line_style" value="dot" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@4@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="5" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{d6a5796c-f734-49a8-87a9-352d15611c9c}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{c0c87af1-2a24-4f68-8d79-a6ce59abe0d0}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{727be38e-f172-474a-b0cf-5f69df2df36c}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" id="{03d91650-7106-4e7e-8f7c-af56947a6eaf}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="1" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MM" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="Interval" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@2" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{86a8e825-c81d-49f5-88ac-887c218134f5}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="85,170,255,255,rgb:0.33333333333333331,0.66666666666666663,1,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="semi_circle" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString"/>
                <Option name="outline_style" value="no" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="1.4" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="6" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{5b3c394e-1744-4d82-83a6-de054c711414}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="189,189,189,255,rgb:0.74117647058823533,0.74117647058823533,0.74117647058823533,1" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="2" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="7" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{7fca9ff7-1bb4-4d5d-a9ab-c26a70ddc325}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="92,92,92,255,rgb:0.36078431372549019,0.36078431372549019,0.36078431372549019,1" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="2" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="8" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{1f7742b0-54ab-45f4-b098-581b09aeb599}" class="FilledLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_width" value="1" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@8@0" frame_rate="10" force_rhr="0" clip_to_extent="1" type="fill" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{33f01fb0-c1a2-4f70-83f6-e10fa68b9658}" class="LinePatternFill" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="-45" type="QString"/>
                <Option name="clip_mode" value="during_render" type="QString"/>
                <Option name="color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                <Option name="coordinate_reference" value="viewport" type="QString"/>
                <Option name="distance" value="0.8" type="QString"/>
                <Option name="distance_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="distance_unit" value="MM" type="QString"/>
                <Option name="line_width" value="0.4" type="QString"/>
                <Option name="line_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="line_width_unit" value="MM" type="QString"/>
                <Option name="offset" value="0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
              <symbol name="@@8@0@0" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" id="{508afb82-d960-4dca-80ca-e3d9036e3141}" class="SimpleLine" enabled="1" pass="0">
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
                    <Option name="line_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                    <Option name="line_style" value="solid" type="QString"/>
                    <Option name="line_width" value="0.1" type="QString"/>
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
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </layer>
            <layer locked="0" id="{1c5e8316-80ed-4f96-847b-c7f0cb0c32cd}" class="LinePatternFill" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="45" type="QString"/>
                <Option name="clip_mode" value="during_render" type="QString"/>
                <Option name="color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                <Option name="coordinate_reference" value="viewport" type="QString"/>
                <Option name="distance" value="0.8" type="QString"/>
                <Option name="distance_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="distance_unit" value="MM" type="QString"/>
                <Option name="line_width" value="0.4" type="QString"/>
                <Option name="line_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="line_width_unit" value="MM" type="QString"/>
                <Option name="offset" value="0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
              <symbol name="@@8@0@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" id="{eb83ee28-9766-422d-b6ca-656468a7b154}" class="SimpleLine" enabled="1" pass="0">
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
                    <Option name="line_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                    <Option name="line_style" value="solid" type="QString"/>
                    <Option name="line_width" value="0.1" type="QString"/>
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
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" id="{b1e620c6-c12f-4eea-89e3-b427325bf157}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.15" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0.5" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{d5728d36-1aed-4d55-a92e-185efea261a3}" class="SimpleLine" enabled="1" pass="0">
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
            <Option name="line_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.15" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="-0.5" type="QString"/>
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
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" id="{25cda2df-f8d3-470a-a033-2d0980a19e4c}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="0" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MM" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@8@3" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{2ccaa618-e7c6-40a9-a34c-3e48a08f6f4a}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="9" frame_rate="10" force_rhr="0" clip_to_extent="1" type="line" is_animated="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" id="{c520deaa-a79a-4309-9fde-ad18896e1c82}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="1" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="0.4" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MM" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="Interval" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@9@0" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{57a45368-9365-4e2d-bf47-be81f032d799}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="half_square" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString"/>
                <Option name="outline_style" value="no" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="1" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" id="{81d9efaf-4926-4a42-8d7f-d52c18d1f0a0}" class="MarkerLine" enabled="1" pass="0">
          <Option type="Map">
            <Option name="average_angle_length" value="4" type="QString"/>
            <Option name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="average_angle_unit" value="MM" type="QString"/>
            <Option name="interval" value="3" type="QString"/>
            <Option name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="interval_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_along_line" value="5" type="QString"/>
            <Option name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_along_line_unit" value="MapUnit" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="place_on_every_part" value="true" type="bool"/>
            <Option name="placements" value="CentralPoint" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="rotate" value="1" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@9@1" frame_rate="10" force_rhr="0" clip_to_extent="1" type="marker" is_animated="0" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" id="{74c34199-2471-4c25-8e65-86d0d61b68a6}" class="SimpleMarker" enabled="1" pass="0">
              <Option type="Map">
                <Option name="angle" value="180" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,0,0,255,rgb:1,0,0,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="arrowhead" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="31,120,180,255,rgb:0.12156862745098039,0.47058823529411764,0.70588235294117652,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.6" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(&quot;invert_level_start&quot; >  &quot;invert_level_end&quot;, 0, 180)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <data-defined-properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </data-defined-properties>
  </renderer-v2>
</qgis>