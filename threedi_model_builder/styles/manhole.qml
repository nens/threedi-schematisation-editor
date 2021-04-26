<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" minScale="100000000" labelsEnabled="0" simplifyLocal="1" version="3.16.5-Hannover" maxScale="-4.656612873077393e-10" simplifyDrawingTol="1" readOnly="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal enabled="0" durationField="" fixedDuration="0" mode="0" endField="" accumulate="0" startField="" endExpression="" durationUnit="min" startExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="RuleRenderer" forceraster="0" enableorderby="0" symbollevels="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule filter="manh_manhole_indicator = 0" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" symbol="0" scalemaxdenom="5000" label="Manhole (inspection)"/>
      <rule filter="manh_manhole_indicator = 1" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" symbol="1" scalemaxdenom="15000" label="Outlet"/>
      <rule filter="manh_manhole_indicator = 2" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" symbol="2" label="Pumping station"/>
      <rule filter="ELSE" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}" symbol="3" scalemaxdenom="5000" label="Manhole (unspecified)"/>
    </rules>
    <symbols>
      <symbol type="marker" name="0" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="1" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="63,128,192,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="85,170,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.75" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2.5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 2.5,1.5)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="2" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0.10000000000000001,0.10000000000000001" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,183" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.7" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4.1" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 4.1,3.1)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,127,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.7" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
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
      <symbol type="marker" name="3" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,9,1,255" k="outline_color"/>
          <prop v="dot" k="outline_style"/>
          <prop v="0.25" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"manh_display_name"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory rotationOffset="270" penAlpha="255" direction="1" showAxis="0" barWidth="5" penColor="#000000" scaleDependency="Area" labelPlacementMethod="XHeight" width="15" opacity="1" scaleBasedVisibility="0" sizeType="MM" height="15" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" spacingUnitScale="3x:0,0,0,0,0,0" minScaleDenominator="-4.65661e-10" backgroundAlpha="255" backgroundColor="#ffffff" diagramOrientation="Up" spacing="0" spacingUnit="MM" lineSizeType="MM" minimumSize="0" penWidth="0" sizeScale="3x:0,0,0,0,0,0" enabled="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol type="line" name="" alpha="1" force_rhr="0" clip_to_extent="1">
          <layer enabled="1" locked="0" pass="0" class="SimpleLine">
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
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
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
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" linePlacementFlags="2" dist="0" obstacle="0" placement="0" showAll="1" zIndex="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
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
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="display_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="calculation_type" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="shape" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="length" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bottom_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="surface_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="drain_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sediment_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manhole_indicator" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
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
    <alias name="" field="shape" index="5"/>
    <alias name="" field="width" index="6"/>
    <alias name="" field="length" index="7"/>
    <alias name="" field="bottom_level" index="8"/>
    <alias name="" field="surface_level" index="9"/>
    <alias name="" field="drain_level" index="10"/>
    <alias name="" field="sediment_level" index="11"/>
    <alias name="" field="manhole_indicator" index="12"/>
    <alias name="" field="zoom_category" index="13"/>
    <alias name="" field="connection_node_id" index="14"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="code" applyOnUpdate="0"/>
    <default expression="" field="display_name" applyOnUpdate="0"/>
    <default expression="" field="calculation_type" applyOnUpdate="0"/>
    <default expression="" field="shape" applyOnUpdate="0"/>
    <default expression="" field="width" applyOnUpdate="0"/>
    <default expression="" field="length" applyOnUpdate="0"/>
    <default expression="" field="bottom_level" applyOnUpdate="0"/>
    <default expression="" field="surface_level" applyOnUpdate="0"/>
    <default expression="" field="drain_level" applyOnUpdate="0"/>
    <default expression="" field="sediment_level" applyOnUpdate="0"/>
    <default expression="" field="manhole_indicator" applyOnUpdate="0"/>
    <default expression="" field="zoom_category" applyOnUpdate="0"/>
    <default expression="" field="connection_node_id" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" constraints="3" field="fid" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="id" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="code" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="display_name" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="calculation_type" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="shape" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="width" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="length" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="bottom_level" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="surface_level" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="drain_level" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="sediment_level" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="manhole_indicator" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="zoom_category" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" field="connection_node_id" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="calculation_type"/>
    <constraint exp="" desc="" field="shape"/>
    <constraint exp="" desc="" field="width"/>
    <constraint exp="" desc="" field="length"/>
    <constraint exp="" desc="" field="bottom_level"/>
    <constraint exp="" desc="" field="surface_level"/>
    <constraint exp="" desc="" field="drain_level"/>
    <constraint exp="" desc="" field="sediment_level"/>
    <constraint exp="" desc="" field="manhole_indicator"/>
    <constraint exp="" desc="" field="zoom_category"/>
    <constraint exp="" desc="" field="connection_node_id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;manh_manhole_indicator&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" name="fid" hidden="0" width="-1"/>
      <column type="field" name="id" hidden="0" width="-1"/>
      <column type="field" name="code" hidden="0" width="-1"/>
      <column type="field" name="display_name" hidden="0" width="-1"/>
      <column type="field" name="calculation_type" hidden="0" width="-1"/>
      <column type="field" name="shape" hidden="0" width="-1"/>
      <column type="field" name="width" hidden="0" width="-1"/>
      <column type="field" name="length" hidden="0" width="-1"/>
      <column type="field" name="bottom_level" hidden="0" width="-1"/>
      <column type="field" name="surface_level" hidden="0" width="-1"/>
      <column type="field" name="drain_level" hidden="0" width="-1"/>
      <column type="field" name="sediment_level" hidden="0" width="-1"/>
      <column type="field" name="manhole_indicator" hidden="0" width="-1"/>
      <column type="field" name="zoom_category" hidden="0" width="-1"/>
      <column type="field" name="connection_node_id" hidden="0" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:/Users/zaap/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\manhole.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer visibilityExpression="" name="Manhole_view" columnCount="1" showLabel="1" visibilityExpressionEnabled="0" groupBox="0">
      <attributeEditorContainer visibilityExpression="" name="General" columnCount="1" showLabel="1" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="manh_id" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_display_name" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_code" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_calculation_type" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Characteristics" columnCount="1" showLabel="1" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="manh_shape" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_width" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_length" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_bottom_level" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_surface_level" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_drain_level" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Visualisation" columnCount="1" showLabel="1" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="manh_manhole_indicator" showLabel="1" index="-1"/>
        <attributeEditorField name="manh_zoom_category" showLabel="1" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" name="Connection node" columnCount="1" showLabel="1" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="manh_connection_node_id" showLabel="1" index="-1"/>
        <attributeEditorField name="node_code" showLabel="1" index="-1"/>
        <attributeEditorField name="node_initial_waterlevel" showLabel="1" index="-1"/>
        <attributeEditorField name="node_storage_area" showLabel="1" index="-1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="bottom_level" editable="1"/>
    <field name="calculation_type" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_id" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="drain_level" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="length" editable="1"/>
    <field name="manh_bottom_level" editable="1"/>
    <field name="manh_calculation_type" editable="1"/>
    <field name="manh_code" editable="1"/>
    <field name="manh_connection_node_id" editable="0"/>
    <field name="manh_display_name" editable="1"/>
    <field name="manh_drain_level" editable="1"/>
    <field name="manh_id" editable="0"/>
    <field name="manh_length" editable="1"/>
    <field name="manh_manhole_indicator" editable="1"/>
    <field name="manh_sediment_level" editable="1"/>
    <field name="manh_shape" editable="1"/>
    <field name="manh_surface_level" editable="1"/>
    <field name="manh_width" editable="1"/>
    <field name="manh_zoom_category" editable="1"/>
    <field name="manhole_indicator" editable="1"/>
    <field name="node_code" editable="1"/>
    <field name="node_id" editable="0"/>
    <field name="node_initial_waterlevel" editable="1"/>
    <field name="node_storage_area" editable="1"/>
    <field name="node_the_geom_linestring" editable="1"/>
    <field name="sediment_level" editable="1"/>
    <field name="shape" editable="1"/>
    <field name="surface_level" editable="1"/>
    <field name="width" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="bottom_level" labelOnTop="0"/>
    <field name="calculation_type" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="drain_level" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="length" labelOnTop="0"/>
    <field name="manh_bottom_level" labelOnTop="0"/>
    <field name="manh_calculation_type" labelOnTop="0"/>
    <field name="manh_code" labelOnTop="0"/>
    <field name="manh_connection_node_id" labelOnTop="0"/>
    <field name="manh_display_name" labelOnTop="0"/>
    <field name="manh_drain_level" labelOnTop="0"/>
    <field name="manh_id" labelOnTop="0"/>
    <field name="manh_length" labelOnTop="0"/>
    <field name="manh_manhole_indicator" labelOnTop="0"/>
    <field name="manh_sediment_level" labelOnTop="0"/>
    <field name="manh_shape" labelOnTop="0"/>
    <field name="manh_surface_level" labelOnTop="0"/>
    <field name="manh_width" labelOnTop="0"/>
    <field name="manh_zoom_category" labelOnTop="0"/>
    <field name="manhole_indicator" labelOnTop="0"/>
    <field name="node_code" labelOnTop="0"/>
    <field name="node_id" labelOnTop="0"/>
    <field name="node_initial_waterlevel" labelOnTop="0"/>
    <field name="node_storage_area" labelOnTop="0"/>
    <field name="node_the_geom_linestring" labelOnTop="0"/>
    <field name="sediment_level" labelOnTop="0"/>
    <field name="shape" labelOnTop="0"/>
    <field name="surface_level" labelOnTop="0"/>
    <field name="width" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"manh_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
