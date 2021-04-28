<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="100000000" readOnly="0" simplifyAlgorithm="0" simplifyLocal="1" version="3.16.5-Hannover" maxScale="0" simplifyDrawingHints="0" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startExpression="" accumulate="0" endField="" enabled="0" durationField="" durationUnit="min" startField="" fixedDuration="0" endExpression="" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol name="0" force_rhr="0" clip_to_extent="1" type="marker" alpha="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="1.2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if(@map_scale&lt;10000, 1.2,0.7)" type="QString"/>
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
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontFamily="MS Shell Dlg 2" namedStyle="Standaard" multilineHeight="1" fontSize="8" fontKerning="1" fontWordSpacing="0" fontItalic="0" fontLetterSpacing="0" fontUnderline="0" fontStrikeout="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textOrientation="horizontal" fontSizeUnit="Point" blendMode="0" capitalization="0" textColor="0,0,0,255" previewBkgrdColor="255,255,255,255" useSubstitutions="0" allowHtml="0" textOpacity="1" isExpression="0" fieldName="code" fontWeight="50">
        <text-buffer bufferJoinStyle="64" bufferNoFill="0" bufferSizeUnits="MM" bufferDraw="1" bufferColor="255,255,255,255" bufferBlendMode="0" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="0.6"/>
        <text-mask maskSizeUnits="MM" maskJoinStyle="128" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskOpacity="1" maskType="0" maskEnabled="0" maskSize="0" maskedSymbolLayers=""/>
        <background shapeDraw="0" shapeFillColor="255,255,255,255" shapeRadiiY="0" shapeType="0" shapeOpacity="1" shapeRotation="0" shapeOffsetX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeBorderColor="128,128,128,255" shapeSizeUnit="MM" shapeJoinStyle="64" shapeSizeY="0" shapeRotationType="0" shapeBorderWidth="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeSVGFile="" shapeSizeType="0" shapeOffsetY="0" shapeBorderWidthUnit="MM">
          <symbol name="markerSymbol" force_rhr="0" clip_to_extent="1" type="marker" alpha="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop v="0" k="angle"/>
              <prop v="125,139,143,255" k="color"/>
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
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowUnder="0" shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowBlendMode="6" shadowOffsetAngle="135" shadowOffsetDist="1" shadowOffsetGlobal="1" shadowRadius="1.5" shadowScale="100" shadowOffsetUnit="MM" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="0" formatNumbers="0" autoWrapLength="0" plussign="0" placeDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" leftDirectionSymbol="&lt;" decimals="3" rightDirectionSymbol=">" addDirectionSymbol="0" wrapChar="" reverseDirectionSymbol="0"/>
      <placement priority="5" maxCurvedCharAngleIn="20" xOffset="0" placement="0" lineAnchorType="0" offsetUnits="MapUnit" yOffset="0" lineAnchorPercent="0.5" distUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" rotationAngle="0" fitInPolygonOnly="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" polygonPlacementFlags="2" centroidWhole="0" maxCurvedCharAngleOut="-20" geometryGenerator="" quadOffset="4" geometryGeneratorEnabled="0" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" offsetType="0" repeatDistanceUnits="MM" preserveRotation="1" centroidInside="0" placementFlags="0" geometryGeneratorType="PointGeometry" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" overrunDistanceUnit="MM" layerType="PointGeometry" labelOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
      <rendering scaleMax="2000" obstacle="1" limitNumLabels="0" scaleVisibility="0" scaleMin="1" minFeatureSize="0" maxNumLabels="2000" fontMinPixelSize="3" mergeLines="0" obstacleType="0" zIndex="0" fontMaxPixelSize="10000" fontLimitPixelSize="0" displayAll="0" upsidedownLabels="0" obstacleFactor="1" drawLabels="1" labelPerPart="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties"/>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
          <Option name="drawToAllParts" value="false" type="bool"/>
          <Option name="enabled" value="0" type="QString"/>
          <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
          <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot; type=&quot;line&quot; alpha=&quot;1&quot;>&lt;layer locked=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
          <Option name="minLength" value="0" type="double"/>
          <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="minLengthUnit" value="MM" type="QString"/>
          <Option name="offsetFromAnchor" value="0" type="double"/>
          <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
          <Option name="offsetFromLabel" value="0" type="double"/>
          <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"id"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory scaleBasedVisibility="0" minimumSize="0" spacingUnit="MM" enabled="0" sizeType="MM" rotationOffset="270" showAxis="0" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" opacity="1" minScaleDenominator="0" direction="1" width="15" barWidth="5" backgroundAlpha="255" backgroundColor="#ffffff" penWidth="0" maxScaleDenominator="1e+08" height="15" diagramOrientation="Up" penColor="#000000" spacingUnitScale="3x:0,0,0,0,0,0" spacing="0" lineSizeType="MM">
      <fontProperties style="" description="MS Shell Dlg 2,7.5,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
      <axisSymbol>
        <symbol name="" force_rhr="0" clip_to_extent="1" type="line" alpha="1">
          <layer locked="0" enabled="1" class="SimpleLine" pass="0">
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
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" dist="0" zIndex="0" obstacle="0" placement="0" linePlacementFlags="2" showAll="1">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties" type="Map">
          <Option name="show" type="Map">
            <Option name="active" value="true" type="bool"/>
            <Option name="field" value="the_geom_linestring" type="QString"/>
            <Option name="type" value="2" type="int"/>
          </Option>
        </Option>
        <Option name="type" value="collection" type="QString"/>
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
    <field name="initial_waterlevel" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="storage_area" configurationFlags="None">
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
    <alias name="" index="0" field="fid"/>
    <alias name="" index="1" field="id"/>
    <alias name="" index="2" field="code"/>
    <alias name="" index="3" field="initial_waterlevel"/>
    <alias name="" index="4" field="storage_area"/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="" applyOnUpdate="0" field="initial_waterlevel"/>
    <default expression="" applyOnUpdate="0" field="storage_area"/>
  </defaults>
  <constraints>
    <constraint constraints="3" unique_strength="1" notnull_strength="1" field="fid" exp_strength="0"/>
    <constraint constraints="3" unique_strength="1" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="code" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="initial_waterlevel" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="storage_area" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="fid" exp=""/>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="code" exp=""/>
    <constraint desc="" field="initial_waterlevel" exp=""/>
    <constraint desc="" field="storage_area" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="1" sortExpression="&quot;code&quot;">
    <columns>
      <column name="code" hidden="0" width="-1" type="field"/>
      <column name="initial_waterlevel" hidden="0" width="-1" type="field"/>
      <column name="storage_area" hidden="0" width="-1" type="field"/>
      <column name="id" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
      <column name="fid" hidden="0" width="-1" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:/Users/zaap/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\connection_node.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>../../../OSGEO4~1/bin</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="General" groupBox="0" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorField name="id" index="1" showLabel="1"/>
      <attributeEditorField name="code" index="2" showLabel="1"/>
      <attributeEditorField name="initial_waterlevel" index="3" showLabel="1"/>
      <attributeEditorField name="storage_area" index="4" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="code" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="initial_waterlevel" editable="1"/>
    <field name="storage_area" editable="1"/>
    <field name="the_geom_linestring" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="code" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="initial_waterlevel" labelOnTop="0"/>
    <field name="storage_area" labelOnTop="0"/>
    <field name="the_geom_linestring" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
