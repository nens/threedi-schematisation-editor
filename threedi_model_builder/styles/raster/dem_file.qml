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
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="-3.425" opacity="1" alphaBand="-1" band="1" classificationMax="16.9869995">
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
        <colorrampshader minimumValue="-3.425" classificationMode="2" maximumValue="16.9869995" clip="0" labelPrecision="4" colorRampType="INTERPOLATED">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="1,133,113,255"/>
            <prop k="color2" v="166,97,26,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;128,205,193,255:0.5;245,245,245,255:0.75;223,194,125,255"/>
          </colorramp>
          <item label="-3,4250" color="#018571" alpha="255" value="-3.4249999523163"/>
          <item label="-1,1570" color="#39a595" alpha="255" value="-1.157000011867934"/>
          <item label="1,1110" color="#72c5b8" alpha="255" value="1.110999928580433"/>
          <item label="3,3790" color="#a7dbd3" alpha="255" value="3.3789998690288"/>
          <item label="5,6470" color="#dbedea" alpha="255" value="5.646999809477165"/>
          <item label="7,9150" color="#f1eadb" alpha="255" value="7.914999749925531"/>
          <item label="10,1830" color="#e7d3a5" alpha="255" value="10.182999690373899"/>
          <item label="12,4510" color="#d9b772" alpha="255" value="12.450999630822265"/>
          <item label="14,7190" color="#c08c46" alpha="255" value="14.718999571270631"/>
          <item label="16,9870" color="#a6611a" alpha="255" value="16.986999511719"/>
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
