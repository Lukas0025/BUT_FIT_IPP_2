<?php

    function recursive_tests($test_path, &$tests, $parse, $parse_path, $int_path) {
        run_tests_indir($test_path, $tests, $parse, $parse_path, $int_path);
        foreach (glob($test_path.'/*', GLOB_ONLYDIR) as $dir) {
            run_tests_indir($dir, $tests, $parse, $parse_path, $int_path);
            recursive_tests($dir, $tests, $parse, $parse_path, $int_path);
        }
    }

    function run_tests_indir($test_path, &$tests, $parse, $parse_path, $int_path) {
        foreach (glob("$test_path/*.src") as $filename) {
            $test_name = substr($filename, 0, -4);
    
            if (file_exists($test_name.'.in')) {
                if ($parse) {
                    exec_test("php $parse_path < $filename", $test_name);
                } else {
                    exec_test("python3 $int_path --source $filename --input $test_name.in", $test_name);
                }
            } else {
                if ($parse) {
                    exec_test("php $parse_path < $filename", $test_name);
                } else {
                    exec_test("python3 $int_path --source $filename", $test_name);
                }
            }
    
            $dir = dirname($test_name);
    
            if (!array_key_exists($dir, $tests)){
                $tests[$dir] = [];
            }
    
            array_push($tests[$dir], [basename($test_name), test_passed($test_name)]);
        }
    }

    function exec_test($command, $test_name) {
        exec("$command > $test_name.testout", $output, $rc);
        file_put_contents($test_name.'.testrc', "$rc\n");
    }

    function fullSuccessRate($array) {
        $success = 0;
        $fail = 0;

        foreach ($array as $dir_tests) {
            foreach ($dir_tests as $item) {
                if ($item[1]) {
                    $success++;
                } else {
                    $fail++;
                }
            }
        }

        return round($success * 100 / ($fail + $success));
    }

    function successRate($array) {
        $success = 0;
        $fail = 0;

        foreach ($array as $item) {
            if ($item[1]) {
                $success++;
            } else {
                $fail++;
            }
        }

        return round($success * 100 / ($fail + $success));
    }

    function test_passed($test_name) {
        if (!file_exists($test_name.'.rc')) {
            file_put_contents($test_name.'.rc', "0\n");
        }

        $retval = null;
        $output = null;
        exec("diff --ignore-all-space $test_name.rc $test_name.testrc", $output, $retval);
        if ($retval != 0) return false;

        $rc = fgets(fopen("$test_name.rc", 'r'));

        if (trim($rc) == '0') {
            exec("diff $test_name.out $test_name.testout", $output, $retval);
            if ($retval != 0) return false;
        }

        return true;
    }