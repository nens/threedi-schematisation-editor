<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="0" version="3.16.3-Hannover" readOnly="0" hasScaleBasedVisibilityFlag="0" maxScale="0" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal enabled="0" accumulate="0" startField="" fixedDuration="0" mode="0" startExpression="" durationUnit="min" endField="" endExpression="" durationField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
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
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cfl_strictness_factor_1d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cfl_strictness_factor_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="convergence_cg" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="convergence_eps" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flow_direction_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_shallow_water_correction" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="general_numerical_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="integration_method" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="limiter_grad_1d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="limiter_grad_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="limiter_slope_crossectional_area_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="limiter_slope_friction_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_nonlin_iterations" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_degree" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="5" type="QString" name="5: for surface 2D flow only"/>
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: for 1D and 2D flow"/>
              </Option>
              <Option type="Map">
                <Option value="70" type="QString" name="70: for surface 1D, 2D surface and groundwater flow or higher"/>
              </Option>
              <Option type="Map">
                <Option value="700" type="QString" name="700: for 1D flow"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minimum_friction_velocity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minimum_surface_area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="precon_cg" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="preissmann_slot" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pump_implicit_ratio" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="thin_water_layer_definition" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_of_cg" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_of_nested_newton" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: When the schematisation does not include 1D-elements with closed cross-sections"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: When the schematisation includes 1D-elements with closed cross-sections"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="cfl_strictness_factor_1d" index="2" name=""/>
    <alias field="cfl_strictness_factor_2d" index="3" name=""/>
    <alias field="convergence_cg" index="4" name=""/>
    <alias field="convergence_eps" index="5" name=""/>
    <alias field="flow_direction_threshold" index="6" name=""/>
    <alias field="frict_shallow_water_correction" index="7" name=""/>
    <alias field="general_numerical_threshold" index="8" name=""/>
    <alias field="integration_method" index="9" name=""/>
    <alias field="limiter_grad_1d" index="10" name=""/>
    <alias field="limiter_grad_2d" index="11" name=""/>
    <alias field="limiter_slope_crossectional_area_2d" index="12" name=""/>
    <alias field="limiter_slope_friction_2d" index="13" name=""/>
    <alias field="max_nonlin_iterations" index="14" name=""/>
    <alias field="max_degree" index="15" name=""/>
    <alias field="minimum_friction_velocity" index="16" name=""/>
    <alias field="minimum_surface_area" index="17" name=""/>
    <alias field="precon_cg" index="18" name=""/>
    <alias field="preissmann_slot" index="19" name=""/>
    <alias field="pump_implicit_ratio" index="20" name=""/>
    <alias field="thin_water_layer_definition" index="21" name=""/>
    <alias field="use_of_cg" index="22" name=""/>
    <alias field="use_of_nested_newton" index="23" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression=" if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="1" applyOnUpdate="0" field="cfl_strictness_factor_1d"/>
    <default expression="1" applyOnUpdate="0" field="cfl_strictness_factor_2d"/>
    <default expression="0.000000001" applyOnUpdate="0" field="convergence_cg"/>
    <default expression="0.00001" applyOnUpdate="0" field="convergence_eps"/>
    <default expression="0.000001" applyOnUpdate="0" field="flow_direction_threshold"/>
    <default expression="0" applyOnUpdate="0" field="frict_shallow_water_correction"/>
    <default expression="0.00000001" applyOnUpdate="0" field="general_numerical_threshold"/>
    <default expression="0" applyOnUpdate="0" field="integration_method"/>
    <default expression="1" applyOnUpdate="0" field="limiter_grad_1d"/>
    <default expression="0" applyOnUpdate="0" field="limiter_grad_2d"/>
    <default expression="0" applyOnUpdate="0" field="limiter_slope_crossectional_area_2d"/>
    <default expression="0" applyOnUpdate="0" field="limiter_slope_friction_2d"/>
    <default expression="20" applyOnUpdate="0" field="max_nonlin_iterations"/>
    <default expression="" applyOnUpdate="0" field="max_degree"/>
    <default expression="0.05" applyOnUpdate="0" field="minimum_friction_velocity"/>
    <default expression="0.00000001" applyOnUpdate="0" field="minimum_surface_area"/>
    <default expression="1" applyOnUpdate="0" field="precon_cg"/>
    <default expression="0" applyOnUpdate="0" field="preissmann_slot"/>
    <default expression="1" applyOnUpdate="0" field="pump_implicit_ratio"/>
    <default expression="0.05" applyOnUpdate="0" field="thin_water_layer_definition"/>
    <default expression="20" applyOnUpdate="0" field="use_of_cg"/>
    <default expression="" applyOnUpdate="0" field="use_of_nested_newton"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="cfl_strictness_factor_1d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="cfl_strictness_factor_2d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="convergence_cg" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="convergence_eps" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="flow_direction_threshold" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="frict_shallow_water_correction" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="general_numerical_threshold" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="integration_method" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="limiter_grad_1d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="limiter_grad_2d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="limiter_slope_crossectional_area_2d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="limiter_slope_friction_2d" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="max_nonlin_iterations" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="max_degree" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="minimum_friction_velocity" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="minimum_surface_area" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="precon_cg" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="preissmann_slot" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="pump_implicit_ratio" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="thin_water_layer_definition" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_of_cg" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_of_nested_newton" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="cfl_strictness_factor_1d"/>
    <constraint exp="" desc="" field="cfl_strictness_factor_2d"/>
    <constraint exp="" desc="" field="convergence_cg"/>
    <constraint exp="" desc="" field="convergence_eps"/>
    <constraint exp="" desc="" field="flow_direction_threshold"/>
    <constraint exp="" desc="" field="frict_shallow_water_correction"/>
    <constraint exp="" desc="" field="general_numerical_threshold"/>
    <constraint exp="" desc="" field="integration_method"/>
    <constraint exp="" desc="" field="limiter_grad_1d"/>
    <constraint exp="" desc="" field="limiter_grad_2d"/>
    <constraint exp="" desc="" field="limiter_slope_crossectional_area_2d"/>
    <constraint exp="" desc="" field="limiter_slope_friction_2d"/>
    <constraint exp="" desc="" field="max_nonlin_iterations"/>
    <constraint exp="" desc="" field="max_degree"/>
    <constraint exp="" desc="" field="minimum_friction_velocity"/>
    <constraint exp="" desc="" field="minimum_surface_area"/>
    <constraint exp="" desc="" field="precon_cg"/>
    <constraint exp="" desc="" field="preissmann_slot"/>
    <constraint exp="" desc="" field="pump_implicit_ratio"/>
    <constraint exp="" desc="" field="thin_water_layer_definition"/>
    <constraint exp="" desc="" field="use_of_cg"/>
    <constraint exp="" desc="" field="use_of_nested_newton"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="cfl_strictness_factor_1d"/>
      <column width="-1" hidden="0" type="field" name="cfl_strictness_factor_2d"/>
      <column width="-1" hidden="0" type="field" name="convergence_cg"/>
      <column width="-1" hidden="0" type="field" name="convergence_eps"/>
      <column width="-1" hidden="0" type="field" name="flow_direction_threshold"/>
      <column width="-1" hidden="0" type="field" name="frict_shallow_water_correction"/>
      <column width="-1" hidden="0" type="field" name="general_numerical_threshold"/>
      <column width="-1" hidden="0" type="field" name="integration_method"/>
      <column width="-1" hidden="0" type="field" name="limiter_grad_1d"/>
      <column width="-1" hidden="0" type="field" name="limiter_grad_2d"/>
      <column width="-1" hidden="0" type="field" name="limiter_slope_crossectional_area_2d"/>
      <column width="-1" hidden="0" type="field" name="limiter_slope_friction_2d"/>
      <column width="-1" hidden="0" type="field" name="max_nonlin_iterations"/>
      <column width="-1" hidden="0" type="field" name="max_degree"/>
      <column width="-1" hidden="0" type="field" name="minimum_friction_velocity"/>
      <column width="-1" hidden="0" type="field" name="minimum_surface_area"/>
      <column width="-1" hidden="0" type="field" name="precon_cg"/>
      <column width="-1" hidden="0" type="field" name="preissmann_slot"/>
      <column width="-1" hidden="0" type="field" name="pump_implicit_ratio"/>
      <column width="-1" hidden="0" type="field" name="thin_water_layer_definition"/>
      <column width="-1" hidden="0" type="field" name="use_of_cg"/>
      <column width="-1" hidden="0" type="field" name="use_of_nested_newton"/>
      <column width="-1" hidden="1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="General" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="1" name="id"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Limiters" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="10" name="limiter_grad_1d"/>
      <attributeEditorField showLabel="1" index="11" name="limiter_grad_2d"/>
      <attributeEditorField showLabel="1" index="12" name="limiter_slope_crossectional_area_2d"/>
      <attributeEditorField showLabel="1" index="13" name="limiter_slope_friction_2d"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Matrix" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="4" name="convergence_cg"/>
      <attributeEditorField showLabel="1" index="5" name="convergence_eps"/>
      <attributeEditorField showLabel="1" index="22" name="use_of_cg"/>
      <attributeEditorField showLabel="1" index="23" name="use_of_nested_newton"/>
      <attributeEditorField showLabel="1" index="15" name="max_degree"/>
      <attributeEditorField showLabel="1" index="14" name="max_nonlin_iterations"/>
      <attributeEditorField showLabel="1" index="18" name="precon_cg"/>
      <attributeEditorField showLabel="1" index="9" name="integration_method"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Thresholds" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="6" name="flow_direction_threshold"/>
      <attributeEditorField showLabel="1" index="8" name="general_numerical_threshold"/>
      <attributeEditorField showLabel="1" index="21" name="thin_water_layer_definition"/>
      <attributeEditorField showLabel="1" index="16" name="minimum_friction_velocity"/>
      <attributeEditorField showLabel="1" index="17" name="minimum_surface_area"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Miscellaneous" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="2" name="cfl_strictness_factor_1d"/>
      <attributeEditorField showLabel="1" index="3" name="cfl_strictness_factor_2d"/>
      <attributeEditorField showLabel="1" index="7" name="frict_shallow_water_correction"/>
      <attributeEditorField showLabel="1" index="20" name="pump_implicit_ratio"/>
      <attributeEditorField showLabel="1" index="19" name="preissmann_slot"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="cfl_strictness_factor_1d"/>
    <field editable="1" name="cfl_strictness_factor_2d"/>
    <field editable="1" name="convergence_cg"/>
    <field editable="1" name="convergence_eps"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="flow_direction_threshold"/>
    <field editable="1" name="frict_shallow_water_correction"/>
    <field editable="1" name="general_numerical_threshold"/>
    <field editable="1" name="id"/>
    <field editable="1" name="integration_method"/>
    <field editable="1" name="limiter_grad_1d"/>
    <field editable="1" name="limiter_grad_2d"/>
    <field editable="1" name="limiter_slope_crossectional_area_2d"/>
    <field editable="1" name="limiter_slope_friction_2d"/>
    <field editable="1" name="max_degree"/>
    <field editable="1" name="max_nonlin_iterations"/>
    <field editable="1" name="minimum_friction_velocity"/>
    <field editable="1" name="minimum_surface_area"/>
    <field editable="1" name="precon_cg"/>
    <field editable="1" name="preissmann_slot"/>
    <field editable="1" name="pump_implicit_ratio"/>
    <field editable="1" name="thin_water_layer_definition"/>
    <field editable="1" name="use_of_cg"/>
    <field editable="1" name="use_of_nested_newton"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="cfl_strictness_factor_1d"/>
    <field labelOnTop="0" name="cfl_strictness_factor_2d"/>
    <field labelOnTop="0" name="convergence_cg"/>
    <field labelOnTop="0" name="convergence_eps"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="flow_direction_threshold"/>
    <field labelOnTop="0" name="frict_shallow_water_correction"/>
    <field labelOnTop="0" name="general_numerical_threshold"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="integration_method"/>
    <field labelOnTop="0" name="limiter_grad_1d"/>
    <field labelOnTop="0" name="limiter_grad_2d"/>
    <field labelOnTop="0" name="limiter_slope_crossectional_area_2d"/>
    <field labelOnTop="0" name="limiter_slope_friction_2d"/>
    <field labelOnTop="0" name="max_degree"/>
    <field labelOnTop="0" name="max_nonlin_iterations"/>
    <field labelOnTop="0" name="minimum_friction_velocity"/>
    <field labelOnTop="0" name="minimum_surface_area"/>
    <field labelOnTop="0" name="precon_cg"/>
    <field labelOnTop="0" name="preissmann_slot"/>
    <field labelOnTop="0" name="pump_implicit_ratio"/>
    <field labelOnTop="0" name="thin_water_layer_definition"/>
    <field labelOnTop="0" name="use_of_cg"/>
    <field labelOnTop="0" name="use_of_nested_newton"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
