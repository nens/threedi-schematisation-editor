<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0" version="3.16.3-Hannover" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" force_rhr="0" type="line">
        <layer locked="0" pass="0" class="SimpleLine" enabled="1">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="5,77,209,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if(@map_scale&lt;10000, 0.66,0.3)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
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
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="calculation_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="100: embedded" value="100" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="101: isolated" value="101" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="102: connected" value="102" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="105: double connected" value="105" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="-1" value="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="0" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5" value="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_start_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="code" index="2"/>
    <alias name="" field="display_name" index="3"/>
    <alias name="" field="calculation_type" index="4"/>
    <alias name="" field="dist_calc_points" index="5"/>
    <alias name="" field="zoom_category" index="6"/>
    <alias name="" field="connection_node_start_id" index="7"/>
    <alias name="" field="connection_node_end_id" index="8"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="code" expression="'new'" applyOnUpdate="0"/>
    <default field="display_name" expression="'new'" applyOnUpdate="0"/>
    <default field="calculation_type" expression="" applyOnUpdate="0"/>
    <default field="dist_calc_points" expression="" applyOnUpdate="0"/>
    <default field="zoom_category" expression="5" applyOnUpdate="0"/>
    <default field="connection_node_start_id" expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent))))" applyOnUpdate="0"/>
    <default field="connection_node_end_id" expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent))))" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="code" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="display_name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="calculation_type" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="dist_calc_points" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="zoom_category" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="connection_node_start_id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="connection_node_end_id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="display_name" desc="" exp=""/>
    <constraint field="calculation_type" desc="" exp=""/>
    <constraint field="dist_calc_points" desc="" exp=""/>
    <constraint field="zoom_category" desc="" exp=""/>
    <constraint field="connection_node_start_id" desc="" exp=""/>
    <constraint field="connection_node_end_id" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1">../../../OSGEO4~1/bin</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>../../../OSGEO4~1/bin</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Channel" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorContainer name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="id" index="1" showLabel="1"/>
        <attributeEditorField name="display_name" index="3" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
        <attributeEditorField name="calculation_type" index="4" showLabel="1"/>
        <attributeEditorField name="dist_calc_points" index="5" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="zoom_category" index="6" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Connection nodes" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="connection_node_start_id" index="7" showLabel="1"/>
        <attributeEditorField name="connection_node_end_id" index="8" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="calculation_type" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_end_id" editable="1"/>
    <field name="connection_node_start_id" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="dist_calc_points" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="calculation_type" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dist_calc_points" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <layerGeometryType>1</layerGeometryType>
</qgis>
