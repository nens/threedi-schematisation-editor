<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" readOnly="0" version="3.16.3-Hannover" styleCategories="LayerConfiguration|Symbology|Labeling|Forms">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol clip_to_extent="1" alpha="1" name="0" force_rhr="0" type="line">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
          <prop v="101,101,101,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.66" k="line_width"/>
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
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(cul_discharge_coefficient_positive, 0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.6667*$length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@1" force_rhr="0" type="marker">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
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
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(cul_discharge_coefficient_negative,0) > 0&#xd;&#xa;AND coalesce(cul_discharge_coefficient_positive,0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.3333*$length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@2" force_rhr="0" type="marker">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
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
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="COALESCE(cul_discharge_coefficient_negative, 0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.3333*$length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@3" force_rhr="0" type="marker">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
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
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="COALESCE(cul_discharge_coefficient_positive, 0) > 0&#xd;&#xa;AND COALESCE(cul_discharge_coefficient_negative) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.66667*$length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@4" force_rhr="0" type="marker">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
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
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MM" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@5" force_rhr="0" type="marker">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="101,101,101,255" k="color"/>
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
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
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
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="2147483647" name="Max" type="int"/>
            <Option value="-2147483648" name="Min" type="int"/>
            <Option value="0" name="Precision" type="int"/>
            <Option value="1" name="Step" type="int"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="invert_level_start_point">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="invert_level_end_point">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="discharge_coefficient_positive">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="discharge_coefficient_negative">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="1.7976931348623157e+308" name="Max" type="double"/>
            <Option value="-1.7976931348623157e+308" name="Min" type="double"/>
            <Option value="4" name="Precision" type="int"/>
            <Option value="1" name="Step" type="double"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="2147483647" name="Max" type="int"/>
            <Option value="-2147483648" name="Min" type="int"/>
            <Option value="0" name="Precision" type="int"/>
            <Option value="1" name="Step" type="int"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
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
    <field name="cross_section_definition_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\culvert.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="" name="Culvert view" showLabel="1" visibilityExpressionEnabled="0">
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpression="" name="General" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField name="cul_id" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_display_name" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_code" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_calculation_type" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_dist_calc_points" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpression="" name="Characteristics" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField name="cul_invert_level_start_point" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_invert_level_end_point" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_friction_type" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_friction_value" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_discharge_coefficient_positive" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_discharge_coefficient_negative" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpression="" name="Cross section definition" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField name="cul_cross_section_definition_id" showLabel="1" index="-1"/>
        <attributeEditorField name="def_code" showLabel="1" index="-1"/>
        <attributeEditorField name="def_shape" showLabel="1" index="-1"/>
        <attributeEditorField name="def_width" showLabel="1" index="-1"/>
        <attributeEditorField name="def_height" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpression="" name="Visualization" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField name="cul_zoom_category" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpression="" name="Connection nodes" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField name="cul_connection_node_start_id" showLabel="1" index="-1"/>
        <attributeEditorField name="cul_connection_node_end_id" showLabel="1" index="-1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="calculation_type" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_end_id" editable="1"/>
    <field name="connection_node_start_id" editable="1"/>
    <field name="cross_section_definition_id" editable="1"/>
    <field name="cul_calculation_type" editable="1"/>
    <field name="cul_code" editable="1"/>
    <field name="cul_connection_node_end_id" editable="0"/>
    <field name="cul_connection_node_start_id" editable="0"/>
    <field name="cul_cross_section_definition_id" editable="1"/>
    <field name="cul_discharge_coefficient_negative" editable="1"/>
    <field name="cul_discharge_coefficient_positive" editable="1"/>
    <field name="cul_display_name" editable="1"/>
    <field name="cul_dist_calc_points" editable="1"/>
    <field name="cul_friction_type" editable="1"/>
    <field name="cul_friction_value" editable="1"/>
    <field name="cul_id" editable="1"/>
    <field name="cul_invert_level_end_point" editable="1"/>
    <field name="cul_invert_level_start_point" editable="1"/>
    <field name="cul_zoom_category" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="0"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="discharge_coefficient_negative" editable="1"/>
    <field name="discharge_coefficient_positive" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="dist_calc_points" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="friction_type" editable="1"/>
    <field name="friction_value" editable="1"/>
    <field name="id" editable="1"/>
    <field name="invert_level_end_point" editable="1"/>
    <field name="invert_level_start_point" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="cross_section_definition_id"/>
    <field labelOnTop="0" name="cul_calculation_type"/>
    <field labelOnTop="0" name="cul_code"/>
    <field labelOnTop="0" name="cul_connection_node_end_id"/>
    <field labelOnTop="0" name="cul_connection_node_start_id"/>
    <field labelOnTop="0" name="cul_cross_section_definition_id"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="cul_display_name"/>
    <field labelOnTop="0" name="cul_dist_calc_points"/>
    <field labelOnTop="0" name="cul_friction_type"/>
    <field labelOnTop="0" name="cul_friction_value"/>
    <field labelOnTop="0" name="cul_id"/>
    <field labelOnTop="0" name="cul_invert_level_end_point"/>
    <field labelOnTop="0" name="cul_invert_level_start_point"/>
    <field labelOnTop="0" name="cul_zoom_category"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="discharge_coefficient_negative"/>
    <field labelOnTop="0" name="discharge_coefficient_positive"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="invert_level_end_point"/>
    <field labelOnTop="0" name="invert_level_start_point"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <layerGeometryType>1</layerGeometryType>
</qgis>
