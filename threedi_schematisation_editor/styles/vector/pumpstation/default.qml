<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" styleCategories="LayerConfiguration|Symbology|Labeling|Forms" readOnly="0" version="3.16.3-Hannover">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" type="marker" force_rhr="0" name="0" alpha="1">
        <layer locked="0" enabled="1" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 4,3)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
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
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
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
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="4" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="4" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="upper_stop_level">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="4" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="4" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: pump reacts only on suction side"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: pump reacts only on delivery side"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" type="QString" name="CheckedState"/>
            <Option value="" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="-1" type="QString" name="-1"/>
              </Option>
              <Option type="Map">
                <Option value="0" type="QString" name="0"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <editform tolerant="1">.</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_schematisation_editor.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer showLabel="1" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" name="Pumpstation point view">
      <attributeEditorContainer showLabel="1" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="General">
        <attributeEditorField showLabel="1" index="-1" name="id"/>
        <attributeEditorField showLabel="1" index="3" name="display_name"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="4" name="start_level"/>
        <attributeEditorField showLabel="1" index="5" name="lower_stop_level"/>
        <attributeEditorField showLabel="1" index="6" name="upper_stop_level"/>
        <attributeEditorField showLabel="1" index="7" name="capacity"/>
        <attributeEditorField showLabel="1" index="8" name="type"/>
        <attributeEditorField showLabel="1" index="-1" name="storage_area"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Visualization">
        <attributeEditorField showLabel="1" index="9" name="sewerage"/>
        <attributeEditorField showLabel="1" index="10" name="zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="11" name="connection_node_id"/>
        <attributeEditorField showLabel="1" index="-1" name="connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="-1" name="connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="capacity"/>
    <field editable="1" name="classification"/>
    <field editable="1" name="code"/>
    <field editable="0" name="connection_node_end_id"/>
    <field editable="0" name="connection_node_id"/>
    <field editable="0" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="lower_stop_level"/>
    <field editable="1" name="id"/>
    <field editable="1" name="sewerage"/>
    <field editable="1" name="start_level"/>
    <field editable="1" name="storage_area"/>
    <field editable="1" name="type"/>
    <field editable="1" name="upper_stop_level"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="capacity"/>
    <field labelOnTop="0" name="classification"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="lower_stop_level"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="sewerage"/>
    <field labelOnTop="0" name="start_level"/>
    <field labelOnTop="0" name="storage_area"/>
    <field labelOnTop="0" name="type"/>
    <field labelOnTop="0" name="upper_stop_level"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
