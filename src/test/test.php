<?php
    include "html.php";
    include "test_support.php";

    ini_set('display_errors', 'stderr');

    function error_print($msg) {
        fwrite(STDERR, "$msg\n");
        exit(10);
    }
    
    $longopts  = array(
        "help",
        "directory:",
        "recursive",
        "parse-script:",
        "int-script:",
        "parse-only",
        "int-only",
        "jexamxml:",
        "jexamcfg:"
    );
    
    $options = getopt("", $longopts);
    $parse = FALSE;
    $interp = FALSE;
    $parse_path = null;
    $int_path = null;

    if (!array_key_exists("directory", $options)) {
        error_print("need directory param");
    }

    $test_path = $options['directory'];

    if (array_key_exists("parse-only", $options) && array_key_exists("int-only", $options)) {
        error_print("cant do --parse-only and --int-only in same time");
    } else if (!array_key_exists("parse-only", $options) && !array_key_exists("int-only", $options)) {
        error_print("need --parse-only or --int-only");
    } else if (array_key_exists("parse-only", $options)) {
        $parse = TRUE;
    } else {
        $interp = TRUE;
    }

    if ($parse) {
        if (!array_key_exists("parse-script", $options)) {
            error_print("need --parse-script");
        }

        $parse_path = $options['parse-script'];
    } else {
        if (!array_key_exists("int-script", $options)) {
            error_print("need --int-script");
        }

        $int_path = $options['int-script'];
    }

    $recursive = FALSE;
    if (array_key_exists("recursive", $options)) {
        $recursive = TRUE;
    }

    $tests = [];

    if ($recursive) {
        recursive_tests($test_path, $tests, $parse, $parse_path, $int_path);
    } else {
        run_tests_indir($test_path, $tests, $parse, $parse_path, $int_path);
    }
    

    $html = "";
    foreach ($tests as $dir => $dir_tests) {
        $test_html = "";
        foreach ($dir_tests as $test) {
            $test_html .= test_html($test[0], $test[1]);
        }

        $html .= forder_html($dir, successRate($dir_tests), $test_html);
    }

    echo generate_html("<h1 class='title'>IPP Automatické testy - " . fullSuccessRate($tests) . "%</h1>" . $html);
?>