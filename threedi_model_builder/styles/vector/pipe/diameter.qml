<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Labeling|Forms|MapTips" version="3.16.9-Hannover" labelsEnabled="1">
  <renderer-v2 enableorderby="0" symbollevels="0" type="categorizedSymbol" forceraster="0" attr="sewerage_type">
    <categories>
      <category value="0" render="true" symbol="0" label="Combined sewer"/>
      <category value="1" render="true" symbol="1" label="Storm drain"/>
      <category value="2" render="true" symbol="2" label="Sanitary sewer"/>
      <category value="3" render="true" symbol="3" label="Transport"/>
      <category value="" render="true" symbol="4" label="Other"/>
    </categories>
    <symbols>
      <symbol clip_to_extent="1" name="0" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="1" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="2" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="3" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="4" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" name="0" type="line" alpha="1" force_rhr="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineStyle" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 1 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 2 then to_real(&quot;cross_section_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape = 3 then (to_real(&quot;cross_section_width&quot;) + to_real(&quot;cross_section_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when cross_section_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(cross_section_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{a59aab93-485b-46fb-bfeb-83aac4af7cc2}">
      <rule scalemaxdenom="5000" description="Crosssection" key="{1e7f1486-e64b-4a35-8a07-9d4f4d85a927}">
        <settings calloutType="simple">
          <text-style fontFamily="MS Gothic" fontLetterSpacing="0" blendMode="0" textOpacity="1" fontWeight="50" fontWordSpacing="0" isExpression="1" fontKerning="1" fontSizeUnit="Point" fontUnderline="0" textColor="0,0,0,255" fieldName="CASE WHEN cross_section_shape = 1 THEN 'rect '||round(cross_section_width*1000)||'x'||round(cross_section_height*1000) &#xd;&#xa;WHEN cross_section_shape = 2 THEN 'Ø'||round(cross_section_width*1000) &#xd;&#xa;WHEN cross_section_shape = 3 THEN 'egg ' || round(cross_section_width*1000) || '/' || round(cross_section_width*1000*1.5,3) &#xd;&#xa;WHEN cross_section_shape in (5, 6) THEN &#xd;&#xa;&#x9;'tab ' ||&#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(cross_section_width, ' ')))*1000) ||&#xd;&#xa;&#x9;'/' || &#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(cross_section_height, ' ')))*1000)&#xd;&#xa;END " fontItalic="0" fontStrikeout="0" fontSize="7" allowHtml="0" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textOrientation="horizontal" capitalization="0" multilineHeight="1" previewBkgrdColor="255,255,255,255" namedStyle="Regular">
            <text-buffer bufferBlendMode="0" bufferDraw="1" bufferNoFill="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferSize="0.7" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferSizeUnits="MM"/>
            <text-mask maskType="0" maskSize="0" maskOpacity="1" maskSizeUnits="MM" maskEnabled="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskJoinStyle="128"/>
            <background shapeBorderColor="128,128,128,255" shapeJoinStyle="64" shapeRotation="0" shapeOffsetUnit="MM" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeRotationType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeRadiiUnit="MM" shapeOffsetX="0" shapeBorderWidth="0" shapeOpacity="1" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeBlendMode="0" shapeSVGFile="" shapeDraw="0" shapeSizeX="0" shapeSizeType="0" shapeSizeUnit="MM" shapeType="0" shapeSizeY="0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0">
              <symbol clip_to_extent="1" name="markerSymbol" type="marker" alpha="1" force_rhr="0">
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <prop v="0" k="angle"/>
                  <prop v="133,182,111,255" k="color"/>
                  <prop v="1" k="horizontal_anchor_point"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="circle" k="name"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="35,35,35,255" k="outline_color"/>
                  <prop v="solid" k="outline_style"/>
                  <prop v="0" k="outline_width"/>
                  <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="diameter" k="scale_method"/>
                  <prop v="2" k="size"/>
                  <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
                  <prop v="MM" k="size_unit"/>
                  <prop v="1" k="vertical_anchor_point"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowRadiusAlphaOnly="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowDraw="0" shadowBlendMode="6" shadowUnder="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowRadius="1.5" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowScale="100"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format leftDirectionSymbol="&lt;" rightDirectionSymbol=">" placeDirectionSymbol="0" addDirectionSymbol="0" formatNumbers="0" multilineAlign="0" autoWrapLength="0" decimals="3" plussign="0" wrapChar="" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0"/>
          <placement centroidInside="0" xOffset="0" maxCurvedCharAngleIn="25" maxCurvedCharAngleOut="-25" repeatDistance="0" overrunDistanceUnit="MM" repeatDistanceUnits="MM" geometryGenerator="" priority="5" overrunDistance="0" rotationAngle="0" geometryGeneratorType="PointGeometry" dist="0" placementFlags="9" placement="2" centroidWhole="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" geometryGeneratorEnabled="0" layerType="LineGeometry" preserveRotation="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetType="0" fitInPolygonOnly="0" quadOffset="4" distUnits="MM" lineAnchorType="0" polygonPlacementFlags="2" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MapUnit" distMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering scaleMax="10000000" mergeLines="0" maxNumLabels="2000" limitNumLabels="0" scaleMin="1" obstacleType="0" obstacleFactor="1" upsidedownLabels="0" scaleVisibility="0" fontLimitPixelSize="0" fontMaxPixelSize="10000" fontMinPixelSize="3" displayAll="0" drawLabels="1" labelPerPart="0" obstacle="1" zIndex="0" minFeatureSize="0"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="Color" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="case &#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
              <Option value="false" name="drawToAllParts" type="bool"/>
              <Option value="0" name="enabled" type="QString"/>
              <Option value="point_on_exterior" name="labelAnchorPoint" type="QString"/>
              <Option value="&lt;symbol clip_to_extent=&quot;1&quot; name=&quot;symbol&quot; type=&quot;line&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
              <Option value="0" name="minLength" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString"/>
              <Option value="MM" name="minLengthUnit" type="QString"/>
              <Option value="0" name="offsetFromAnchor" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString"/>
              <Option value="MM" name="offsetFromAnchorUnit" type="QString"/>
              <Option value="0" name="offsetFromLabel" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString"/>
              <Option value="MM" name="offsetFromLabelUnit" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="calculation_type">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="friction_type">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="material">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_quality">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sewerage_type">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="profile_num">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="original_length">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_start_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\pipe.ui</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Formulieren van QGIS mogen een functie van Python hebben die wordt aangeroepen wanneer het formulier wordt geopend.

Gebruik deze functie om extra logica aan uw formulieren toe te voegen.

Voer de naam van de functie in in het veld "Python Init functie".
Een voorbeeld volgt:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer visibilityExpression="" name="Pipe view" columnCount="1" groupBox="0" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorContainer visibilityExpression="" name="General" columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="id" showLabel="1" index="-1"/>
        <attributeEditorField name="display_name" showLabel="1" index="-1"/>
        <attributeEditorField name="code" showLabel="1" index="-1"/>
        <attributeEditorField name="calculation_type" showLabel="1" index="-1"/>
        <attributeEditorField name="dist_calc_points" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Characteristics" columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="invert_level_start_point" showLabel="1" index="-1"/>
        <attributeEditorField name="invert_level_end_point" showLabel="1" index="-1"/>
        <attributeEditorField name="friction_value" showLabel="1" index="-1"/>
        <attributeEditorField name="friction_type" showLabel="1" index="-1"/>
        <attributeEditorField name="material" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Cross section definition" columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="cross_section_shape" showLabel="1" index="-1"/>
        <attributeEditorField name="cross_section_width" showLabel="1" index="-1"/>
        <attributeEditorField name="cross_section_height" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Visualization" columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="sewerage_type" showLabel="1" index="-1"/>
        <attributeEditorField name="zoom_category" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Connection nodes" columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="connection_node_start_id" showLabel="1" index="-1"/>
        <attributeEditorField name="connection_node_end_id" showLabel="1" index="-1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_end_id"/>
    <field editable="1" name="connection_node_start_id"/>
    <field editable="1" name="cross_section_height"/>
    <field editable="1" name="cross_section_shape"/>
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
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="0" name="connection_node_end_id"/>
    <field editable="0" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="invert_level_end_point"/>
    <field editable="1" name="invert_level_start_point"/>
    <field editable="1" name="material"/>
    <field editable="1" name="original_length"/>
    <field editable="1" name="pipe_quality"/>
    <field editable="1" name="profile_num"/>
    <field editable="1" name="quality"/>
    <field editable="1" name="sewerage_type"/>
    <field editable="1" name="zoom_category"/>
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
    <field name="calculation_type" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dist_calc_points" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="invert_level_end_point" labelOnTop="0"/>
    <field name="invert_level_start_point" labelOnTop="0"/>
    <field name="material" labelOnTop="0"/>
    <field name="original_length" labelOnTop="0"/>
    <field name="pipe_quality" labelOnTop="0"/>
    <field name="profile_num" labelOnTop="0"/>
    <field name="quality" labelOnTop="0"/>
    <field name="sewerage_type" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
    <field name="profile_num" labelOnTop="0"/>
    <field name="sewerage_type" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
