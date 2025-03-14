<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 symbollevels="0" referencescale="-1" forceraster="0" enableorderby="0" type="RuleRenderer">
    <rules key="{d31a927e-288e-42f0-ad01-468ef9c5284b}">
      <rule symbol="0" key="{eb59b065-5195-49eb-8070-9209f84a6bb1}" filter=" &quot;affects_2d&quot;" label="Affects 2D" />
      <rule symbol="1" key="{589bea04-af72-4e16-9998-8eb102576b84}" filter=" &quot;affects_1d2d_closed&quot;" label="Affects 1D2D closed" />
      <rule symbol="2" key="{eb7b921b-f0ec-4940-89a9-fa8f137fb53a}" filter=" &quot;affects_1d2d_open_water&quot;" label="Affects 1D2D open water" />
      <rule symbol="3" key="{36df1983-893a-458b-bcea-6fea94eecc5d}" filter="not affects_2d and not affects_1d2d_closed and not affects_1d2d_open_water" label="Affects nothing" />
    </rules>
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="line" name="0" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="3" enabled="1" class="SimpleLine" id="{f03df01a-fe53-4637-8d12-ed9d011fa77e}">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern" />
            <Option value="square" type="QString" name="capstyle" />
            <Option value="5;2" type="QString" name="customdash" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale" />
            <Option value="MM" type="QString" name="customdash_unit" />
            <Option value="0" type="QString" name="dash_pattern_offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale" />
            <Option value="MM" type="QString" name="dash_pattern_offset_unit" />
            <Option value="0" type="QString" name="draw_inside_polygon" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="170,91,82,255" type="QString" name="line_color" />
            <Option value="solid" type="QString" name="line_style" />
            <Option value="0.86" type="QString" name="line_width" />
            <Option value="MM" type="QString" name="line_width_unit" />
            <Option value="0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="0" type="QString" name="ring_filter" />
            <Option value="0" type="QString" name="trim_distance_end" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale" />
            <Option value="MM" type="QString" name="trim_distance_end_unit" />
            <Option value="0" type="QString" name="trim_distance_start" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale" />
            <Option value="MM" type="QString" name="trim_distance_start_unit" />
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners" />
            <Option value="0" type="QString" name="use_custom_dash" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option name="properties" />
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="line" name="1" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine" id="{23436ee6-2152-49e5-baca-37007587ac73}">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale" />
            <Option value="MM" type="QString" name="average_angle_unit" />
            <Option value="6" type="QString" name="interval" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale" />
            <Option value="MM" type="QString" name="interval_unit" />
            <Option value="1.6" type="QString" name="offset" />
            <Option value="2" type="QString" name="offset_along_line" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_along_line_unit" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="true" type="bool" name="place_on_every_part" />
            <Option value="Interval" type="QString" name="placements" />
            <Option value="0" type="QString" name="ring_filter" />
            <Option value="1" type="QString" name="rotate" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option name="properties" />
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="marker" name="@1@0" frame_rate="10">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name" />
                <Option name="properties" />
                <Option value="collection" type="QString" name="type" />
              </Option>
            </data_defined_properties>
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker" id="{aecb381f-ba78-4df5-8ee8-bcc304b75b4c}">
              <Option type="Map">
                <Option value="0" type="QString" name="angle" />
                <Option value="square" type="QString" name="cap_style" />
                <Option value="170,91,82,255" type="QString" name="color" />
                <Option value="1" type="QString" name="horizontal_anchor_point" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="circle" type="QString" name="name" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="0,0,0,255" type="QString" name="outline_color" />
                <Option value="no" type="QString" name="outline_style" />
                <Option value="0" type="QString" name="outline_width" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="diameter" type="QString" name="scale_method" />
                <Option value="1.6" type="QString" name="size" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
                <Option value="MM" type="QString" name="size_unit" />
                <Option value="1" type="QString" name="vertical_anchor_point" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name" />
                  <Option name="properties" />
                  <Option value="collection" type="QString" name="type" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine" id="{70a13038-4c7f-4678-b3ad-dcdc56881b60}">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale" />
            <Option value="MM" type="QString" name="average_angle_unit" />
            <Option value="6" type="QString" name="interval" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale" />
            <Option value="MM" type="QString" name="interval_unit" />
            <Option value="-1.6" type="QString" name="offset" />
            <Option value="2" type="QString" name="offset_along_line" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_along_line_unit" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="true" type="bool" name="place_on_every_part" />
            <Option value="Interval" type="QString" name="placements" />
            <Option value="0" type="QString" name="ring_filter" />
            <Option value="1" type="QString" name="rotate" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option name="properties" />
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="marker" name="@1@1" frame_rate="10">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name" />
                <Option name="properties" />
                <Option value="collection" type="QString" name="type" />
              </Option>
            </data_defined_properties>
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker" id="{2ee1037a-8932-4832-843d-8e7b749a992e}">
              <Option type="Map">
                <Option value="0" type="QString" name="angle" />
                <Option value="square" type="QString" name="cap_style" />
                <Option value="170,91,82,255" type="QString" name="color" />
                <Option value="1" type="QString" name="horizontal_anchor_point" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="circle" type="QString" name="name" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="0,0,0,255" type="QString" name="outline_color" />
                <Option value="no" type="QString" name="outline_style" />
                <Option value="0" type="QString" name="outline_width" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="diameter" type="QString" name="scale_method" />
                <Option value="1.8" type="QString" name="size" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
                <Option value="MM" type="QString" name="size_unit" />
                <Option value="1" type="QString" name="vertical_anchor_point" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name" />
                  <Option name="properties" />
                  <Option value="collection" type="QString" name="type" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="line" name="2" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine" id="{369b9603-7019-4234-9cc3-a908d66099d3}">
          <Option type="Map">
            <Option value="4" type="QString" name="average_angle_length" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="average_angle_map_unit_scale" />
            <Option value="MM" type="QString" name="average_angle_unit" />
            <Option value="3" type="QString" name="interval" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="interval_map_unit_scale" />
            <Option value="MM" type="QString" name="interval_unit" />
            <Option value="0" type="QString" name="offset" />
            <Option value="2" type="QString" name="offset_along_line" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_along_line_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_along_line_unit" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="true" type="bool" name="place_on_every_part" />
            <Option value="Interval" type="QString" name="placements" />
            <Option value="0" type="QString" name="ring_filter" />
            <Option value="1" type="QString" name="rotate" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option name="properties" />
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="marker" name="@2@0" frame_rate="10">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name" />
                <Option name="properties" />
                <Option value="collection" type="QString" name="type" />
              </Option>
            </data_defined_properties>
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker" id="{218c4d56-4d0c-42d2-a248-5d7abf137684}">
              <Option type="Map">
                <Option value="0" type="QString" name="angle" />
                <Option value="square" type="QString" name="cap_style" />
                <Option value="255,0,0,255" type="QString" name="color" />
                <Option value="1" type="QString" name="horizontal_anchor_point" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="line" type="QString" name="name" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="170,91,82,255" type="QString" name="outline_color" />
                <Option value="solid" type="QString" name="outline_style" />
                <Option value="0.6" type="QString" name="outline_width" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="diameter" type="QString" name="scale_method" />
                <Option value="1.4" type="QString" name="size" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
                <Option value="MM" type="QString" name="size_unit" />
                <Option value="1" type="QString" name="vertical_anchor_point" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name" />
                  <Option name="properties" />
                  <Option value="collection" type="QString" name="type" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" is_animated="0" type="line" name="3" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="0" enabled="1" class="SimpleLine" id="{ea5438f1-bd14-4f24-93a8-d88d60da9a65}">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern" />
            <Option value="square" type="QString" name="capstyle" />
            <Option value="5;2" type="QString" name="customdash" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale" />
            <Option value="MM" type="QString" name="customdash_unit" />
            <Option value="0" type="QString" name="dash_pattern_offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale" />
            <Option value="MM" type="QString" name="dash_pattern_offset_unit" />
            <Option value="0" type="QString" name="draw_inside_polygon" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="170,91,82,255" type="QString" name="line_color" />
            <Option value="dot" type="QString" name="line_style" />
            <Option value="0.26" type="QString" name="line_width" />
            <Option value="MM" type="QString" name="line_width_unit" />
            <Option value="0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="0" type="QString" name="ring_filter" />
            <Option value="0" type="QString" name="trim_distance_end" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale" />
            <Option value="MM" type="QString" name="trim_distance_end_unit" />
            <Option value="0" type="QString" name="trim_distance_start" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale" />
            <Option value="MM" type="QString" name="trim_distance_start_unit" />
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners" />
            <Option value="0" type="QString" name="use_custom_dash" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option name="properties" />
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  </qgis>