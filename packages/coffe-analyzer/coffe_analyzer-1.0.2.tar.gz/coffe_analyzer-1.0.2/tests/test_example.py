import os
import sys
import pytest

pkg_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_path not in sys.path:
    sys.path.append(pkg_path)
    
from src.coffeanalyzer.coffeanalyzer import CoffeInstance

def main():
    path_csv = 'tests/test_files/example.csv'

    loss_coffe = CoffeInstance(
        ignored_states=['O'], 
        ignored_results=['No Loss']
        )

    script_results = loss_coffe.get_simplified_expression_from_csv(path_csv)

    return script_results

def test_total_loss():
    script_results = main()
    expected_result = "(A_F AND B_F) OR (C_F AND D_F)"

    assert script_results['Total Loss'] == expected_result

def test_partial_loss():
    script_results = main()
    expected_result = "A_F OR B_F OR C_F OR D_F"

    assert script_results['Partial Loss'] == expected_result

def test_custom_headers_error():
    path_csv = 'tests/test_files/example.csv'

    loss_coffe = CoffeInstance(
        ignored_states=['O'], 
        ignored_results=['No Loss'],
        custom_headers=["A", "B", "C"]
        )
    
    with pytest.raises(ValueError):
        _ = loss_coffe.get_simplified_expression_from_csv(path_csv)
