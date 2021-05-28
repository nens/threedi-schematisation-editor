<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" version="3.16.3-Hannover" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
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
    <field name="use_2d_flow" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_1d_flow" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manhole_storage_area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="output_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_timesteps" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_time" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-dd HH:mm:ss" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd HH:mm:ss" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_date" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="grid_space" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="kmax" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="guess_dams" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flooding_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="advection_1d" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: Do not use advection 1d" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: Use advection 1d" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Experimental advection 1d" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3: Experimental advection 1d" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4: Experimental advection 1d" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5: Experimental advection 1d" value="5" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="6: Experimental advection 1d" value="6" type="QString"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: Do not use advection 2d" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: Use advection 2d" value="1" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chèzy" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_coef_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="water_level_ini_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="max" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="min" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="average" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
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
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_obstacle_height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="embedded_cutoff_threshold" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="epsg_code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timestep_plus" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_angle_1d_advection" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minimum_sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maximum_sim_time_step" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_avg" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wind_shielding_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_0d_inflow" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: do not use 0d inflow" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: use v2_impervious_surface" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: use v2_surface" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size_volume_2d" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_2d_rain" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="max" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="min" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="average" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="interflow_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="control_group_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="simple_infiltration_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="groundwater_settings_id" configurationFlags="None">
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
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="use_2d_flow" index="2"/>
    <alias name="" field="use_1d_flow" index="3"/>
    <alias name="" field="manhole_storage_area" index="4"/>
    <alias name="" field="name" index="5"/>
    <alias name="" field="sim_time_step" index="6"/>
    <alias name="" field="output_time_step" index="7"/>
    <alias name="" field="nr_timesteps" index="8"/>
    <alias name="" field="start_time" index="9"/>
    <alias name="" field="start_date" index="10"/>
    <alias name="" field="grid_space" index="11"/>
    <alias name="" field="dist_calc_points" index="12"/>
    <alias name="" field="kmax" index="13"/>
    <alias name="" field="guess_dams" index="14"/>
    <alias name="" field="table_step_size" index="15"/>
    <alias name="" field="flooding_threshold" index="16"/>
    <alias name="" field="advection_1d" index="17"/>
    <alias name="" field="advection_2d" index="18"/>
    <alias name="" field="dem_file" index="19"/>
    <alias name="" field="frict_type" index="20"/>
    <alias name="" field="frict_coef" index="21"/>
    <alias name="" field="frict_coef_file" index="22"/>
    <alias name="" field="water_level_ini_type" index="23"/>
    <alias name="" field="initial_waterlevel" index="24"/>
    <alias name="" field="initial_waterlevel_file" index="25"/>
    <alias name="" field="interception_global" index="26"/>
    <alias name="" field="interception_file" index="27"/>
    <alias name="" field="dem_obstacle_detection" index="28"/>
    <alias name="" field="dem_obstacle_height" index="29"/>
    <alias name="" field="embedded_cutoff_threshold" index="30"/>
    <alias name="" field="epsg_code" index="31"/>
    <alias name="" field="timestep_plus" index="32"/>
    <alias name="" field="max_angle_1d_advection" index="33"/>
    <alias name="" field="minimum_sim_time_step" index="34"/>
    <alias name="" field="maximum_sim_time_step" index="35"/>
    <alias name="" field="frict_avg" index="36"/>
    <alias name="" field="wind_shielding_file" index="37"/>
    <alias name="" field="use_0d_inflow" index="38"/>
    <alias name="" field="table_step_size_1d" index="39"/>
    <alias name="" field="table_step_size_volume_2d" index="40"/>
    <alias name="" field="use_2d_rain" index="41"/>
    <alias name="" field="initial_groundwater_level" index="42"/>
    <alias name="" field="initial_groundwater_level_file" index="43"/>
    <alias name="" field="initial_groundwater_level_type" index="44"/>
    <alias name="" field="numerical_settings_id" index="45"/>
    <alias name="" field="interflow_settings_id" index="46"/>
    <alias name="" field="control_group_id" index="47"/>
    <alias name="" field="simple_infiltration_settings_id" index="48"/>
    <alias name="" field="groundwater_settings_id" index="49"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="use_2d_flow" expression="" applyOnUpdate="0"/>
    <default field="use_1d_flow" expression="" applyOnUpdate="0"/>
    <default field="manhole_storage_area" expression="" applyOnUpdate="0"/>
    <default field="name" expression="" applyOnUpdate="0"/>
    <default field="sim_time_step" expression="" applyOnUpdate="0"/>
    <default field="output_time_step" expression="" applyOnUpdate="0"/>
    <default field="nr_timesteps" expression="" applyOnUpdate="0"/>
    <default field="start_time" expression=" to_date( now() ) ||  ' 00:00:00'" applyOnUpdate="0"/>
    <default field="start_date" expression=" to_date(now() )" applyOnUpdate="0"/>
    <default field="grid_space" expression="" applyOnUpdate="0"/>
    <default field="dist_calc_points" expression="10000" applyOnUpdate="0"/>
    <default field="kmax" expression="" applyOnUpdate="0"/>
    <default field="guess_dams" expression="0" applyOnUpdate="0"/>
    <default field="table_step_size" expression="0.01" applyOnUpdate="0"/>
    <default field="flooding_threshold" expression="0.001" applyOnUpdate="0"/>
    <default field="advection_1d" expression="" applyOnUpdate="0"/>
    <default field="advection_2d" expression="" applyOnUpdate="0"/>
    <default field="dem_file" expression="" applyOnUpdate="0"/>
    <default field="frict_type" expression="2" applyOnUpdate="0"/>
    <default field="frict_coef" expression="" applyOnUpdate="0"/>
    <default field="frict_coef_file" expression="" applyOnUpdate="0"/>
    <default field="water_level_ini_type" expression="" applyOnUpdate="0"/>
    <default field="initial_waterlevel" expression="" applyOnUpdate="0"/>
    <default field="initial_waterlevel_file" expression="" applyOnUpdate="0"/>
    <default field="interception_global" expression="" applyOnUpdate="0"/>
    <default field="interception_file" expression="" applyOnUpdate="0"/>
    <default field="dem_obstacle_detection" expression="0" applyOnUpdate="0"/>
    <default field="dem_obstacle_height" expression="" applyOnUpdate="0"/>
    <default field="embedded_cutoff_threshold" expression="" applyOnUpdate="0"/>
    <default field="epsg_code" expression="" applyOnUpdate="0"/>
    <default field="timestep_plus" expression="0" applyOnUpdate="0"/>
    <default field="max_angle_1d_advection" expression="" applyOnUpdate="0"/>
    <default field="minimum_sim_time_step" expression="" applyOnUpdate="0"/>
    <default field="maximum_sim_time_step" expression="" applyOnUpdate="0"/>
    <default field="frict_avg" expression="0" applyOnUpdate="0"/>
    <default field="wind_shielding_file" expression="" applyOnUpdate="0"/>
    <default field="use_0d_inflow" expression="" applyOnUpdate="0"/>
    <default field="table_step_size_1d" expression="" applyOnUpdate="0"/>
    <default field="table_step_size_volume_2d" expression="" applyOnUpdate="0"/>
    <default field="use_2d_rain" expression="" applyOnUpdate="0"/>
    <default field="initial_groundwater_level" expression="" applyOnUpdate="0"/>
    <default field="initial_groundwater_level_file" expression="" applyOnUpdate="0"/>
    <default field="initial_groundwater_level_type" expression="" applyOnUpdate="0"/>
    <default field="numerical_settings_id" expression="1" applyOnUpdate="0"/>
    <default field="interflow_settings_id" expression="" applyOnUpdate="0"/>
    <default field="control_group_id" expression="" applyOnUpdate="0"/>
    <default field="simple_infiltration_settings_id" expression="" applyOnUpdate="0"/>
    <default field="groundwater_settings_id" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="use_2d_flow" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="use_1d_flow" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="manhole_storage_area" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="sim_time_step" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="output_time_step" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="nr_timesteps" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="start_time" constraints="5" exp_strength="2" notnull_strength="2" unique_strength="0"/>
    <constraint field="start_date" constraints="5" exp_strength="2" notnull_strength="2" unique_strength="0"/>
    <constraint field="grid_space" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="dist_calc_points" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="kmax" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="guess_dams" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="table_step_size" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="flooding_threshold" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="advection_1d" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="advection_2d" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="dem_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="frict_type" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="frict_coef" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="frict_coef_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="water_level_ini_type" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="initial_waterlevel" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="initial_waterlevel_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="interception_global" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="interception_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="dem_obstacle_detection" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="dem_obstacle_height" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="embedded_cutoff_threshold" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="epsg_code" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="timestep_plus" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="max_angle_1d_advection" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="minimum_sim_time_step" constraints="4" exp_strength="2" notnull_strength="0" unique_strength="0"/>
    <constraint field="maximum_sim_time_step" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="frict_avg" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="wind_shielding_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="use_0d_inflow" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="table_step_size_1d" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="table_step_size_volume_2d" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="use_2d_rain" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="initial_groundwater_level" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="initial_groundwater_level_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="initial_groundwater_level_type" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="numerical_settings_id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="interflow_settings_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="control_group_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="simple_infiltration_settings_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="groundwater_settings_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="use_2d_flow" desc="" exp=""/>
    <constraint field="use_1d_flow" desc="" exp=""/>
    <constraint field="manhole_storage_area" desc="" exp=""/>
    <constraint field="name" desc="" exp=""/>
    <constraint field="sim_time_step" desc="" exp=""/>
    <constraint field="output_time_step" desc="" exp=""/>
    <constraint field="nr_timesteps" desc="" exp=""/>
    <constraint field="start_time" desc="" exp="&quot;start_time&quot;"/>
    <constraint field="start_date" desc="" exp="&quot;start_date&quot; is not null"/>
    <constraint field="grid_space" desc="" exp=""/>
    <constraint field="dist_calc_points" desc="" exp=""/>
    <constraint field="kmax" desc="" exp=""/>
    <constraint field="guess_dams" desc="" exp=""/>
    <constraint field="table_step_size" desc="" exp=""/>
    <constraint field="flooding_threshold" desc="" exp=""/>
    <constraint field="advection_1d" desc="" exp=""/>
    <constraint field="advection_2d" desc="" exp=""/>
    <constraint field="dem_file" desc="" exp=""/>
    <constraint field="frict_type" desc="" exp=""/>
    <constraint field="frict_coef" desc="" exp=""/>
    <constraint field="frict_coef_file" desc="" exp=""/>
    <constraint field="water_level_ini_type" desc="" exp=""/>
    <constraint field="initial_waterlevel" desc="" exp=""/>
    <constraint field="initial_waterlevel_file" desc="" exp=""/>
    <constraint field="interception_global" desc="" exp=""/>
    <constraint field="interception_file" desc="" exp=""/>
    <constraint field="dem_obstacle_detection" desc="" exp=""/>
    <constraint field="dem_obstacle_height" desc="" exp=""/>
    <constraint field="embedded_cutoff_threshold" desc="" exp=""/>
    <constraint field="epsg_code" desc="" exp=""/>
    <constraint field="timestep_plus" desc="" exp=""/>
    <constraint field="max_angle_1d_advection" desc="" exp=""/>
    <constraint field="minimum_sim_time_step" desc="" exp=" &quot;minimum_sim_time_step&quot; &lt; &quot;sim_time_step&quot; "/>
    <constraint field="maximum_sim_time_step" desc="" exp=""/>
    <constraint field="frict_avg" desc="" exp=""/>
    <constraint field="wind_shielding_file" desc="" exp=""/>
    <constraint field="use_0d_inflow" desc="" exp=""/>
    <constraint field="table_step_size_1d" desc="" exp=""/>
    <constraint field="table_step_size_volume_2d" desc="" exp=""/>
    <constraint field="use_2d_rain" desc="" exp=""/>
    <constraint field="initial_groundwater_level" desc="" exp=""/>
    <constraint field="initial_groundwater_level_file" desc="" exp=""/>
    <constraint field="initial_groundwater_level_type" desc="" exp=""/>
    <constraint field="numerical_settings_id" desc="" exp=""/>
    <constraint field="interflow_settings_id" desc="" exp=""/>
    <constraint field="control_group_id" desc="" exp=""/>
    <constraint field="simple_infiltration_settings_id" desc="" exp=""/>
    <constraint field="groundwater_settings_id" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
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
    <attributeEditorContainer name="General" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="id" index="1" showLabel="1"/>
      <attributeEditorField name="name" index="5" showLabel="1"/>
      <attributeEditorField name="use_0d_inflow" index="38" showLabel="1"/>
      <attributeEditorField name="use_1d_flow" index="3" showLabel="1"/>
      <attributeEditorField name="use_2d_rain" index="41" showLabel="1"/>
      <attributeEditorField name="use_2d_flow" index="2" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Grid" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="grid_space" index="11" showLabel="1"/>
      <attributeEditorField name="kmax" index="13" showLabel="1"/>
      <attributeEditorField name="table_step_size" index="15" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Terrain information" visibilityExpression="&quot;advection_1d&quot;" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorContainer name="DEM" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="dem_file" index="19" showLabel="1"/>
        <attributeEditorField name="epsg_code" index="31" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Friction" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="frict_coef_file" index="22" showLabel="1"/>
        <attributeEditorField name="frict_coef" index="21" showLabel="1"/>
        <attributeEditorField name="frict_type" index="20" showLabel="1"/>
        <attributeEditorField name="frict_avg" index="36" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Groundwater" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="initial_groundwater_level_file" index="43" showLabel="1"/>
        <attributeEditorField name="initial_groundwater_level" index="42" showLabel="1"/>
        <attributeEditorField name="initial_groundwater_level_type" index="44" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Initial waterlevel" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="initial_waterlevel_file" index="25" showLabel="1"/>
        <attributeEditorField name="initial_waterlevel" index="24" showLabel="1"/>
        <attributeEditorField name="water_level_ini_type" index="23" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Interception" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="interception_file" index="27" showLabel="1"/>
        <attributeEditorField name="interception_global" index="26" showLabel="1"/>
        <attributeEditorField name="max_interception" index="-1" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Wind" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="wind_shielding_file" index="37" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer name="Time" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="start_date" index="10" showLabel="1"/>
      <attributeEditorField name="start_time" index="9" showLabel="1"/>
      <attributeEditorField name="sim_time_step" index="6" showLabel="1"/>
      <attributeEditorField name="timestep_plus" index="32" showLabel="1"/>
      <attributeEditorField name="minimum_sim_time_step" index="34" showLabel="1"/>
      <attributeEditorField name="maximum_sim_time_step" index="35" showLabel="1"/>
      <attributeEditorField name="nr_timesteps" index="8" showLabel="1"/>
      <attributeEditorField name="output_time_step" index="7" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Settings id's" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="interflow_settings_id" index="46" showLabel="1"/>
      <attributeEditorField name="groundwater_settings_id" index="49" showLabel="1"/>
      <attributeEditorField name="numerical_settings_id" index="45" showLabel="1"/>
      <attributeEditorField name="simple_infiltration_settings_id" index="48" showLabel="1"/>
      <attributeEditorField name="control_group_id" index="47" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Extra options 1D" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="advection_1d" index="17" showLabel="1"/>
      <attributeEditorField name="dist_calc_points" index="12" showLabel="1"/>
      <attributeEditorField name="manhole_storage_area" index="4" showLabel="1"/>
      <attributeEditorField name="max_angle_1d_advection" index="33" showLabel="1"/>
      <attributeEditorField name="table_step_size_1d" index="39" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Extra options 2D" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="advection_2d" index="18" showLabel="1"/>
      <attributeEditorField name="dem_obstacle_detection" index="28" showLabel="1"/>
      <attributeEditorField name="guess_dams" index="14" showLabel="1"/>
      <attributeEditorField name="dem_obstacle_height" index="29" showLabel="1"/>
      <attributeEditorField name="embedded_cutoff_threshold" index="30" showLabel="1"/>
      <attributeEditorField name="flooding_threshold" index="16" showLabel="1"/>
      <attributeEditorField name="table_step_size_volume_2d" index="40" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="advection_1d" editable="1"/>
    <field name="advection_2d" editable="1"/>
    <field name="control_group_id" editable="1"/>
    <field name="dem_file" editable="1"/>
    <field name="dem_obstacle_detection" editable="1"/>
    <field name="dem_obstacle_height" editable="1"/>
    <field name="dist_calc_points" editable="1"/>
    <field name="embedded_cutoff_threshold" editable="1"/>
    <field name="epsg_code" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="flooding_threshold" editable="1"/>
    <field name="frict_avg" editable="1"/>
    <field name="frict_coef" editable="1"/>
    <field name="frict_coef_file" editable="1"/>
    <field name="frict_type" editable="1"/>
    <field name="grid_space" editable="1"/>
    <field name="groundwater_settings_id" editable="1"/>
    <field name="guess_dams" editable="1"/>
    <field name="id" editable="1"/>
    <field name="initial_groundwater_level" editable="1"/>
    <field name="initial_groundwater_level_file" editable="1"/>
    <field name="initial_groundwater_level_type" editable="1"/>
    <field name="initial_waterlevel" editable="1"/>
    <field name="initial_waterlevel_file" editable="1"/>
    <field name="interception_file" editable="1"/>
    <field name="interception_global" editable="1"/>
    <field name="interflow_settings_id" editable="1"/>
    <field name="kmax" editable="1"/>
    <field name="manhole_storage_area" editable="1"/>
    <field name="max_angle_1d_advection" editable="1"/>
    <field name="max_interception" editable="1"/>
    <field name="max_interception_file" editable="1"/>
    <field name="maximum_sim_time_step" editable="1"/>
    <field name="minimum_sim_time_step" editable="1"/>
    <field name="name" editable="1"/>
    <field name="nr_timesteps" editable="1"/>
    <field name="numerical_settings_id" editable="1"/>
    <field name="output_time_step" editable="1"/>
    <field name="sim_time_step" editable="1"/>
    <field name="simple_infiltration_settings_id" editable="1"/>
    <field name="start_date" editable="1"/>
    <field name="start_time" editable="1"/>
    <field name="table_step_size" editable="1"/>
    <field name="table_step_size_1d" editable="1"/>
    <field name="table_step_size_volume_2d" editable="1"/>
    <field name="timestep_plus" editable="1"/>
    <field name="use_0d_inflow" editable="1"/>
    <field name="use_1d_flow" editable="1"/>
    <field name="use_2d_flow" editable="1"/>
    <field name="use_2d_rain" editable="1"/>
    <field name="water_level_ini_type" editable="1"/>
    <field name="wind_shielding_file" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="advection_1d" labelOnTop="0"/>
    <field name="advection_2d" labelOnTop="0"/>
    <field name="control_group_id" labelOnTop="0"/>
    <field name="dem_file" labelOnTop="0"/>
    <field name="dem_obstacle_detection" labelOnTop="0"/>
    <field name="dem_obstacle_height" labelOnTop="0"/>
    <field name="dist_calc_points" labelOnTop="0"/>
    <field name="embedded_cutoff_threshold" labelOnTop="0"/>
    <field name="epsg_code" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="flooding_threshold" labelOnTop="0"/>
    <field name="frict_avg" labelOnTop="0"/>
    <field name="frict_coef" labelOnTop="0"/>
    <field name="frict_coef_file" labelOnTop="0"/>
    <field name="frict_type" labelOnTop="0"/>
    <field name="grid_space" labelOnTop="0"/>
    <field name="groundwater_settings_id" labelOnTop="0"/>
    <field name="guess_dams" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="initial_groundwater_level" labelOnTop="0"/>
    <field name="initial_groundwater_level_file" labelOnTop="0"/>
    <field name="initial_groundwater_level_type" labelOnTop="0"/>
    <field name="initial_waterlevel" labelOnTop="0"/>
    <field name="initial_waterlevel_file" labelOnTop="0"/>
    <field name="interception_file" labelOnTop="0"/>
    <field name="interception_global" labelOnTop="0"/>
    <field name="interflow_settings_id" labelOnTop="0"/>
    <field name="kmax" labelOnTop="0"/>
    <field name="manhole_storage_area" labelOnTop="0"/>
    <field name="max_angle_1d_advection" labelOnTop="0"/>
    <field name="max_interception" labelOnTop="0"/>
    <field name="max_interception_file" labelOnTop="0"/>
    <field name="maximum_sim_time_step" labelOnTop="0"/>
    <field name="minimum_sim_time_step" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="nr_timesteps" labelOnTop="0"/>
    <field name="numerical_settings_id" labelOnTop="0"/>
    <field name="output_time_step" labelOnTop="0"/>
    <field name="sim_time_step" labelOnTop="0"/>
    <field name="simple_infiltration_settings_id" labelOnTop="0"/>
    <field name="start_date" labelOnTop="0"/>
    <field name="start_time" labelOnTop="0"/>
    <field name="table_step_size" labelOnTop="0"/>
    <field name="table_step_size_1d" labelOnTop="0"/>
    <field name="table_step_size_volume_2d" labelOnTop="0"/>
    <field name="timestep_plus" labelOnTop="0"/>
    <field name="use_0d_inflow" labelOnTop="0"/>
    <field name="use_1d_flow" labelOnTop="0"/>
    <field name="use_2d_flow" labelOnTop="0"/>
    <field name="use_2d_rain" labelOnTop="0"/>
    <field name="water_level_ini_type" labelOnTop="0"/>
    <field name="wind_shielding_file" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
