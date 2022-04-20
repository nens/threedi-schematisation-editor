<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" maxScale="0" version="3.16.9-Hannover" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal enabled="0" mode="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="0" opacity="1" alphaBand="-1" band="1" classificationMax="1032">
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
        <colorrampshader minimumValue="0" classificationMode="2" maximumValue="1032" clip="0" labelPrecision="4" colorRampType="INTERPOLATED">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="240,249,232,255"/>
            <prop k="color2" v="8,104,172,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;186,228,188,255:0.5;123,204,196,255:0.75;67,162,202,255"/>
          </colorramp>
          <item label="0,0000" color="#f0f9e8" alpha="255" value="0"/>
          <item label="114,6667" color="#d8f0d5" alpha="255" value="114.66666666666667"/>
          <item label="229,3333" color="#c0e7c1" alpha="255" value="229.33333333333334"/>
          <item label="344,0000" color="#a5dcbf" alpha="255" value="344"/>
          <item label="458,6667" color="#89d2c2" alpha="255" value="458.6666666666667"/>
          <item label="573,3333" color="#6ec3c6" alpha="255" value="573.3333333333334"/>
          <item label="688,0000" color="#56b0c8" alpha="255" value="688"/>
          <item label="802,6667" color="#3c9cc7" alpha="255" value="802.6666666666667"/>
          <item label="917,3333" color="#2282ba" alpha="255" value="917.3333333333334"/>
          <item label="1032,0000" color="#0868ac" alpha="255" value="1032"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeRed="255" colorizeOn="0" saturation="0" colorizeGreen="128" colorizeStrength="100" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
