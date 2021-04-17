<?php
    include "html.php";
    include "test_support.php";

    ini_set('display_errors', 'stderr');

    function error_print($msg) {
        fwrite(STDERR, "$msg\n");
        exit(10);
    }

    function error_print_io($msg) {
        fwrite(STDERR, "$msg\n");
        exit(41);
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

    if (array_key_exists("help", $options)) {
        print_r("simeple test script for IPP21 project\n\n");
        print_r("Params:\n");
        print_r("--directory with tests directory\n");
        print_r("--recursive find test in subdirs\n");
        print_r("--parse-script testing parse script\n");
        print_r("--int-script testing interpret script\n");
        print_r("--parse-only run only parse tests\n");
        print_r("--int-only run only interpret tests\n");
        print_r("--jexamxml\n");
        print_r("--jexamcfg\n");
        exit(0);
    }

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

    $jexamxml = [
        "jexamxml" => "",
        "jexamcfg" => ""
    ];

    if (array_key_exists("jexamxml", $options)) {
        $jexamxml["jexamxml"] = $options["jexamxml"];
    } else {
        $jexamxml["jexamxml"] = "/pub/courses/ipp/jexamxml/jexamxml.jar";
    }
    
    if  (array_key_exists("jexamcfg", $options)) {
        $jexamxml["jexamcfg"] = $options["jexamcfg"];
    } else {
        $jexamxml["jexamcfg"] = "/pub/courses/ipp/jexamxml/options";
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

    //check if can access all dirs
    if (!file_exists($test_path) || !is_dir($test_path)) {
        error_print_io("cant open dir with path with tests");
    }

    if (!is_readable($parse_path) && $parse) {
        error_print_io("cant open prase script");
    }

    if ($parse) {
        if (!is_readable($jexamxml['jexamcfg']) || !is_readable($jexamxml['jexamxml'])) {
            error_print_io("cant open jexam files");
        }
    }

    if (!is_readable($int_path) && !$parse) {
        error_print_io("cant open int script");
    }

    $tests = [];

    if ($recursive) {
        run_tests_indir($test_path, $tests, $parse, $parse_path, $int_path, $jexamxml);
        recursive_tests($test_path, $tests, $parse, $parse_path, $int_path, $jexamxml);
    } else {
        run_tests_indir($test_path, $tests, $parse, $parse_path, $int_path, $jexamxml);
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

    exit(0);
?>