"""
Runs the full SauceDemo automated test suite and prints a summary report.
Usage: python run_all_tests.py
"""
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run:  {result.testsRun}")
    print(f"Failures:   {len(result.failures)}")
    print(f"Errors:     {len(result.errors)}")
    print(f"Passed:     {result.testsRun - len(result.failures) - len(result.errors)}")
