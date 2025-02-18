<?xml version='1.0' encoding='utf-8'?>
<qgis><fieldConfiguration>
    <field configurationFlags="NoFlag" name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cfl_strictness_factor_1d">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cfl_strictness_factor_2d">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="convergence_cg">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="convergence_eps">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="flow_direction_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="friction_shallow_water_depth_correction">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Off" />
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Max between average and divided channel based friction" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Always linearized" />
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Linearizes the depth based on a weighted average" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="general_numerical_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="time_integration_method">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Euler implicit" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="limiter_waterlevel_gradient_1d">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="1" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="0" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="limiter_waterlevel_gradient_2d">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="1" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="0" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="limiter_slope_crossectional_area_2d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Off" />
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Higher order scheme" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Cross-sections treated as upwind method volume/surface area" />
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Combination / thin water layer approach" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="limiter_slope_friction_2d">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="1" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="0" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="max_non_linear_newton_iterations">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="0" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="max_degree_gauss_seidel">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="5" type="QString" name="5: For surface 2D flow only" />
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: For 1D and 2D flow" />
              </Option>
              <Option type="Map">
                <Option value="70" type="QString" name="70: For surface 1D, 2D surface and groundwater flow or higher" />
              </Option>
              <Option type="Map">
                <Option value="700" type="QString" name="700: For 1D flow" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="min_friction_velocity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="min_surface_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="use_preconditioner_cg">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNullState" />
            <Option value="1" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="0" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="preissmann_slot">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="pump_implicit_ratio">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="limiter_slope_thin_water_layer">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="use_of_cg">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="1" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="use_nested_newton">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: For schematisations without closed cross-sections" />
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: For schematisation with closed cross-sections" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="flooding_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>