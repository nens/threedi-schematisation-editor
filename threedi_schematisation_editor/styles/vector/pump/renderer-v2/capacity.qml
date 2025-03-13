<?xml version='1.0' encoding='utf-8'?>
<qgis><renderer-v2 type="RuleRenderer" enableorderby="0" referencescale="-1" forceraster="0" symbollevels="0">
    <rules key="{a754b3b6-32f1-4905-987a-48076fc6f5b1}">
      <rule label="&lt; 1 L/s" symbol="0" key="{7d756727-4730-4b29-9193-399a6997bb08}" filter="&quot;capacity&quot; &gt;= 0.000000 AND &quot;capacity&quot; &lt;= 1.000000" />
      <rule label="1 - 10 L/s" symbol="1" key="{4d53a218-ca07-42b3-b0af-98a3d3cdb434}" filter="&quot;capacity&quot; &gt; 1.000000 AND &quot;capacity&quot; &lt;= 10.000000" />
      <rule label="10 - 20 L/s" symbol="2" key="{73e00a94-1474-48a3-8466-26093d4ed33b}" filter="&quot;capacity&quot; &gt; 10.000000 AND &quot;capacity&quot; &lt;= 20.000000" />
      <rule label="20 - 50 L/s" symbol="3" key="{38274205-b52d-447c-ac86-9efbfb040ef4}" filter="&quot;capacity&quot; &gt; 20.000000 AND &quot;capacity&quot; &lt;= 50.000000" />
      <rule label="50 - 100 L/s" symbol="4" key="{be3eb17b-1327-4f75-be00-88b16cd5fbd2}" filter="&quot;capacity&quot; &gt; 50.000000 AND &quot;capacity&quot; &lt;= 100.000000" />
      <rule label="100 - 200 L/s" symbol="5" key="{c6526e69-9119-4950-b12c-9c197622c8d2}" filter="&quot;capacity&quot; &gt; 100.000000 AND &quot;capacity&quot; &lt;= 200.000000" />
      <rule label="200 - 500 L/s" symbol="6" key="{e587f070-4734-4646-ac47-e68febed9ffe}" filter="&quot;capacity&quot; &gt; 200.000000 AND &quot;capacity&quot; &lt;= 500.000000" />
      <rule label="500 - 1000 L/s" symbol="7" key="{708fb390-7ac9-4c58-b4d0-030a1e648e55}" filter="&quot;capacity&quot; &gt; 500.000000 AND &quot;capacity&quot; &lt;= 1000.000000" />
      <rule label="1000 - 2000 L/s" symbol="8" key="{db34dafa-0b03-4720-aa14-166bcae04b70}" filter="&quot;capacity&quot; &gt; 1000.000000 AND &quot;capacity&quot; &lt;= 2000.000000" />
      <rule label="&gt; 2000 L/s" symbol="9" key="{7c5ff552-6335-461a-8ad1-7167095c55f5}" filter="&quot;capacity&quot; &gt; 2000.000000 AND &quot;capacity&quot; &lt;= 999999999.000000" />
      <rule label="NULL (invalid)" symbol="10" key="{9220bb11-fdf2-451b-aed8-c6b86f2437e7}" filter="ELSE" />
    </rules>
    <symbols>
      <symbol type="marker" force_rhr="0" name="0" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{7d933e1f-3f84-4c69-858b-d68afc1d4169}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="0.5" />
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
      <symbol type="marker" force_rhr="0" name="1" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{3294aaaf-ae5b-4643-9b30-e2cafb1cda1b}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="1.2" />
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
      <symbol type="marker" force_rhr="0" name="10" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{5d421ee4-e9d8-49cf-839d-2eb11477e32d}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="255,213,181,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="255,35,35,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="3.3" />
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
      <symbol type="marker" force_rhr="0" name="2" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{0e62717e-fbe4-4a1d-8f94-4013e91e339d}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="1.9" />
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
      <symbol type="marker" force_rhr="0" name="3" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{1de763a2-556a-4e35-9263-02d7afbb70dd}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="2.6" />
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
      <symbol type="marker" force_rhr="0" name="4" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{985ed6be-5643-4cb0-90a3-cdf3a9fa9577}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="3.3" />
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
      <symbol type="marker" force_rhr="0" name="5" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{31c4888c-9cbf-488e-95ea-fad53ec9514a}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="4" />
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
      <symbol type="marker" force_rhr="0" name="6" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{d1ac680c-cffb-4d1c-bd2d-2600c41b417c}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="4.7" />
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
      <symbol type="marker" force_rhr="0" name="7" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{56c02f9a-c765-4b41-b509-0c29739a6317}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="5.4" />
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
      <symbol type="marker" force_rhr="0" name="8" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{90a54dc6-1326-49a6-9637-f53a15493c63}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="6.1" />
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
      <symbol type="marker" force_rhr="0" name="9" alpha="1" frame_rate="10" clip_to_extent="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value="" />
            <Option name="properties" />
            <Option type="QString" name="type" value="collection" />
          </Option>
        </data_defined_properties>
        <layer class="SimpleMarker" locked="0" pass="0" id="{579a1161-8fc0-460a-860c-3c9bd22a15f2}" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="0" />
            <Option type="QString" name="cap_style" value="square" />
            <Option type="QString" name="color" value="185,185,185,255" />
            <Option type="QString" name="horizontal_anchor_point" value="1" />
            <Option type="QString" name="joinstyle" value="bevel" />
            <Option type="QString" name="name" value="pentagon" />
            <Option type="QString" name="offset" value="0,0" />
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="offset_unit" value="MM" />
            <Option type="QString" name="outline_color" value="77,77,77,255" />
            <Option type="QString" name="outline_style" value="solid" />
            <Option type="QString" name="outline_width" value="0.6" />
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" />
            <Option type="QString" name="outline_width_unit" value="MM" />
            <Option type="QString" name="scale_method" value="diameter" />
            <Option type="QString" name="size" value="6.8" />
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
    </symbols>
  </renderer-v2>
  </qgis>