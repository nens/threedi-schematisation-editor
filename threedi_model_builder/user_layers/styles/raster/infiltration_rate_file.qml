<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0" version="3.16.4-Hannover" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal mode="0" fetchMode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer band="1" alphaBand="-1" classificationMin="0" classificationMax="480" opacity="1" nodataColor="" type="singlebandpseudocolor">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" colorRampType="INTERPOLATED" classificationMode="1" maximumValue="480" minimumValue="0" labelPrecision="4">
          <colorramp name="[source]" type="gradient">
            <prop k="color1" v="240,249,232,255"/>
            <prop k="color2" v="8,104,172,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;186,228,188,255:0.5;123,204,196,255:0.75;67,162,202,255"/>
          </colorramp>
          <item label="0.0000" value="0" color="#f0f9e8" alpha="255"/>
          <item label="56.4706" value="56.47056" color="#d7f0d4" alpha="255"/>
          <item label="103.5293" value="103.52928" color="#c2e7c2" alpha="255"/>
          <item label="150.5880" value="150.588" color="#aadebe" alpha="255"/>
          <item label="197.6472" value="197.6472" color="#91d5c1" alpha="255"/>
          <item label="244.7059" value="244.70592000000002" color="#79cbc5" alpha="255"/>
          <item label="291.7646" value="291.76464" color="#63bac7" alpha="255"/>
          <item label="338.8234" value="338.82336" color="#4daac9" alpha="255"/>
          <item label="385.8826" value="385.88256" color="#3696c4" alpha="255"/>
          <item label="432.9413" value="432.94128" color="#1f7fb8" alpha="255"/>
          <item label="480.0000" value="480" color="#0868ac" alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
