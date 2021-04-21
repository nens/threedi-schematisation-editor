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
    <rasterrenderer band="1" alphaBand="-1" classificationMin="0" classificationMax="0.5835" opacity="1" nodataColor="" type="singlebandpseudocolor">
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
        <colorrampshader clip="0" colorRampType="INTERPOLATED" classificationMode="1" maximumValue="0.5835" minimumValue="0" labelPrecision="4">
          <colorramp name="[source]" type="gradient">
            <prop k="color1" v="241,238,246,255"/>
            <prop k="color2" v="152,0,67,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;215,181,216,255:0.5;223,101,176,255:0.75;221,28,119,255"/>
          </colorramp>
          <item label="0.0000" value="0" color="#f1eef6" alpha="255"/>
          <item label="0.0759" value="0.075855" color="#e4d1e7" alpha="255"/>
          <item label="0.1517" value="0.15171" color="#d8b2d7" alpha="255"/>
          <item label="0.2276" value="0.227565" color="#dc88c2" alpha="255"/>
          <item label="0.3034" value="0.30342" color="#df5fac" alpha="255"/>
          <item label="0.3793" value="0.379275" color="#de398e" alpha="255"/>
          <item label="0.4551" value="0.45513" color="#d51871" alpha="255"/>
          <item label="0.5252" value="0.52515" color="#b40b58" alpha="255"/>
          <item label="0.5835" value="0.5835" color="#980043" alpha="255"/>
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
