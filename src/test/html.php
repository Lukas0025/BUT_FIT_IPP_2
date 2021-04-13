<?php
    function test_html($name, $pass) {
        
        $status = $pass ? "PASS" : "FAIL";
        $status_class = $pass ? "pass" : "fail";
        
        return "<div class='test'>
            <div class='$status_class base'>
                <span class='status'>$status</span> - 
                <span class='name'>$name</span>
            </div>
        </div><hr>";
    }

    function forder_html($name, $success_rate, $tests) {
        return "<div class='forder'>
            <div class='forderbase'>
                <span class='name'>$name</span>
                <div class='progress'>
                    <span>$success_rate%</span>
                    <progress value='$success_rate' max='100'> $success_rate% </progress>
                </div>
            </div>
            <div class='tests'>
                $tests
            </div>
        </div>";
    }

    function generate_html($body) {
        $simple_css = ".forderbase > * {
            display: inline-block;
            font-size: 27px;
            font-weight: bold;
        }

        .title {
            text-align: center;
            margin: 40px;
        }
        
        .forderbase {
            background-color: lightgray;
            border-radius: 20px;
            padding: 22px;
        }
        
        .progress {
            float: right;
        }
        
        .tests {
            margin-left: 30px;
        }
        
        .tests {
            background-color: #f3f1f1;
            border-radius: 10px;
            padding: 16px;
        }
        
        .pass > .status {
            color: green;
        }
    
        .fail > .status {
            color: red;
        }
        
        .base {
            font-size: 20px;
            font-weight: bold;
        }
        
        .info {
            margin-left: 25px;
        }";

        return "<html><head><style>$simple_css</style></head><body>$body</body></html>";
    }

