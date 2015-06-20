import sys
import math
from pulp import *
from collections import namedtuple

# declaring keys
MATERIAL_ONE_ONE_TIN = '1:1 TiN'
MATERIAL_TWO_ONE_TIN = '2:1 TiN'
MATERIAL_W = 'W'
MATERIAL_IL = 'IL'
MATERIAL_HFO2 = 'HfO2'
MATERIAL_LA2O3 = 'La2O3'
MATERIAL_AL2O3 = 'Al2O3'
MATERIAL_TIALC = 'TiAlC'
MATERIAL_SIGE = 'SiGe'
MATERIAL_TAN = 'TaN'
MATERIAL_TASIN = 'TaSiN'
MATERIAL_AL = 'Al'
MATERIAL_SR2O3 = 'Sr2O3'
MATERIAL_CE2O3 = 'Ce2O3'
MATERIAL_Y2O3 = 'Y2O3'
MATERIAL_ZRO2 = 'ZrO2'
MATERIAL_SO2 = 'SO2'
MATERIAL_GEO2 = 'GeO2'

#declaring voltage_per_thickness
VOLTAGE_PER_THICKNESS = dict([])
VOLTAGE_PER_THICKNESS[MATERIAL_ONE_ONE_TIN] = 5.0
VOLTAGE_PER_THICKNESS[MATERIAL_TWO_ONE_TIN] = 3.0
VOLTAGE_PER_THICKNESS[MATERIAL_W] = 5.0
VOLTAGE_PER_THICKNESS[MATERIAL_IL] = 1.0
VOLTAGE_PER_THICKNESS[MATERIAL_HFO2] = 1.0
VOLTAGE_PER_THICKNESS[MATERIAL_LA2O3] = -4.0
VOLTAGE_PER_THICKNESS[MATERIAL_AL2O3] = 2.0
VOLTAGE_PER_THICKNESS[MATERIAL_TIALC] = -1.0
VOLTAGE_PER_THICKNESS[MATERIAL_SIGE] = 4.0
VOLTAGE_PER_THICKNESS[MATERIAL_TAN] = 5.0
VOLTAGE_PER_THICKNESS[MATERIAL_TASIN] = 4.0
VOLTAGE_PER_THICKNESS[MATERIAL_AL] = 3.0
VOLTAGE_PER_THICKNESS[MATERIAL_SR2O3] = 0.5
VOLTAGE_PER_THICKNESS[MATERIAL_CE2O3] = 0.3
VOLTAGE_PER_THICKNESS[MATERIAL_Y2O3] = -4.0
VOLTAGE_PER_THICKNESS[MATERIAL_ZRO2] = 1.0
VOLTAGE_PER_THICKNESS[MATERIAL_SO2] = 1.0
VOLTAGE_PER_THICKNESS[MATERIAL_GEO2] = 2.0

#declaring the materials NOT used for EOT calculation
MATERIALS_NOT_USED_FOR_EOT_CALCULATION = {MATERIAL_IL, MATERIAL_HFO2, MATERIAL_LA2O3, MATERIAL_TIALC}

#declaring the EOT coefficients
EOT_COEFFICIENT = dict([])
EOT_COEFFICIENT[MATERIAL_ONE_ONE_TIN] = 1.0/30
EOT_COEFFICIENT[MATERIAL_TWO_ONE_TIN] = -1.0/30
EOT_COEFFICIENT[MATERIAL_W] = 1.0/30
EOT_COEFFICIENT[MATERIAL_IL] = 1.0
EOT_COEFFICIENT[MATERIAL_HFO2] = 1.0/20
EOT_COEFFICIENT[MATERIAL_LA2O3] = -1.0/30
EOT_COEFFICIENT[MATERIAL_AL2O3] = 1.0/25
#EOT_COEFFICIENT[MATERIAL_TIALC] = <unknown>
EOT_COEFFICIENT[MATERIAL_SIGE] = 1.0/25
EOT_COEFFICIENT[MATERIAL_TAN] = 1.0/20
EOT_COEFFICIENT[MATERIAL_TASIN] = 1.0/25
EOT_COEFFICIENT[MATERIAL_AL] = 1.0/25
EOT_COEFFICIENT[MATERIAL_SR2O3] = 1.0/25
EOT_COEFFICIENT[MATERIAL_CE2O3] = 1.0/15
EOT_COEFFICIENT[MATERIAL_Y2O3] = -1.0/25
EOT_COEFFICIENT[MATERIAL_ZRO2] = 1.0/20
EOT_COEFFICIENT[MATERIAL_SO2] = 1.0/20
EOT_COEFFICIENT[MATERIAL_GEO2] = 1.0/15

DASHES = '-----------------------------'

execution_output = namedtuple('execution_output', ['binary_integer_programming_variables', 'binary_integer_programming_status'])

def have_nonpositive_thickness_material(material_name_to_thickness):
	for material_name in material_name_to_thickness:
		if material_name_to_thickness[material_name] <= 0:
			return True
	return False

def have_compulsory_materials(material_name_to_thickness):
	if MATERIAL_IL not in material_name_to_thickness:
		return False
	if MATERIAL_HFO2 not in material_name_to_thickness:
		return False
	if MATERIAL_LA2O3 not in material_name_to_thickness:
		return False
	if MATERIAL_TIALC not in material_name_to_thickness:
		return False
	if MATERIAL_ONE_ONE_TIN not in material_name_to_thickness and MATERIAL_TWO_ONE_TIN not in material_name_to_thickness:
		return False
	return True

def execute(material_name_to_thickness, epsilon, vt, verbose):
	if have_nonpositive_thickness_material(material_name_to_thickness):
		raise Exception('No material may have non-positive thickness')

	if epsilon <= 0:
		raise Exception('The epsilon value must be positive')

	if not have_compulsory_materials(material_name_to_thickness):
		raise Exception('Missing some compulsory materials')

	if verbose:
		print DASHES
		print 'Starting Computation'
		print 'Material name to Thickness Map:', material_name_to_thickness
		print 'Vt =', vt
		print 'epsilon =', epsilon
		print DASHES

	prob = LpProblem('finding_material_combination', LpMinimize)
	material_name_to_variable = dict([])
	material_index = 0
	for material_name in material_name_to_thickness:
		var_name = "var_"+material_name
		var = LpVariable(var_name, cat='Binary')
		material_name_to_variable[material_name] = var
		material_index += 1


	objective_terms_arr = []
	optional_materials_in_eot = set([])

	has_both_one_one_tin_and_two_one_tin = (MATERIAL_ONE_ONE_TIN in material_name_to_thickness) and (MATERIAL_TWO_ONE_TIN in material_name_to_thickness)

	for material_name in material_name_to_variable:
		if material_name in MATERIALS_NOT_USED_FOR_EOT_CALCULATION:
			pass
		elif not has_both_one_one_tin_and_two_one_tin and material_name == MATERIAL_ONE_ONE_TIN:
			pass
		elif not has_both_one_one_tin_and_two_one_tin and material_name == MATERIAL_TWO_ONE_TIN:
			pass		
		else:
			var = material_name_to_variable[material_name]
			term = (var, EOT_COEFFICIENT[material_name] * material_name_to_thickness[material_name])
			objective_terms_arr += [term]
			optional_materials_in_eot |= set([material_name])

	objective = LpAffineExpression(objective_terms_arr)
	prob.setObjective(objective)

	if verbose:
		print 'Objective function to Minimize: ', objective

	compulsory_material_remarks = []

	vt_terms_arr = []
	vt_lhs_cons = 0.0
	for material_name in material_name_to_variable:
		coefficient_value = VOLTAGE_PER_THICKNESS[material_name] * material_name_to_thickness[material_name]
		if material_name in optional_materials_in_eot:
			term = (material_name_to_variable[material_name], coefficient_value)
			vt_terms_arr += [term]
		else:
			term = coefficient_value
			vt_lhs_cons += term
			if verbose:
				compulsory_material_remarks += [material_name+' ; voltage per thickness = '+str(VOLTAGE_PER_THICKNESS[material_name])+' ; thickness = '+str(material_name_to_thickness[material_name])+' ; Vt term value = '+str(coefficient_value)]

	if verbose and len(compulsory_material_remarks) > 0:
		print 'Compulsory Materials:'
		for remark in compulsory_material_remarks:
			print '\t'+remark

	vt_expression = LpAffineExpression(vt_terms_arr)
	upperbound = vt + epsilon - vt_lhs_cons
	lowerbound = vt - epsilon - vt_lhs_cons

	upperbound_constraint = LpConstraint(vt_expression, sense=constants.LpConstraintLE, name='upperbound_constraint', rhs=upperbound)
	lowerbound_constraint = LpConstraint(vt_expression, sense=constants.LpConstraintGE, name='lowerbound_constraint', rhs=lowerbound)

	if verbose:
		print 'Upperbound Constraint:',upperbound_constraint
		print 'Lowerbound Constraint:',lowerbound_constraint

	prob.constraints[upperbound_constraint.name] = upperbound_constraint
	prob.constraints[lowerbound_constraint.name] = lowerbound_constraint

	if has_both_one_one_tin_and_two_one_tin:
		#Only one of them is compulsory, but it's ok to use both of them
		tin_constraint = LpConstraint(LpAffineExpression([(material_name_to_variable[MATERIAL_ONE_ONE_TIN], 1), (material_name_to_variable[MATERIAL_TWO_ONE_TIN], 1)]), sense=constants.LpConstraintGE, name='tin_constraint', rhs=1)
		prob.constraints[tin_constraint.name] = tin_constraint
		if verbose:
			print '(1:1) TiN and (2:1) TiN Constraint:', tin_constraint

	#Solving the problem
	#GLPK().solve(prob)
	prob.solve()	
	binary_integer_programming_variables = dict([])
	for v in prob.variables():
		binary_integer_programming_variables[v.name] = v.varValue

	binary_integer_programming_status=LpStatus[prob.status]

	output = execution_output(binary_integer_programming_variables=binary_integer_programming_variables, binary_integer_programming_status=binary_integer_programming_status)

	if verbose:
		print DASHES
		print 'Computation Is Completed'
		print 'Variables:',binary_integer_programming_variables
		print 'Status:',binary_integer_programming_status
		print DASHES

	return output


