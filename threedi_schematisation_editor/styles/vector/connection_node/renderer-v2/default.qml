<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 referencescale="-1" forceraster="0" symbollevels="0" enableorderby="0" type="RuleRenderer">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule filter=" &quot;visualisation&quot; = -1" symbol="0" key="{e471b7e3-40dc-47f7-9585-dc29adb086ed}" label="Connection node" />
      <rule filter="visualisation = 0" symbol="1" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" scalemaxdenom="5000" label="Manhole" />
      <rule filter=" &quot;visualisation&quot; = 3" symbol="2" key="{e566bc63-cb1c-4211-87bd-f88971394bc8}" label="Infiltration manhole" />
      <rule filter="visualisation = 4" symbol="3" key="{7a87fed8-6e71-442f-b0a3-9c2f6704bdc4}" label="Gully" />
      <rule filter="visualisation = 1" symbol="4" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" scalemaxdenom="15000" label="Outlet" />
      <rule filter="visualisation = 2" symbol="5" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" label="Pump chamber" />
      <rule filter="ELSE" symbol="6" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}" scalemaxdenom="5000" label="Other" />
    </rules>
    <symbols>
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{ec807e83-b8aa-4a25-af71-34881bb131ab}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="255,255,255,255" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="circle" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="0,0,0,255" type="QString" name="outline_color" />
            <Option value="solid" type="QString" name="outline_style" />
            <Option value="0" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="1.2" type="QString" name="size" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
            <Option value="MM" type="QString" name="size_unit" />
            <Option value="1" type="QString" name="vertical_anchor_point" />
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active" />
                  <Option value="if(@map_scale&lt;10000, 1.2,0.7)" type="QString" name="expression" />
                  <Option value="3" type="int" name="type" />
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="1">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{4122d25e-458d-418d-9377-f928e4ca5723}" class="FilledMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="255,255,255,255" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="square_with_corners" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="2" type="QString" name="size" />
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
          <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="fill" name="@1@0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name" />
                <Option name="properties" />
                <Option value="collection" type="QString" name="type" />
              </Option>
            </data_defined_properties>
            <layer id="{4cf9ae9a-90f7-4c8e-944e-2d608e75ffa8}" class="SimpleFill" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale" />
                <Option value="255,255,255,255" type="QString" name="color" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="35,35,35,255" type="QString" name="outline_color" />
                <Option value="solid" type="QString" name="outline_style" />
                <Option value="0" type="QString" name="outline_width" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="solid" type="QString" name="style" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name" />
                  <Option name="properties" />
                  <Option value="collection" type="QString" name="type" />
                </Option>
              </data_defined_properties>
            </layer>
            <layer id="{df9e69c7-edba-4012-861d-c4fde476e62e}" class="SimpleFill" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale" />
                <Option value="7,7,7,255" type="QString" name="color" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="0,0,0,255" type="QString" name="outline_color" />
                <Option value="solid" type="QString" name="outline_style" />
                <Option value="0" type="QString" name="outline_width" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="dense5" type="QString" name="style" />
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
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="2">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{c18385b9-03ba-4400-84b6-c1bc0e12742c}" class="FilledMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="255,255,255,255" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="square_with_corners" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="2" type="QString" name="size" />
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
          <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="fill" name="@2@0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name" />
                <Option name="properties" />
                <Option value="collection" type="QString" name="type" />
              </Option>
            </data_defined_properties>
            <layer id="{ac626486-ba1f-40d2-9813-d9c6988b29c6}" class="SimpleFill" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale" />
                <Option value="255,255,255,255" type="QString" name="color" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="35,35,35,255" type="QString" name="outline_color" />
                <Option value="no" type="QString" name="outline_style" />
                <Option value="0.26" type="QString" name="outline_width" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="solid" type="QString" name="style" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name" />
                  <Option name="properties" />
                  <Option value="collection" type="QString" name="type" />
                </Option>
              </data_defined_properties>
            </layer>
            <layer id="{050c041c-51c1-4c34-9829-6447a5e8e67a}" class="SimpleFill" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale" />
                <Option value="31,120,180,255" type="QString" name="color" />
                <Option value="bevel" type="QString" name="joinstyle" />
                <Option value="0,0" type="QString" name="offset" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="31,120,180,255" type="QString" name="outline_color" />
                <Option value="solid" type="QString" name="outline_style" />
                <Option value="0.2" type="QString" name="outline_width" />
                <Option value="MM" type="QString" name="outline_width_unit" />
                <Option value="dense5" type="QString" name="style" />
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
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="3">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{38f13dd4-c971-488d-a109-78bec16bfc7e}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="113,113,113,255" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="trapezoid" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="0,0,0,255" type="QString" name="outline_color" />
            <Option value="solid" type="QString" name="outline_style" />
            <Option value="0" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="2.8" type="QString" name="size" />
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
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="4">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{bd980f15-cffc-4c8f-9918-e342da825619}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="63,128,192,255" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="miter" type="QString" name="joinstyle" />
            <Option value="square" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="85,170,255,255" type="QString" name="outline_color" />
            <Option value="solid" type="QString" name="outline_style" />
            <Option value="0.75" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="2.5" type="QString" name="size" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
            <Option value="MM" type="QString" name="size_unit" />
            <Option value="1" type="QString" name="vertical_anchor_point" />
          </Option>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="0.5" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="0.2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="outerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
            <effect type="drawSource">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active" />
                  <Option value="if(@map_scale&lt;10000, 2.5,1.5)" type="QString" name="expression" />
                  <Option value="3" type="int" name="type" />
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="5">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{61bbe8ca-6508-477a-bb54-44dcdf415a6d}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="85,255,127,0" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="pentagon" type="QString" name="name" />
            <Option value="0.10000000000000001,0.10000000000000001" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="0,0,0,183" type="QString" name="outline_color" />
            <Option value="solid" type="QString" name="outline_style" />
            <Option value="0.7" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="4.1" type="QString" name="size" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
            <Option value="MM" type="QString" name="size_unit" />
            <Option value="1" type="QString" name="vertical_anchor_point" />
          </Option>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="0.5" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="0.2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="outerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
            <effect type="drawSource">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active" />
                  <Option value="if(@map_scale&lt;10000, 4.1,3.1)" type="QString" name="expression" />
                  <Option value="3" type="int" name="type" />
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
        <layer id="{e2cbe16c-b060-42a8-8a53-6e55851589d4}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="85,255,127,0" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="pentagon" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="255,127,0,255" type="QString" name="outline_color" />
            <Option value="solid" type="QString" name="outline_style" />
            <Option value="0.7" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="4" type="QString" name="size" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale" />
            <Option value="MM" type="QString" name="size_unit" />
            <Option value="1" type="QString" name="vertical_anchor_point" />
          </Option>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="0.5" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="0.2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="outerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
            <effect type="drawSource">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="1" type="QString" name="enabled" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerShadow">
              <Option type="Map">
                <Option value="13" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,0,255" type="QString" name="color" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="135" type="QString" name="offset_angle" />
                <Option value="2" type="QString" name="offset_distance" />
                <Option value="MM" type="QString" name="offset_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_unit_scale" />
                <Option value="1" type="QString" name="opacity" />
              </Option>
            </effect>
            <effect type="innerGlow">
              <Option type="Map">
                <Option value="0" type="QString" name="blend_mode" />
                <Option value="2.645" type="QString" name="blur_level" />
                <Option value="MM" type="QString" name="blur_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="blur_unit_scale" />
                <Option value="0,0,255,255" type="QString" name="color1" />
                <Option value="0,255,0,255" type="QString" name="color2" />
                <Option value="0" type="QString" name="color_type" />
                <Option value="ccw" type="QString" name="direction" />
                <Option value="0" type="QString" name="discrete" />
                <Option value="2" type="QString" name="draw_mode" />
                <Option value="0" type="QString" name="enabled" />
                <Option value="0.5" type="QString" name="opacity" />
                <Option value="gradient" type="QString" name="rampType" />
                <Option value="255,255,255,255" type="QString" name="single_color" />
                <Option value="rgb" type="QString" name="spec" />
                <Option value="2" type="QString" name="spread" />
                <Option value="MM" type="QString" name="spread_unit" />
                <Option value="3x:0,0,0,0,0,0" type="QString" name="spread_unit_scale" />
              </Option>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name" />
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active" />
                  <Option value="if(@map_scale&lt;10000, 4,3)" type="QString" name="expression" />
                  <Option value="3" type="int" name="type" />
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type" />
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol frame_rate="10" clip_to_extent="1" alpha="1" force_rhr="0" is_animated="0" type="marker" name="6">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name" />
            <Option name="properties" />
            <Option value="collection" type="QString" name="type" />
          </Option>
        </data_defined_properties>
        <layer id="{422d8fea-c0ae-4c75-8117-3d1ad28885b2}" class="SimpleMarker" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option value="0" type="QString" name="angle" />
            <Option value="square" type="QString" name="cap_style" />
            <Option value="85,255,127,0" type="QString" name="color" />
            <Option value="1" type="QString" name="horizontal_anchor_point" />
            <Option value="bevel" type="QString" name="joinstyle" />
            <Option value="square" type="QString" name="name" />
            <Option value="0,0" type="QString" name="offset" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale" />
            <Option value="MM" type="QString" name="offset_unit" />
            <Option value="255,9,1,255" type="QString" name="outline_color" />
            <Option value="dot" type="QString" name="outline_style" />
            <Option value="0.25" type="QString" name="outline_width" />
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale" />
            <Option value="MM" type="QString" name="outline_width_unit" />
            <Option value="diameter" type="QString" name="scale_method" />
            <Option value="2" type="QString" name="size" />
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
    </symbols>
  </renderer-v2>
  </qgis>