<?php
    include "html.php";

    function exec_test($command, $test_name) {
        exec("$command > $test_name.testout", $output, $rc);
        file_put_contents($test_name.'.testrc', "$rc\n");
    }

    function test_passed($test_name) {
        if (!file_exists($test_name.'.rc')) {
            file_put_contents($test_name.'.rc', "0\n");
        }

        $retval = null;
        $output = null;
        exec("diff --ignore-all-space $test_name.rc $test_name.testrc", $output, $retval);
        if ($retval != 0) return false;
        
        exec("diff $test_name.out $test_name.testout", $output, $retval);
        if ($retval != 0) return false;

        return true;
    }

    $test_path = "/home/lukasplevac/Plocha/tests";
    $int_path = "python3 ../interpret/interpret.py";

    $passed = [];
    $failed = [];

    foreach (glob("$test_path/*/*.src") as $filename) {
        $test_name = substr($filename, 0, -4);

        if (file_exists($test_name.'.in')) {
            exec_test("$int_path --source $filename --input $test_name.in", $test_name);
        } else {
            exec_test("$int_path --source $filename", $test_name);
        }

        if (test_passed($test_name)) {
            array_push($passed, $test_name);
        } else {
            array_push($failed, $test_name);
        }
    }

    $html = "";
    foreach ($failed as $fail) {
        $html .= test_html($fail, false);
    }

    foreach ($passed as $pass) {
        $html .= test_html($pass, true);
    }

    echo $html;

    echo count($failed)


?>