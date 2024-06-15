# SAE ARP4761 Annex Q
# Section Q.4.4.1 - Combined Functional Failure Effects Analysis

import os
import sys

pkg_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_path not in sys.path:
    sys.path.append(pkg_path)

from src.coffeanalyzer.coffeanalyzer import CoffeInstance

def test_highspeed_overrun():
    path_csv = 'tests/test_files/table_Q-4-6.csv'

    overrun_coffe = CoffeInstance(
        ignored_states=['O'], 
        ignored_results=['No overrun', 'Low-speed overrun'], 
        custom_headers=['WBrake', 'GrndSpoiler', 'ThrustRev', 'Flap']
        )

    script_results = overrun_coffe.get_simplified_expression_from_csv(path_csv)

    # Last paragraph of Section Q.4.4.1 states:
    # Through the CoFFE analysis it can be concluded that “the total loss of wheel brake function in addition 
    # to the partial (or total) loss of any ground spoiler or thrust reverser or flap functions” might result 
    # in high-speed overruns. 
    # Thus:
    arp_result = "WBrake_F AND (Flap_D OR Flap_F OR GrndSpoiler_D OR GrndSpoiler_F OR ThrustRev_D OR ThrustRev_F)"

    assert script_results['High-speed overrun'] == arp_result
