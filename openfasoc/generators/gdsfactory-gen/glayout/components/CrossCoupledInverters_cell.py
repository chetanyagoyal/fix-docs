####
# Compiled Glayout
# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/
# 2024-05-16 12:04:37.648184

from glayout.pdk.mappedpdk import MappedPDK
from gdsfactory import Component
from glayout.pdk.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance
from glayout.pdk.util.port_utils import remove_ports_with_prefix
from glayout.primitives.fet import nmos
from glayout.primitives.fet import pmos
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap
from glayout.primitives.mimcap import mimcap_array
from glayout.primitives.via_gen import via_stack
from glayout.primitives.via_gen import via_array
from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.placement.four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.components.diff_pair import diff_pair_generic
from glayout.routing.smart_route import smart_route
from glayout.routing.L_route import L_route
from glayout.routing.c_route import c_route
from glayout.routing.straight_route import straight_route

def CrossCoupledInverters_cell(
	pdk: MappedPDK,
	ccinvs_numfingers: int, 
):
	pdk.activate()
	CrossCoupledInverters = Component(name="CrossCoupledInverters")
	maxmetalsep = pdk.util_max_metal_seperation()
	double_maxmetalsep = 2*pdk.util_max_metal_seperation()
	triple_maxmetalsep = 3*pdk.util_max_metal_seperation()
	quadruple_maxmetalsep = 4*pdk.util_max_metal_seperation()
	# placing ccinvs centered at the origin
	ccinvs = generic_4T_interdigitzed(pdk,**{'numcols': ccinvs_numfingers, 'top_row_device': "pfet", 'bottom_row_device': "nfet"})
	ccinvs_ref = prec_ref_center(ccinvs)
	CrossCoupledInverters.add(ccinvs_ref)
	CrossCoupledInverters.add_ports(ccinvs_ref.get_ports_list(),prefix="ccinvs_")
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_source_E"],CrossCoupledInverters.ports["ccinvs_top_B_source_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_A_source_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_source_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_drain_E"],CrossCoupledInverters.ports["ccinvs_top_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_A_drain_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_B_drain_E"],CrossCoupledInverters.ports["ccinvs_top_A_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_B_drain_E"],CrossCoupledInverters.ports["ccinvs_bottom_A_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_B_gate_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_gate_W"],CrossCoupledInverters.ports["ccinvs_bottom_A_gate_W"],ccinvs_ref,CrossCoupledInverters,**{})
	return CrossCoupledInverters
