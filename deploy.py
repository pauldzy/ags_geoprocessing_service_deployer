import arcpy
import os
import __builtin__
import xml.dom.minidom as DOM;

#------------------------------------------------------------------------------
#
# Waters Services Geoprocessing Services Deployment Script
# Version 2.0
#
#------------------------------------------------------------------------------

# The name of your ArcGIS Server administrator connection in ArcCatalog
# This can be changed as needed
ags_con_name = "industux";

# The name of your rad_ags SDE database connection in ArcCatalog
# This can be changed as needed (new!)
rad_con_name = "rad_ags";

# Service properties handled directly by arcpy.CreateGPSDDraft
draft_service_name   = "WATERS_SERVICES";
draft_folder_name    = None;
draft_summary        = "EPA Office of Water provides a suite of interoperable services that expose components that perform complex analysis and supporting strategic datasets, such as NHD, NHDPlus, and WBD."
draft_tags           = "EPA";
draft_execution_type = "ASynchronous";
draft_max_records    = 10000;
draft_minInstances   = 2;
draft_maxInstances   = 4;
draft_maxUsageTime   = 600;
draft_maxWaitTime    = 60;
draft_maxIdleTime    = 1800;
# Hash of any additional general properties to be applied to the sddraft file
ags_properties = {}

# Hash of services to enable or disable
ags_services = {
    'WPSServer': True
}

# Array of Hash of properties to be applied to individual services
ags_service_props = {
    'WPSServer': {'abstract': 'EPA Office of Waters WPS Services'}
}

#------------------------------------------------------------------------------
# No further changes should be necessary
#------------------------------------------------------------------------------
def soe_enable(doc,soe,value):
   typeNames = doc.getElementsByTagName('TypeName');
   
   for typeName in typeNames:
      if typeName.firstChild.data == soe:
         extension = typeName.parentNode
         for extElement in extension.childNodes:
            if extElement.tagName == 'Enabled':
               if value is True:
                  extElement.firstChild.data = 'true';
               else:
                  extElement.firstChild.data = 'false';
                  
   return doc;
   
def srv_property(doc,property,value):
   keys = doc.getElementsByTagName('Key')
   for key in keys:
      if key.hasChildNodes():
         if key.firstChild.data == property:
            if value is True:
               key.nextSibling.firstChild.data = 'true';
            elif value is False:
               key.nextSibling.firstChild.data = 'false';
            else:
               key.nextSibling.firstChild.data = value
   return doc;

def soe_property(doc,soe,soeProperty,soePropertyValue):
   typeNames = doc.getElementsByTagName('TypeName');
   
   for typeName in typeNames:
       if typeName.firstChild.data == soe:
           extension = typeName.parentNode
           for extElement in extension.childNodes:
               if extElement.tagName in ['Props','Info']:
                   for propArray in extElement.childNodes:
                       for propSet in propArray.childNodes:
                           for prop in propSet.childNodes:
                               if prop.tagName == "Key":
                                   if prop.firstChild.data == soeProperty:
                                       if prop.nextSibling.hasChildNodes():
                                           prop.nextSibling.firstChild.data = soePropertyValue
                                       else:
                                           txt = doc.createTextNode(soePropertyValue)
                                           prop.nextSibling.appendChild(txt)
   return doc;
   
#------------------------------------------------------------------------------
#- Step 10
#- Verify that the connections exist and are good
#------------------------------------------------------------------------------
arcpy.AddMessage("Validating ArcCatalog Connections:");
         
ags_con = "GIS Servers\\" + ags_con_name + ".ags";
if arcpy.Exists(ags_con):
   arcpy.AddMessage("   Service will be deployed to " + ags_con);
   
else:
   arcpy.AddMessage(" ");
   arcpy.AddMessage("  Connection named GIS Servers\\" + ags_con_name + ".ags not found.");
   ags_con2 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\\" + ags_con_name + ".ags"
   
   if arcpy.Exists(ags_con2):
      ags_con = ags_con2;
      arcpy.AddMessage("   Service will be deployed to " + ags_con);
      
   else:
      arcpy.AddMessage(" ");
      arcpy.AddMessage("  No luck checking " + ags_con2);
      ags_con3 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\" + ags_con_name + ".ags"
      
      if arcpy.Exists(ags_con3):
         ags_con = ags_con3;
         arcpy.AddMessage("   Service will be deployed to " + ags_con);
         
      else:  
         arcpy.AddMessage(" ");
         arcpy.AddMessage("  No luck checking " + ags_con3);
         ags_con4 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\" + ags_con_name + ".ags"
         
         if arcpy.Exists(ags_con4):
            ags_con = ags_con4;
            arcpy.AddMessage("   Service will be deployed to " + ags_con);
            
         else:  
            arcpy.AddMessage(" ");
            arcpy.AddMessage("  No luck checking " + ags_con4);
            arcpy.AddMessage("  Unable to find a valid connection for " + ags_con_name);
            exit(-1);
         
rad_con = "Database Connections\\" + rad_con_name + ".sde";
if arcpy.Exists(rad_con):
   arcpy.AddMessage("   Service will utilize geodatabase at " + rad_con);
   
else:
   arcpy.AddMessage(" ");
   arcpy.AddMessage("  Connection named Database Connections\\" + rad_con_name + ".sde not found.");
   rad_con2 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.3\\ArcCatalog\\" + rad_con_name + ".sde"
   
   if arcpy.Exists(rad_con2):
      rad_con = rad_con2;
      arcpy.AddMessage("   Service will utilize geodatabase at " + rad_con);
      
   else:
      arcpy.AddMessage(" ");
      arcpy.AddMessage("  No luck checking " + rad_con2);
      rad_con3 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\" + ags_con_name + ".sde"
      
      if arcpy.Exists(rad_con3):
         rad_con = rad_con3;
         arcpy.AddMessage("   Service will utilize geodatabase at " + rad_con);
         
      else:  
         arcpy.AddMessage(" ");
         arcpy.AddMessage("  No luck checking " + rad_con3);
         rad_con4 = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\" + ags_con_name + ".sde"
         
         if arcpy.Exists(rad_con4):
            rad_con = rad_con4;
            arcpy.AddMessage("   Service will utilize geodatabase at " + rad_con);
            
         else:  
            arcpy.AddMessage(" ");
            arcpy.AddMessage("  No luck checking " + rad_con4);
            arcpy.AddMessage("  Unable to find a valid connection for " + rad_con_name);
            exit(-1);

try:
   desc = arcpy.Describe(rad_con);
   cp = desc.connectionProperties;

except arcpy.ExecuteError:
   print(arcpy.GetMessages(2));
       
arcpy.AddMessage("      User    : " + cp.user);
arcpy.AddMessage("      Instance: " + cp.instance);
   
#------------------------------------------------------------------------------
#- Step 20
#- Alter the database sde connection in the toolbox
#------------------------------------------------------------------------------
arcpy.AddMessage("Adjusting toolbox geodatabase connection.");
temp_tool = arcpy.CreateScratchName(
    "WATERS_Services"
   ,".pyt"
   ,None
   ,arcpy.env.scratchFolder
);

new_file = open(temp_tool,'w');
old_file = open("WATERS_Services.pyt");
for line in old_file:
   new_file.write(
      line.replace(
          "Database Connections\\rad_ags.sde"
         ,"Database Connections\\" + rad_con_name + ".sde"
      )
   );
   
new_file.close();
old_file.close();

xml_1 = temp_tool.replace(".pyt",".pyt.xml");

new_file = open(xml_1,'w');
old_file = open("WATERS_Services.pyt.xml");
for line in old_file:
   new_file.write(line);
new_file.close();
old_file.close();

xml_2 = temp_tool.replace(".pyt",".NavigationService.pyt.xml");

new_file = open(xml_2,'w');
old_file = open("WATERS_Services.NavigationService.pyt.xml");
for line in old_file:
   new_file.write(line);
new_file.close();
old_file.close();

xml_3 = temp_tool.replace(".pyt",".NavigationDelineationService.pyt.xml");

new_file = open(xml_3,'w');
old_file = open("WATERS_Services.NavigationDelineationService.pyt.xml");
for line in old_file:
   new_file.write(line);
new_file.close();
old_file.close();

xml_4 = temp_tool.replace(".pyt",".UpstreamDownstreamService.pyt.xml");

new_file = open(xml_4,'w');
old_file = open("WATERS_Services.UpstreamDownstreamService.pyt.xml");
for line in old_file:
   new_file.write(line);
new_file.close();
old_file.close();
   
#------------------------------------------------------------------------------
#- Step 30
#- Import the toolbox
#------------------------------------------------------------------------------
arcpy.AddMessage("Importing the toolbox.");
try:
   owservices = arcpy.ImportToolbox(temp_tool);

except Exception as err:
   arcpy.AddError(err)
   exit -1;

#------------------------------------------------------------------------------
#- Step 40
#- Run Navigation Service
#------------------------------------------------------------------------------
arcpy.AddMessage("Dry running Navigation Service.");
try:
   __builtin__.dz_deployer = True;
   # the values provided below become the initial AGS defaults
   navsrv_results = owservices.NavigationService(
       pNavigationType='Upstream with Tributaries'       
      ,pStartPermanentIdentifier=None
      ,pStartReachCode=None
      ,pStartMeasure=None
      ,pStopPermanentIdentifier=None
      ,pStopReachCode=None
      ,pStopMeasure=None
      ,pMaxDistanceKM=5
      ,pMaxFlowTimeHour=None
   );
   
except Exception as err:
   arcpy.AddError(err)
   exit -1;
   
#------------------------------------------------------------------------------
#- Step 50
#- Run Navigation Delineation Service
#------------------------------------------------------------------------------
arcpy.AddMessage("Dry running Navigation Delineation Service.");
try:
   __builtin__.dz_deployer = True;
   # the values provided below become the initial AGS defaults
   navdelin_results = owservices.NavigationDelineationService(
       pNavigationType='Upstream with Tributaries'       
      ,pStartPermanentIdentifier=None
      ,pStartReachCode=None
      ,pStartMeasure=None
      ,pStopPermanentIdentifier=None
      ,pStopReachCode=None
      ,pStopMeasure=None
      ,pMaxDistanceKM=5
      ,pMaxFlowTimeHour=None
      ,pFeatureType="NHDPlus Catchments"
      ,pAggregateFeatures=True
      ,pReturnNavigation=False
   );
   
except Exception as err:
   arcpy.AddError(err)
   exit -1;
   
#------------------------------------------------------------------------------
#- Step 60
#- Run Upstream Downstream Service
#------------------------------------------------------------------------------
arcpy.AddMessage("Dry running Upstream Downstream Service.");
try:
   __builtin__.dz_deployer = True;
   # the values provided below become the initial AGS defaults
   updn_results = owservices.UpstreamDownstreamService(
       pNavigationType='Upstream with Tributaries'       
      ,pStartPermanentIdentifier=None
      ,pStartReachCode=None
      ,pStartMeasure=None
      ,pStopPermanentIdentifier=None
      ,pStopReachCode=None
      ,pStopMeasure=None
      ,pMaxDistanceKM=5
      ,pMaxFlowTimeHour=None
      ,pEventTypeList=None
   );
   
except Exception as err:
   arcpy.AddError(err)
   exit -1;
   
#------------------------------------------------------------------------------
#- Step 70
#- Create the sddraft file
#------------------------------------------------------------------------------
arcpy.AddMessage("Generating sddraft file.");
try:
   sd = arcpy.CreateScratchName(
       "WATERS_Services"
      ,".sd"
      ,None
      ,arcpy.env.scratchFolder
   );
   
   sddraft = arcpy.CreateScratchName(
       "WATERS_Services"
      ,".sddraft"
      ,None
      ,arcpy.env.scratchFolder
   );
   
   arcpy.CreateGPSDDraft(
       result=[navsrv_results,navdelin_results,updn_results]
      ,out_sddraft=sddraft
      ,service_name=draft_service_name
      ,server_type="ARCGIS_SERVER"
      ,connection_file_path=ags_con
      ,copy_data_to_server=False
      ,folder_name=draft_folder_name
      ,summary=draft_summary
      ,tags=draft_tags
      ,executionType=draft_execution_type
      ,resultMapServer=False
      ,showMessages="INFO"
      ,maximumRecords=draft_max_records
      ,minInstances=draft_minInstances
      ,maxInstances=draft_maxInstances
      ,maxUsageTime=draft_maxUsageTime
      ,maxWaitTime=draft_maxWaitTime
      ,maxIdleTime=draft_maxIdleTime
   );
   
except arcpy.ExecuteError:
   print(arcpy.GetMessages(2));
   
#------------------------------------------------------------------------------
#- Step 80
#- Analyze the SD
#------------------------------------------------------------------------------
arcpy.AddMessage("Analyzing service definition.");
analysis = arcpy.mapping.AnalyzeForSD(sddraft);

if analysis['errors'] != {}:
   print '---- ERRORS ----'
   vars = analysis['errors']
   for ((message, code), layerlist) in vars.iteritems():
      print '    ', message, ' (CODE %i)' % code
      if len(layerlist) > 0:
         print '       applies to:',
         for layer in layerlist:
            print layer.name,
         print

if analysis['warnings'] != {}:
   print '---- WARNINGS ----'
   vars = analysis['warnings']
   for ((message, code), layerlist) in vars.iteritems():
      print '    ', message, ' (CODE %i)' % code
      if len(layerlist) > 0:
         print '       applies to:',
         for layer in layerlist:
            print layer.name,
         print
         
if analysis['messages'] != {}:
   print '---- MESSAGES ----'
   vars = analysis['messages']
   for ((message, code), layerlist) in vars.iteritems():
      print '    ', message, ' (CODE %i)' % code
      if len(layerlist) > 0:
         print '       applies to:',
         for layer in layerlist:
            print layer.name,
         print

#------------------------------------------------------------------------------
#- Step 90
#- Alter the sddraft file 
#------------------------------------------------------------------------------
arcpy.AddMessage("Altering sddraft as needed.");       
doc = DOM.parse(sddraft)
for k, v in ags_properties.iteritems():
   doc = srv_property(doc,k,v);
for k, v in ags_services.iteritems():
   doc = soe_enable(doc,k,v);
for k, v in ags_service_props.iteritems():
   doc = soe_property(doc,k,v.keys()[0],v.values()[0]);
f = open(sddraft, 'w');
doc.writexml(f);
f.close();

#------------------------------------------------------------------------------
#- Step 100
#- Deploy the service
#------------------------------------------------------------------------------ 
arcpy.AddMessage("Deploying to ArcGIS Server."); 
if analysis['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft,sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd,ags_con)
    
