import arcpy
import sys,os
import uuid, json
import __builtin__

class Toolbox(object):

   def __init__(self):
      """Define the toolbox (the name of the toolbox is the name of the
      .pyt file).""";
      self.label = "Toolbox";
      self.alias = "";

      # List of tool classes associated with this toolbox
      self.tools = [
          NavigationService
         ,NavigationDelineationService
         ,UpstreamDownstreamSearchService
         ,PointIndexingService
      ];

class NavigationService(object):
   
   # NavigationService
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "NavigationService"
      self.name  = "NavigationService"
      self.description = "The EPA Office of Water Navigation Service provides standard stream traversal on the NHDPlus hydrology network.  " + \
         "For more information see " +  \
         "<a href='http://www2.epa.gov/waterdata/navigation-service' target='_blank'>" + \
         "EPA service documentation</a>.";
      self.canRunInBackground = False;

   # NavigationService
   def getParameterInfo(self):
      """Define parameter definitions"""
       
      # First parameter
      param0 = arcpy.Parameter(
          displayName="Navigation Type:"
         ,name="pNavigationType"
         ,datatype="String"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param0.value = "Upstream with Tributaries";
      param0.filter.type = "ValueList";
      param0.filter.list = [
          "Upstream with Tributaries"
         ,"Upstream Main Path Only"
         ,"Downstream with Divergences"
         ,"Downstream Main Path Only"
         ,"Point to Point"
         ,"UT"
         ,"UM"
         ,"DD"
         ,"DM"
         ,"PP"
      ];
      
      param1 = arcpy.Parameter(
          displayName="Start NHDPlus Permanent Identifier:"
         ,name="pStartPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param2 = arcpy.Parameter(
          displayName="Start NHDPlus ComID:"
         ,name="pStartComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param3 = arcpy.Parameter(
          displayName="Start Reach Code:"
         ,name="pStartReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param4 = arcpy.Parameter(
          displayName="Start Measure:"
         ,name="pStartMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param5 = arcpy.Parameter(
          displayName="Stop NHDPlus Permanent Identifier:"
         ,name="pStopPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param6 = arcpy.Parameter(
          displayName="Stop NHDPlus ComID:"
         ,name="pStopComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param7 = arcpy.Parameter(
          displayName="Stop Reach Code:"
         ,name="pStopReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param8 = arcpy.Parameter(
          displayName="Stop Measure:"
         ,name="pStopMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param9 = arcpy.Parameter(
          displayName="Maximum Distance (KM):"
         ,name="pMaxDistanceKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      param9.value = 5;
      
      param10 = arcpy.Parameter(
          displayName="Maximum Flow Time (Hour):"
         ,name="pMaxFlowTimeHour"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param11 = arcpy.Parameter(
          displayName="NavigationResults"
         ,name="pNavigationResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      param11.schema.featureTypeRule = "AsSpecified";
      param11.schema.featureType = "Simple";
      param11.schema.geometryTypeRule = "AsSpecified";
      param11.schema.geometryType = "Polyline";
      param11.schema.fieldsRule = "AllNoFIDs";
      
      param12 = arcpy.Parameter(
          displayName="ReturnCode"
         ,name="pReturnCode"
         ,datatype="GPLong"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param13 = arcpy.Parameter(
          displayName="StatusMessage"
         ,name="pStatusMessage"
         ,datatype="GPString"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      params = [
          param0
         ,param1
         ,param2
         ,param3
         ,param4
         ,param5
         ,param6
         ,param7
         ,param8
         ,param9
         ,param10
         ,param11
         ,param12
         ,param13
      ];
      
      return params

   # NavigationService
   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   # NavigationService
   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         return;
      
      if parameters[0].altered:
         if parameters[0].value in [
             "Point to Point"
            ,"PP"
         ]:
            # Turn on stop parameters
            parameters[5].enabled = True;
            parameters[6].enabled = True;
            parameters[7].enabled = True;
            parameters[8].enabled = True;
            # Turn off distance parameters
            parameters[9].enabled = False;
            #parameters[10].enabled = False;
         elif parameters[0].value in [
             "Upstream with Tributaries"
            ,"UT"
            ,"Upstream Main Path Only"
            ,"UM"
            ,"Downstream with Divergences"
            ,"DD"
            ,"Downstream Main Path Only"
            ,"DM"
         ]:
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
         else:
            # set default to UT
            parameters[0].value   = "Upstream with Tributaries";
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
      
      # when startPermanentIdentifier entered
      if parameters[1].altered   \
      and not parameters[1].hasBeenValidated \
      and ( parameters[2].value or parameters[3].value):
         # Blank startComid and startReachCode
         parameters[2].value = None;
         parameters[3].value = None;
      # when startComID entered
      elif parameters[2].altered  \
      and not parameters[2].hasBeenValidated \
      and ( parameters[1].value or parameters[3].value):
         # Blank startPermanentIdentifier and startReachcode
         parameters[1].value = None;
         parameters[3].value = None;
      # when startReachcode entered
      elif parameters[3].altered  \
      and not parameters[3].hasBeenValidated \
      and ( parameters[1].value or parameters[2].value):
         # Blank startPermanentIdentifier and startComID
         parameters[1].value = None;
         parameters[2].value = None;  
         
      # when stopPermanentIdentifier entered
      if parameters[5].altered   \
      and not parameters[5].hasBeenValidated \
      and ( parameters[6].value or parameters[7].value):
         # Blank stopComid and stopReachCode
         parameters[6].value = None;
         parameters[7].value = None;
      # when stopComID entered
      elif parameters[6].altered   \
      and not parameters[6].hasBeenValidated \
      and ( parameters[5].value or parameters[7].value):
         # Blank stopPermanentIdentifier and stopReachcode
         parameters[5].value = None;
         parameters[7].value = None;
      # when stopReachcode entered
      elif parameters[7].altered   \
      and not parameters[7].hasBeenValidated \
      and ( parameters[5].value or parameters[6].value):
         # Blank stopPermanentIdentifier and stopComID
         parameters[5].value = None;
         parameters[6].value = None;
      
      return

   # NavigationService
   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      
      # this is some kludgey esri bs
      if not hasattr(__builtin__, "dz_deployer")  \
      or __builtin__.dz_deployer is False:

         # Verify that a start id has been provided
         if  not parameters[1].valueAsText \
         and not parameters[2].valueAsText \
         and not parameters[3].valueAsText :
            parameters[1].setErrorMessage(
               "Start Permanent Identifier, Start ComID or Start Reach Code is required"
            );
         
         # Verify that a stop id has been provided for PP         
         if parameters[0].valueAsText in ["Point to Point","PP"] \
         and not parameters[5].valueAsText \
         and not parameters[6].valueAsText \
         and not parameters[7].valueAsText :
            parameters[5].setErrorMessage(
               "Stop Permanent Identifier, Stop ComID or Stop Reach Code is required for Point to Point Navigation"
            );
            
         # Verify that ComID is a positive integer
         if parameters[2].value:
            boo_bad = False;
            try:
               num_val = float(parameters[2].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[2].setErrorMessage(
                  "ComID values must be a positive integers"
               );
               
         # Verify that ComID is a positive integer
         if parameters[6].value:
            boo_bad = False;
            try:
               num_val = float(parameters[6].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[6].setErrorMessage(
                  "ComID values must be a positive integers"
               );
         
         # Verify that start measure is numeric between 0 and 100         
         if parameters[4].value:
            boo_bad = False;
            try:
               num_val = float(parameters[4].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[4].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               );
         
         # Verify that stop measure is numeric between 0 and 100 
         if parameters[8].value:
            boo_bad = False;
            try:
               num_val = float(parameters[8].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[8].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               ); 

         # Verify that max distance is a number
         if parameters[9].value:
            boo_bad = False;
            try:
               num_val = float(parameters[9].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[9].setErrorMessage(
                  "Maximum distance values must be a number"
               ); 
         
         # Verify that max flow time is a number
         if parameters[10].value:
            boo_bad = False;
            try:
               num_val = float(parameters[10].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[10].setErrorMessage(
                  "Maximum flow time values must be a number"
               );

      return;

   # NavigationService
   def execute(self, parameters, messages):
      """The source code of the tool."""

      #------------------------------------------------------------------------
      #-- Step 10
      #-- Load variables from form parameters
      #------------------------------------------------------------------------
      str_navigation_orig  = parameters[0].valueAsText;
      str_start_permid     = parameters[1].valueAsText;
      str_start_comid      = parameters[2].valueAsText;
      str_start_reachcode  = parameters[3].valueAsText;
      str_start_measure    = parameters[4].valueAsText;
      
      if parameters[5].enabled:
         str_stop_permid   = parameters[5].valueAsText;
      else:
         str_stop_permid   = None;
         
      if parameters[6].enabled:
         str_stop_comid   = parameters[6].valueAsText;
      else:
         str_stop_comid   = None;
      
      if parameters[7].enabled:
         str_stop_reachcode = parameters[7].valueAsText;
      else:
         str_stop_reachcode = None;
         
      if parameters[8].enabled:
         str_stop_measure  = parameters[8].value;
      else:
         str_stop_measure  = None;
         
      if parameters[9].enabled:
         str_max_distancekm = parameters[9].value;
      else:
         str_max_distancekm = None;
         
      if parameters[10].enabled:
         str_max_flowtimehour = parameters[10].value;
      else:
         str_max_flowtimehour = None;
      
      # Swap verbose checklist names to service abbreviations
      if str_navigation_orig == "Upstream with Tributaries":
         str_navigation_type = "UT";
      elif str_navigation_orig == "Upstream Main Path Only":
         str_navigation_type = "UM";
      elif str_navigation_orig == "Downstream with Divergences":
         str_navigation_type = "DD";
      elif str_navigation_orig == "Downstream Main Path Only":
         str_navigation_type = "DM";
      elif str_navigation_orig == "Point to Point":
         str_navigation_type = "PP";
      else:
         # Allow REST users to submit abbreviations if they want
         str_navigation_type = str_navigation_orig;
         
      #------------------------------------------------------------------------
      #-- Step 20
      #-- Account for silly deployer issues with AGS
      #------------------------------------------------------------------------
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         str_navigation_type  = "UT";
         str_start_permid     = "4709538";
         str_start_comid      = None;
         str_start_reachcode  = None;
         str_start_measure    = "50";
         str_stop_permid      = None;
         str_stop_comid       = None;
         str_stop_reachcode   = None;
         str_stop_measure     = None;
         str_max_distancekm   = "5";
         str_max_flowtimehour = None;
      
      #------------------------------------------------------------------------
      #-- Step 30
      #-- Make variable SQL ready
      #------------------------------------------------------------------------
      if str_start_permid is None:
         str_start_permid = "NULL";
      else:
         str_start_permid = "'" + str_start_permid + "'";
         
      if str_start_comid is None:
         str_start_comid = "NULL";
         
      if str_start_reachcode is None:
         str_start_reachcode = "NULL";
      else:
         str_start_reachcode = "'" + str_start_reachcode + "'";
      
      if str_start_measure is None:
         str_start_measure = "NULL";
      
      if str_stop_permid is None:
         str_stop_permid = "NULL";
      else:
         str_stop_permid = "'" + str_stop_permid + "'";
         
      if str_stop_comid is None:
         str_stop_comid = "NULL";
         
      if str_stop_reachcode is None:
         str_stop_reachcode = "NULL";
      else:
         str_stop_reachcode = "'" + str_stop_reachcode + "'";
      
      if str_stop_measure is None:
         str_stop_measure = "NULL";
         
      if str_max_distancekm is None:
         str_max_distancekm = "NULL";
         
      if str_max_flowtimehour is None:
         str_max_flowtimehour = "NULL";

      #------------------------------------------------------------------------
      #-- Step 40
      #-- Define any workspace parameters
      #-- Note that you may force the workspace to a hard-coded 
      #-- location if desired (this does not bother the AGS deployment)
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying SDE Environment");
      try:
         #arcpy.env.workspace = "C:\esri_dump";
         #arcpy.env.scratchWorkspace = "C:\esri_dump";
         arcpy.env.overwriteOutput = True;

      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 50
      #-- Create the service scratch space
      #------------------------------------------------------------------------
      try:
         scratch_path = arcpy.CreateScratchName(
             "NavigationResults"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         )
         scratch_name = scratch_path.split(os.sep)[-1];
         
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 60
      #-- Create the database connection
      #------------------------------------------------------------------------
      try:
         sde_conn = arcpy.ArcSDESQLExecute("Database Connections\\rad_ags.sde");      
      
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 70
      #-- Generate the transaction id
      #------------------------------------------------------------------------
      str_session_id = '{' + str(uuid.uuid4()) + '}';
      
      #------------------------------------------------------------------------
      #-- Step 80
      #-- Build the PLSQL statement
      #------------------------------------------------------------------------
      sql_statement1 = """
         DECLARE
            num_return_code NUMBER;
            str_status_message VARCHAR2(4000 Char);
            str_session_id VARCHAR2(40 Char);
         BEGIN
            str_session_id := '""" + str_session_id  + """';
            INSERT INTO
            nhdplus_navigation.tmp_navigation_status(
                session_id
               ,session_datestamp
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,nhdplus_navigation.tmp_navigation_status_seq.NEXTVAL
            );
            nhdplus_navigation.navigator_main.navigate(
                pNavigationType           => '""" + str_navigation_type  + """'
               ,pStartComID               => """  + str_start_comid      + """
               ,pStartPermanentIdentifier => """  + str_start_permid     + """
               ,pStartReachcode           => """  + str_start_reachcode  + """
               ,pStartMeasure             => """  + str_start_measure    + """
               ,pStopComID                => """  + str_stop_comid       + """
               ,pStopPermanentIdentifier  => """  + str_stop_permid      + """
               ,pStopReachcode            => """  + str_stop_reachcode   + """
               ,pStopMeasure              => """  + str_stop_measure     + """
               ,pMaxDistanceKm            => """  + str_max_distancekm   + """
               ,pMaxFlowTimeHour          => """  + str_max_flowtimehour + """
               ,pDebug                    => 'FALSE'
               ,pAddFlowlineAttributes    => 'TRUE'
               ,pAddFlowlineGeometry      => 'TRUE'
               ,pReturnCode               => num_return_code
               ,pStatusMessage            => str_status_message
               ,pSessionID                => str_session_id
            );
            COMMIT;
         END;
      """;
      
      #------------------------------------------------------------------------
      #-- Step 90
      #-- Execute the Database Service
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Executing the Service");
      try:
         sde_return = sde_conn.execute(sql_statement1)
      
      except Exception as err:
         arcpy.AddError(err)
         exit -1;
         
      #------------------------------------------------------------------------
      #-- Step 100
      #-- Verify results from the status table
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying Results");
      sql_statement2 = """
         SELECT
          a.return_code
         ,a.status_message
         FROM
         nhdplus_navigation.tmp_navigation_status a
         WHERE
         a.session_id = '""" + str_session_id + """'
      """      
      
      try:
         sde_return = sde_conn.execute(sql_statement2)
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      if sde_return[0][0] <> 0:
         arcpy.AddMessage("   Navigation completed with status code " + str(int(sde_return[0][0])));
         
         # Need to create an empty feature class to please AGS
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name
         );
         arcpy.SetParameterAsText(11,scratch_path);
         
         arcpy.SetParameterAsText(12,int(sde_return[0][0]));
         arcpy.SetParameterAsText(13,sde_return[0][1]);
         return;
                
      #------------------------------------------------------------------------
      #-- Step 110
      #-- Cough out results from the results table
      #-- These endpoints are in the rad_ags schema to avoid schema 
      #-- out of date issues
      #------------------------------------------------------------------------                
      arcpy.AddMessage("   Exporting Results from Database");
      try:
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.NAVIGATION_TMP_RESULTS"
            ,arcpy.env.scratchGDB
            ,scratch_name
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      arcpy.SetParameterAsText(11,scratch_path);
      arcpy.SetParameterAsText(12,0);
      arcpy.SetParameterAsText(13,"");

      arcpy.AddMessage("   Navigation Complete");
      
class NavigationDelineationService(object):

   # NavigationDelineationService
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "NavigationDelineationService"
      self.name  = "NavigationDelineationService"
      self.description = "The EPA Office of Water Navigation Delineation Service provides an areal representation of the " + \
         "navigation process by linking navigated flowlines to associated areal geographies. " + \
         "The service has been optimized to aggregate and return NHDPlus catchments. " + \
         "For more information see " +  \
         "<a href='http://www2.epa.gov/waterdata/navigation-delineation-service' target='_blank'>" + \
         "EPA service documentation</a>.";
      self.canRunInBackground = False

   # NavigationDelineationService
   def getParameterInfo(self):
      """Define parameter definitions"""
       
      # First parameter
      param0 = arcpy.Parameter(
          displayName="Navigation Type:"
         ,name="pNavigationType"
         ,datatype="String"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param0.value = "Upstream with Tributaries";
      param0.filter.type = "ValueList";
      param0.filter.list = [
          "Upstream with Tributaries"
         ,"Upstream Main Path Only"
         ,"Downstream with Divergences"
         ,"Downstream Main Path Only"
         ,"Point to Point"
         ,"UT"
         ,"UM"
         ,"DD"
         ,"DM"
         ,"PP"
      ];
      
      param1 = arcpy.Parameter(
          displayName="Start NHDPlus Permanent Identifier:"
         ,name="pStartPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param2 = arcpy.Parameter(
          displayName="Start NHDPlus ComID:"
         ,name="pStartComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param3 = arcpy.Parameter(
          displayName="Start Reach Code:"
         ,name="pStartReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param4 = arcpy.Parameter(
          displayName="Start Measure:"
         ,name="pStartMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param5 = arcpy.Parameter(
          displayName="Stop NHDPlus Permanent Identifier:"
         ,name="pStopPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param6 = arcpy.Parameter(
          displayName="Stop NHDPlus ComID:"
         ,name="pStopComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param7 = arcpy.Parameter(
          displayName="Stop Reach Code:"
         ,name="pStopReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param8 = arcpy.Parameter(
          displayName="Stop Measure:"
         ,name="pStopMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param9 = arcpy.Parameter(
          displayName="Maximum Distance (KM):"
         ,name="pMaxDistanceKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      param9.value = 5;
      
      param10 = arcpy.Parameter(
          displayName="Maximum Flow Time (Hour):"
         ,name="pMaxFlowTimeHour"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param11 = arcpy.Parameter(
          displayName="Feature Type:"
         ,name="pFeatureType"
         ,datatype="String"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param11.value = "NHDPlus Catchments";
      param11.filter.type = "ValueList";
      param11.filter.list = [
          "NHDPlus Catchments"
      ];
      
      param12 = arcpy.Parameter(
          displayName="Aggregate Features:"
         ,name="pAggregateFeatures"
         ,datatype="GPBoolean"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param12.value = True;
      
      param13 = arcpy.Parameter(
          displayName="Return Navigation Results:"
         ,name="pReturnNavigation"
         ,datatype="GPBoolean"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param13.value = False;
      
      param14 = arcpy.Parameter(
          displayName="Split Initial Catchment:"
         ,name="pSplitInitialCatchment"
         ,datatype="GPBoolean"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      param14.value = False;
      
      param15 = arcpy.Parameter(
          displayName="Delineation Results:"
         ,name="pDelineationResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param16 = arcpy.Parameter(
          displayName="Navigation Results:"
         ,name="pNavigationResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param17 = arcpy.Parameter(
          displayName="ReturnCode"
         ,name="pReturnCode"
         ,datatype="GPLong"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param18 = arcpy.Parameter(
          displayName="StatusMessage"
         ,name="pStatusMessage"
         ,datatype="GPString"
         ,parameterType="Derived"
         ,direction="Output"
      );

      params = [
          param0
         ,param1
         ,param2
         ,param3
         ,param4
         ,param5
         ,param6
         ,param7
         ,param8
         ,param9
         ,param10
         ,param11
         ,param12
         ,param13
         ,param14
         ,param15
         ,param16
         ,param17
         ,param18
      ];
      
      return params

   # NavigationDelineationService
   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   # NavigationDelineationService
   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         return;
         
      if parameters[0].altered:
         if parameters[0].value in [
             "Point to Point"
            ,"PP"
         ]:
            # Turn on stop parameters
            parameters[5].enabled = True;
            parameters[6].enabled = True;
            parameters[7].enabled = True;
            parameters[8].enabled = True;
            # Turn off distance parameters
            parameters[9].enabled = False;
            #parameters[10].enabled = False;
         elif parameters[0].value in [
             "Upstream with Tributaries"
            ,"UT"
            ,"Upstream Main Path Only"
            ,"UM"
            ,"Downstream with Divergences"
            ,"DD"
            ,"Downstream Main Path Only"
            ,"DM"
         ]:
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
         else:
            # set default to UT
            parameters[0].value   = "Upstream with Tributaries";
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
      
      # when startPermanentIdentifier entered
      if parameters[1].altered   \
      and not parameters[1].hasBeenValidated \
      and ( parameters[2].value or parameters[3].value):
         # Blank startComid and startReachCode
         parameters[2].value = None;
         parameters[3].value = None;
      # when startComID entered
      elif parameters[2].altered  \
      and not parameters[2].hasBeenValidated \
      and ( parameters[1].value or parameters[3].value):
         # Blank startPermanentIdentifier and startReachcode
         parameters[1].value = None;
         parameters[3].value = None;
      # when startReachcode entered
      elif parameters[3].altered  \
      and not parameters[3].hasBeenValidated \
      and ( parameters[1].value or parameters[2].value):
         # Blank startPermanentIdentifier and startComID
         parameters[1].value = None;
         parameters[2].value = None;  
         
      # when stopPermanentIdentifier entered
      if parameters[5].altered   \
      and not parameters[5].hasBeenValidated \
      and ( parameters[6].value or parameters[7].value):
         # Blank stopComid and stopReachCode
         parameters[6].value = None;
         parameters[7].value = None;
      # when stopComID entered
      elif parameters[6].altered   \
      and not parameters[6].hasBeenValidated \
      and ( parameters[5].value or parameters[7].value):
         # Blank stopPermanentIdentifier and stopReachcode
         parameters[5].value = None;
         parameters[7].value = None;
      # when stopReachcode entered
      elif parameters[7].altered   \
      and not parameters[7].hasBeenValidated \
      and ( parameters[5].value or parameters[6].value):
         # Blank stopPermanentIdentifier and stopComID
         parameters[5].value = None;
         parameters[6].value = None;
      
      return

   # NavigationDelineationService
   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      
      # this is some kludgey esri bs
      if not hasattr(__builtin__, "dz_deployer")  \
      or __builtin__.dz_deployer is False:
         
         # Verify that a start id has been provided
         if  not parameters[1].valueAsText \
         and not parameters[2].valueAsText \
         and not parameters[3].valueAsText :
            parameters[1].setErrorMessage(
               "Start Permanent Identifier, Start ComID or Start Reach Code is required"
            );
         
         # Verify that a stop id has been provided for PP         
         if parameters[0].valueAsText in ["Point to Point","PP"] \
         and not parameters[5].valueAsText \
         and not parameters[6].valueAsText \
         and not parameters[7].valueAsText :
            parameters[5].setErrorMessage(
               "Stop Permanent Identifier, Stop ComID or Stop Reach Code is required for Point to Point Navigation"
            );
            
         # Verify that ComID is a positive integer
         if parameters[2].value:
            boo_bad = False;
            try:
               num_val = float(parameters[2].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[2].setErrorMessage(
                  "ComID values must be a positive integers"
               );
               
         # Verify that ComID is a positive integer
         if parameters[6].value:
            boo_bad = False;
            try:
               num_val = float(parameters[6].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[6].setErrorMessage(
                  "ComID values must be a positive integers"
               );
         
         # Verify that start measure is numeric between 0 and 100         
         if parameters[4].value:
            boo_bad = False;
            try:
               num_val = float(parameters[4].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[4].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               );
         
         # Verify that stop measure is numeric between 0 and 100 
         if parameters[8].value:
            boo_bad = False;
            try:
               num_val = float(parameters[8].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[8].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               ); 

         # Verify that max distance is a number
         if parameters[9].value:
            boo_bad = False;
            try:
               num_val = float(parameters[9].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[9].setErrorMessage(
                  "Maximum distance values must be a number"
               ); 
         
         # Verify that max flow time is a number
         if parameters[10].value:
            boo_bad = False;
            try:
               num_val = float(parameters[10].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[10].setErrorMessage(
                  "Maximum flow time values must be a number"
               );
               
         # Add in sorry charlie message for split catchment parameter
         if parameters[14].valueAsText == "true":
            parameters[14].setErrorMessage(
               "Split Catchment functionality not available on Oracle at this time."
            );
         
      return

   # NavigationDelineationService
   def execute(self, parameters, messages):
      """The source code of the tool."""
      
      #------------------------------------------------------------------------
      #-- Step 10
      #-- Load variables from form parameters
      #------------------------------------------------------------------------
      str_navigation_orig  = parameters[0].valueAsText;
      str_start_permid     = parameters[1].valueAsText;
      str_start_comid      = parameters[2].valueAsText;
      str_start_reachcode  = parameters[3].valueAsText;
      str_start_measure    = parameters[4].valueAsText;
      
      if parameters[5].enabled:
         str_stop_permid   = parameters[5].valueAsText;
      else:
         str_stop_permid   = None;
         
      if parameters[6].enabled:
         str_stop_comid   = parameters[6].valueAsText;
      else:
         str_stop_comid   = None;   
      
      if parameters[7].enabled:
         str_stop_reachcode = parameters[7].valueAsText;
      else:
         str_stop_reachcode = None;
         
      if parameters[8].enabled:
         str_stop_measure  = parameters[8].valueAsText;
      else:
         str_stop_measure  = None;
         
      if parameters[9].enabled:
         str_max_distancekm = parameters[9].valueAsText;
      else:
         str_max_distancekm = None;
         
      if parameters[10].enabled:
         str_max_flowtimehour = parameters[10].valueAsText;
      else:
         str_max_flowtimehour = None;
         
      str_feature_orig = parameters[11].valueAsText;
      
      if parameters[12].valueAsText == "true":
         boo_aggregation = True;
      else:
         boo_aggregation = False;
         
      if parameters[13].valueAsText == "true":
         boo_nav_results = True;
      else:
         boo_nav_results = False;
      
      if str_navigation_orig == "Upstream with Tributaries":
         str_navigation_type = "UT";
      elif str_navigation_orig == "Upstream Main Path Only":
         str_navigation_type = "UM";
      elif str_navigation_orig == "Downstream with Divergences":
         str_navigation_type = "DD";
      elif str_navigation_orig == "Downstream Main Path Only":
         str_navigation_type = "DM";
      elif str_navigation_orig == "Point to Point":
         str_navigation_type = "PP";
      else:
         # Allow REST users to submit abbreviations if they want
         str_navigation_type = str_navigation_orig;
         
      if str_feature_orig == "NHDPlus Catchments":
         str_feature_type = "CATCHMENT_TOPO";
      else:
         str_feature_type = str_feature_orig;
         
      if boo_aggregation:
         str_aggregation = "'TRUE'";
         str_query_filter = " AND SOURCEFC = 'AGGR'";
      else:
         str_aggregation = "'FALSE'";
         str_query_filter = " AND SOURCEFC <> 'AGGR'";
       
      if boo_nav_results:
         str_nav_results = "'BOTH'";
      else:
         str_nav_results = "'FEATURE'";
         
      #------------------------------------------------------------------------
      #-- Step 20
      #-- Account for silly deployer issues with AGS
      #------------------------------------------------------------------------
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         str_navigation_type  = "UT";
         str_start_permid     = "4709538";
         str_start_comid      = None;
         str_start_reachcode  = None;
         str_start_measure    = "50";
         str_stop_permid      = None;
         str_stop_comid       = None;
         str_stop_reachcode   = None;
         str_stop_measure     = None;
         str_max_distancekm   = "5";
         str_max_flowtimehour = None;
         str_feature_type     = "CATCHMENT_TOPO";
         str_aggregation      = "'TRUE'";
         str_query_filter     = " AND SOURCEFC = 'AGGR'";
         str_nav_results      = "'BOTH'";
         
      #------------------------------------------------------------------------
      #-- Step 30
      #-- Make variable SQL ready
      #------------------------------------------------------------------------
      if str_start_permid is None:
         str_start_permid = "NULL";
      else:
         str_start_permid = "'" + str_start_permid + "'";
         
      if str_start_comid is None:
         str_start_comid = "NULL";
         
      if str_start_reachcode is None:
         str_start_reachcode = "NULL";
      else:
         str_start_reachcode = "'" + str_start_reachcode + "'";
      
      if str_start_measure is None:
         str_start_measure = "NULL";
      
      if str_stop_permid is None:
         str_stop_permid = "NULL";
      else:
         str_stop_permid = "'" + str_stop_permid + "'";
      
      if str_stop_comid is None:
         str_stop_comid = "NULL";
         
      if str_stop_reachcode is None:
         str_stop_reachcode = "NULL";
      else:
         str_stop_reachcode = "'" + str_stop_reachcode + "'";
      
      if str_stop_measure is None:
         str_stop_measure = "NULL";
      
      if str_max_distancekm is None:
         str_max_distancekm = "NULL";
         
      if str_max_flowtimehour is None:
         str_max_flowtimehour = "NULL";
         
      #------------------------------------------------------------------------
      #-- Step 40
      #-- Define any workspace parameters
      #-- Note that you may force the workspace to a hard-coded 
      #-- location if desired (this does not bother the AGS deployment)
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying SDE Environment");
      try:
         #arcpy.env.workspace = "C:\esri_dump";
         #arcpy.env.scratchWorkspace = "C:\esri_dump";
         arcpy.env.overwriteOutput = True;

      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 50
      #-- Create the service scratch space
      #------------------------------------------------------------------------
      try:
         scratch_path_delin = arcpy.CreateScratchName(
             "DelinResults"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_delin = scratch_path_delin.split(os.sep)[-1];
         
         scratch_path_nav = arcpy.CreateScratchName(
             "NavResults"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_nav = scratch_path_nav.split(os.sep)[-1];
         
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 60
      #-- Create the database connection
      #------------------------------------------------------------------------
      try:
         sde_conn = arcpy.ArcSDESQLExecute("Database Connections\\rad_ags.sde");      
      
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 70
      #-- Generate the transactional session id
      #------------------------------------------------------------------------
      str_session_id = '{' + str(uuid.uuid4()) + '}';
      
      #------------------------------------------------------------------------
      #-- Step 80
      #-- Build the PLSQL statement
      #------------------------------------------------------------------------
      sql_statement1 = """
         DECLARE
            num_return_code NUMBER;
            str_status_message VARCHAR2(4000 Char);
            str_session_id VARCHAR2(40 Char);
            str_feature_type VARCHAR2(4000 Char);
         BEGIN
            str_session_id := '""" + str_session_id  + """';
            str_feature_type := '""" + str_feature_type + """';
            INSERT INTO
            nhdplus_navigation.tmp_navigation_status(
                session_id
               ,session_datestamp
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,nhdplus_navigation.tmp_navigation_status_seq.NEXTVAL
            );            
            INSERT INTO
            nhdplus_delineation.tmp_delineation_status(
                session_id
               ,session_datestamp
               ,feature_type
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,str_feature_type
               ,nhdplus_delineation.tmp_delineation_status_seq.NEXTVAL
            );
            nhdplus_delineation.delineation.basin_delineator(
                pNavigationType           => '""" + str_navigation_type  + """'
               ,pStartComID               => """  + str_start_comid      + """
               ,pStartPermanentIdentifier => """  + str_start_permid     + """
               ,pStartReachcode           => """  + str_start_reachcode  + """
               ,pStartMeasure             => """  + str_start_measure    + """
               ,pStopComID                => """  + str_stop_comid       + """
               ,pStopPermanentIdentifier  => """  + str_stop_permid      + """
               ,pStopReachcode            => """  + str_stop_reachcode   + """
               ,pStopMeasure              => """  + str_stop_measure     + """
               ,pMaxDistanceKm            => """  + str_max_distancekm   + """
               ,pMaxFlowTimeHour          => """  + str_max_flowtimehour + """
               ,pFeatureType              => str_feature_type
               ,pOutputFlag               => """ + str_nav_results + """
               ,pAggregationFlag          => """ + str_aggregation + """
               ,pReturnCode               => num_return_code
               ,pStatusMessage            => str_status_message
               ,pSessionID                => str_session_id
            );
            COMMIT;
         END;
      """;
      
      #------------------------------------------------------------------------
      #-- Step 90
      #-- Execute the Database Service
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Executing the Service");
      try:
         sde_return = sde_conn.execute(sql_statement1)
      
      except Exception as err:
         arcpy.AddError(err)
         exit -1;
         
      #------------------------------------------------------------------------
      #-- Step 100
      #-- Verify results from the status table
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying Results");
      sql_statement2 = """
         SELECT
          a.return_code
         ,a.status_message
         FROM
         nhdplus_delineation.tmp_delineation_status a
         WHERE
         a.session_id = '""" + str_session_id + """'
      """      
      
      try:
         sde_return = sde_conn.execute(sql_statement2)
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      if sde_return[0][0] <> 0:
         arcpy.AddMessage("   Delineation completed with status code " + str(int(sde_return[0][0])));
         
         # Need to create an empty feature class to please AGS
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_delin
         );
         arcpy.SetParameterAsText(15,scratch_path_delin);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_nav
         );
         arcpy.SetParameterAsText(16,scratch_path_nav);
         
         arcpy.SetParameterAsText(17,int(sde_return[0][0]));
         arcpy.SetParameterAsText(18,sde_return[0][1]);
         return;
                
      #------------------------------------------------------------------------
      #-- Step 120
      #-- Cough out results from the results table
      #------------------------------------------------------------------------                
      arcpy.AddMessage("   Exporting Results from Database");
      try:
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.DELINEATION_TMP_CATCHMENTS"
            ,arcpy.env.scratchGDB
            ,scratch_name_delin
            ,"SESSION_ID = '" + str_session_id + "'" + str_query_filter
         );
         
         if boo_nav_results:
            arcpy.FeatureClassToFeatureClass_conversion(
                "Database Connections\\rad_ags.sde\\RAD_AGS.NAVIGATION_TMP_RESULTS"
               ,arcpy.env.scratchGDB
               ,scratch_name_nav
               ,"SESSION_ID = '" + str_session_id + "'" 
            );
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      if not boo_nav_results:
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_nav
         );
      
      arcpy.SetParameterAsText(15,scratch_path_delin);      
      arcpy.SetParameterAsText(16,scratch_path_nav);

      arcpy.SetParameterAsText(17,0);
      arcpy.SetParameterAsText(18,"");
      arcpy.AddMessage("   Delineation Complete");
      
class UpstreamDownstreamSearchService(object):

   # UpstreamDownstreamSearchService
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "UpstreamDownstreamSearchService"
      self.name  = "UpstreamDownstreamSearchService"
      self.description = "The EPA Office of Water Upstream/Downstream Search service is designed to provide standard traversal " + \
         "and event discovery functions upon the NHDPlus stream network.  " + \
         "For more information see " +  \
         "<a href='http://www2.epa.gov/waterdata/upstreamdownstream-search-service' target='_blank'>" + \
         "EPA service documentation</a>.";
      self.canRunInBackground = False

   # UpstreamDownstreamSearchService
   def getParameterInfo(self):
      """Define parameter definitions"""
       
      # First parameter
      param0 = arcpy.Parameter(
          displayName="Navigation Type:"
         ,name="pNavigationType"
         ,datatype="String"
         ,parameterType="Required"
         ,direction="Input"
         ,enabled=True
      );
      param0.value = "Upstream with Tributaries";
      param0.filter.type = "ValueList";
      param0.filter.list = [
          "Upstream with Tributaries"
         ,"Upstream Main Path Only"
         ,"Downstream with Divergences"
         ,"Downstream Main Path Only"
         ,"Point to Point"
         ,"UT"
         ,"UM"
         ,"DD"
         ,"DM"
         ,"PP"
      ];
      
      param1 = arcpy.Parameter(
          displayName="Start NHDPlus Permanent Identifier:"
         ,name="pStartPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param2 = arcpy.Parameter(
          displayName="Start NHDPlus ComID:"
         ,name="pStartComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param3 = arcpy.Parameter(
          displayName="Start Reach Code:"
         ,name="pStartReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param4 = arcpy.Parameter(
          displayName="Start Measure:"
         ,name="pStartMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param5 = arcpy.Parameter(
          displayName="Stop NHDPlus Permanent Identifier:"
         ,name="pStopPermanentIdentifier"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param6 = arcpy.Parameter(
          displayName="Stop NHDPlus ComID:"
         ,name="pStopComID"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param7 = arcpy.Parameter(
          displayName="Stop Reach Code:"
         ,name="pStopReachCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param8 = arcpy.Parameter(
          displayName="Stop Measure:"
         ,name="pStopMeasure"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param9 = arcpy.Parameter(
          displayName="Maximum Distance (KM):"
         ,name="pMaxDistanceKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      param9.value = 5;
      
      param10 = arcpy.Parameter(
          displayName="Maximum Flow Time (Hour):"
         ,name="pMaxFlowTimeHour"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      
      param11 = arcpy.Parameter(
          displayName="EventType:"
         ,name="pEventTypeList"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,multiValue=True
         ,enabled=True
      );
      param11.filter.type = "ValueList";
      param11.filter.list = [
          "10001: 303(d) Listed Impaired Waters"
         ,"10002: 305(b) Assessed Waters"
         ,"10003: Beaches"
         ,"10006: Clean Watersheds Needs Survey"
         ,"10009: Fish Consumption Advisories"
         ,"10010: Fish Tissue Data"
         ,"10011: Nonpoint Source Projects"
         ,"10012: STORET Water Monitoring Locations"
         ,"10015: Facilities that Discharge to Water"
         ,"10018: TMDLs on Impaired Waters"
         ,"10023: Impaired Waters with TMDLs"
         ,"10024: 305(b) Waters as Assessed"
         ,"10028: Facility Registration System Public"
      ];
      
      param12 = arcpy.Parameter(
          displayName="Event Area Results:"
         ,name="pEventAResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param13 = arcpy.Parameter(
          displayName="Event Line Results:"
         ,name="pEventLResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param14 = arcpy.Parameter(
          displayName="Event Point Results:"
         ,name="pEventPResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param15 = arcpy.Parameter(
          displayName="Navigation Results:"
         ,name="pNavigationResults"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param16 = arcpy.Parameter(
          displayName="ReturnCode"
         ,name="pReturnCode"
         ,datatype="GPLong"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param17 = arcpy.Parameter(
          displayName="StatusMessage"
         ,name="pStatusMessage"
         ,datatype="GPString"
         ,parameterType="Derived"
         ,direction="Output"
      );

      params = [
          param0
         ,param1
         ,param2
         ,param3
         ,param4
         ,param5
         ,param6
         ,param7
         ,param8
         ,param9
         ,param10
         ,param11
         ,param12
         ,param13
         ,param14
         ,param15
         ,param16
         ,param17
      ];
      
      return params

   # UpstreamDownstreamSearchService
   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   # UpstreamDownstreamSearchService
   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         return;
         
      if parameters[0].altered:
         if parameters[0].value in [
             "Point to Point"
            ,"PP"
         ]:
            # Turn on stop parameters
            parameters[5].enabled = True;
            parameters[6].enabled = True;
            parameters[7].enabled = True;
            parameters[8].enabled = True;
            # Turn off distance parameters
            parameters[9].enabled = False;
            #parameters[10].enabled = False;
         elif parameters[0].value in [
             "Upstream with Tributaries"
            ,"UT"
            ,"Upstream Main Path Only"
            ,"UM"
            ,"Downstream with Divergences"
            ,"DD"
            ,"Downstream Main Path Only"
            ,"DM"
         ]:
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
         else:
            # set default to UT
            parameters[0].value   = "Upstream with Tributaries";
            # Turn off stop parameters
            parameters[5].enabled = False;
            parameters[6].enabled = False;
            parameters[7].enabled = False;
            parameters[8].enabled = False;
            # Turn on distance parameters
            parameters[9].enabled = True
            #parameters[10].enabled = True;
      
      # when startPermanentIdentifier entered
      if parameters[1].altered   \
      and not parameters[1].hasBeenValidated \
      and ( parameters[2].value or parameters[3].value):
         # Blank startComid and startReachCode
         parameters[2].value = None;
         parameters[3].value = None;
      # when startComID entered
      elif parameters[2].altered  \
      and not parameters[2].hasBeenValidated \
      and ( parameters[1].value or parameters[3].value):
         # Blank startPermanentIdentifier and startReachcode
         parameters[1].value = None;
         parameters[3].value = None;
      # when startReachcode entered
      elif parameters[3].altered  \
      and not parameters[3].hasBeenValidated \
      and ( parameters[1].value or parameters[2].value):
         # Blank startPermanentIdentifier and startComID
         parameters[1].value = None;
         parameters[2].value = None;  
         
      # when stopPermanentIdentifier entered
      if parameters[5].altered   \
      and not parameters[5].hasBeenValidated \
      and ( parameters[6].value or parameters[7].value):
         # Blank stopComid and stopReachCode
         parameters[6].value = None;
         parameters[7].value = None;
      # when stopComID entered
      elif parameters[6].altered   \
      and not parameters[6].hasBeenValidated \
      and ( parameters[5].value or parameters[7].value):
         # Blank stopPermanentIdentifier and stopReachcode
         parameters[5].value = None;
         parameters[7].value = None;
      # when stopReachcode entered
      elif parameters[7].altered   \
      and not parameters[7].hasBeenValidated \
      and ( parameters[5].value or parameters[6].value):
         # Blank stopPermanentIdentifier and stopComID
         parameters[5].value = None;
         parameters[6].value = None;
      
      return

   # UpstreamDownstreamSearchService
   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      
      # this is some kludgey esri bs
      if not hasattr(__builtin__, "dz_deployer")  \
      or __builtin__.dz_deployer is False:
         
         # Verify that a start id has been provided
         if  not parameters[1].valueAsText \
         and not parameters[2].valueAsText \
         and not parameters[3].valueAsText :
            parameters[1].setErrorMessage(
               "Start Permanent Identifier, Start ComID or Start Reach Code is required"
            );
         
         # Verify that a stop id has been provided for PP         
         if parameters[0].valueAsText in ["Point to Point","PP"] \
         and not parameters[5].valueAsText \
         and not parameters[6].valueAsText \
         and not parameters[7].valueAsText :
            parameters[5].setErrorMessage(
               "Stop Permanent Identifier, Stop ComID or Stop Reach Code is required for Point to Point Navigation"
            );
            
         # Verify that ComID is a positive integer
         if parameters[2].value:
            boo_bad = False;
            try:
               num_val = float(parameters[2].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[2].setErrorMessage(
                  "ComID values must be a positive integers"
               );
               
         # Verify that ComID is a positive integer
         if parameters[6].value:
            boo_bad = False;
            try:
               num_val = float(parameters[6].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0:
               parameters[6].setErrorMessage(
                  "ComID values must be a positive integers"
               );
         
         # Verify that start measure is numeric between 0 and 100         
         if parameters[4].value:
            boo_bad = False;
            try:
               num_val = float(parameters[4].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[4].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               );
         
         # Verify that stop measure is numeric between 0 and 100 
         if parameters[8].value:
            boo_bad = False;
            try:
               num_val = float(parameters[8].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad or num_val < 0 or num_val > 100:
               parameters[8].setErrorMessage(
                  "Reach measures must be a number between 0 and 100"
               ); 

         # Verify that max distance is a number
         if parameters[9].value:
            boo_bad = False;
            try:
               num_val = float(parameters[9].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[9].setErrorMessage(
                  "Maximum distance values must be a number"
               ); 
         
         # Verify that max flow time is a number
         if parameters[10].value:
            boo_bad = False;
            try:
               num_val = float(parameters[10].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[10].setErrorMessage(
                  "Maximum distance values must be a number"
               );
      
      return

   # UpstreamDownstreamSearchService
   def execute(self, parameters, messages):
      """The source code of the tool."""
      
      #------------------------------------------------------------------------
      #-- Step 10
      #-- Load variables from form parameters
      #------------------------------------------------------------------------
      str_navigation_orig  = parameters[0].valueAsText;
      str_start_permid     = parameters[1].valueAsText;
      str_start_comid      = parameters[2].valueAsText;
      str_start_reachcode  = parameters[3].valueAsText;
      str_start_measure    = parameters[4].valueAsText;
      
      if parameters[5].enabled:
         str_stop_permid   = parameters[5].valueAsText;
      else:
         str_stop_permid   = None;
         
      if parameters[6].enabled:
         str_stop_comid    = parameters[6].valueAsText;
      else:
         str_stop_comid    = None;
      
      if parameters[7].enabled:
         str_stop_reachcode = parameters[7].valueAsText;
      else:
         str_stop_reachcode = None;
         
      if parameters[8].enabled:
         str_stop_measure  = parameters[8].valueAsText;
      else:
         str_stop_measure  = None;
         
      if parameters[9].enabled:
         str_max_distancekm = parameters[9].valueAsText;
      else:
         str_max_distancekm = None;
         
      if parameters[10].enabled:
         str_max_flowtimehour = parameters[10].valueAsText;
      else:
         str_max_flowtimehour = None;
         
      str_event_list = parameters[11].valueAsText;
      
      if str_event_list is not None:
         lst_event_list = str_event_list.split(";");
      else:
         lst_event_list = [];
      
      str_event_list_final = "";
      for i in range(len(lst_event_list)):
         str_event_list_final += lst_event_list[i][1:6];
         if i < len(lst_event_list) - 1:
            str_event_list_final += ","
      
      if str_navigation_orig == "Upstream with Tributaries":
         str_navigation_type = "UT";
      elif str_navigation_orig == "Upstream Main Path Only":
         str_navigation_type = "UM";
      elif str_navigation_orig == "Downstream with Divergences":
         str_navigation_type = "DD";
      elif str_navigation_orig == "Downstream Main Path Only":
         str_navigation_type = "DM";
      elif str_navigation_orig == "Point to Point":
         str_navigation_type = "PP";
      else:
         # Allow REST users to submit abbreviations if they want
         str_navigation_type = str_navigation_orig;
         
      #------------------------------------------------------------------------
      #-- Step 20
      #-- Account for silly deployer issues with AGS
      #------------------------------------------------------------------------
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         str_navigation_type  = "UT";
         str_start_permid     = "4709538";
         str_start_comid      = None;
         str_start_reachcode  = None;
         str_start_measure    = "50";
         str_stop_permid      = None;
         str_stop_comid       = None;
         str_stop_reachcode   = None;
         str_stop_measure     = None;
         str_max_distancekm   = "5";
         str_max_flowtimehour = None;
         str_event_list_final = "10001";
       
      #------------------------------------------------------------------------
      #-- Step 30
      #-- Make variable SQL ready
      #------------------------------------------------------------------------
      if str_start_permid is None:
         str_start_permid = "NULL";
      else:
         str_start_permid = "'" + str_start_permid + "'";
         
      if str_start_comid is None:
         str_start_comid = "NULL";
         
      if str_start_reachcode is None:
         str_start_reachcode = "NULL";
      else:
         str_start_reachcode = "'" + str_start_reachcode + "'";
      
      if str_start_measure is None:
         str_start_measure = "NULL";
      
      if str_stop_permid is None:
         str_stop_permid = "NULL";
      else:
         str_stop_permid = "'" + str_stop_permid + "'";
         
      if str_stop_comid is None:
         str_stop_comid = "NULL";
         
      if str_stop_reachcode is None:
         str_stop_reachcode = "NULL";
      else:
         str_stop_reachcode = "'" + str_stop_reachcode + "'";
      
      if str_stop_measure is None:
         str_stop_measure = "NULL";
      
      if str_max_distancekm is None:
         str_max_distancekm = "NULL";
         
      if str_max_flowtimehour is None:
         str_max_flowtimehour = "NULL";
         
      #------------------------------------------------------------------------
      #-- Step 40
      #-- Define any workspace parameters
      #-- Note that you may force the workspace to a hard-coded 
      #-- location if desired (this does not bother the AGS deployment)
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying SDE Environment");
      try:
         #arcpy.env.workspace = "C:\esri_dump";
         #arcpy.env.scratchWorkspace = "C:\esri_dump";
         arcpy.env.overwriteOutput = True;

      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 50
      #-- Create the service scratch space
      #------------------------------------------------------------------------
      try:
         scratch_path_evt_a = arcpy.CreateScratchName(
             "EventResults_Area"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_evt_a = scratch_path_evt_a.split(os.sep)[-1];
         
         scratch_path_evt_l = arcpy.CreateScratchName(
             "EventResults_Line"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_evt_l = scratch_path_evt_l.split(os.sep)[-1];
         
         scratch_path_evt_p = arcpy.CreateScratchName(
             "EventResults_Point"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_evt_p = scratch_path_evt_p.split(os.sep)[-1];
         
         scratch_path_nav = arcpy.CreateScratchName(
             "NavResults"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         );
         scratch_name_nav = scratch_path_nav.split(os.sep)[-1];
         
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 60
      #-- Create the database connection
      #------------------------------------------------------------------------
      try:
         sde_conn = arcpy.ArcSDESQLExecute("Database Connections\\rad_ags.sde");      
      
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 70
      #-- Generate the transactional session id
      #------------------------------------------------------------------------
      str_session_id = '{' + str(uuid.uuid4()) + '}';
      
      #------------------------------------------------------------------------
      #-- Step 80
      #-- Build the PLSQL statement
      #------------------------------------------------------------------------
      sql_statement1 = """
         DECLARE
            num_return_code NUMBER;
            str_status_message VARCHAR2(4000 Char);
            str_session_id VARCHAR2(40 Char);
            vry_events MDSYS.SDO_NUMBER_ARRAY;
         BEGIN
            str_session_id := '""" + str_session_id  + """';
            INSERT INTO
            nhdplus_navigation.tmp_navigation_status(
                session_id
               ,session_datestamp
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,nhdplus_navigation.tmp_navigation_status_seq.NEXTVAL
            );            
            INSERT INTO
            upstream_downstream_pub.tmp_events_status(
                session_id
               ,session_datestamp
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,upstream_downstream_pub.tmp_events_status_seq.NEXTVAL
            );
            vry_events := MDSYS.SDO_NUMBER_ARRAY(""" + str_event_list_final + """);
            upstream_downstream_pub.updn.updn_main(
                pNavigationType           => '""" + str_navigation_type  + """'
               ,pStartComID               => """  + str_start_comid      + """
               ,pStartPermanentIdentifier => """  + str_start_permid     + """
               ,pStartReachcode           => """  + str_start_reachcode  + """
               ,pStartMeasure             => """  + str_start_measure    + """
               ,pStopComID                => """  + str_stop_comid       + """
               ,pStopPermanentIdentifier  => """  + str_stop_permid      + """
               ,pStopReachcode            => """  + str_stop_reachcode   + """
               ,pStopMeasure              => """  + str_stop_measure     + """
               ,pMaxDistanceKm            => """  + str_max_distancekm   + """
               ,pMaxFlowTimeHour          => """  + str_max_flowtimehour + """
               ,pEventTypeList            => vry_events
               ,pArchiveCycleList         => NULL
               ,pReturnCode               => num_return_code
               ,pStatusMessage            => str_status_message
               ,pSessionID                => str_session_id
            );
            COMMIT;
         END;
      """;
      
      #------------------------------------------------------------------------
      #-- Step 90
      #-- Execute the Database Service
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Executing the Service");
      try:
         sde_return = sde_conn.execute(sql_statement1)
      
      except Exception as err:
         arcpy.AddError(err)
         exit -1;
         
      #------------------------------------------------------------------------
      #-- Step 100
      #-- Verify results from the status table
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying Results");
      sql_statement2 = """
         SELECT
          a.return_code
         ,a.status_message
         FROM
         upstream_downstream_pub.tmp_events_status a
         WHERE
         a.session_id = '""" + str_session_id + """'
      """      
      
      try:
         sde_return = sde_conn.execute(sql_statement2)
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      if sde_return[0][0] <> 0:
         arcpy.AddMessage("   Upstream Downstream Search completed with status code " + str(int(sde_return[0][0])));
         
         # Need to create an empty feature class to please AGS
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_evt_a
         );
         arcpy.SetParameterAsText(12,scratch_path_evt_a);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_evt_l
         );
         arcpy.SetParameterAsText(13,scratch_path_evt_l);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_evt_p
         );
         arcpy.SetParameterAsText(14,scratch_path_evt_p);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_nav
         );
         arcpy.SetParameterAsText(15,scratch_path_nav);
         
         arcpy.SetParameterAsText(16,int(sde_return[0][0]));
         arcpy.SetParameterAsText(17,sde_return[0][1]);
         return;
                
      #------------------------------------------------------------------------
      #-- Step 110
      #-- Cough out results from the results table
      #------------------------------------------------------------------------                
      arcpy.AddMessage("   Exporting Results from Database");
      try:
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.UPDNPUB_TMP_EVENTS_A"
            ,arcpy.env.scratchGDB
            ,scratch_name_evt_a
            ,"SESSION_ID = '" + str_session_id + "'"
         );
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;   

      try:         
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.UPDNPUB_TMP_EVENTS_L"
            ,arcpy.env.scratchGDB
            ,scratch_name_evt_l
            ,"SESSION_ID = '" + str_session_id + "'"
         );
         
      except Exception as err:
         arcpy.AddError(err);
         exit -1;   

      try: 
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.UPDNPUB_TMP_EVENTS_P"
            ,arcpy.env.scratchGDB
            ,scratch_name_evt_p
            ,"SESSION_ID = '" + str_session_id + "'"
         );
         
      except Exception as err:
         arcpy.AddError(err);
         exit -1;   

      try: 
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.NAVIGATION_TMP_RESULTS"
            ,arcpy.env.scratchGDB
            ,scratch_name_nav
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
      
      arcpy.SetParameterAsText(12,scratch_path_evt_a);
      arcpy.SetParameterAsText(13,scratch_path_evt_l);
      arcpy.SetParameterAsText(14,scratch_path_evt_p);
      arcpy.SetParameterAsText(15,scratch_path_nav);
      arcpy.SetParameterAsText(16,0);
      arcpy.SetParameterAsText(17,"");

      arcpy.AddMessage("   Upstream Downstream Search Complete");
      
class PointIndexingService(object):
   
   # PointIndexingService
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "PointIndexingService"
      self.name  = "PointIndexingService"
      self.description = "The EPA Office of Water Point Indexing service provides a simplified point indexing function " + \
         "for linking a point to NHDPlus hydrology network via either a straightforward shortest distance snap or via " + \
         "raindrop indexing utilizing the NHDPlus flow direction grid. The service returns the point, information about " + \
         "the indexing action and NHD flowline information describing the nearest NHD hydrography. For more information see " +  \
         "<a href='http://www2.epa.gov/waterdata/point-indexing-service' target='_blank'>" + \
         "EPA service documentation</a>.";
      self.canRunInBackground = False;

   # PointIndexingService
   def getParameterInfo(self):
      """Define parameter definitions"""
       
      # First parameter
      param0 = arcpy.Parameter(
          displayName="(1) Point Input Feature Class:"
         ,name="pGeometryFC"
         ,datatype="GPFeatureRecordSetLayer"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param1 = arcpy.Parameter(
          displayName="(1) Point Input Text Representation (Esri JSON, GeoJSON or WKT):"
         ,name="pGeometryText"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param2 = arcpy.Parameter(
          displayName="(1) Point Input X Value:"
         ,name="pGeometryX"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param3 = arcpy.Parameter(
          displayName="(1) Point Input Y Value:"
         ,name="pGeometryY"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param4 = arcpy.Parameter(
          displayName="(2) Point Input Esri Coordinate System Name:"
         ,name="pGeometryCSEsriName"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param5 = arcpy.Parameter(
          displayName="(2) Point Input Esri Coordinate System Factory Code:"
         ,name="pGeometryCSFactoryCode"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param6 = arcpy.Parameter(
          displayName="(2) Point Input Coordinate System WKT:"
         ,name="pGeometryCSText"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param7 = arcpy.Parameter(
          displayName="(3) Point Indexing Method:"
         ,name="pIndexingMethod"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      param7.value = "DISTANCE";
      param7.filter.type = "ValueList";
      param7.filter.list = [
          "DISTANCE"
         ,"RAINDROP"
      ];
      
      param8 = arcpy.Parameter(
          displayName="(4) List of NHD FCodes to Allow (comma-delimited):"
         ,name="pFcodeAllow"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param9 = arcpy.Parameter(
          displayName="(5) List of NHD FCodes to Deny (comma-delimited):"
         ,name="pFcodeDeny"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      
      param10 = arcpy.Parameter(
          displayName="(6) Maximum Distance Snap (KM):"
         ,name="pDistanceMaxDistKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=True
      );
      param10.value = "2";
      
      param11 = arcpy.Parameter(
          displayName="(7) Maximum Raindrop Path Distance (KM):"
         ,name="pRaindropPathMaxDistKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      param11.value = "5";
      
      param12 = arcpy.Parameter(
          displayName="(7) Maximum Raindrop Snap Distance (KM):"
         ,name="pRaindropSnapMaxDistKM"
         ,datatype="String"
         ,parameterType="Optional"
         ,direction="Input"
         ,enabled=False
      );
      param12.value = "0.25";

      param13 = arcpy.Parameter(
          displayName="StartPoint"
         ,name="pStartPoint"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      param13.schema.featureTypeRule = "AsSpecified";
      param13.schema.featureType = "Simple";
      param13.schema.geometryTypeRule = "AsSpecified";
      param13.schema.geometryType = "Point";
      param13.schema.fieldsRule = "AllNoFIDs";
      
      param14 = arcpy.Parameter(
          displayName="EndPoint"
         ,name="pEndPoint"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      param14.schema.featureTypeRule = "AsSpecified";
      param14.schema.featureType = "Simple";
      param14.schema.geometryTypeRule = "AsSpecified";
      param14.schema.geometryType = "Point";
      param14.schema.fieldsRule = "AllNoFIDs";
      
      param15 = arcpy.Parameter(
          displayName="IndexPath"
         ,name="pIndexPath"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      param15.schema.featureTypeRule = "AsSpecified";
      param15.schema.featureType = "Simple";
      param15.schema.geometryTypeRule = "AsSpecified";
      param15.schema.geometryType = "Polyline";
      param15.schema.fieldsRule = "AllNoFIDs";
      
      param16 = arcpy.Parameter(
          displayName="Flowlines"
         ,name="pFlowlines"
         ,datatype="DEFeatureClass"
         ,parameterType="Derived"
         ,direction="Output"
      );
      param16.schema.featureTypeRule = "AsSpecified";
      param16.schema.featureType = "Simple";
      param16.schema.geometryTypeRule = "AsSpecified";
      param16.schema.geometryType = "Polyline";
      param16.schema.fieldsRule = "AllNoFIDs";
      
      param17 = arcpy.Parameter(
          displayName="ReturnCode"
         ,name="pReturnCode"
         ,datatype="GPLong"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      param18 = arcpy.Parameter(
          displayName="StatusMessage"
         ,name="pStatusMessage"
         ,datatype="GPString"
         ,parameterType="Derived"
         ,direction="Output"
      );
      
      params = [
          param0
         ,param1
         ,param2
         ,param3
         ,param4
         ,param5
         ,param6
         ,param7
         ,param8
         ,param9
         ,param10
         ,param11
         ,param12
         ,param13
         ,param14
         ,param15
         ,param16
         ,param17
         ,param18
      ];
      
      return params;

   # PointIndexingService
   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   # PointIndexingService
   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         return;

      if parameters[7].altered:
         if parameters[7].value == "DISTANCE":
            parameters[10].enabled = True;
            parameters[11].enabled = False;
            parameters[12].enabled = False;
         elif parameters[7].value == "RAINDROP":
            parameters[10].enabled = False;
            parameters[11].enabled = True;
            parameters[12].enabled = True;

   # PointIndexingService
   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      
      # this is some kludgey esri bs
      if not hasattr(__builtin__, "dz_deployer")  \
      or __builtin__.dz_deployer is False:
         
         if parameters[1].value    \
         and not parameters[0].value:
            # first check if input is json
            boo_json = True;
            try:
               str_json = json.loads(parameters[1].valueAsText);
               
            except:
               boo_json = False;
               
            # if that failed then try for wkt
            boo_wkt = True;
            if not boo_json:
               try:
                  geom_obj = arcpy.FromWKT(parameters[1].valueAsText);            
               
               except:
                  boo_wkt = False;
                  
            if not boo_json and not boo_wkt:
               parameters[1].setErrorMessage(
                  "Text input must be valid GeoJSON, WKT or Esri JSON."
               );
               return;
               
            if boo_json:   
               boo_valid = True;
               try:
                  geom_obj = arcpy.AsShape(str_json,False);
               except:
                  boo_valid = False;
                  
               if not boo_valid:
                  boo_valid = True;
                  try:
                     geom_obj = arcpy.AsShape(str_json,True);
                  except:
                     boo_valid = False;
                     
               if not boo_valid:
                  parameters[1].setErrorMessage(
                     "Unable to parse input JSON as either GeoJSON or Esri JSON geometry."
                  );
                  return;
                  
               if  geom_obj.spatialReference is not None    \
               and geom_obj.spatialReference.factoryCode <> 0:
                  parameters[4].value = geom_obj.spatialReference.name;
                  parameters[5].value = geom_obj.spatialReference.factoryCode;
                  parameters[6].value = geom_obj.spatialReference.exportToString();

         if parameters[2].value        \
         and not parameters[0].value   \
         and not parameters[1].value:
            boo_bad = False;
            try:
               num_val = float(parameters[2].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[2].setErrorMessage(
                  "Coordinate values must be numeric values."
               );
               
         if parameters[3].value        \
         and not parameters[0].value   \
         and not parameters[1].value:
            boo_bad = False;
            try:
               num_val = float(parameters[3].valueAsText);
            except ValueError:
               boo_bad = True;
               
            if boo_bad:
               parameters[3].setErrorMessage(
                  "Coordinate values must be numeric values."
               );
         
         if  not parameters[0].value       \
         and not parameters[1].value       \
         and not parameters[2].value       \
         and not parameters[3].value:
            parameters[0].setErrorMessage(
               "One form of geometry input is required."
            );
            parameters[1].setErrorMessage(
               "One form of geometry input is required."
            );
            parameters[2].setErrorMessage(
               "One form of geometry input is required."
            );
            parameters[3].setErrorMessage(
               "One form of geometry input is required."
            );
           
         if  not parameters[0].value       \
         and not parameters[4].value       \
         and not parameters[5].value       \
         and not parameters[6].value:
            parameters[4].setErrorMessage(
               "One form of geometry cs input is required."
            );
            parameters[5].setErrorMessage(
               "One form of geometry cs input is required."
            );
            parameters[6].setErrorMessage(
               "One form of geometry cs input is required."
            );
            
      return;

   # PointIndexingService
   def execute(self, parameters, messages):
      """The source code of the tool."""
      
      def esri2waters(factoryCode):
         if factoryCode == 4269:
           srid = 8265;
         elif factoryCode < 32767:
           srid = factoryCode;
         elif factoryCode in [900913,102100,102113]:
           srid = 3857;
         else:
           srid = factoryCode;
                
         return srid;                
      
      #------------------------------------------------------------------------
      #-- Step 10
      #-- Load the simple form variables
      #------------------------------------------------------------------------
      str_indexing_method  = parameters[7].valueAsText;
      str_fcode_allow      = parameters[8].valueAsText;
      str_fcode_deny       = parameters[9].valueAsText;
      str_distance_max_km  = parameters[10].valueAsText;
      str_rain_path_max_km = parameters[11].valueAsText;
      str_rain_snap_max_km = parameters[12].valueAsText;
      
      if str_indexing_method is None:
         str_indexing_method = "DISTANCE";
      
      if str_distance_max_km is None:
         str_distance_max_km = "NULL";
         
      if str_rain_path_max_km is None:
         str_rain_path_max_km = "NULL";
         
      if str_rain_snap_max_km is None:
         str_rain_snap_max_km = "NULL";
         
      if str_fcode_allow is None:
         str_fcode_allow = "";
         
      if str_fcode_deny is None:
         str_fcode_deny = "";
         
      #------------------------------------------------------------------------
      #-- Step 20
      #-- Load point from feature class if file input
      #------------------------------------------------------------------------
      num_srid = None;
      str_wkt_geom = None;
      boo_override_cs = False;
      
      str_point_fc     = parameters[0].valueAsText;
      if str_point_fc == "{}":
         str_point_fc = None;
         
      str_point_txt    = parameters[1].valueAsText;
      str_point_x      = parameters[2].valueAsText;
      str_point_y      = parameters[3].valueAsText;
      str_cs_esri_name = parameters[4].valueAsText;
      str_cs_fact_code = parameters[5].valueAsText;
      str_cs_wkt       = parameters[6].valueAsText;
      
      #------------------------------------------------------------------------
      # User is forcing a CS so we will always use it if given
      #------------------------------------------------------------------------
      if str_cs_esri_name is not None   \
      or str_cs_fact_code is not None   \
      or str_cs_wkt       is not None:
         boo_override_cs = True;
      
      #------------------------------------------------------------------------
      # If user provides a FC object then we will use it and ignore others
      #------------------------------------------------------------------------
      if str_point_fc is not None:
         if not boo_override_cs:
            desc = arcpy.Describe(str_point_fc);
            sr   = desc.spatialReference;
            num_srid = esri2waters(sr.factoryCode);
         
         str_wkt_geom = arcpy.da.SearchCursor(str_point_fc,["SHAPE@WKT"]).next()[0];
      
      #------------------------------------------------------------------------
      # Next process any textual geometries
      #------------------------------------------------------------------------
      elif str_point_txt is not None:
         try:
            geom = arcpy.FromWKT(str_point_txt);
         except:
            pass;
            
         try:
            geom = arcpy.AsShape(json.loads(str_point_txt),False);
         except:
            pass;
            
         try:
            geom = arcpy.AsShape(json.loads(str_point_txt),True);
         except:
            pass;
         
         if not boo_override_cs:
            if geom.spatialReference is not None:
               num_srid = esri2waters(geom.spatialReference.factoryCode);
            
         str_wkt_geom = geom.WKT;
      
      #------------------------------------------------------------------------
      # Final option is raw x and y coerced into dumb WKT
      #------------------------------------------------------------------------      
      elif str_point_x is not None and str_point_y is not None:
         str_wkt_geom = "POINT(" + str_point_x + " " + str_point_y + ")";
         
      #------------------------------------------------------------------------
      #-- Step 30
      #-- Sort out the coordinate system if not provide by step 20
      #------------------------------------------------------------------------
      if num_srid is None or boo_override_cs:
         sr = None;
         if str_cs_esri_name is not None:
            sr = arcpy.SpatialReference(str_cs_esri_name);
            
         elif str_cs_fact_code is not None:
            num_cs_fact_code = int(str_cs_fact_code);
            sr = arcpy.SpatialReference(num_cs_fact_code);
            
         elif str_cs_wkt is not None:
            sr = arcpy.SpatialReference()
            sr.loadFromString(str_cs_wkt)
         
         if sr is not None:
            num_srid = esri2waters(sr.factoryCode);
            
      if num_srid is None or num_srid == 0:
         num_srid = 8265;
         
      #arcpy.AddMessage("Geom: " + str(str_wkt_geom));
      #arcpy.AddMessage("CS: " + str(num_srid));
      
      #------------------------------------------------------------------------
      #-- Step 40
      #-- Account for silly deployer issues with AGS
      #------------------------------------------------------------------------
      if hasattr(__builtin__, "dz_deployer") \
      and __builtin__.dz_deployer is True:
         str_wkt_geom          = "POINT(-118.15 33.80)";
         num_srid              = 8265;
         str_fcode_allow       = "";
         str_fcode_deny        = "";
         str_indexing_method   = "DISTANCE";
         str_distance_max_km   = "10";
         str_rain_path_max_km  = "5";
         str_rain_snap_max_km  = "0.25";
      
      #------------------------------------------------------------------------
      #-- Step 50
      #-- Define any workspace parameters
      #-- Note that you may force the workspace to a hard-coded 
      #-- location if desired (this does not bother the AGS deployment)
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying SDE Environment");
      try:
         #arcpy.env.workspace = "C:\esri_dump";
         #arcpy.env.scratchWorkspace = "C:\esri_dump";
         arcpy.env.overwriteOutput = True;

      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 60
      #-- Create the service scratch space
      #------------------------------------------------------------------------
      try:
         scratch_path_sp = arcpy.CreateScratchName(
             "StartPoint"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         )
         scratch_name_sp = scratch_path_sp.split(os.sep)[-1];
         
         scratch_path_ep = arcpy.CreateScratchName(
             "EndPoint"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         )
         scratch_name_ep = scratch_path_ep.split(os.sep)[-1];
         
         scratch_path_ip = arcpy.CreateScratchName(
             "IndexingPath"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         )
         scratch_name_ip = scratch_path_ip.split(os.sep)[-1];
         
         scratch_path_fl = arcpy.CreateScratchName(
             "Flowlines"
            ,""
            ,"FeatureClass"
            ,arcpy.env.scratchGDB
         )
         scratch_name_fl = scratch_path_fl.split(os.sep)[-1];
         
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 70
      #-- Create the database connection
      #------------------------------------------------------------------------
      try:
         sde_conn = arcpy.ArcSDESQLExecute("Database Connections\\rad_ags.sde");      
      
      except Exception as err:
         arcpy.AddError(err);
         
      #------------------------------------------------------------------------
      #-- Step 80
      #-- Generate the transaction id
      #------------------------------------------------------------------------
      str_session_id = '{' + str(uuid.uuid4()) + '}';
      
      #------------------------------------------------------------------------
      #-- Step 90
      #-- Build the PLSQL statement
      #------------------------------------------------------------------------
      sql_statement1 = """
         DECLARE
            num_return_code    NUMBER;
            num_path_lengthkm  NUMBER;
            num_input_srid     NUMBER;
            str_status_message VARCHAR2(4000 Char);
            str_session_id     VARCHAR2(40 Char);
            sdo_input          MDSYS.SDO_GEOMETRY;
            ary_fcode_allow    MDSYS.SDO_NUMBER_ARRAY;
            ary_fcode_deny     MDSYS.SDO_NUMBER_ARRAY;
         BEGIN
            str_session_id  := '""" + str_session_id  + """';
            num_input_srid  := """ + str(num_srid) + """;
            sdo_input       := MDSYS.SDO_GEOMETRY('""" + str_wkt_geom  + """',num_input_srid);
            ary_fcode_allow := MDSYS.SDO_NUMBER_ARRAY(""" + str_fcode_allow  + """);
            ary_fcode_deny  := MDSYS.SDO_NUMBER_ARRAY(""" + str_fcode_deny  + """);
            INSERT INTO
            nhdplus_indexing.tmp_pt_indexing_status(
                session_id
               ,session_datestamp
               ,objectid
            ) VALUES (
                str_session_id
               ,SYSTIMESTAMP
               ,nhdplus_indexing.tmp_pt_indexing_status_seq.NEXTVAL
            );
            nhdplus_indexing.point_indexing.flat_indexer(
                pPoint                  => sdo_input 
               ,pIndexingMethod         => '"""  + str_indexing_method + """'
               ,pFcodeAllow             => ary_fcode_allow 
               ,pFcodeDeny              => ary_fcode_deny
               ,pDistanceMaxDistKM      => """  + str_distance_max_km + """
               ,pRaindropPathMaxDistKM  => """  + str_rain_path_max_km + """
               ,pRaindropSnapMaxDistKM  => """  + str_rain_snap_max_km + """
               ,pReturnCode             => num_return_code
               ,pStatusMessage          => str_status_message
               ,pIndexingLineLengthKM   => num_path_lengthkm
               ,pSessionID              => str_session_id
            );
            COMMIT;
         END;
      """;
      
      #------------------------------------------------------------------------
      #-- Step 100
      #-- Execute the Database Service
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Executing the Service");
      try:
         sde_return = sde_conn.execute(sql_statement1)
      
      except Exception as err:
         arcpy.AddError(err)
         exit -1;
         
      #------------------------------------------------------------------------
      #-- Step 110
      #-- Verify results from the status table
      #------------------------------------------------------------------------
      arcpy.AddMessage("   Verifying Results");
      sql_statement2 = """
         SELECT
          a.return_code
         ,a.status_message
         FROM
         nhdplus_indexing.tmp_pt_indexing_status a
         WHERE
         a.session_id = '""" + str_session_id + """'
      """      
      
      try:
         sde_return = sde_conn.execute(sql_statement2)
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
      
      #------------------------------------------------------------------------
      #-- Step 120
      #-- Account for the situation where no results are returned.
      #-- Its an "error" but represents acceptable results
      #------------------------------------------------------------------------
      if sde_return[0][0] <> 0:
         arcpy.AddMessage("   Point Indexing completed with status code " + str(int(sde_return[0][0])));
         
         # Need to create an empty feature class to please AGS
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_sp
         );
         arcpy.SetParameterAsText(13,scratch_path_sp);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_ep
         );
         arcpy.SetParameterAsText(14,scratch_path_ep);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_ip
         );
         arcpy.SetParameterAsText(15,scratch_path_ip);
         
         arcpy.CreateFeatureclass_management(
             arcpy.env.scratchGDB
            ,scratch_name_fl
         );
         arcpy.SetParameterAsText(16,scratch_path_fl);

         arcpy.SetParameterAsText(17,int(sde_return[0][0]));
         arcpy.SetParameterAsText(18,sde_return[0][1]);
         return;
                
      #------------------------------------------------------------------------
      #-- Step 130
      #-- Cough out results from the results table
      #------------------------------------------------------------------------                
      arcpy.AddMessage("   Exporting Results from Database");
      try:
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.INDEXING_TMP_PT_START"
            ,arcpy.env.scratchGDB
            ,scratch_name_sp
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
         
      except Exception as err:
         arcpy.AddError(err);
         exit -1;

      try:         
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.INDEXING_TMP_PT_END"
            ,arcpy.env.scratchGDB
            ,scratch_name_ep
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
         
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.INDEXING_TMP_PT_INDEXINGLINE"
            ,arcpy.env.scratchGDB
            ,scratch_name_ip
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
         
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      try:
         arcpy.FeatureClassToFeatureClass_conversion(
             "Database Connections\\rad_ags.sde\\RAD_AGS.INDEXING_TMP_PT_FLOWLINES"
            ,arcpy.env.scratchGDB
            ,scratch_name_fl
            ,"SESSION_ID = '" + str_session_id + "'" 
         );
      
      except Exception as err:
         arcpy.AddError(err);
         exit -1;
         
      arcpy.SetParameterAsText(13,scratch_path_sp);
      arcpy.SetParameterAsText(14,scratch_path_ep);
      arcpy.SetParameterAsText(15,scratch_path_ip);
      arcpy.SetParameterAsText(16,scratch_path_fl);
      
      arcpy.SetParameterAsText(17,0);
      arcpy.SetParameterAsText(18,"");

      arcpy.AddMessage("   Point Indexing Complete");
      
