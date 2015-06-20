import iedm_2015

#Set your target Vt here
target_vt = 500

#Set your epsilon value here. The application will find material combination whose Vt value is ... target_vt-epsilon <= calculated_vt <= target_vt+epsilon
epsilon = 50

#Set to True if you want to see the details
verbose = False

#Set the material thickness here. Comment the materials which you don't want to use. The thickness MUST BE positive. Note that you MUST use the compulsory materials
#The compulsory materials are: IL, HfO2, La2O3, TiAlC, either one of 1:1 TiN or 2:1 TiN (you can use both of them as well)
material_name_to_thickness = dict([])
material_name_to_thickness[iedm_2015.MATERIAL_ONE_ONE_TIN] = 50.0 #1:1 TiN
material_name_to_thickness[iedm_2015.MATERIAL_TWO_ONE_TIN] = 50.0 #2:1 TiN
material_name_to_thickness[iedm_2015.MATERIAL_W] = 50.0 #W
material_name_to_thickness[iedm_2015.MATERIAL_IL] = 10.0 #IL
material_name_to_thickness[iedm_2015.MATERIAL_HFO2] = 20.0 #HfO2
material_name_to_thickness[iedm_2015.MATERIAL_LA2O3] = 4.0 #La2O3
material_name_to_thickness[iedm_2015.MATERIAL_AL2O3] = 4.0 #Al2O3
material_name_to_thickness[iedm_2015.MATERIAL_TIALC] = 50.0 #TiAlC
material_name_to_thickness[iedm_2015.MATERIAL_SIGE] = 20.0 #SiGe
#material_name_to_thickness[iedm_2015.MATERIAL_TAN] = 20.0 #TaN
#material_name_to_thickness[iedm_2015.MATERIAL_TASIN] = 20.0 #TaSiN
#material_name_to_thickness[iedm_2015.MATERIAL_AL] = 20.0 #Al
material_name_to_thickness[iedm_2015.MATERIAL_SR2O3] = 10.0 #Sr2O3
#material_name_to_thickness[iedm_2015.MATERIAL_CE2O3] = 20.0 #Ce2O3
#material_name_to_thickness[iedm_2015.MATERIAL_Y2O3] = 20.0 #Y2O3
#material_name_to_thickness[iedm_2015.MATERIAL_ZRO2] = 20.0 #ZrO2
#material_name_to_thickness[iedm_2015.MATERIAL_SO2] = 20.0 #SO2
#material_name_to_thickness[iedm_2015.MATERIAL_GEO2] = 20.0 #GeO2


#Do not change this section. This section is to run the main logic
execution_output = iedm_2015.execute(material_name_to_thickness, epsilon, target_vt, verbose)
print 'Status:', execution_output.binary_integer_programming_status
print 'Optional Materials:'
for variable in execution_output.binary_integer_programming_variables:
	print '\t'+variable+' : '+str(execution_output.binary_integer_programming_variables[variable])

