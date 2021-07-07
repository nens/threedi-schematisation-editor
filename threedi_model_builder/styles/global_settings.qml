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
    <field name="use_2d_flow" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_1d_flow" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manhole_storage_area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="output_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_timesteps" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_time" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="yyyy-MM-dd HH:mm:ss" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd HH:mm:ss" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_date" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="yyyy-MM-dd" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="grid_space" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="kmax" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="guess_dams" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flooding_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="advection_1d" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Do not use advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Use advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Experimental advection 1d"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="advection_2d" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Do not use advection 2d"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Use advection 2d"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_coef" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_coef_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="water_level_ini_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="max"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="min"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="average"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="interception_global" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="interception_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="dem_obstacle_detection" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_obstacle_height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="embedded_cutoff_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="epsg_code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timestep_plus" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_angle_1d_advection" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minimum_sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maximum_sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_avg" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wind_shielding_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_0d_inflow" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: do not use 0d inflow"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: use v2_impervious_surface"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: use v2_surface"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size_1d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size_volume_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_2d_rain" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="max"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="min"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="average"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="numerical_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="interflow_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="control_group_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="simple_infiltration_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="groundwater_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="use_2d_flow" index="2" name=""/>
    <alias field="use_1d_flow" index="3" name=""/>
    <alias field="manhole_storage_area" index="4" name=""/>
    <alias field="name" index="5" name=""/>
    <alias field="sim_time_step" index="6" name=""/>
    <alias field="output_time_step" index="7" name=""/>
    <alias field="nr_timesteps" index="8" name=""/>
    <alias field="start_time" index="9" name=""/>
    <alias field="start_date" index="10" name=""/>
    <alias field="grid_space" index="11" name=""/>
    <alias field="dist_calc_points" index="12" name=""/>
    <alias field="kmax" index="13" name=""/>
    <alias field="guess_dams" index="14" name=""/>
    <alias field="table_step_size" index="15" name=""/>
    <alias field="flooding_threshold" index="16" name=""/>
    <alias field="advection_1d" index="17" name=""/>
    <alias field="advection_2d" index="18" name=""/>
    <alias field="dem_file" index="19" name=""/>
    <alias field="frict_type" index="20" name=""/>
    <alias field="frict_coef" index="21" name=""/>
    <alias field="frict_coef_file" index="22" name=""/>
    <alias field="water_level_ini_type" index="23" name=""/>
    <alias field="initial_waterlevel" index="24" name=""/>
    <alias field="initial_waterlevel_file" index="25" name=""/>
    <alias field="interception_global" index="26" name=""/>
    <alias field="interception_file" index="27" name=""/>
    <alias field="dem_obstacle_detection" index="28" name=""/>
    <alias field="dem_obstacle_height" index="29" name=""/>
    <alias field="embedded_cutoff_threshold" index="30" name=""/>
    <alias field="epsg_code" index="31" name=""/>
    <alias field="timestep_plus" index="32" name=""/>
    <alias field="max_angle_1d_advection" index="33" name=""/>
    <alias field="minimum_sim_time_step" index="34" name=""/>
    <alias field="maximum_sim_time_step" index="35" name=""/>
    <alias field="frict_avg" index="36" name=""/>
    <alias field="wind_shielding_file" index="37" name=""/>
    <alias field="use_0d_inflow" index="38" name=""/>
    <alias field="table_step_size_1d" index="39" name=""/>
    <alias field="table_step_size_volume_2d" index="40" name=""/>
    <alias field="use_2d_rain" index="41" name=""/>
    <alias field="initial_groundwater_level" index="42" name=""/>
    <alias field="initial_groundwater_level_file" index="43" name=""/>
    <alias field="initial_groundwater_level_type" index="44" name=""/>
    <alias field="numerical_settings_id" index="45" name=""/>
    <alias field="interflow_settings_id" index="46" name=""/>
    <alias field="control_group_id" index="47" name=""/>
    <alias field="simple_infiltration_settings_id" index="48" name=""/>
    <alias field="groundwater_settings_id" index="49" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="use_2d_flow"/>
    <default expression="" applyOnUpdate="0" field="use_1d_flow"/>
    <default expression="" applyOnUpdate="0" field="manhole_storage_area"/>
    <default expression="" applyOnUpdate="0" field="name"/>
    <default expression="" applyOnUpdate="0" field="sim_time_step"/>
    <default expression="" applyOnUpdate="0" field="output_time_step"/>
    <default expression="" applyOnUpdate="0" field="nr_timesteps"/>
    <default expression=" to_date( now() ) ||  ' 00:00:00'" applyOnUpdate="0" field="start_time"/>
    <default expression=" to_date(now() )" applyOnUpdate="0" field="start_date"/>
    <default expression="" applyOnUpdate="0" field="grid_space"/>
    <default expression="10000" applyOnUpdate="0" field="dist_calc_points"/>
    <default expression="" applyOnUpdate="0" field="kmax"/>
    <default expression="0" applyOnUpdate="0" field="guess_dams"/>
    <default expression="0.01" applyOnUpdate="0" field="table_step_size"/>
    <default expression="0.001" applyOnUpdate="0" field="flooding_threshold"/>
    <default expression="" applyOnUpdate="0" field="advection_1d"/>
    <default expression="" applyOnUpdate="0" field="advection_2d"/>
    <default expression="" applyOnUpdate="0" field="dem_file"/>
    <default expression="2" applyOnUpdate="0" field="frict_type"/>
    <default expression="" applyOnUpdate="0" field="frict_coef"/>
    <default expression="" applyOnUpdate="0" field="frict_coef_file"/>
    <default expression="" applyOnUpdate="0" field="water_level_ini_type"/>
    <default expression="" applyOnUpdate="0" field="initial_waterlevel"/>
    <default expression="" applyOnUpdate="0" field="initial_waterlevel_file"/>
    <default expression="" applyOnUpdate="0" field="interception_global"/>
    <default expression="" applyOnUpdate="0" field="interception_file"/>
    <default expression="0" applyOnUpdate="0" field="dem_obstacle_detection"/>
    <default expression="" applyOnUpdate="0" field="dem_obstacle_height"/>
    <default expression="" applyOnUpdate="0" field="embedded_cutoff_threshold"/>
    <default expression="" applyOnUpdate="0" field="epsg_code"/>
    <default expression="0" applyOnUpdate="0" field="timestep_plus"/>
    <default expression="" applyOnUpdate="0" field="max_angle_1d_advection"/>
    <default expression="" applyOnUpdate="0" field="minimum_sim_time_step"/>
    <default expression="" applyOnUpdate="0" field="maximum_sim_time_step"/>
    <default expression="0" applyOnUpdate="0" field="frict_avg"/>
    <default expression="" applyOnUpdate="0" field="wind_shielding_file"/>
    <default expression="" applyOnUpdate="0" field="use_0d_inflow"/>
    <default expression="" applyOnUpdate="0" field="table_step_size_1d"/>
    <default expression="" applyOnUpdate="0" field="table_step_size_volume_2d"/>
    <default expression="" applyOnUpdate="0" field="use_2d_rain"/>
    <default expression="" applyOnUpdate="0" field="initial_groundwater_level"/>
    <default expression="" applyOnUpdate="0" field="initial_groundwater_level_file"/>
    <default expression="" applyOnUpdate="0" field="initial_groundwater_level_type"/>
    <default expression="1" applyOnUpdate="0" field="numerical_settings_id"/>
    <default expression="" applyOnUpdate="0" field="interflow_settings_id"/>
    <default expression="" applyOnUpdate="0" field="control_group_id"/>
    <default expression="" applyOnUpdate="0" field="simple_infiltration_settings_id"/>
    <default expression="" applyOnUpdate="0" field="groundwater_settings_id"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_2d_flow" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_1d_flow" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="manhole_storage_area" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="name" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="sim_time_step" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="output_time_step" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="nr_timesteps" unique_strength="0"/>
    <constraint constraints="5" exp_strength="2" notnull_strength="2" field="start_time" unique_strength="0"/>
    <constraint constraints="5" exp_strength="2" notnull_strength="2" field="start_date" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="grid_space" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="dist_calc_points" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="kmax" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="guess_dams" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="table_step_size" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="flooding_threshold" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="advection_1d" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="advection_2d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="dem_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="frict_type" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="frict_coef" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="frict_coef_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="water_level_ini_type" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="initial_waterlevel" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="initial_waterlevel_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="interception_global" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="interception_file" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="dem_obstacle_detection" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="dem_obstacle_height" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="embedded_cutoff_threshold" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="epsg_code" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="timestep_plus" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="max_angle_1d_advection" unique_strength="0"/>
    <constraint constraints="4" exp_strength="2" notnull_strength="0" field="minimum_sim_time_step" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="maximum_sim_time_step" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="frict_avg" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="wind_shielding_file" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_0d_inflow" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="table_step_size_1d" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="table_step_size_volume_2d" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="use_2d_rain" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="initial_groundwater_level" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="initial_groundwater_level_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="initial_groundwater_level_type" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="numerical_settings_id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="interflow_settings_id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="control_group_id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="simple_infiltration_settings_id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="groundwater_settings_id" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="use_2d_flow"/>
    <constraint exp="" desc="" field="use_1d_flow"/>
    <constraint exp="" desc="" field="manhole_storage_area"/>
    <constraint exp="" desc="" field="name"/>
    <constraint exp="" desc="" field="sim_time_step"/>
    <constraint exp="" desc="" field="output_time_step"/>
    <constraint exp="" desc="" field="nr_timesteps"/>
    <constraint exp="&quot;start_time&quot;" desc="" field="start_time"/>
    <constraint exp="&quot;start_date&quot; is not null" desc="" field="start_date"/>
    <constraint exp="" desc="" field="grid_space"/>
    <constraint exp="" desc="" field="dist_calc_points"/>
    <constraint exp="" desc="" field="kmax"/>
    <constraint exp="" desc="" field="guess_dams"/>
    <constraint exp="" desc="" field="table_step_size"/>
    <constraint exp="" desc="" field="flooding_threshold"/>
    <constraint exp="" desc="" field="advection_1d"/>
    <constraint exp="" desc="" field="advection_2d"/>
    <constraint exp="" desc="" field="dem_file"/>
    <constraint exp="" desc="" field="frict_type"/>
    <constraint exp="" desc="" field="frict_coef"/>
    <constraint exp="" desc="" field="frict_coef_file"/>
    <constraint exp="" desc="" field="water_level_ini_type"/>
    <constraint exp="" desc="" field="initial_waterlevel"/>
    <constraint exp="" desc="" field="initial_waterlevel_file"/>
    <constraint exp="" desc="" field="interception_global"/>
    <constraint exp="" desc="" field="interception_file"/>
    <constraint exp="" desc="" field="dem_obstacle_detection"/>
    <constraint exp="" desc="" field="dem_obstacle_height"/>
    <constraint exp="" desc="" field="embedded_cutoff_threshold"/>
    <constraint exp="" desc="" field="epsg_code"/>
    <constraint exp="" desc="" field="timestep_plus"/>
    <constraint exp="" desc="" field="max_angle_1d_advection"/>
    <constraint exp=" &quot;minimum_sim_time_step&quot; &lt; &quot;sim_time_step&quot; " desc="" field="minimum_sim_time_step"/>
    <constraint exp="" desc="" field="maximum_sim_time_step"/>
    <constraint exp="" desc="" field="frict_avg"/>
    <constraint exp="" desc="" field="wind_shielding_file"/>
    <constraint exp="" desc="" field="use_0d_inflow"/>
    <constraint exp="" desc="" field="table_step_size_1d"/>
    <constraint exp="" desc="" field="table_step_size_volume_2d"/>
    <constraint exp="" desc="" field="use_2d_rain"/>
    <constraint exp="" desc="" field="initial_groundwater_level"/>
    <constraint exp="" desc="" field="initial_groundwater_level_file"/>
    <constraint exp="" desc="" field="initial_groundwater_level_type"/>
    <constraint exp="" desc="" field="numerical_settings_id"/>
    <constraint exp="" desc="" field="interflow_settings_id"/>
    <constraint exp="" desc="" field="control_group_id"/>
    <constraint exp="" desc="" field="simple_infiltration_settings_id"/>
    <constraint exp="" desc="" field="groundwater_settings_id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="use_2d_flow"/>
      <column width="-1" hidden="0" type="field" name="use_1d_flow"/>
      <column width="-1" hidden="0" type="field" name="manhole_storage_area"/>
      <column width="-1" hidden="0" type="field" name="name"/>
      <column width="-1" hidden="0" type="field" name="sim_time_step"/>
      <column width="-1" hidden="0" type="field" name="output_time_step"/>
      <column width="-1" hidden="0" type="field" name="nr_timesteps"/>
      <column width="-1" hidden="0" type="field" name="start_time"/>
      <column width="-1" hidden="0" type="field" name="start_date"/>
      <column width="-1" hidden="0" type="field" name="grid_space"/>
      <column width="-1" hidden="0" type="field" name="dist_calc_points"/>
      <column width="-1" hidden="0" type="field" name="kmax"/>
      <column width="-1" hidden="0" type="field" name="guess_dams"/>
      <column width="-1" hidden="0" type="field" name="table_step_size"/>
      <column width="-1" hidden="0" type="field" name="flooding_threshold"/>
      <column width="-1" hidden="0" type="field" name="advection_1d"/>
      <column width="-1" hidden="0" type="field" name="advection_2d"/>
      <column width="-1" hidden="0" type="field" name="dem_file"/>
      <column width="-1" hidden="0" type="field" name="frict_type"/>
      <column width="-1" hidden="0" type="field" name="frict_coef"/>
      <column width="-1" hidden="0" type="field" name="frict_coef_file"/>
      <column width="-1" hidden="0" type="field" name="water_level_ini_type"/>
      <column width="-1" hidden="0" type="field" name="initial_waterlevel"/>
      <column width="-1" hidden="0" type="field" name="initial_waterlevel_file"/>
      <column width="-1" hidden="0" type="field" name="interception_global"/>
      <column width="-1" hidden="0" type="field" name="interception_file"/>
      <column width="-1" hidden="0" type="field" name="dem_obstacle_detection"/>
      <column width="-1" hidden="0" type="field" name="dem_obstacle_height"/>
      <column width="-1" hidden="0" type="field" name="embedded_cutoff_threshold"/>
      <column width="-1" hidden="0" type="field" name="epsg_code"/>
      <column width="-1" hidden="0" type="field" name="timestep_plus"/>
      <column width="-1" hidden="0" type="field" name="max_angle_1d_advection"/>
      <column width="-1" hidden="0" type="field" name="minimum_sim_time_step"/>
      <column width="-1" hidden="0" type="field" name="maximum_sim_time_step"/>
      <column width="-1" hidden="0" type="field" name="frict_avg"/>
      <column width="-1" hidden="0" type="field" name="wind_shielding_file"/>
      <column width="-1" hidden="0" type="field" name="use_0d_inflow"/>
      <column width="-1" hidden="0" type="field" name="table_step_size_1d"/>
      <column width="-1" hidden="0" type="field" name="table_step_size_volume_2d"/>
      <column width="-1" hidden="0" type="field" name="use_2d_rain"/>
      <column width="-1" hidden="0" type="field" name="initial_groundwater_level"/>
      <column width="-1" hidden="0" type="field" name="initial_groundwater_level_file"/>
      <column width="-1" hidden="0" type="field" name="initial_groundwater_level_type"/>
      <column width="-1" hidden="0" type="field" name="numerical_settings_id"/>
      <column width="-1" hidden="0" type="field" name="interflow_settings_id"/>
      <column width="-1" hidden="0" type="field" name="control_group_id"/>
      <column width="-1" hidden="0" type="field" name="simple_infiltration_settings_id"/>
      <column width="-1" hidden="0" type="field" name="groundwater_settings_id"/>
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
      <attributeEditorField showLabel="1" index="5" name="name"/>
      <attributeEditorField showLabel="1" index="38" name="use_0d_inflow"/>
      <attributeEditorField showLabel="1" index="3" name="use_1d_flow"/>
      <attributeEditorField showLabel="1" index="41" name="use_2d_rain"/>
      <attributeEditorField showLabel="1" index="2" name="use_2d_flow"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Grid" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="11" name="grid_space"/>
      <attributeEditorField showLabel="1" index="13" name="kmax"/>
      <attributeEditorField showLabel="1" index="15" name="table_step_size"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="&quot;advection_1d&quot;" columnCount="1" name="Terrain information" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="DEM" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="19" name="dem_file"/>
        <attributeEditorField showLabel="1" index="31" name="epsg_code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Friction" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="22" name="frict_coef_file"/>
        <attributeEditorField showLabel="1" index="21" name="frict_coef"/>
        <attributeEditorField showLabel="1" index="20" name="frict_type"/>
        <attributeEditorField showLabel="1" index="36" name="frict_avg"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Groundwater" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="43" name="initial_groundwater_level_file"/>
        <attributeEditorField showLabel="1" index="42" name="initial_groundwater_level"/>
        <attributeEditorField showLabel="1" index="44" name="initial_groundwater_level_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Initial waterlevel" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="25" name="initial_waterlevel_file"/>
        <attributeEditorField showLabel="1" index="24" name="initial_waterlevel"/>
        <attributeEditorField showLabel="1" index="23" name="water_level_ini_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Interception" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="27" name="interception_file"/>
        <attributeEditorField showLabel="1" index="26" name="interception_global"/>
        <attributeEditorField showLabel="1" index="-1" name="max_interception"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Wind" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="37" name="wind_shielding_file"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Time" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="10" name="start_date"/>
      <attributeEditorField showLabel="1" index="9" name="start_time"/>
      <attributeEditorField showLabel="1" index="6" name="sim_time_step"/>
      <attributeEditorField showLabel="1" index="32" name="timestep_plus"/>
      <attributeEditorField showLabel="1" index="34" name="minimum_sim_time_step"/>
      <attributeEditorField showLabel="1" index="35" name="maximum_sim_time_step"/>
      <attributeEditorField showLabel="1" index="8" name="nr_timesteps"/>
      <attributeEditorField showLabel="1" index="7" name="output_time_step"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Settings id's" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="46" name="interflow_settings_id"/>
      <attributeEditorField showLabel="1" index="49" name="groundwater_settings_id"/>
      <attributeEditorField showLabel="1" index="45" name="numerical_settings_id"/>
      <attributeEditorField showLabel="1" index="48" name="simple_infiltration_settings_id"/>
      <attributeEditorField showLabel="1" index="47" name="control_group_id"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Extra options 1D" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="17" name="advection_1d"/>
      <attributeEditorField showLabel="1" index="12" name="dist_calc_points"/>
      <attributeEditorField showLabel="1" index="4" name="manhole_storage_area"/>
      <attributeEditorField showLabel="1" index="33" name="max_angle_1d_advection"/>
      <attributeEditorField showLabel="1" index="39" name="table_step_size_1d"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Extra options 2D" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="18" name="advection_2d"/>
      <attributeEditorField showLabel="1" index="28" name="dem_obstacle_detection"/>
      <attributeEditorField showLabel="1" index="14" name="guess_dams"/>
      <attributeEditorField showLabel="1" index="29" name="dem_obstacle_height"/>
      <attributeEditorField showLabel="1" index="30" name="embedded_cutoff_threshold"/>
      <attributeEditorField showLabel="1" index="16" name="flooding_threshold"/>
      <attributeEditorField showLabel="1" index="40" name="table_step_size_volume_2d"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="advection_1d"/>
    <field editable="1" name="advection_2d"/>
    <field editable="1" name="control_group_id"/>
    <field editable="1" name="dem_file"/>
    <field editable="1" name="dem_obstacle_detection"/>
    <field editable="1" name="dem_obstacle_height"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="embedded_cutoff_threshold"/>
    <field editable="1" name="epsg_code"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="flooding_threshold"/>
    <field editable="1" name="frict_avg"/>
    <field editable="1" name="frict_coef"/>
    <field editable="1" name="frict_coef_file"/>
    <field editable="1" name="frict_type"/>
    <field editable="1" name="grid_space"/>
    <field editable="1" name="groundwater_settings_id"/>
    <field editable="1" name="guess_dams"/>
    <field editable="1" name="id"/>
    <field editable="1" name="initial_groundwater_level"/>
    <field editable="1" name="initial_groundwater_level_file"/>
    <field editable="1" name="initial_groundwater_level_type"/>
    <field editable="1" name="initial_waterlevel"/>
    <field editable="1" name="initial_waterlevel_file"/>
    <field editable="1" name="interception_file"/>
    <field editable="1" name="interception_global"/>
    <field editable="1" name="interflow_settings_id"/>
    <field editable="1" name="kmax"/>
    <field editable="1" name="manhole_storage_area"/>
    <field editable="1" name="max_angle_1d_advection"/>
    <field editable="1" name="max_interception"/>
    <field editable="1" name="max_interception_file"/>
    <field editable="1" name="maximum_sim_time_step"/>
    <field editable="1" name="minimum_sim_time_step"/>
    <field editable="1" name="name"/>
    <field editable="1" name="nr_timesteps"/>
    <field editable="1" name="numerical_settings_id"/>
    <field editable="1" name="output_time_step"/>
    <field editable="1" name="sim_time_step"/>
    <field editable="1" name="simple_infiltration_settings_id"/>
    <field editable="1" name="start_date"/>
    <field editable="1" name="start_time"/>
    <field editable="1" name="table_step_size"/>
    <field editable="1" name="table_step_size_1d"/>
    <field editable="1" name="table_step_size_volume_2d"/>
    <field editable="1" name="timestep_plus"/>
    <field editable="1" name="use_0d_inflow"/>
    <field editable="1" name="use_1d_flow"/>
    <field editable="1" name="use_2d_flow"/>
    <field editable="1" name="use_2d_rain"/>
    <field editable="1" name="water_level_ini_type"/>
    <field editable="1" name="wind_shielding_file"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="advection_1d"/>
    <field labelOnTop="0" name="advection_2d"/>
    <field labelOnTop="0" name="control_group_id"/>
    <field labelOnTop="0" name="dem_file"/>
    <field labelOnTop="0" name="dem_obstacle_detection"/>
    <field labelOnTop="0" name="dem_obstacle_height"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="embedded_cutoff_threshold"/>
    <field labelOnTop="0" name="epsg_code"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="flooding_threshold"/>
    <field labelOnTop="0" name="frict_avg"/>
    <field labelOnTop="0" name="frict_coef"/>
    <field labelOnTop="0" name="frict_coef_file"/>
    <field labelOnTop="0" name="frict_type"/>
    <field labelOnTop="0" name="grid_space"/>
    <field labelOnTop="0" name="groundwater_settings_id"/>
    <field labelOnTop="0" name="guess_dams"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="initial_groundwater_level"/>
    <field labelOnTop="0" name="initial_groundwater_level_file"/>
    <field labelOnTop="0" name="initial_groundwater_level_type"/>
    <field labelOnTop="0" name="initial_waterlevel"/>
    <field labelOnTop="0" name="initial_waterlevel_file"/>
    <field labelOnTop="0" name="interception_file"/>
    <field labelOnTop="0" name="interception_global"/>
    <field labelOnTop="0" name="interflow_settings_id"/>
    <field labelOnTop="0" name="kmax"/>
    <field labelOnTop="0" name="manhole_storage_area"/>
    <field labelOnTop="0" name="max_angle_1d_advection"/>
    <field labelOnTop="0" name="max_interception"/>
    <field labelOnTop="0" name="max_interception_file"/>
    <field labelOnTop="0" name="maximum_sim_time_step"/>
    <field labelOnTop="0" name="minimum_sim_time_step"/>
    <field labelOnTop="0" name="name"/>
    <field labelOnTop="0" name="nr_timesteps"/>
    <field labelOnTop="0" name="numerical_settings_id"/>
    <field labelOnTop="0" name="output_time_step"/>
    <field labelOnTop="0" name="sim_time_step"/>
    <field labelOnTop="0" name="simple_infiltration_settings_id"/>
    <field labelOnTop="0" name="start_date"/>
    <field labelOnTop="0" name="start_time"/>
    <field labelOnTop="0" name="table_step_size"/>
    <field labelOnTop="0" name="table_step_size_1d"/>
    <field labelOnTop="0" name="table_step_size_volume_2d"/>
    <field labelOnTop="0" name="timestep_plus"/>
    <field labelOnTop="0" name="use_0d_inflow"/>
    <field labelOnTop="0" name="use_1d_flow"/>
    <field labelOnTop="0" name="use_2d_flow"/>
    <field labelOnTop="0" name="use_2d_rain"/>
    <field labelOnTop="0" name="water_level_ini_type"/>
    <field labelOnTop="0" name="wind_shielding_file"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
