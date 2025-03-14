<?xml version='1.0' encoding='utf-8'?>
<qgis><fieldConfiguration>
    <field configurationFlags="NoFlag" name="id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="tags">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="crest_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="3" type="QString" name="3: Broad crested" />
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: Short crested" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="crest_level">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="4" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="material_id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="-2147483648" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="friction_value">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="4" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chézy" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="discharge_coefficient_positive">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="4" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="discharge_coefficient_negative">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="4" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="connection_node_id_start">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="-2147483648" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="connection_node_id_end">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="-2147483648" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cross_section_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Closed rectangle" />
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Open rectangle" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Circle" />
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Egg" />
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Tabulated rectangle" />
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Tabulated trapezium" />
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: YZ" />
              </Option>
              <Option type="Map">
                <Option value="8" type="QString" name="8: Inverted egg" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cross_section_width">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="3" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cross_section_height">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="-1.7976931348623157e+308" type="double" name="Min" />
            <Option value="3" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="cross_section_table">
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