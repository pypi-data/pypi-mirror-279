within FMI.Examples.FMI2.CoSimulation;

model Dahlquist
  "This model implements the Dahlquist test equation."

  import FMI.FMI2.Interfaces.*;
  import FMI.FMI2.Functions.*;

  parameter Modelica.Units.SI.Time startTime = 0.0 annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Modelica.Units.SI.Time stopTime = Modelica.Constants.inf annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Real tolerance = 0.0 annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Boolean visible = false annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Boolean loggingOn = false annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Boolean logToFile = false annotation(Dialog(tab="FMI", group="Parameters"));

  parameter String logFile = getInstanceName() + ".txt" annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Boolean logFMICalls = false annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Modelica.Units.SI.Time communicationStepSize = 0.1 annotation(Dialog(tab="FMI", group="Parameters"));

  parameter Real 'k' = 1;

  RealOutput 'x' annotation (Placement(transformation(extent={ { 600, -10.0 }, { 620, 10.0 } }), iconTransformation(extent={ { 600, -10.0 }, { 620, 10.0 } })));

protected

  FMI.Internal.ModelicaFunctions callbacks = FMI.Internal.ModelicaFunctions();

  FMI.Internal.ExternalFMU instance = FMI.Internal.ExternalFMU(
    callbacks,
    Modelica.Utilities.Files.loadResource("modelica://FMI/Resources/FMUs/85f015d"),
    1,
    "Dahlquist",
    getInstanceName(),
    1,
    "{221063D2-EF4A-45FE-B954-B5BFEEA9A59B}",
    visible,
    loggingOn,
    logFMICalls,
    logToFile,
    logFile);
  Boolean initialized;

initial algorithm

  FMI2SetupExperiment(instance, tolerance > 0.0, tolerance, startTime, stopTime < Modelica.Constants.inf, stopTime);

  FMI2SetReal(instance, {3}, 1, {'k'});

  FMI2EnterInitializationMode(instance);


algorithm

  when {initial(), sample(startTime, communicationStepSize)} then


    if time >= communicationStepSize + startTime then
      if not initialized then
        FMI2ExitInitializationMode(instance);
        initialized := true;
      end if;
      FMI2DoStep(instance, time, communicationStepSize, true);
    end if;

    'x' := FMI2GetRealScalar(instance, 1);

  end when;

  annotation (
    Icon(coordinateSystem(
      preserveAspectRatio=false,
      extent={{-600,-100}, {600,100}}),
      graphics={
        Text(extent={{-600,110}, {600,150}}, lineColor={0,0,255}, textString="%name"),
        Rectangle(extent={{-600,-100},{600,100}}, lineColor={95,95,95}, fillColor={255,255,255}, fillPattern=FillPattern.Solid)
      }
    ),
    Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-600,-100}, {600,100}})),
    experiment(StopTime=10.0)
  );
end Dahlquist;