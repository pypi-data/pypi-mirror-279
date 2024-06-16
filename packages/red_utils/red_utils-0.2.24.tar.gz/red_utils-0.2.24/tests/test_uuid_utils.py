from __future__ import annotations

from .std_tests.uuid_util_tests.expect_fail_tests import (
    test_fail_first_n_chars,
    test_fail_gen_uuid,
    test_fail_get_rand_uuid,
    test_fail_trim_uuid,
)
from .std_tests.uuid_util_tests.expect_pass_tests import (
    test_first_n_chars,
    test_gen_uuid,
    test_gen_uuid_str,
    test_get_rand_uuid,
    test_get_rand_uuid_str,
    test_get_rand_uuid_trim,
    test_trim_uuid,
    test_trim_uuid_str,
)
