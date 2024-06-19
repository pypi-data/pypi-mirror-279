from .templates import ExtendedModel

FCDE = ExtendedModel(
  boxWidth=0.14509394397496592,
  rows=25,
  columns=[None, 0.02818371763906058, 0.03653445043604164, None, 0.02818371763906058, 0.03653445043604164, None],
  pre_row_offsets=[1/25],
  post_row_offsets=[1.8/25, 0.8/25]
)
"""Official model of the Catalan Chess Federation (Federació Catalana d'Escacs, FCdE)"""

ANDORRA = ExtendedModel(
  boxWidth=0.141,
  rows=20,
  columns=[None, 0.024, 0.05, None, 0.024, 0.05, None],
  pre_row_offsets=[0.03, 0.05]
)
"""Official model of the Andorran Chess Federation"""

LLOBREGAT23 = ExtendedModel(
  boxWidth=0.23,
  rows=30,
  columns=[None, 0.07, None],
  pre_row_offsets=[0.8/30, 1/30]
)
"""Model used in the IV Llobregat Open (December 2023)"""