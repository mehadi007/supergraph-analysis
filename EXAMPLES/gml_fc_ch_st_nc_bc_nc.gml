graph [
	comment "This is the fc_ch_st_nc_bc_nc graph"
	directed 0
	node [
	  id 1
	  label "1"
	  type "fc"
	  image "fc.png"
	  size 3
	]
	node [
	  id 2
	  label "2"
	  type "ch"
	  image "ch.png"
	  size 4
	]
	node [
	  id 3
	  label "3"
	  type "st"
	  image "st.png"
	  size 7
	]
	node [
	  id 4
	  label "4"
	  type "nc"
	  image "nc.png"
	  size 4
	]
	node [
	  id 5
	  label "5"
	  type "bc"
	  image "bc.png"
	  size 5
	]
	node [
	  id 6
	  label "6"
	  type "nb"
	  image "nb.png"
	  size 6
	]
	node [
	  id 7
	  label "7"
	  type "noise"
	  image noise.png
	  size 0
	]
	edge [
	   source 1
	   target 2
	   weight 3
	   norm_interaction 0.250
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 1
	   target 3
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 1
	   target 4
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 1
	   target 5
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 1
	   target 6
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 2
	   target 3
	   weight 0
	   norm_interaction 0.000
	   overlap 1
	   norm_overlap 0.250
	]
	edge [
	   source 2
	   target 4
	   weight 1
	   norm_interaction 0.062
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 2
	   target 5
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 2
	   target 6
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 3
	   target 4
	   weight 1
	   norm_interaction 0.036
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 3
	   target 5
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 3
	   target 6
	   weight 0
	   norm_interaction 0.000
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 4
	   target 5
	   weight 2
	   norm_interaction 0.100
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 4
	   target 6
	   weight 1
	   norm_interaction 0.042
	   overlap 0
	   norm_overlap 0.000
	]
	edge [
	   source 5
	   target 6
	   weight 0
	   weight 0.000
	   overlap 1
	   norm_overlap 0.200
	]
]
