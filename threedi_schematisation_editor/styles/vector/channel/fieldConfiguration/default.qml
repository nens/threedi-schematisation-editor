<?xml version='1.0' encoding='utf-8'?>
<qgis><fieldConfiguration>
    <field configurationFlags="NoFlag" name="id">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="double" name="Max" />
            <Option value="-2147483648" type="double" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
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
    <field configurationFlags="NoFlag" name="exchange_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="100" type="QString" name="100: Embedded" />
              </Option>
              <Option type="Map">
                <Option value="101" type="QString" name="101: Isolated" />
              </Option>
              <Option type="Map">
                <Option value="102" type="QString" name="102: Connected" />
              </Option>
              <Option type="Map">
                <Option value="105" type="QString" name="105: Double connected" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="calculation_point_distance">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
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
    <field configurationFlags="NoFlag" name="exchange_thickness">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="0" type="double" name="Min" />
            <Option value="3" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="hydraulic_conductivity_in">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="0" type="double" name="Min" />
            <Option value="3" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="hydraulic_conductivity_out">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="1.7976931348623157e+308" type="double" name="Max" />
            <Option value="0" type="double" name="Min" />
            <Option value="3" type="int" name="Precision" />
            <Option value="1" type="double" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>