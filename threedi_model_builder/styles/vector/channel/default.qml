<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" readOnly="0" version="3.16.9-Hannover">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" type="line" alpha="1" force_rhr="0" name="0">
        <layer class="SimpleLine" locked="0" pass="0" enabled="1">
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
          <prop v="5,77,209,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 0.66,0.3)" type="QString" name="expression"/>
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
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id">
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
    <field configurationFlags="None" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="100" type="QString" name="100: embedded"/>
              </Option>
              <Option type="Map">
                <Option value="101" type="QString" name="101: isolated"/>
              </Option>
              <Option type="Map">
                <Option value="102" type="QString" name="102: connected"/>
              </Option>
              <Option type="Map">
                <Option value="105" type="QString" name="105: double connected"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="zoom_category">
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
    <field configurationFlags="None" name="connection_node_start_id">
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
    <field configurationFlags="None" name="connection_node_end_id">
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
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="fid" name=""/>
    <alias index="1" field="id" name=""/>
    <alias index="2" field="code" name=""/>
    <alias index="3" field="display_name" name=""/>
    <alias index="4" field="calculation_type" name=""/>
    <alias index="5" field="dist_calc_points" name=""/>
    <alias index="6" field="zoom_category" name=""/>
    <alias index="7" field="connection_node_start_id" name=""/>
    <alias index="8" field="connection_node_end_id" name=""/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="'new'" field="code" applyOnUpdate="0"/>
    <default expression="'new'" field="display_name" applyOnUpdate="0"/>
    <default expression="" field="calculation_type" applyOnUpdate="0"/>
    <default expression="" field="dist_calc_points" applyOnUpdate="0"/>
    <default expression="5" field="zoom_category" applyOnUpdate="0"/>
    <default expression="" field="connection_node_start_id" applyOnUpdate="0"/>
    <default expression="" field="connection_node_end_id" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="3" field="fid" notnull_strength="1" unique_strength="1"/>
    <constraint exp_strength="0" constraints="3" field="id" notnull_strength="1" unique_strength="1"/>
    <constraint exp_strength="0" constraints="1" field="code" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" constraints="1" field="display_name" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" constraints="1" field="calculation_type" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" constraints="1" field="dist_calc_points" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="zoom_category" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="connection_node_start_id" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="connection_node_end_id" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="code"/>
    <constraint desc="" exp="" field="display_name"/>
    <constraint desc="" exp="" field="calculation_type"/>
    <constraint desc="" exp="" field="dist_calc_points"/>
    <constraint desc="" exp="" field="zoom_category"/>
    <constraint desc="" exp="" field="connection_node_start_id"/>
    <constraint desc="" exp="" field="connection_node_end_id"/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\channel.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>../../../OSGEO4~1/bin</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer columnCount="1" visibilityExpressionEnabled="0" groupBox="0" showLabel="1" name="Channel" visibilityExpression="">
      <attributeEditorContainer columnCount="1" visibilityExpressionEnabled="0" groupBox="1" showLabel="1" name="General" visibilityExpression="">
        <attributeEditorField index="1" showLabel="1" name="id"/>
        <attributeEditorField index="3" showLabel="1" name="display_name"/>
        <attributeEditorField index="2" showLabel="1" name="code"/>
        <attributeEditorField index="4" showLabel="1" name="calculation_type"/>
        <attributeEditorField index="5" showLabel="1" name="dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpressionEnabled="0" groupBox="1" showLabel="1" name="Visualization" visibilityExpression="">
        <attributeEditorField index="6" showLabel="1" name="zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpressionEnabled="0" groupBox="1" showLabel="1" name="Connection nodes" visibilityExpression="">
        <attributeEditorField index="7" showLabel="1" name="connection_node_start_id"/>
        <attributeEditorField index="8" showLabel="1" name="connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="0" name="connection_node_end_id"/>
    <field editable="0" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="fid"/>
    <field editable="0" name="id"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <layerGeometryType>1</layerGeometryType>
</qgis>
