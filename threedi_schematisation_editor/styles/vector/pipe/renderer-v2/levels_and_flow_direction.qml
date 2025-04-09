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
        <layer class="SimpleLine" locked="0" pass="0" id="{186b2031-0712-472b-9614-911e00827838}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{60a56c76-b838-4dbe-b915-8da53ee117ed}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@0@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{5c4f4fbf-a484-4ac9-8a95-2978cd3f1a60}" enabled="1">
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
                <Option type="QString" name="outline_color" value="255,170,0,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="SimpleLine" locked="0" pass="0" id="{a0bcd67c-62b5-4b03-95a7-abb46296407f}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{81d9efaf-4926-4a42-8d7f-d52c18d1f0a0}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@1@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{74c34199-2471-4c25-8e65-86d0d61b68a6}" enabled="1">
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
                <Option type="QString" name="outline_color" value="85,170,255,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="SimpleLine" locked="0" pass="0" id="{de5ac325-49f8-41a6-93ee-51bcc4eb9da5}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{b06d6e62-24ca-4731-87b1-473d2c07b956}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@2@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{59e59b7e-e70c-4838-a8f2-7e68025a06b7}" enabled="1">
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
                <Option type="QString" name="outline_color" value="255,0,0,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="SimpleLine" locked="0" pass="0" id="{7f4dc1b8-5b5a-4480-9170-85208b50212e}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{60bf162b-e8c3-4cb2-884d-274cc8bd82cd}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@3@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{94fe1b23-a51f-411f-b5c0-ec3ac8a35ce4}" enabled="1">
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
                <Option type="QString" name="outline_color" value="153,153,153,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="SimpleLine" locked="0" pass="0" id="{2141b90c-ed33-40a0-a852-2beeca806ff5}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{67669e96-7bec-4e61-9e56-116d91a53858}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@4@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{e7b9c81a-8f29-4d73-a9dc-6760c12be63e}" enabled="1">
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
                <Option type="QString" name="outline_color" value="85,170,255,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="SimpleLine" locked="0" pass="0" id="{d6a5796c-f734-49a8-87a9-352d15611c9c}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{c0c87af1-2a24-4f68-8d79-a6ce59abe0d0}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@5@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{727be38e-f172-474a-b0cf-5f69df2df36c}" enabled="1">
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
                <Option type="QString" name="outline_color" value="85,170,255,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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
        <layer class="MarkerLine" locked="0" pass="0" id="{03d91650-7106-4e7e-8f7c-af56947a6eaf}" enabled="1">
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
            <layer class="SimpleMarker" locked="0" pass="0" id="{86a8e825-c81d-49f5-88ac-887c218134f5}" enabled="1">
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
        <layer class="SimpleLine" locked="0" pass="0" id="{5b3c394e-1744-4d82-83a6-de054c711414}" enabled="1">
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
      </symbol>
      <symbol type="line" force_rhr="0" name="7" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{7fca9ff7-1bb4-4d5d-a9ab-c26a70ddc325}" enabled="1">
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
      </symbol>
      <symbol type="line" force_rhr="0" name="8" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" pass="0" id="{5b4ad054-8c06-4daf-8120-f4b3ad08e8ff}" enabled="1">
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
        <layer class="MarkerLine" locked="0" pass="0" id="{f2dedb8e-b8cd-4699-b295-3b56ed58d5b7}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="average_angle_length" value="4" />
            <Option type="QString" name="average_angle_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="average_angle_unit" value="MM" />
            <Option type="QString" name="interval" value="3" />
            <Option type="QString" name="interval_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="interval_unit" value="MM" />
            <Option type="QString" name="offset" value="0" />
            <Option type="QString" name="offset_along_line" value="5" />
            <Option type="QString" name="offset_along_line_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_along_line_unit" value="MapUnit" />
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
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true" />
                  <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                  <Option type="int" name="type" value="3" />
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
          <symbol type="marker" force_rhr="0" name="@8@1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value="" />
                <Option name="properties" />
                <Option type="QString" name="type" value="collection" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" locked="0" pass="0" id="{af7461d6-c58e-47b6-8ff3-20fad46a01a4}" enabled="1">
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
                <Option type="QString" name="outline_color" value="0,0,0,255" />
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
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="degrees(&#09;azimuth(&#13;&#10;&#09;&#09;start_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ), &#13;&#10;&#09;&#09;&#09;&#09; @project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;), &#13;&#10;&#09;&#09;end_point(&#13;&#10;&#09;&#09;&#09;transform(&#13;&#10;&#09;&#09;&#09;&#09;$geometry,&#13;&#10;&#09;&#09;&#09;&#09;layer_property(  @layer , 'crs' ),&#13;&#10;&#09;&#09;&#09;&#09;@project_crs &#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;)&#13;&#10;&#09;+ &#13;&#10;if(&quot;invert_level_start&quot; &gt;  &quot;invert_level_end&quot;, pi()/-2, pi()/2))" />
                      <Option type="int" name="type" value="3" />
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true" />
                      <Option type="QString" name="expression" value="&quot;invert_level_start&quot; !=  &quot;invert_level_end&quot;" />
                      <Option type="int" name="type" value="3" />
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