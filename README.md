# Formula Modeling DSL

The Intermediate.dsl file defines a DSL for Formula that represents general
application structure relationships, and can be used as an intermediate representation
of languages like AADL, SysML2 and others. The goal is to be able to convert
various models into a common DSL that can be used to reason about the models.

## aadl_to_intermediate
The aadl_to_intermediate utility is a simplistic Python script that uses regular
expressions to match patterns in an AADL file and generate an intermediate file.
To run it, just supply an input AADL filename and an output 4ML filename:
```
python3 aadl_to_intermediate.py missile_guidance_v5.aadl guidance.4ml
```

## AADL to Intermediate Language Mappings

# Components
Various structures in AADL are mapped into a Component in IL. For example, system, bus, and data are all represented
as components, as are the implementations of these structures. Here is an example system from an AADL file:
```
    system Sensor
        features
            turn_on: in event port;
            turn_off: in event port;
        modes
          on : mode;
          off : initial mode;
          fail : mode;
    end Sensor;
```

The corresponding IL representation is:
```
  Sensor is Component("Sensor").
  Sensor_turn_on is Port(Sensor, "turn_on").
  PortType(Sensor_turn_on, "in", "").
  Sensor_turn_off is Port(Sensor, "turn_off").
  PortType(Sensor_turn_off, "in", "").
  Sensor_on_mode is Condition(Sensor, "mode").
  Sensor_off_mode is Condition(Sensor, "mode").
  InitialCondition(Sensor,Sensor_off_mode).
  Sensor_fail_mode is Condition(Sensor, "mode").
```
The system named "Sensor" is defined as a component. Its features are modeled as ports. Its modes are implemented
as conditions.

# Inheritance
When one AADL structure extends another, this is represented with `Inherit()` in IL:
```
    system GPS extends NavigationalSensorDependentOnRadio
```

```
  Gps is Component("Gps").
  Inherit(NavigationalSensorDependentOnRadio,Gps).
```
There are rules in IL to copy items from a parent into a child in an inheritance relationship, so that
NavigationalSensorDependentOnRadio would include the features and modes of Gps.

# Subcomponents
A component in AADL can contain subcomponents. The component may also require that ports in one subcomponent
be connected to components in another.

Here is portion of an AADL declaration that defines several subcomponents:
```
    system implementation MissileGuidanceUnit.Impl
        subcomponents
            -- systems: sensors, actuators
            gps: system GPS.Impl;
            ins: system INS.Impl;
            st: system SeekerTrackerComponent.Impl;
            fc: system FinControl.Impl;
            -- communication buses
            network_switch: bus MissileGuidanceBus.Impl;
            router: system Router.Impl;
            -- controllers
            controller: system ControllerBoard.Impl;
            mgp: system MissileGuidanceProgram.Impl;
            gs: system GroundStation.Impl;
            cell_net: bus MCCellularNetwork.Impl;
```

Here is the equivalent declaration in IL:
```
  MissileGuidanceUnit_Impl is Component("MissileGuidanceUnit_Impl").
  Inherit(MissileGuidanceUnit, MissileGuidanceUnit_Impl).
  MissileGuidanceUnit_Impl_gps is Subcomponent(MissileGuidanceUnit_Impl, "gps", Gps_Impl).
  MissileGuidanceUnit_Impl_ins is Subcomponent(MissileGuidanceUnit_Impl, "ins", Ins_Impl).
  MissileGuidanceUnit_Impl_st is Subcomponent(MissileGuidanceUnit_Impl, "st", SeekerTrackerComponent_Impl).
  MissileGuidanceUnit_Impl_fc is Subcomponent(MissileGuidanceUnit_Impl, "fc", FinControl_Impl).
  MissileGuidanceUnit_Impl_network_switch is Subcomponent(MissileGuidanceUnit_Impl, "network_switch", MissileGuidanceBus_Impl).
  MissileGuidanceUnit_Impl_router is Subcomponent(MissileGuidanceUnit_Impl, "router", Router_Impl).
  MissileGuidanceUnit_Impl_controller is Subcomponent(MissileGuidanceUnit_Impl, "controller", ControllerBoard_Impl).
  MissileGuidanceUnit_Impl_mgp is Subcomponent(MissileGuidanceUnit_Impl, "mgp", MissileGuidanceProgram_Impl).
  MissileGuidanceUnit_Impl_gs is Subcomponent(MissileGuidanceUnit_Impl, "gs", GroundStation_Impl).
  MissileGuidanceUnit_Impl_cell_net is Subcomponent(MissileGuidanceUnit_Impl, "cell_net", MCCellularNetwork_Impl).
```

# Connections
A connection can also be from the port of one component to the port of another:
```
  op1: port mgp.out_reset -> ins.in_reset;
```
This is represented in IL as a PortConnection:
```
  PortConnection(MissileGuidanceUnit_Impl, "op1", "mgp", "out_reset", "ins", "in_reset").
```

Sometimes a port in a component is connected to a bus - a connection at the component level, instead
of a connection to one of the features of another connection. For example, here is a connection
from a port to a bus:
```
            bac1: bus access gps.TCPA <-> network_switch;
```

This is defined as a BusConnection in IL:
```
  BusConnection(MissileGuidanceUnit_Impl, "bac1", "gps", "TCPA", MissileGuidanceUnit_Impl_network_switch).
```

# Required Connections
In AADL a feature can require the presence of another component. This is currently modeled in IL with
two different required relationships.

```
TCPA: requires bus access MissileGuidanceBus.Impl;
```

First, the `Requires()` structure says that a particular feature requires the presence of another component
as another feature in the containing component.
```
  Requires(Gps, MissileGuidanceBus_Impl).
  Gps_TCPA is Port(Gps, "TCPA").
```

Next, the port carries a requirement that it be connected to a component of the specified type. A rule in IL
can check to ensure that such a connection exists.
```
  PortType(Gps_TCPA, "out", "MissileGuidanceBus.Impl").
  PortRequires(Gps_TCPA, MissileGuidanceBus_Impl).
```

