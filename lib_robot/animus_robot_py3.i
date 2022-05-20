/* animus_robot_py3.i */
%module animus_robot_py3
%include typemaps.i
%include cdata.i

%begin %{
    #define SWIG_PYTHON_STRICT_BYTE_CHAR
%}

%{
   #include "animus_robot.h"
%}

%pragma(java) jniclasscode=%{
  static {
    System.loadLibrary("animus_robot");
  }
%}

%include "animus_robot.h"

%inline %{

  SWIGCDATA Setup(char* p0, int p1) {
     ProtoMessageC protoreq = (ProtoMessageC) { p1, (void*)p0 };
     ProtoMessageC protoret = SetupGo(protoreq);
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA RegisterRobot(char* p0, int p1) {
     ProtoMessageC protoreq = (ProtoMessageC) { p1, (void*)p0 };
     ProtoMessageC protoret = RegisterRobotGo(protoreq);
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA ReadRobotConfig() {
     ProtoMessageC protoret = ReadRobotConfigGo();
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA StartRobotComms(char* p0, int p1) {
     ProtoMessageC protoreq = (ProtoMessageC) { p1, (void*)p0 };
     ProtoMessageC protoret = StartRobotCommsGo(protoreq);
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA GetNextAction(int p0) {
     ProtoMessageC protoret = GetNextActionGo(p0);
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA SetModality(char* p0, int p1, char* p2, int p3) {
     ProtoMessageC protoreq = (ProtoMessageC) { p3, (void*)p2 };
     ProtoMessageC protoret = SetModalityGo(p0, p1, protoreq);
     return cdata_void(protoret.data, protoret.len);
  }

  SWIGCDATA CloseRobotComms() {
     ProtoMessageC protoret = CloseRobotCommsGo();
     return cdata_void(protoret.data, protoret.len);
  }
%}

