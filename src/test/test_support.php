<?php
    /* config for code interprets */
    /* for merlin:
        php7.4
        python3.8
        java
    */
    $php_exec = "php";
    $python_exec = "python3";
    $java_exec = "java";

    /**
     * Runs test rucursive for subdirs in dir and dir it self
     * @param $test_path path to test dir
     * @param $test [OUTPUT] array with tests and status of test (pass/not pass)
     * @param $parse bool is testing parse if false testing interpret
     * @param $parse_path path to parse program
     * @param $int_path path to interpret program
     * @param $jexamxml array of config for jexamxml diff if null
     */
    function recursive_tests($test_path, &$tests, $parse, $parse_path, $int_path, $jexamxml) {
        foreach (glob($test_path.'/*', GLOB_ONLYDIR) as $dir) {
            run_tests_indir($dir, $tests, $parse, $parse_path, $int_path, $jexamxml);
            recursive_tests($dir, $tests, $parse, $parse_path, $int_path, $jexamxml);
        }
    }

    /**
     * Runs test on files on dir
     * @param $test_path path to test dir
     * @param $test [OUTPUT] array with tests and status of test (pass/not pass)
     * @param $parse bool is testing parse if false testing interpret
     * @param $parse_path path to parse program
     * @param $int_path path to interpret program
     * @param $jexamxml array of config for jexamxml diff if null
     */
    function run_tests_indir($test_path, &$tests, $parse, $parse_path, $int_path, $jexamxml) {
        global $php_exec, $python_exec;

        foreach (glob("$test_path/*.src") as $filename) {
            $test_name = substr($filename, 0, -4);

            if (!is_readable($filename)) {
                error_print_io("cant open test file $filename");
            }
    
            if (file_exists($test_name.'.in')) {

                if (!is_readable($test_name.'.in')) {
                    error_print_io("cant open test file $filename");
                }

                if ($parse) {
                    exec_test("$php_exec $parse_path < $filename", $test_name);
                } else {
                    exec_test("$python_exec $int_path --source $filename --input $test_name.in", $test_name);
                }
            } else {
                if ($parse) {
                    exec_test("$php_exec $parse_path < $filename", $test_name);
                } else {
                    exec_test("$python_exec $int_path --source $filename", $test_name);
                }
            }
    
            $dir = dirname($test_name);
    
            if (!array_key_exists($dir, $tests)){
                $tests[$dir] = [];
            }
    
            array_push($tests[$dir], [basename($test_name), test_passed($test_name, $parse, $jexamxml)]);
        }
    }

    /**
     * exec test (save output to file and return code)
     * @param $command command to test
     * @param $test_name name of test (for file save name.testrc and name.testout)
     */
    function exec_test($command, $test_name) {
        exec("$command > $test_name.testout", $output, $rc);
        file_put_contents($test_name.'.testrc', "$rc\n");
    }

    /**
     * get success rate of all tests in %
     * @param $array array of exec tests
     */
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

    /**
     * get success rate of all tests in dir in %
     * @param $array array of exec tests in dir
     */
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

    /**
     * check if test pass or not
     * @param $test_name name of test for find output files
     * @param $parse say if parse program tests or interpret tests
     * @param $jexamxml array of config for jexamxml diff if $parse == false
     * @return bool
     */
    function test_passed($test_name, $parse, $jexamxml) {
        global $java_exec;

        if (!file_exists($test_name.'.rc')) {
            file_put_contents($test_name.'.rc', "0\n");
        }

        if (!is_readable($test_name.'.rc')) {
            error_print_io("cant open test file $test_name.rc");
        }

        if (!is_readable($test_name.'.testrc')) {
            error_print_io("cant open test file $test_name.testrc");
        }

        $retval = null;
        $output = null;

        exec("diff --ignore-all-space $test_name.rc $test_name.testrc", $output, $retval);
        if ($retval != 0) return false;

        $rc = fgets(fopen("$test_name.rc", 'r'));

        if (trim($rc) == '0') { //if return coude is not zero i dont care about output

            if (!is_readable($test_name.'.out')) {
                error_print_io("cant open test file $test_name.out");
            }
            
            if (!is_readable($test_name.'.testout')) {
                error_print_io("cant open test file $test_name.testout");
            }    

            if ($parse) {
                exec("$java_exec -jar {$jexamxml['jexamxml']} $test_name.out $test_name.testout {$jexamxml['jexamcfg']}", $output, $retval);
            } else {
                exec("diff $test_name.out $test_name.testout", $output, $retval);
            }

            if ($retval != 0) return false;
        }

        return true;
    }