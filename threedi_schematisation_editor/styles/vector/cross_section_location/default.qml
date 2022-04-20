<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol type="marker" alpha="1" clip_to_extent="1" force_rhr="0" name="0">
        <layer pass="0" class="SimpleMarker" enabled="1" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="diamond"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 2,0.5)" type="QString" name="expression"/>
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
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reference_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_shape" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="2" type="QString" name="Circle"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="Egg"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="Rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="Tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="Tabulated trapezium"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_width" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="3" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_height" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="3" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_table" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="code" index="2" name=""/>
    <alias field="reference_level" index="3" name=""/>
    <alias field="friction_type" index="4" name=""/>
    <alias field="friction_value" index="5" name=""/>
    <alias field="bank_level" index="6" name=""/>
    <alias field="channel_id" index="7" name=""/>
    <alias field="cross_section_shape" index="8" name=""/>
    <alias field="cross_section_width" index="9" name=""/>
    <alias field="cross_section_height" index="10" name=""/>
    <alias field="cross_section_table" index="11" name=""/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="code" applyOnUpdate="0"/>
    <default expression="" field="reference_level" applyOnUpdate="0"/>
    <default expression="" field="friction_type" applyOnUpdate="0"/>
    <default expression="" field="friction_value" applyOnUpdate="0"/>
    <default expression="" field="bank_level" applyOnUpdate="0"/>
    <default expression="" field="channel_id" applyOnUpdate="0"/>
    <default expression="" field="cross_section_shape" applyOnUpdate="0"/>
    <default expression="" field="cross_section_width" applyOnUpdate="0"/>
    <default expression="" field="cross_section_height" applyOnUpdate="0"/>
    <default expression="" field="cross_section_table" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="fid" constraints="3" unique_strength="1" notnull_strength="1"/>
    <constraint exp_strength="0" field="id" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="code" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="reference_level" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="friction_type" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="friction_value" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="bank_level" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="channel_id" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_shape" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_width" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_height" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_table" constraints="0" unique_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="reference_level" desc="" exp=""/>
    <constraint field="friction_type" desc="" exp=""/>
    <constraint field="friction_value" desc="" exp=""/>
    <constraint field="bank_level" desc="" exp=""/>
    <constraint field="channel_id" desc="" exp=""/>
    <constraint field="cross_section_shape" desc="" exp=""/>
    <constraint field="cross_section_width" desc="" exp=""/>
    <constraint field="cross_section_height" desc="" exp=""/>
    <constraint field="cross_section_table" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_schematisation_editor\forms\ui\cross_section_location.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_schematisation_editor.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="Cross section location view">
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="General">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="reference_level"/>
        <attributeEditorField showLabel="1" index="6" name="bank_level"/>
        <attributeEditorField showLabel="1" index="4" name="friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="friction_value"/>
        <attributeEditorField showLabel="1" index="7" name="channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="Cross section">
        <attributeEditorField showLabel="1" index="8" name="cross_section_shape"/>
        <attributeEditorField showLabel="1" index="10" name="cross_section_height"/>
        <attributeEditorField showLabel="1" index="9" name="cross_section_width"/>
        <attributeEditorField showLabel="1" index="11" name="cross_section_table"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="0" name="Cross section definition_height"/>
    <field editable="0" name="Cross section definition_shape"/>
    <field editable="0" name="Cross section definition_width"/>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="1" name="cross_section_height"/>
    <field editable="1" name="cross_section_shape"/>
    <field editable="1" name="cross_section_table"/>
    <field editable="1" name="cross_section_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="reference_level"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="Cross section definition_height"/>
    <field labelOnTop="0" name="Cross section definition_shape"/>
    <field labelOnTop="0" name="Cross section definition_width"/>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="cross_section_height"/>
    <field labelOnTop="0" name="cross_section_shape"/>
    <field labelOnTop="0" name="cross_section_table"/>
    <field labelOnTop="0" name="cross_section_width"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="reference_level"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"fid"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
