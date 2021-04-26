<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" labelsEnabled="0" readOnly="0" version="3.16.5-Hannover" simplifyMaxScale="1" simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyDrawingHints="1" minScale="100000000" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startField="" enabled="0" mode="0" fixedDuration="0" endExpression="" durationUnit="min" accumulate="0" startExpression="" durationField="" endField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="RuleRenderer" forceraster="0" symbollevels="0" enableorderby="0">
    <rules key="{1c4a4e03-d442-4bb0-8ffc-82b9a703e08f}">
      <rule symbol="0" label="Combined sewer" key="{844e5e28-ad8f-43dc-ae9b-2eedeecde873}" filter="pipe_sewerage_type = 0"/>
      <rule symbol="1" label="Storm drain" key="{3b41f70d-2dfe-4438-8b1a-3722a52ff82b}" filter="pipe_sewerage_type = 1"/>
      <rule symbol="2" label="Sanitary sewer" key="{c8833167-878e-49b2-bd37-5019aeea2451}" filter="pipe_sewerage_type = 2"/>
      <rule symbol="3" label="Transport" key="{d62bccfa-4138-43ba-ab6d-51eae9f5b079}" filter="pipe_sewerage_type = 3"/>
      <rule symbol="4" label="Spillway" key="{3d909156-553e-4d45-8a2f-02337ffb74d5}" filter="pipe_sewerage_type = 4"/>
      <rule symbol="5" label="Syphon" key="{a445abaf-878b-4b6b-8f1d-1314d1271d38}" filter="pipe_sewerage_type =5"/>
      <rule symbol="6" label="Storage" key="{c6ba261b-8172-407e-bc72-8487b24a1cc4}" filter="pipe_sewerage_type = 6"/>
      <rule symbol="7" label="Storage and settlement tank" key="{8eb66a66-0335-4672-a78d-1aac6c4702ff}" filter="pipe_sewerage_type = 7"/>
      <rule symbol="8" label="Other" key="{aa320dac-96a8-41e4-af30-3e9153ceaeae}" filter="ELSE"/>
    </rules>
    <symbols>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="1">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="2">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="3">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
          <prop v="0.7" k="line_width"/>
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
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="4">
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
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="dot" k="line_style"/>
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="5">
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
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
          <prop v="MM" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="interval" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol type="marker" alpha="1" force_rhr="0" clip_to_extent="1" name="@5@1">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="85,170,255,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="semi_circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
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
        </layer>
      </symbol>
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="6">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
          <prop v="189,189,189,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
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
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="7">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
          <prop v="92,92,92,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
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
      <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="8">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
          <prop v="dot" k="line_style"/>
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontKerning="1" fontFamily="MS Shell Dlg 2" allowHtml="0" fontUnderline="0" previewBkgrdColor="255,255,255,255" fontLetterSpacing="0" fontItalic="0" textColor="0,0,0,255" textOrientation="horizontal" useSubstitutions="0" isExpression="0" fontStrikeout="0" fontSizeUnit="Point" multilineHeight="1" textOpacity="1" fontWeight="50" fontWordSpacing="0" fieldName="ROWID" blendMode="0" fontSize="8.25" capitalization="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" namedStyle="Standaard">
        <text-buffer bufferSizeUnits="MM" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferNoFill="0" bufferDraw="0" bufferJoinStyle="64" bufferOpacity="1" bufferBlendMode="0"/>
        <text-mask maskedSymbolLayers="" maskType="0" maskEnabled="0" maskSize="0" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSizeUnits="MM" maskJoinStyle="128"/>
        <background shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeSVGFile="" shapeType="0" shapeRadiiUnit="MM" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeOffsetX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeBlendMode="0" shapeRadiiY="0" shapeSizeY="0" shapeOffsetY="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeSizeType="0" shapeSizeX="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeJoinStyle="64" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRotationType="0">
          <symbol type="marker" alpha="1" force_rhr="0" clip_to_extent="1" name="markerSymbol">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="213,180,60,255" k="color"/>
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
                  <Option type="QString" value="" name="name"/>
                  <Option name="properties"/>
                  <Option type="QString" value="collection" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowDraw="0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowOpacity="0.7" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6" shadowOffsetUnit="MM" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowUnder="0" shadowScale="100" shadowRadiusAlphaOnly="0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format reverseDirectionSymbol="0" decimals="3" plussign="0" multilineAlign="0" formatNumbers="0" wrapChar="" addDirectionSymbol="0" placeDirectionSymbol="0" rightDirectionSymbol=">" autoWrapLength="0" useMaxLineLengthForAutoWrap="1" leftDirectionSymbol="&lt;"/>
      <placement dist="0" yOffset="0" distMapUnitScale="3x:0,0,0,0,0,0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" maxCurvedCharAngleOut="-20" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" layerType="LineGeometry" offsetType="0" repeatDistance="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetUnits="MapUnit" rotationAngle="0" maxCurvedCharAngleIn="20" distUnits="MM" priority="5" lineAnchorType="0" quadOffset="4" fitInPolygonOnly="0" polygonPlacementFlags="2" overrunDistance="0" repeatDistanceUnits="MM" centroidWhole="0" geometryGenerator="" lineAnchorPercent="0.5" placementFlags="10" placement="2" xOffset="0" geometryGeneratorType="PointGeometry"/>
      <rendering scaleVisibility="0" upsidedownLabels="0" zIndex="0" drawLabels="1" obstacleType="0" mergeLines="0" fontMaxPixelSize="10000" scaleMax="10000000" labelPerPart="0" scaleMin="1" limitNumLabels="0" obstacleFactor="1" obstacle="1" maxNumLabels="2000" displayAll="0" fontLimitPixelSize="0" fontMinPixelSize="3" minFeatureSize="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" value="" name="name"/>
          <Option name="properties"/>
          <Option type="QString" value="collection" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option type="QString" value="pole_of_inaccessibility" name="anchorPoint"/>
          <Option type="Map" name="ddProperties">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
          <Option type="bool" value="false" name="drawToAllParts"/>
          <Option type="QString" value="0" name="enabled"/>
          <Option type="QString" value="point_on_exterior" name="labelAnchorPoint"/>
          <Option type="QString" value="&lt;symbol type=&quot;line&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot; name=&quot;symbol&quot;>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; value=&quot;&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; value=&quot;collection&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol"/>
          <Option type="double" value="0" name="minLength"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale"/>
          <Option type="QString" value="MM" name="minLengthUnit"/>
          <Option type="double" value="0" name="offsetFromAnchor"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale"/>
          <Option type="QString" value="MM" name="offsetFromAnchorUnit"/>
          <Option type="double" value="0" name="offsetFromLabel"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale"/>
          <Option type="QString" value="MM" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property value="ROWID" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory maxScaleDenominator="1e+08" enabled="0" penWidth="0" minimumSize="0" minScaleDenominator="0" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" barWidth="5" penColor="#000000" spacing="0" penAlpha="255" width="15" sizeType="MM" scaleDependency="Area" spacingUnitScale="3x:0,0,0,0,0,0" lineSizeType="MM" direction="1" showAxis="0" backgroundColor="#ffffff" diagramOrientation="Up" height="15" scaleBasedVisibility="0" spacingUnit="MM" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" opacity="1">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
      <axisSymbol>
        <symbol type="line" alpha="1" force_rhr="0" clip_to_extent="1" name="">
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
  <DiagramLayerSettings zIndex="0" placement="2" dist="0" linePlacementFlags="2" showAll="1" priority="0" obstacle="0">
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
    <field configurationFlags="None" name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="friction_type">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="material">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="sewerage_type">
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
    <field configurationFlags="None" name="profile_num">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="original_length">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="connection_node_start_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="connection_node_end_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_definition_id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="id"/>
    <alias index="2" name="" field="code"/>
    <alias index="3" name="" field="display_name"/>
    <alias index="4" name="" field="calculation_type"/>
    <alias index="5" name="" field="dist_calc_points"/>
    <alias index="6" name="" field="invert_level_start_point"/>
    <alias index="7" name="" field="invert_level_end_point"/>
    <alias index="8" name="" field="friction_value"/>
    <alias index="9" name="" field="friction_type"/>
    <alias index="10" name="" field="material"/>
    <alias index="11" name="" field="sewerage_type"/>
    <alias index="12" name="" field="zoom_category"/>
    <alias index="13" name="" field="profile_num"/>
    <alias index="14" name="" field="original_length"/>
    <alias index="15" name="" field="connection_node_start_id"/>
    <alias index="16" name="" field="connection_node_end_id"/>
    <alias index="17" name="" field="cross_section_definition_id"/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="code"/>
    <default expression="" applyOnUpdate="0" field="display_name"/>
    <default expression="" applyOnUpdate="0" field="calculation_type"/>
    <default expression="" applyOnUpdate="0" field="dist_calc_points"/>
    <default expression="" applyOnUpdate="0" field="invert_level_start_point"/>
    <default expression="" applyOnUpdate="0" field="invert_level_end_point"/>
    <default expression="" applyOnUpdate="0" field="friction_value"/>
    <default expression="" applyOnUpdate="0" field="friction_type"/>
    <default expression="" applyOnUpdate="0" field="material"/>
    <default expression="" applyOnUpdate="0" field="sewerage_type"/>
    <default expression="" applyOnUpdate="0" field="zoom_category"/>
    <default expression="" applyOnUpdate="0" field="profile_num"/>
    <default expression="" applyOnUpdate="0" field="original_length"/>
    <default expression="" applyOnUpdate="0" field="connection_node_start_id"/>
    <default expression="" applyOnUpdate="0" field="connection_node_end_id"/>
    <default expression="" applyOnUpdate="0" field="cross_section_definition_id"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1" field="fid"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="id"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="code"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="display_name"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="calculation_type"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="dist_calc_points"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="invert_level_start_point"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="invert_level_end_point"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="friction_value"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="friction_type"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="material"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="sewerage_type"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="zoom_category"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="profile_num"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="original_length"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="connection_node_start_id"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="connection_node_end_id"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="cross_section_definition_id"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="calculation_type"/>
    <constraint exp="" desc="" field="dist_calc_points"/>
    <constraint exp="" desc="" field="invert_level_start_point"/>
    <constraint exp="" desc="" field="invert_level_end_point"/>
    <constraint exp="" desc="" field="friction_value"/>
    <constraint exp="" desc="" field="friction_type"/>
    <constraint exp="" desc="" field="material"/>
    <constraint exp="" desc="" field="sewerage_type"/>
    <constraint exp="" desc="" field="zoom_category"/>
    <constraint exp="" desc="" field="profile_num"/>
    <constraint exp="" desc="" field="original_length"/>
    <constraint exp="" desc="" field="connection_node_start_id"/>
    <constraint exp="" desc="" field="connection_node_end_id"/>
    <constraint exp="" desc="" field="cross_section_definition_id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" width="-1" name="fid" hidden="0"/>
      <column type="field" width="-1" name="id" hidden="0"/>
      <column type="field" width="-1" name="code" hidden="0"/>
      <column type="field" width="-1" name="display_name" hidden="0"/>
      <column type="field" width="-1" name="calculation_type" hidden="0"/>
      <column type="field" width="-1" name="dist_calc_points" hidden="0"/>
      <column type="field" width="-1" name="invert_level_start_point" hidden="0"/>
      <column type="field" width="-1" name="invert_level_end_point" hidden="0"/>
      <column type="field" width="-1" name="friction_value" hidden="0"/>
      <column type="field" width="-1" name="friction_type" hidden="0"/>
      <column type="field" width="-1" name="material" hidden="0"/>
      <column type="field" width="-1" name="sewerage_type" hidden="0"/>
      <column type="field" width="-1" name="zoom_category" hidden="0"/>
      <column type="field" width="-1" name="profile_num" hidden="0"/>
      <column type="field" width="-1" name="original_length" hidden="0"/>
      <column type="field" width="-1" name="connection_node_start_id" hidden="0"/>
      <column type="field" width="-1" name="connection_node_end_id" hidden="0"/>
      <column type="field" width="-1" name="cross_section_definition_id" hidden="0"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:/Users/zaap/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\pipe.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" columnCount="1" name="Pipe view" visibilityExpression="" showLabel="1">
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="General" visibilityExpression="" showLabel="1">
        <attributeEditorField name="pipe_id" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_display_name" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_code" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_calculation_type" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_dist_calc_points" index="-1" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Characteristics" visibilityExpression="" showLabel="1">
        <attributeEditorField name="pipe_invert_level_start_point" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_invert_level_end_point" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_friction_value" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_friction_type" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_material" index="-1" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Cross section definition" visibilityExpression="" showLabel="1">
        <attributeEditorField name="pipe_cross_section_definition_id" index="-1" showLabel="1"/>
        <attributeEditorField name="def_shape" index="-1" showLabel="1"/>
        <attributeEditorField name="def_width" index="-1" showLabel="1"/>
        <attributeEditorField name="def_height" index="-1" showLabel="1"/>
        <attributeEditorField name="def_code" index="-1" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Visualization" visibilityExpression="" showLabel="1">
        <attributeEditorField name="pipe_sewerage_type" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_zoom_category" index="-1" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" columnCount="1" name="Connection nodes" visibilityExpression="" showLabel="1">
        <attributeEditorField name="pipe_connection_node_start_id" index="-1" showLabel="1"/>
        <attributeEditorField name="pipe_connection_node_end_id" index="-1" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_end_id"/>
    <field editable="1" name="connection_node_start_id"/>
    <field editable="1" name="cross_section_definition_id"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
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
    <field editable="1" name="pipe_calculation_type"/>
    <field editable="1" name="pipe_code"/>
    <field editable="0" name="pipe_connection_node_end_id"/>
    <field editable="0" name="pipe_connection_node_start_id"/>
    <field editable="1" name="pipe_cross_section_definition_id"/>
    <field editable="1" name="pipe_display_name"/>
    <field editable="1" name="pipe_dist_calc_points"/>
    <field editable="1" name="pipe_friction_type"/>
    <field editable="1" name="pipe_friction_value"/>
    <field editable="1" name="pipe_id"/>
    <field editable="1" name="pipe_invert_level_end_point"/>
    <field editable="1" name="pipe_invert_level_start_point"/>
    <field editable="1" name="pipe_material"/>
    <field editable="1" name="pipe_original_length"/>
    <field editable="1" name="pipe_pipe_quality"/>
    <field editable="1" name="pipe_profile_num"/>
    <field editable="1" name="pipe_sewerage_type"/>
    <field editable="1" name="pipe_zoom_category"/>
    <field editable="1" name="profile_num"/>
    <field editable="1" name="sewerage_type"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="cross_section_definition_id"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="invert_level_end_point"/>
    <field labelOnTop="0" name="invert_level_start_point"/>
    <field labelOnTop="0" name="material"/>
    <field labelOnTop="0" name="original_length"/>
    <field labelOnTop="0" name="pipe_calculation_type"/>
    <field labelOnTop="0" name="pipe_code"/>
    <field labelOnTop="0" name="pipe_connection_node_end_id"/>
    <field labelOnTop="0" name="pipe_connection_node_start_id"/>
    <field labelOnTop="0" name="pipe_cross_section_definition_id"/>
    <field labelOnTop="0" name="pipe_display_name"/>
    <field labelOnTop="0" name="pipe_dist_calc_points"/>
    <field labelOnTop="0" name="pipe_friction_type"/>
    <field labelOnTop="0" name="pipe_friction_value"/>
    <field labelOnTop="0" name="pipe_id"/>
    <field labelOnTop="0" name="pipe_invert_level_end_point"/>
    <field labelOnTop="0" name="pipe_invert_level_start_point"/>
    <field labelOnTop="0" name="pipe_material"/>
    <field labelOnTop="0" name="pipe_original_length"/>
    <field labelOnTop="0" name="pipe_pipe_quality"/>
    <field labelOnTop="0" name="pipe_profile_num"/>
    <field labelOnTop="0" name="pipe_sewerage_type"/>
    <field labelOnTop="0" name="pipe_zoom_category"/>
    <field labelOnTop="0" name="profile_num"/>
    <field labelOnTop="0" name="sewerage_type"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
