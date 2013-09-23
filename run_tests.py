from sqlalchemy.dialects import registry

registry.register("crate", "crate.client.sqlalchemy", "CrateDialect")

from sqlalchemy.testing import runner


# use this in setup.py 'test_suite':
# test_suite="run_tests.setup_py_test"
def setup_py_test():
    runner.setup_py_test()

if __name__ == '__main__':
    runner.main()
