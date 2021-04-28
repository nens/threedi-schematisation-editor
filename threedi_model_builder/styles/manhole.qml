<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingTol="1" simplifyDrawingHints="0" version="3.16.5-Hannover" minScale="100000000" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" maxScale="-4.656612873077393e-10" simplifyMaxScale="1" labelsEnabled="0" readOnly="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal endExpression="" startExpression="" fixedDuration="0" durationUnit="min" enabled="0" durationField="" endField="" accumulate="0" mode="0" startField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" symbollevels="0" type="RuleRenderer" enableorderby="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule filter="manhole_indicator = 0" label="Manhole (inspection)" symbol="0" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}"/>
      <rule filter="manhole_indicator = 1" label="Outlet" symbol="1" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}"/>
      <rule filter="manhole_indicator = 2" label="Pumping station" symbol="2" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}"/>
      <rule scalemaxdenom="5000" filter="ELSE" label="Manhole (unspecified)" symbol="3" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}"/>
    </rules>
    <symbols>
      <symbol type="marker" force_rhr="0" name="0" clip_to_extent="1" alpha="1">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" force_rhr="0" name="1" clip_to_extent="1" alpha="1">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
          <effect type="effectStack" enabled="0">
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
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 2.5,1.5)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" force_rhr="0" name="2" clip_to_extent="1" alpha="1">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
          <effect type="effectStack" enabled="0">
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
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 4.1,3.1)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
          <effect type="effectStack" enabled="0">
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
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 4,3)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" force_rhr="0" name="3" clip_to_extent="1" alpha="1">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>COALESCE( "display_name", '&lt;NULL>' )</value>
      <value>"manh_display_name"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory labelPlacementMethod="XHeight" height="15" sizeScale="3x:0,0,0,0,0,0" width="15" penColor="#000000" minimumSize="0" scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" sizeType="MM" scaleBasedVisibility="0" spacingUnit="MM" penAlpha="255" opacity="1" minScaleDenominator="-4.65661e-10" spacingUnitScale="3x:0,0,0,0,0,0" rotationOffset="270" maxScaleDenominator="1e+08" direction="1" penWidth="0" barWidth="5" spacing="0" diagramOrientation="Up" lineSizeType="MM" showAxis="0" backgroundAlpha="255" backgroundColor="#ffffff">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol type="line" force_rhr="0" name="" clip_to_extent="1" alpha="1">
          <layer enabled="1" class="SimpleLine" pass="0" locked="0">
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
                <Option type="QString" value="" name="name"/>
                <Option name="properties"/>
                <Option type="QString" value="collection" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="2" showAll="1" zIndex="0" priority="0" dist="0" obstacle="0" placement="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="calculation_type">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="shape">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="length">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="sediment_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="manhole_indicator">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="zoom_category">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="connection_node_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="code" index="2" name=""/>
    <alias field="display_name" index="3" name=""/>
    <alias field="calculation_type" index="4" name=""/>
    <alias field="shape" index="5" name=""/>
    <alias field="width" index="6" name=""/>
    <alias field="length" index="7" name=""/>
    <alias field="bottom_level" index="8" name=""/>
    <alias field="surface_level" index="9" name=""/>
    <alias field="drain_level" index="10" name=""/>
    <alias field="sediment_level" index="11" name=""/>
    <alias field="manhole_indicator" index="12" name=""/>
    <alias field="zoom_category" index="13" name=""/>
    <alias field="connection_node_id" index="14" name=""/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="code" applyOnUpdate="0" expression=""/>
    <default field="display_name" applyOnUpdate="0" expression=""/>
    <default field="calculation_type" applyOnUpdate="0" expression=""/>
    <default field="shape" applyOnUpdate="0" expression=""/>
    <default field="width" applyOnUpdate="0" expression=""/>
    <default field="length" applyOnUpdate="0" expression=""/>
    <default field="bottom_level" applyOnUpdate="0" expression=""/>
    <default field="surface_level" applyOnUpdate="0" expression=""/>
    <default field="drain_level" applyOnUpdate="0" expression=""/>
    <default field="sediment_level" applyOnUpdate="0" expression=""/>
    <default field="manhole_indicator" applyOnUpdate="0" expression=""/>
    <default field="zoom_category" applyOnUpdate="0" expression=""/>
    <default field="connection_node_id" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="3" field="fid" unique_strength="1" exp_strength="0" notnull_strength="1"/>
    <constraint constraints="0" field="id" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="code" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="display_name" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="calculation_type" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="shape" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="width" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="length" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="bottom_level" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="surface_level" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="drain_level" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="sediment_level" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="manhole_indicator" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="zoom_category" unique_strength="0" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" field="connection_node_id" unique_strength="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="display_name" desc="" exp=""/>
    <constraint field="calculation_type" desc="" exp=""/>
    <constraint field="shape" desc="" exp=""/>
    <constraint field="width" desc="" exp=""/>
    <constraint field="length" desc="" exp=""/>
    <constraint field="bottom_level" desc="" exp=""/>
    <constraint field="surface_level" desc="" exp=""/>
    <constraint field="drain_level" desc="" exp=""/>
    <constraint field="sediment_level" desc="" exp=""/>
    <constraint field="manhole_indicator" desc="" exp=""/>
    <constraint field="zoom_category" desc="" exp=""/>
    <constraint field="connection_node_id" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;manh_manhole_indicator&quot;" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" width="-1" name="fid" hidden="0"/>
      <column type="field" width="-1" name="id" hidden="0"/>
      <column type="field" width="-1" name="code" hidden="0"/>
      <column type="field" width="-1" name="display_name" hidden="0"/>
      <column type="field" width="-1" name="calculation_type" hidden="0"/>
      <column type="field" width="-1" name="shape" hidden="0"/>
      <column type="field" width="-1" name="width" hidden="0"/>
      <column type="field" width="-1" name="length" hidden="0"/>
      <column type="field" width="-1" name="bottom_level" hidden="0"/>
      <column type="field" width="-1" name="surface_level" hidden="0"/>
      <column type="field" width="-1" name="drain_level" hidden="0"/>
      <column type="field" width="-1" name="sediment_level" hidden="0"/>
      <column type="field" width="-1" name="manhole_indicator" hidden="0"/>
      <column type="field" width="-1" name="zoom_category" hidden="0"/>
      <column type="field" width="-1" name="connection_node_id" hidden="0"/>
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
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpressionEnabled="0" name="Manhole_view" showLabel="1" visibilityExpression="">
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" name="General" showLabel="1" visibilityExpression="">
        <attributeEditorField index="-1" name="manh_id" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_display_name" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_code" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_calculation_type" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" name="Characteristics" showLabel="1" visibilityExpression="">
        <attributeEditorField index="-1" name="manh_shape" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_width" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_length" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_bottom_level" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_surface_level" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_drain_level" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" name="Visualisation" showLabel="1" visibilityExpression="">
        <attributeEditorField index="-1" name="manh_manhole_indicator" showLabel="1"/>
        <attributeEditorField index="-1" name="manh_zoom_category" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" name="Connection node" showLabel="1" visibilityExpression="">
        <attributeEditorField index="-1" name="manh_connection_node_id" showLabel="1"/>
        <attributeEditorField index="-1" name="node_code" showLabel="1"/>
        <attributeEditorField index="-1" name="node_initial_waterlevel" showLabel="1"/>
        <attributeEditorField index="-1" name="node_storage_area" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bottom_level"/>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="drain_level"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="length"/>
    <field editable="1" name="manh_bottom_level"/>
    <field editable="1" name="manh_calculation_type"/>
    <field editable="1" name="manh_code"/>
    <field editable="0" name="manh_connection_node_id"/>
    <field editable="1" name="manh_display_name"/>
    <field editable="1" name="manh_drain_level"/>
    <field editable="0" name="manh_id"/>
    <field editable="1" name="manh_length"/>
    <field editable="1" name="manh_manhole_indicator"/>
    <field editable="1" name="manh_sediment_level"/>
    <field editable="1" name="manh_shape"/>
    <field editable="1" name="manh_surface_level"/>
    <field editable="1" name="manh_width"/>
    <field editable="1" name="manh_zoom_category"/>
    <field editable="1" name="manhole_indicator"/>
    <field editable="1" name="node_code"/>
    <field editable="0" name="node_id"/>
    <field editable="1" name="node_initial_waterlevel"/>
    <field editable="1" name="node_storage_area"/>
    <field editable="1" name="node_the_geom_linestring"/>
    <field editable="1" name="sediment_level"/>
    <field editable="1" name="shape"/>
    <field editable="1" name="surface_level"/>
    <field editable="1" name="width"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="bottom_level"/>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="drain_level"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="length"/>
    <field labelOnTop="0" name="manh_bottom_level"/>
    <field labelOnTop="0" name="manh_calculation_type"/>
    <field labelOnTop="0" name="manh_code"/>
    <field labelOnTop="0" name="manh_connection_node_id"/>
    <field labelOnTop="0" name="manh_display_name"/>
    <field labelOnTop="0" name="manh_drain_level"/>
    <field labelOnTop="0" name="manh_id"/>
    <field labelOnTop="0" name="manh_length"/>
    <field labelOnTop="0" name="manh_manhole_indicator"/>
    <field labelOnTop="0" name="manh_sediment_level"/>
    <field labelOnTop="0" name="manh_shape"/>
    <field labelOnTop="0" name="manh_surface_level"/>
    <field labelOnTop="0" name="manh_width"/>
    <field labelOnTop="0" name="manh_zoom_category"/>
    <field labelOnTop="0" name="manhole_indicator"/>
    <field labelOnTop="0" name="node_code"/>
    <field labelOnTop="0" name="node_id"/>
    <field labelOnTop="0" name="node_initial_waterlevel"/>
    <field labelOnTop="0" name="node_storage_area"/>
    <field labelOnTop="0" name="node_the_geom_linestring"/>
    <field labelOnTop="0" name="sediment_level"/>
    <field labelOnTop="0" name="shape"/>
    <field labelOnTop="0" name="surface_level"/>
    <field labelOnTop="0" name="width"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>COALESCE( "display_name", '&lt;NULL>' )</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
