<?php

require __DIR__ . '/../vendor/autoload.php';

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

$logger = new Logger('ChanIQLogger');
$logger->pushHandler(new StreamHandler(__DIR__ . '/../log/chaniq-php.log', Logger::DEBUG));

?>