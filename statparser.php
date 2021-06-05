<?php

class GameResult
{
    const COMPLETION_BIT1              = 1;    //C&C95 for bit 1 prints "C&C95 - Completion status is player 2 resigned.\n"
    const COMPLETION_DISCONNECTED      = 2;    //Lost Connection To or Kicked/Autokicked CONFIRMED// for bit 2 C&C95 prints "C&C95 - Completion status is player 1 disconnected.\n"
    const COMPLETION_BIT4              = 4;
    const COMPLETION_NO_COMPLETION  = 8;    //Player didn't see game completion// //<CCHyper> 0x8 is i think when the player didn't see the end of the game Needs checking
    const COMPLETION_QUIT              = 16;   //Player Resigned/Quit it seems, Hitting Quit ingame sets this CONFIRMED /////Seems to be set when a player was specifically kicked via the Kick button instead of waiting for timeout
    const COMPLETION_BIT32             = 32;
    const COMPLETION_DRAW              = 64;   //CONFIRMED for Red Alert, unknown for TS/YR
    const COMPLETION_BIT128            = 128;
    const COMPLETION_WON               = 256;  //CONFIRMED
    const COMPLETION_DEFEATED          = 512;  //CONFIRMED
    const COMPLETION_BIT1024           = 1024;
    const COMPLETION_BIT2048           = 2048;
    const COMPLETION_BIT4096           = 4096;
    const COMPLETION_BIT8192           = 8192;
    const COMPLETION_BIT16384          = 16384;
    const COMPLETION_BIT32768          = 32768;
}

$CountableHeaps = [
        "UNB" => "Units Bought",
        "INB" => "Infantry Bought",
        "PLB" => "Planes Bought",
        "VSB" => "Ships Built",
        "BLB" => "Buildings Bought",
        "UNK" => "Units Killed",
        "INK" => "Infantry Killed",
        "PLK" => "Planes Killed",
        "VSK" => "Ships Killed",
        "BLK" => "Buildings Killed",
        "BLC" => "Buildings Captured",
        "UNL" => "Units Left",
        "INL" => "Infantry Left",
        "PLL" => "Planes Left",
        "BLL" => "Buildings Left",
        "VSL" => "Ships Left",
        "CRA" => "Crates Found"
    ];

$Types =  [
            "CR" =>
            [
                "Armor",
                "Firepower",
                "HealBase",
                "Money",
                "Reveal",
                "Speed",
                "Veteran",
                "Unit",
                "Invulnerability",
                "IonStorm",
                "Gas",
                "Tiberium",
                "Pod",
                "Cloak",
                "Darkness",
                "Explosion",
                "ICBM",
                "Napalm",
                "Squad"
            ],
            "IN" => [
                "E1",
                "E2",
                "SHK",
                "ENGINEER",
                "JUMPJET",
                "GHOST",
                "YURI",
                "IVAN",
                "DESO",
                "DOG",
                "CIV1",
                "CIV2",
                "CIV3",
                "CTECH",
                "WEEDGUY",
                "CLEG",
                "SPY",
                "CCOMAND",
                "PTROOP",
                "CIVAN",
                "YURIPR",
                "SNIPE",
                "COW",
                "ALL",
                "TANY",
                "FLAKT",
                "TERROR",
                "SENGINEER",
                "ADOG",
                "VLADIMIR",
                "PENTGEN",
                "PRES",
                "SSRV",
                "CIVA",
                "CIVB",
                "CIVC",
                "CIVBBP",
                "CIVBFM",
                "CIVBF",
                "CIVBTM",
                "CIVSFM",
                "CIVSF",
                "CIVSTM",
                "POLARB",
                "JOSH",
                "YENGINEER",
                "GGI",
                "INIT",
                "BORIS",
                "BRUTE",
                "VIRUS",
                "CLNT",
                "ARND",
                "STLN",
                "CAML",
                "EINS",
                "MUMY",
                "RMNV",
                "LUNR",
                "DNOA",
                "DNOB",
                "SLAV",
                "WWLF",
                "YDOG",
                "YADOG",
            ],
            "UN" =>
            [
                "AMCV",
                "HARV",
                "APOC",
                "HTNK",
                "SAPC",
                "CAR",
                "BUS",
                "WINI",
                "PICK",
                "MTNK",
                "HORV",
                "TRUCKA",
                "TRUCKB",
                "CARRIER",
                "V3",
                "ZEP",
                "DRON",
                "HTK",
                "DEST",
                "SUB",
                "AEGIS",
                "LCRF",
                "DRED",
                "SHAD",
                "SQD",
                "DLPH",
                "SMCV",
                "TNKD",
                "HOWI",
                "TTNK",
                "HIND",
                "LTNK",
                "CMON",
                "CMIN",
                "SREF",
                "XCOMET",
                "HYD",
                "MGTK",
                "FV",
                "DeathDummy",
                "VLAD",
                "DTRUCK",
                "PROPA",
                "CONA",
                "COP",
                "EUROC",
                "LIMO",
                "STANG",
                "SUVB",
                "SUVW",
                "TAXI",
                "PTRUCK",
                "CRUISE",
                "TUG",
                "CDEST",
                "YHVR",
                "PCV",
                "SMIN",
                "SMON",
                "YCAB",
                "YTNK",
                "BFRT",
                "TELE",
                "CAOS",
                "DDBX",
                "BCAB",
                "BSUB",
                "SCHP",
                "JEEP",
                "MIND",
                "DISK",
                "UTNK",
                "ROBO",
                "YDUM",
                "SCHD",
                "DOLY",
                "CBLC",
                "FTRK",
                "AMBU",
                "CIVP",
                "VISC_LRG",
                "VISC_SML"
            ],
            "PL" => [
                "APACHE",
                "ORCA",
                "HORNET",
                "V3ROCKET",
                "ASW",
                "DMISL",
                "PDPLANE",
                "BEAG",
                "CARGOPLANE",
                "BPLN",
                "SPYP",
                "CMISL",
            ],
            "BL" => [
                "GAPOWR",
                "GAREFN", //Ore Refinery
                "GACNST",
                "GAPILE", //Barracks
                "GASAND",
                "GADEPT", //War factory
                "GATECH",
                "GAWEAP", //Service depot
                "CALAB",
                "NAPOWR",
                "NATECH",
                "NAHAND",
                "GAWALL",
                "NARADR",
                "NAWEAP",
                "NAREFN",
                "NAWALL",
                "CAHSE07",
                "NAPSIS",
                "CASYDN01",
                "NALASR",
                "NASAM",
                "CASYDN02",
                "GAYARD",
                "NAIRON",
                "NACNST",
                "NADEPT",
                "GACSPH",
                "GADUMY",
                "GAWEAT",
                "CABHUT",
                "GALITE",
                "REDLAMP",
                "GRENLAMP",
                "BLUELAMP",
                "YELWLAMP",
                "PURPLAMP",
                "INORANLAMP",
                "INGRNLMP",
                "INREDLMP",
                "INBLULMP",
                "CITY01",
                "CITY02",
                "CITY03",
                "CITY04",
                "CITY05",
                "CITY06",
                "CAHOSP",
                "INGALITE",
                "INYELWLAMP",
                "INPURPLAMP",
                "NEGLAMP",
                "NEGRED",
                "TESLA",
                "NAMISL",
                "ATESLA",
                "CAMACH",
                "TSTLAMP",
                "CASYDN03",
                "AMMOCRAT",
                "GAGREEN",
                "NAYARD",
                "GASPYSAT",
                "GAGAP",
                "GTGCAN",
                "NANRCT",
                "GAPILL",
                "NAFLAK",
                "CAOUTP",
                "CATHOSP",
                "CAAIRP",
                "CAOILD",
                "NACLON",
                "GAOREP",
                "CACITY01",
                "CACITY02",
                "CACITY03",
                "CACITY04",
                "CANEWY01",
                "CANEWY04",
                "CANEWY05",
                "CASWST01",
                "CATECH01",
                "CATEXS01",
                "CATEXS02",
                "CAWASH01",
                "CAFARM01",
                "CAFARM02",
                "CALIT01E",
                "CALIT01N",
                "CALIT01S",
                "CALIT01W",
                "CAMISC01",
                "CAMISC02",
                "CAMISC03",
                "CAMISC04",
                "CAPOL01E",
                "CAPOL01N",
                "CAPOL01S",
                "CAPOL01W",
                "CASIN01E",
                "CASIN01N",
                "CASIN01S",
                "CASIN01W",
                "CAPARS01",
                "GAAIRC",
                "CAFRMA",
                "CAFRMB",
                "CAWASH05",
                "CAWASH04",
                "CAWASH03",
                "CAWASH07",
                "CAWASH11",
                "CAWSH12",
                "CAWASH14",
                "CAWASH09",
                "CAWASH10",
                "CAWASH13",
                "CAARMY01",
                "CAUSFGL",
                "CAWASH08",
                "CALIT03E",
                "CALIT03N",
                "CALIT03S",
                "CALIT03W",
                "CALIT02L",
                "CALIT02R",
                "CAHSE01",
                "CAWT01",
                "CATS01",
                "CABARN02",
                "CAWA2A",
                "CAWA2B",
                "CAWA2C",
                "CAWA2D",
                "AMRADR", //power plant
                "CAPRS03",
                "CAGARD01",
                "CARUS01",
                "CAMIAM01",
                "CATRAN01",
                "CAMIAM02",
                "CANWY05",
                "MAYAN",
                "CAEUR1",
                "CAEUR2",
                "CAEUR04",
                "CAMEX01",
                "CARUS02A",
                "CARUS02B",
                "CARUS02C",
                "CARUS02D",
                "CARUS02E",
                "CARUS02F",
                "CANEWY06",
                "CANEWY07",
                "CANEWY08",
                "CAPARS02",
                "CAPARS08",
                "CAPARS09",
                "CARUS03",
                "CANEWY10",
                "CANEWY11",
                "CANEWY12",
                "CANEWY13",
                "CANEWY14",
                "CANEWY15",
                "CANEWY16",
                "CANEWY17",
                "CANEWY18",
                "CAPARS04",
                "CAPARS05",
                "CAPARS06",
                "CAPARS07",
                "CAWASH15",
                "CAPARS10",
                "CAPARS13",
                "CAPARS14",
                "CAGAS01",
                "CAPARS11",
                "CAPARS12",
                "CAFARM06",
                "CAMIAM04",
                "NAPSYB",
                "NAPSYA",
                "CAIND01",
                "CACOLO01",
                "CANWY09",
                "CANWY22",
                "CANWY23",
                "CANWY24",
                "CANWY25",
                "CANWY26",
                "CATEXS03",
                "CATEXS04",
                "CATEXS05",
                "CARUS02G",
                "CACHIG04",
                "CAMIAM03",
                "CARUS07",
                "CATEXS06",
                "CATEXS07",
                "CATEXS08",
                "CACHIG01",
                "CACHIG02",
                "CACHIG03",
                "CAWASH16",
                "CAWASH17",
                "CACHIG05",
                "CAWASH19",
                "CARUS08",
                "CARUS09",
                "CARUS10",
                "CARUS11",
                "CANEWY20",
                "CANEWY21",
                "CARUS04",
                "CARUS05",
                "CARUS06",
                "CAMSC01",
                "CAMSC02",
                "CAMSC03",
                "CAMSC04",
                "CAMSC05",
                "CAMSC06",
                "CAMSC07",
                "CAWASH18",
                "CAEURO05",
                "CAPARK01",
                "CAPARK02",
                "CAPARK03",
                "CAHSE02",
                "CAHSE03",
                "CAHSE04",
                "CASTRT01",
                "CASTRT02",
                "CASTL01",
                "CASTL02",
                "CASTL03",
                "CASTL04",
                "CAHSE05",
                "CAHSE06",
                "CAMIAM05",
                "CAMIAM06",
                "CAMIAM07",
                "CAFNCB",
                "CAFNCW",
                "CAMEX02",
                "CAMEX03",
                "CAMEX04",
                "CAMEX05",
                "CACHIG06",
                "CAMSC08",
                "CAMSC09",
                "CAARMY02",
                "CAARMY03",
                "CAARMY04",
                "TEMMORLAMP",
                "TEMDAYLAMP",
                "TEMDUSLAMP",
                "TEMNITLAMP",
                "SNOMORLAMP",
                "SNODAYLAMP",
                "SNODUSLAMP",
                "SNONITLAMP",
                "CAKRMW",
                "CARUFGL",
                "CAFRFGL",
                "CATRAN02",
                "CACUFGL",
                "CASKFGL",
                "CALBFGL",
                "CAMIAM08",
                "CAMISC05",
                "CAMISC06",
                "CASTL05A",
                "CASTL05B",
                "CASTL05C",
                "CASTL05D",
                "CASTL05E",
                "CASTL05F",
                "CASTL05G",
                "CASTL05H",
                "CAMSC10",
                "CAGEFGL",
                "CAUKFGL",
                "CAWASH06",
                "CAMSC11",
                "CAMSC12",
                "CAMSC13",
                "CAPOFGL",
                "CAMSC12A",
                "CAMOV01",
                "CAMOV02",
                "CABUNK01",
                "CABUNK02",
                "CAFNCP",
                "CASTRT03",
                "CASTRT04",
                "CASTRT05",
                "YACNST",
                "YAPOWR",
                "YABRCK",
                "YAWEAP",
                "YAYARD",
                "YADEPT",
                "YATECH",
                "GAFWLL",
                "YAGGUN",
                "YAPSYT",
                "NAINDP",
                "YAGRND",
                "YAGNTC",
                "CASLAB",
                "CATIME",
                "YAPPET",
                "CALOND04",
                "CALOND05",
                "CALOND06",
                "CAMOON01",
                "CATRAN03",
                "CAEAST01",
                "CAEGYP01",
                "CAEGYP02",
                "CAEGYP03",
                "CALA01",
                "CALA02",
                "CALA03",
                "CALA04",
                "CALA05",
                "CALOND01",
                "CALOND02",
                "CALOND03",
                "CAMORR01",
                "CAMORR02",
                "CAMORR03",
                "CASANF01",
                "CASANF02",
                "CASANF03",
                "CASANF04",
                "CASANF05",
                "CASEAT01",
                "NATBNK",
                "GAGATE_A",
                "CASANF09",
                "CASANF10",
                "CASANF11",
                "CASANF12",
                "CASANF13",
                "CASANF14",
                "CASANF06",
                "CASANF07",
                "CASANF08",
                "CASEAT02",
                "YACOMD",
                "YAPPPT",
                "GAROBO",
                "YAREFN",
                "YAROCK",
                "NABNKR",
                "CASANF15",
                "CASANF16",
                "CASANF17",
                "CASANF18",
                "CASIN03E",
                "CASIN03S",
                "CAURB01",
                "CAURB02",
                "CAURB03",
                "CAPOWR",
                "CALA07",
                "CAEGYP06",
                "CALA08",
                "CAEAST02",
                "CABARR01",
                "CABARR02",
                "CAMORR04",
                "CAMORR05",
                "CALA09",
                "CAEGYP04",
                "CAEGYP05",
                "CALA06",
                "CAMORR06",
                "CAMORR07",
                "CAMORR08",
                "CAMORR09",
                "CAMORR10",
                "CATIME01",
                "CATIME02",
                "CALA10",
                "CALA11",
                "CALA12",
                "CALA13",
                "CAPARK04",
                "CAPARK05",
                "CAPARK06",
                "CALA14",
                "CALA15",
                "CABUNK03",
                "CABUNK04",
                "CALUNR01",
                "CALUNR02",
            ]
        ];

class YRStatParser
{
    public function getSide($side)
    {
        switch($side)
        {
            case 0:
                return "America";
            case 1:
                return "Korea";
            case 2:
                return "France";
            case 3:
                return "Germany";
            case 4:
                return "Great Britain";
            case 5:
                return "Libya";
            case 6:
                return "Iraq";
            case 7:
                return "Cuba";
            case 8:
                return "Russia";
            case 9:
                return "Yuri";
        }
        return "";
    }

    private function getFieldValue($ttl, $data)
    {
        $response = ["raw" => null, "val" => null];

        switch ($ttl["type"])
        {
            //FIELDTYPE_BYTE
            case 1:
                $v = unpack("C", $data);
                $response["val"] = $v[1];
                break;

            //FIELDTYPE_BOOLEAN
            case 2:
                $v = unpack("C", $data);
                if ($v[1] == 0)
                {
                    $response["val"] = false;
                    break;
                }
                else
                {
                    $response["val"] = true;
                    break;
                }

            //FIELDTYPE_SHORT
            case 3:
                $v = unpack("n", $data);
                $response["val"] = $v[1];
                break;

            //FIELDTYPE_UNSIGNED_SHORT
            case 4:
                $v = unpack("n", $data);
                $response["val"] = $v[1];
                break;

            //FIELDTYPE_LONG
            case 5:
                $v = unpack("N", $data);
                $response["val"] = $v[1];
                break;

            //FIELDTYPE_UNSIGNED_LONG
            case 6:
                $v = unpack("N", $data);
                $response["val"] = $v[1];
                break;

            //FIELDTYPE_CHAR
            case 7:
                $ttl["length"] -= 1;
                $v = unpack("a$ttl[length]", $data);
                //Make sure we only allow visual ascii characters and replace bad chars with ?
                $response["val"] = preg_replace('/[^\x20-\x7e]/', '?', $v[1]);
                break;

            //FIELDTYPE_CUSTOM_LENGTH
            case 20:
                $response["val"] = null;
                $response["raw"] = substr($data, 0, $ttl["length"]);;
                break;
        }

        return $response;
    }

    public function processStatsDmp($file)
    {
        global $CountableHeaps;
        global $Types;

        if($file == null)
            return null;

        $fh = fopen(realpath($file), "r");
        $data = fread($fh, 4);

        if (!$data) {
           return "Error";
        }

        $pad = 0;
        $result = [];

        while (!feof($fh))
        {
            $data = fread($fh, 8);
            if (!$data)
            {
                break;
            }

            $ttl = unpack("A4tag/ntype/nlength", $data);
            $pad = ($ttl["length"] % 4) ? 4 - ($ttl["length"] %  4) : 0;

            if ($ttl["length"] > 0)
            {
                $data = fread($fh, $ttl["length"]);

                if ($pad > 0 )
                {
                    fread($fh, $pad);
                }

                $fieldValueArr = $this->getFieldValue($ttl, $data);
                $result[$ttl["tag"]] = ["tag" => $ttl["tag"], "length" => $ttl["length"], "raw" => base64_encode($fieldValueArr["raw"]), "value" => $fieldValueArr["val"]];
            }
        }

        foreach ($CountableHeaps as $type => $name)
        {

            for ($i = 0; $i < 8; $i++)
            {
                if (isset($result["$type$i"]))
                {  
                    $raw = base64_decode($result["$type$i"]["raw"]);
                    $length = $result["$type$i"]["length"];

                    for ($j = 0, $t = 0; $j < $length; $j += 4, ++$t)
                    {
                        $count = unpack("N", substr($raw, $j, 4))[1];
                        if ($count > 0)
                        {
                            $cat = substr($type, 0, -1);
                            $result["$type$i"]["counts"][$Types[$cat][$t]] = $count;
                        }
                    }
                }
            }
        }

        return $result;
    }

    public function getGameStats($result, $thisPlayerName)
    {
        global $CountableHeaps;

        $playerStats = array();
        $gameResult = null;
        $gameReport = [];
        $reporter = null;
        $cncnetGame = "yr";

        foreach($result as $key => $value)
        {
            $property = substr($key, 0, -1);

            if ($property == "NAM")
            {
                $id = substr($key, -1);
                $playerStats[$id] = [];
                $playerStats[$id]["name"] = $value['value'];
                if ($thisPlayerName == $playerStats[$id]["name"]) {
                    $reporter = $playerStats[$id];
                }
            }
        }

        foreach($result as $key => $value)
        {
            $cid = substr($key, -1); // Current Index
            $property = substr($key, 0, -1); // Property without index

            if (is_numeric($cid) && $cid >= 0 && $cid < 8)
            {
                switch($property)
                {
                case "CMP":
                    $gameResult = $value["value"];
                    $playerStats[$cid]['disconnected'] =
                        ($gameResult & GameResult::COMPLETION_DISCONNECTED)  ? true : false;
                    $playerStats[$cid]['no_completion'] =
                        ($gameResult & GameResult::COMPLETION_NO_COMPLETION) ? true : false;
                    $playerStats[$cid]['quit'] = ($gameResult & GameResult::COMPLETION_QUIT) ? true : false;
                    $playerStats[$cid]['won'] =  ($gameResult & GameResult::COMPLETION_WON)  ? true : false;
                    $playerStats[$cid]['draw'] = ($gameResult & GameResult::COMPLETION_DRAW) ? true : false;
                    $playerStats[$cid]['defeated'] =
                        ($gameResult & GameResult::COMPLETION_DEFEATED) ? true : false;

                    $refl = new \ReflectionClass('GameResult');
                    foreach ($refl->getConstants() as $k=>$v){
                        if ($gameResult & $v) {
                            $gameResult = $k;
                            break;
                        }
                    }
                    break;
                case "RSG":
                    $playerStats[$cid]['quit'] = $value["value"];
                    break;
                case "DED":
                    $playerStats[$cid]['defeated'] = $value["value"];
                    break;
                case "ALY":
                    // Unsupported ATM. My idea is that local_team_id should be the ID of the lowest ALLY -or-yourself
                    // For now everyone is on his own team
                    $playerStats[$cid]['local_team_id'] = $cid;
                    break;
                case "SPC":
                    $playerStats[$cid]['spectator'] = $value["value"];
                    break;

                case "LCN": //TS lost connection
                case "CON":
                    $playerStats[$cid]['disconnected'] = $value["value"];
                    break;

                case "CTY":
                    $playerStats[$cid]['side'] = $this->getSide(intval($value['value']));
                    break;
                case "NAM":
                    break;
                case "CRD":
                    $playerStats[$cid]['funds_left'] = $value["value"];
                    break;
                default:
                    $heap_count_key = strtolower(str_replace(' ', '_', $CountableHeaps[$property]));
                    if (array_key_exists($property, $CountableHeaps) && array_key_exists("counts", $value)) {
                        $playerStats[$cid]['detailed_counts'][$heap_count_key] = $value['counts'];

                        foreach ($value['counts'] as $type => $count) {
                            if (array_key_exists($heap_count_key, $playerStats[$cid])) {
                                $playerStats[$cid][$heap_count_key] += $count;
                            } else {
                                $playerStats[$cid][$heap_count_key] = $count;
                            }
                        }
                    } else {
                        $playerStats[$cid]['raw'][$property] = $value['value'];
                    }
                }
            } else {
               switch($key)
                {
                case "CMPL":
                    // Must be RA, not sure what to do though
                    if ($value["value"] == GameResult::COMPLETION_DRAW)
                    {
                        foreach ($playerStats as $playerGR)
                        {
                            $playerGR['draw'] = true;
                            $playerGR['won'] = false;
                            $playerGR['defeated'] = false;
                            $playerGR['no_completion'] = false;
                        }
                    }
                    else {
                        $gameWon = !$reporter['defeated'] && !$reporter['quit'];

                        foreach ($playerStats as $playerGR)
                        {
                            $playerGR['won'] = !$gameWon;
                            $playerGR['defeated'] = !$playerGR['won'];
                            $playerGR['no_completion'] = false;
                        }

                        $reporter['won'] = $gameWon;
                        $reporter['no_completion'] = false;
                        $reporter['defeated'] = !$reporter['won'];
                    }
                    break;
                case "OOSY":
                    $gameReport['reconnection_error'] = $value["value"];
                    if ($gameReport['reconnection_error'])
                    {
                        // If the game recons then the reporter marks himself as winner, admin will sort it out later
                        foreach ($playerStats as $playerGR)
                        {
                            $playerGR['won'] = false;
                        }
                        $reporter['won'] = true;
                    }
                    break;
                case "SDFX":
                    foreach ($playerStats as $playerGR)
                    {
                        $playerGR['disconnected'] = $value["value"];
                    }
                    break;
                case "DURA":
                    $gameReport['duration'] = $value["value"];
                    break;
                case "AFPS":
                    $gameReport['fps'] = $value["value"];
                    break;
                case "QUIT":
                    if ($reporter !== null && $cncnetGame != "ra")
                    {
                        $reporter['quit'] = $value["value"];
                    }
                    $gameReport['finished'] = !$value["value"];
                    break;
                case "FINI":
                    $gameReport['finished'] = $value["value"];
                    break;
                case "TIME":
                    $gameReport['local_time'] = date('r', $value['value']);
                    $gameReport['epoch_time'] = $value['value'];
                    break;
                case "SCEN":
                    $gameReport['map'] = $value['value'];
                    break;
                case "UNIT":
                    $gameReport['starting_units'] = $value['value'];
                    break;
                case "CRED":
                    $gameReport['starting_credits'] = $value['value'];
                    break;
                case "SUPR":
                    $gameReport['superweapons'] = $value['value'] ? true : false;
                    break;
                case "CRAT":
                    $gameReport['crates'] = $value['value'] ? true : false;
                    break;
                case "PLRS":
                    $gameReport['players_in_game'] = $value['value'];
                    break;
                case "BAMR":
                    $gameReport['build_off_ally_conyards'] = $value['value'] & 2 ? true : false;
                    $gameReport['mcv_redeploy'] = $value['value'] & 1 ? true : false;
                    break;
                case "SHRT":
                    $gameReport['short_game'] = $value['value'] ? true : false;
                    break;
                case "AIPL":
                    $gameReport['ai_players'] = $value['value'];
                    break;
                default:
                    $gameReport['raw'][$key] = $value['value'];
                }
            } 
        }

        return ['gameReport' =>  $gameReport,
        'playerStats' => $playerStats,
        'gameResult' => $gameResult];
    }

    public function saveToJsonFile($obj, $file)
    {
        $raw_json = Null;
        try
        {
            $raw_json = json_encode($obj, JSON_PRETTY_PRINT);
        }
        catch (Exception $e)
        {
            $raw_json = Null;
        }

        if ($raw_json == Null)
        {
            switch (json_last_error()) {
            case JSON_ERROR_NONE:
                error_log('saveToJsonFile - No errors');
                break;
            case JSON_ERROR_DEPTH:
                error_log('saveToJsonFile - Maximum stack depth exceeded');
                break;
            case JSON_ERROR_STATE_MISMATCH:
                error_log('saveToJsonFile - Underflow or the modes mismatch');
                break;
            case JSON_ERROR_CTRL_CHAR:
                error_log('saveToJsonFile - Unexpected control character found');
                break;
            case JSON_ERROR_SYNTAX:
                error_log('saveToJsonFile - Syntax error, malformed JSON');
                break;
            case JSON_ERROR_UTF8:
                error_log('saveToJsonFile - Malformed UTF-8 characters, possibly incorrectly encoded');
                break;
            default:
                error_log('saveToJsonFile - Unknown error');
                break;
            }
        }

        file_put_contents($file, $raw_json);
    }
}

$thisPlayerName = $argv[1];
$statsDmpFilePath = $argv[2];
$gameStatsFolder = $argv[3];

date_default_timezone_set("Asia/Kolkata");
$parser = new YRStatParser();

echo "Running YRStatParser with [thisPlayerName: $thisPlayerName, statsDmpFilePath: $statsDmpFilePath, gameStatsFolder: $gameStatsFolder]\n";
$rawStats = $parser->processStatsDmp($statsDmpFilePath);
$gameStats = $parser->getGameStats($rawStats, $thisPlayerName);
$epochDate = date('Y-m-d H-i-s', $gameStats['gameReport']['epoch_time']);
$statsFolder = "$gameStatsFolder/$epochDate";

if (!file_exists($statsFolder)) {
    mkdir($statsFolder, 0755, true);
}

$outpout_stats_dmp = "$statsFolder/{$gameStats['gameReport']['epoch_time']}_stats.dmp";
$output_stats_parsed = "$statsFolder/{$gameStats['gameReport']['epoch_time']}_stats_parsed.json";
$output_stats_raw = "$statsFolder/{$gameStats['gameReport']['epoch_time']}_stats_raw.json";

copy($statsDmpFilePath, $outpout_stats_dmp);
$parser->saveToJsonFile($gameStats, $output_stats_parsed);
$parser->saveToJsonFile($rawStats, $output_stats_raw);

echo "stats_dmp: $outpout_stats_dmp\n";
echo "stats_parsed: $output_stats_parsed\n";
echo "stats_raw: $output_stats_raw\n";

?>